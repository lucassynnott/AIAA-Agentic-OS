#!/usr/bin/env python3
"""
YouTube Channel Finder

Searches YouTube by keywords, scrapes channel data, and filters by engagement metrics
to find top-performing channels in any niche.

Uses YouTube Data API v3 (free, 10K quota/day) with SerpAPI fallback.

Usage:
    python3 execution/scrape_youtube_channels.py --keywords "email marketing" --max-results 50
    python3 execution/scrape_youtube_channels.py --keywords "cold email" --min-subscribers 10000 --sort-by subscribers

Follows directive: directives/youtube_channel_finder.md
"""

import os
import sys
import json
import csv
import argparse
import pickle
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Google API imports
try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("Note: Google API libraries not installed. Using SerpAPI only.")
    print("Install with: pip install google-api-python-client google-auth google-auth-oauthlib")

YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_youtube_credentials():
    """Get YouTube API credentials using existing OAuth setup."""
    project_root = Path(__file__).parent.parent
    token_path = project_root / "token_youtube.json"
    credentials_path = project_root / "client_secrets.json"
    
    creds = None
    
    # Try to load existing token
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), YOUTUBE_SCOPES)
        except Exception:
            pass
    
    # If no valid credentials, try to refresh or create new
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        
        if not creds and credentials_path.exists():
            print("  Authorizing YouTube API (one-time browser auth)...")
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next time
        if creds:
            with open(token_path, "w") as f:
                f.write(creds.to_json())
    
    return creds


def search_youtube_channels(
    keywords: list,
    max_results: int = 50,
    language: str = None,
    country: str = None
) -> list:
    """
    Search YouTube for channels using YouTube Data API v3.
    Falls back to SerpAPI if YouTube API is unavailable.
    """
    all_channels = []
    seen_channel_ids = set()
    
    # Try YouTube Data API first
    if GOOGLE_API_AVAILABLE:
        try:
            creds = get_youtube_credentials()
            if creds:
                youtube = build("youtube", "v3", credentials=creds)
                print("  Using YouTube Data API v3 (free, 10K quota/day)")
                
                for keyword in keywords:
                    print(f"Searching YouTube for: '{keyword}'...")
                    
                    try:
                        # Search for channels
                        search_response = youtube.search().list(
                            q=keyword,
                            type="channel",
                            part="snippet",
                            maxResults=min(50, max_results),
                            relevanceLanguage=language if language else "en",
                            regionCode=country if country else None
                        ).execute()
                        
                        # Get channel IDs from search results
                        channel_ids = []
                        for item in search_response.get("items", []):
                            channel_id = item["snippet"]["channelId"]
                            if channel_id not in seen_channel_ids:
                                channel_ids.append(channel_id)
                                seen_channel_ids.add(channel_id)
                        
                        if not channel_ids:
                            print(f"  No new channels found for '{keyword}'")
                            continue
                        
                        # Get detailed channel statistics (1 quota unit per channel)
                        channels_response = youtube.channels().list(
                            id=",".join(channel_ids),
                            part="snippet,statistics,brandingSettings"
                        ).execute()
                        
                        count_before = len(all_channels)
                        
                        for channel in channels_response.get("items", []):
                            snippet = channel.get("snippet", {})
                            stats = channel.get("statistics", {})
                            branding = channel.get("brandingSettings", {}).get("channel", {})
                            
                            channel_data = {
                                "channelId": channel["id"],
                                "channelName": snippet.get("title", "Unknown"),
                                "channelHandle": snippet.get("customUrl", ""),
                                "channelUrl": f"https://youtube.com/channel/{channel['id']}",
                                "subscriberCount": int(stats.get("subscriberCount", 0)) if not stats.get("hiddenSubscriberCount") else 0,
                                "viewCount": int(stats.get("viewCount", 0)),
                                "videoCount": int(stats.get("videoCount", 0)),
                                "description": snippet.get("description", "")[:500],
                                "thumbnailUrl": snippet.get("thumbnails", {}).get("default", {}).get("url", ""),
                                "country": snippet.get("country", ""),
                                "publishedAt": snippet.get("publishedAt", ""),
                                "verified": False,  # Not available in API
                                "keywords": branding.get("keywords", ""),
                            }
                            
                            # Fix channel URL if custom URL exists
                            if channel_data["channelHandle"]:
                                channel_data["channelUrl"] = f"https://youtube.com/{channel_data['channelHandle']}"
                            
                            all_channels.append(channel_data)
                        
                        new_channels = len(all_channels) - count_before
                        print(f"  Found {new_channels} new channels ({len(all_channels)} total unique)")
                        
                        if len(all_channels) >= max_results:
                            break
                            
                    except Exception as e:
                        print(f"  Error searching '{keyword}': {e}")
                        continue
                
                if all_channels:
                    return all_channels
                    
        except Exception as e:
            print(f"  YouTube API error: {e}")
            print("  Falling back to SerpAPI...")
    
    # Fallback to SerpAPI
    return search_youtube_channels_serpapi(keywords, max_results, language, country)


def search_youtube_channels_serpapi(
    keywords: list,
    max_results: int = 50,
    language: str = None,
    country: str = None
) -> list:
    """
    Fallback: Search YouTube for channels using SerpAPI.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("Error: No SERPAPI_API_KEY found and YouTube API unavailable")
        sys.exit(1)

    print("  Using SerpAPI fallback")
    all_channels = []
    seen_channel_ids = set()
    
    for keyword in keywords:
        print(f"Searching YouTube for: '{keyword}'...")
        
        params = {
            "engine": "youtube",
            "search_query": keyword,
            "sp": "EgIQAg%253D%253D",  # Filter for channels
            "api_key": api_key,
        }
        
        if language:
            params["hl"] = language
        if country:
            params["gl"] = country
        
        try:
            response = requests.get("https://serpapi.com/search", params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            channel_results = data.get("channel_results", [])
            count_before = len(all_channels)
            
            for channel in channel_results:
                channel_id = channel.get("channel_id") or channel.get("link", "").split("/")[-1]
                
                if channel_id and channel_id not in seen_channel_ids:
                    seen_channel_ids.add(channel_id)
                    
                    subs_str = channel.get("subscribers", "0")
                    subscribers = parse_subscriber_count(subs_str)
                    
                    channel_data = {
                        "channelId": channel_id,
                        "channelName": channel.get("title", "Unknown"),
                        "channelHandle": channel.get("handle", ""),
                        "channelUrl": channel.get("link", f"https://youtube.com/channel/{channel_id}"),
                        "subscriberCount": subscribers,
                        "viewCount": 0,
                        "videoCount": channel.get("video_count", 0),
                        "description": channel.get("description", ""),
                        "thumbnailUrl": channel.get("thumbnail", {}).get("static", "") if isinstance(channel.get("thumbnail"), dict) else channel.get("thumbnail", ""),
                        "verified": channel.get("verified", False),
                    }
                    all_channels.append(channel_data)
            
            new_channels = len(all_channels) - count_before
            print(f"  Found {new_channels} new channels ({len(all_channels)} total unique)")
            
            if len(all_channels) >= max_results:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"  Error searching '{keyword}': {e}")
            continue
    
    return all_channels


def parse_subscriber_count(subs_str: str) -> int:
    """Parse subscriber count strings like '1.2M subscribers' to integers."""
    if not subs_str or subs_str == "0":
        return 0
    
    # Remove 'subscribers' text and clean up
    subs_str = str(subs_str).lower().replace("subscribers", "").replace("subscriber", "").strip()
    
    try:
        if "k" in subs_str:
            return int(float(subs_str.replace("k", "")) * 1000)
        elif "m" in subs_str:
            return int(float(subs_str.replace("m", "")) * 1000000)
        elif "b" in subs_str:
            return int(float(subs_str.replace("b", "")) * 1000000000)
        else:
            return int(float(subs_str.replace(",", "")))
    except (ValueError, AttributeError):
        return 0





def normalize_channel_data(raw_channel: dict) -> dict:
    """
    Normalize channel data into consistent output format.
    """
    channel = {
        "channel_name": raw_channel.get("channelName", "Unknown"),
        "channel_handle": raw_channel.get("channelHandle", ""),
        "channel_url": raw_channel.get("channelUrl", ""),
        "channel_id": raw_channel.get("channelId", ""),
        "subscribers": raw_channel.get("subscriberCount", 0),
        "total_views": raw_channel.get("viewCount", 0),
        "video_count": raw_channel.get("videoCount", 0),
        "description": (raw_channel.get("description", "") or "")[:500],
        "profile_image": raw_channel.get("thumbnailUrl", ""),
        "country": raw_channel.get("country", ""),
        "published_at": raw_channel.get("publishedAt", ""),
        "verified": raw_channel.get("verified", False),
    }
    
    # Ensure handle starts with @
    if channel["channel_handle"] and not channel["channel_handle"].startswith("@"):
        channel["channel_handle"] = f"@{channel['channel_handle']}"
    
    return channel


def filter_channels(
    channels: list,
    min_subscribers: int = None,
    max_subscribers: int = None,
    min_videos: int = None,
    min_views: int = None
) -> list:
    """
    Filter channels based on criteria.
    """
    filtered = []
    
    for channel in channels:
        # Apply subscriber filters
        if min_subscribers and channel["subscribers"] < min_subscribers:
            continue
        if max_subscribers and channel["subscribers"] > max_subscribers:
            continue
            
        # Apply video count filter
        if min_videos and channel["video_count"] < min_videos:
            continue
            
        # Apply view count filter
        if min_views and channel["total_views"] < min_views:
            continue
            
        filtered.append(channel)
    
    return filtered


def sort_channels(channels: list, sort_by: str = "relevance") -> list:
    """
    Sort channels by specified metric.
    """
    if sort_by == "subscribers":
        return sorted(channels, key=lambda x: x["subscribers"], reverse=True)
    elif sort_by == "views":
        return sorted(channels, key=lambda x: x["total_views"], reverse=True)
    elif sort_by == "videos":
        return sorted(channels, key=lambda x: x["video_count"], reverse=True)
    else:
        # relevance - keep original order from search
        return channels


def save_results(
    channels: list,
    search_params: dict,
    output_format: str = "json",
    output_prefix: str = "youtube_channels"
) -> dict:
    """
    Save results to file(s).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(".tmp")
    output_dir.mkdir(exist_ok=True)
    
    output_files = {}
    
    # Prepare full output data
    output_data = {
        "search_params": search_params,
        "total_found": len(channels),
        "scraped_at": datetime.now().isoformat(),
        "channels": channels
    }
    
    # Save JSON
    if output_format in ["json", "both"]:
        json_file = output_dir / f"{output_prefix}_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        output_files["json"] = str(json_file)
        print(f"Saved JSON: {json_file}")
    
    # Save CSV
    if output_format in ["csv", "both"]:
        csv_file = output_dir / f"{output_prefix}_{timestamp}.csv"
        
        csv_fields = [
            "channel_name", "channel_handle", "channel_url", 
            "subscribers", "total_views", "video_count",
            "description", "join_date", "country"
        ]
        
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
            writer.writeheader()
            for channel in channels:
                writer.writerow(channel)
                
        output_files["csv"] = str(csv_file)
        print(f"Saved CSV: {csv_file}")
    
    return output_files


def main():
    parser = argparse.ArgumentParser(
        description="Find top YouTube channels by keywords with filtering and sorting"
    )
    
    # Search parameters
    parser.add_argument(
        "--keywords", 
        nargs="+", 
        required=True,
        help="Search terms to find channels (can provide multiple)"
    )
    parser.add_argument(
        "--max-results", 
        type=int, 
        default=50,
        help="Maximum channels to return (default: 50)"
    )
    
    # Filters
    parser.add_argument(
        "--min-subscribers", 
        type=int,
        help="Minimum subscriber count filter"
    )
    parser.add_argument(
        "--max-subscribers", 
        type=int,
        help="Maximum subscriber count filter"
    )
    parser.add_argument(
        "--min-videos", 
        type=int,
        help="Minimum video count filter"
    )
    parser.add_argument(
        "--min-views", 
        type=int,
        help="Minimum total view count filter"
    )
    
    # Sorting
    parser.add_argument(
        "--sort-by", 
        choices=["subscribers", "views", "videos", "relevance"],
        default="relevance",
        help="Sort results by metric (default: relevance)"
    )
    
    # Location/Language
    parser.add_argument(
        "--language",
        help="Filter by language code (e.g., en, es, de)"
    )
    parser.add_argument(
        "--country",
        help="Filter by country code (e.g., US, UK, CA)"
    )
    
    # Output
    parser.add_argument(
        "--output-format",
        choices=["json", "csv", "both"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--output-prefix",
        default="youtube_channels",
        help="Custom prefix for output filename"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("YouTube Channel Finder")
    print("=" * 60)
    print(f"Keywords: {', '.join(args.keywords)}")
    print(f"Max Results: {args.max_results}")
    if args.min_subscribers:
        print(f"Min Subscribers: {args.min_subscribers:,}")
    if args.max_subscribers:
        print(f"Max Subscribers: {args.max_subscribers:,}")
    if args.min_videos:
        print(f"Min Videos: {args.min_videos}")
    if args.min_views:
        print(f"Min Views: {args.min_views:,}")
    print(f"Sort By: {args.sort_by}")
    print("=" * 60)
    
    # Step 1: Search for channels
    print("\n[1/4] Searching YouTube...")
    raw_channels = search_youtube_channels(
        keywords=args.keywords,
        max_results=args.max_results,
        language=args.language,
        country=args.country
    )
    
    if not raw_channels:
        print("No channels found. Try different keywords.")
        sys.exit(1)
    
    print(f"Found {len(raw_channels)} channels from search")
    
    # Step 2: Normalize data
    print("\n[2/4] Normalizing channel data...")
    channels = [normalize_channel_data(ch) for ch in raw_channels]
    
    # Step 3: Filter
    print("\n[3/4] Applying filters...")
    channels = filter_channels(
        channels,
        min_subscribers=args.min_subscribers,
        max_subscribers=args.max_subscribers,
        min_videos=args.min_videos,
        min_views=args.min_views
    )
    print(f"{len(channels)} channels after filtering")
    
    if not channels:
        print("No channels match your filters. Try relaxing the criteria.")
        sys.exit(1)
    
    # Step 4: Sort
    print(f"\n[4/4] Sorting by {args.sort_by}...")
    channels = sort_channels(channels, args.sort_by)
    
    # Limit to max results
    channels = channels[:args.max_results]
    
    # Save results
    print("\nSaving results...")
    search_params = {
        "keywords": args.keywords,
        "filters": {
            "min_subscribers": args.min_subscribers,
            "max_subscribers": args.max_subscribers,
            "min_videos": args.min_videos,
            "min_views": args.min_views
        },
        "sort_by": args.sort_by,
        "language": args.language,
        "country": args.country
    }
    
    output_files = save_results(
        channels,
        search_params,
        output_format=args.output_format,
        output_prefix=args.output_prefix
    )
    
    # Print summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total channels found: {len(channels)}")
    
    if channels:
        print(f"\nTop 5 channels:")
        for i, ch in enumerate(channels[:5], 1):
            subs = f"{ch['subscribers']:,}" if ch['subscribers'] else "N/A"
            print(f"  {i}. {ch['channel_name']} ({ch['channel_handle']}) - {subs} subscribers")
    
    print(f"\nOutput files:")
    for fmt, path in output_files.items():
        print(f"  {fmt.upper()}: {path}")
    
    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
