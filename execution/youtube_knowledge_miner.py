#!/usr/bin/env python3
"""
YouTube Knowledge Miner - Extract best practices from YouTube channels

Workflow:
1. Find top channels in your niche
2. Get their best performing videos
3. Get transcripts via transcript APIs (Supadata -> TranscriptAPI -> youtube-transcript-api)
4. Convert transcripts to how-to manuals using Claude/Gemini
5. Filter manuals worth turning into skills
6. Generate skill bibles

Usage:
    python3 execution/youtube_knowledge_miner.py \
        --niche "meta ads" "facebook advertising" \
        --max-channels 10 \
        --videos-per-channel 5 \
        --output-dir .tmp/knowledge_mine

Environment Variables:
    SUPADATA_API_KEY      - Primary transcript API (supadata.ai)
    TRANSCRIPTAPI_KEY     - Secondary transcript API (transcriptapi.com)
    OPENROUTER_API_KEY    - For Claude manual generation

Follows directive: directives/youtube_knowledge_miner.md
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    print("Error: Google API libraries required")
    print("Install with: pip install google-api-python-client google-auth google-auth-oauthlib")
    sys.exit(1)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Error: requests library required")
    sys.exit(1)

YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_youtube_credentials():
    """Get YouTube API credentials."""
    project_root = Path(__file__).parent.parent
    token_path = project_root / "token_youtube.json"
    credentials_path = project_root / "client_secrets.json"

    creds = None
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), YOUTUBE_SCOPES)
        except Exception:
            pass

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds and credentials_path.exists():
            print("  Authorizing YouTube API...")
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)

        if creds:
            with open(token_path, "w") as f:
                f.write(creds.to_json())

    return creds


def find_top_channels(keywords: list, max_channels: int = 10, min_subscribers: int = 5000) -> list:
    """Find top YouTube channels for given keywords."""
    print(f"\n[1/6] Finding top channels for: {', '.join(keywords)}")

    creds = get_youtube_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    all_channels = []
    seen_ids = set()

    for keyword in keywords:
        print(f"  Searching: '{keyword}'...")
        try:
            search_response = youtube.search().list(
                q=keyword,
                type="channel",
                part="snippet",
                maxResults=25,
                relevanceLanguage="en"
            ).execute()

            channel_ids = [item["snippet"]["channelId"] for item in search_response.get("items", [])]

            if channel_ids:
                channels_response = youtube.channels().list(
                    id=",".join(channel_ids),
                    part="snippet,statistics,contentDetails"
                ).execute()

                for channel in channels_response.get("items", []):
                    if channel["id"] in seen_ids:
                        continue

                    stats = channel.get("statistics", {})
                    subs = int(stats.get("subscriberCount", 0))

                    if subs >= min_subscribers:
                        seen_ids.add(channel["id"])
                        all_channels.append({
                            "id": channel["id"],
                            "name": channel["snippet"]["title"],
                            "handle": channel["snippet"].get("customUrl", ""),
                            "subscribers": subs,
                            "views": int(stats.get("viewCount", 0)),
                            "videos": int(stats.get("videoCount", 0)),
                            "description": channel["snippet"].get("description", "")[:300],
                            "uploads_playlist": channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads", "")
                        })
        except Exception as e:
            print(f"    Error: {e}")
            continue

    # Sort by subscribers and limit
    all_channels.sort(key=lambda x: x["subscribers"], reverse=True)
    all_channels = all_channels[:max_channels]

    print(f"  Found {len(all_channels)} qualifying channels")
    for i, ch in enumerate(all_channels[:5], 1):
        print(f"    {i}. {ch['name']} ({ch['subscribers']:,} subs)")

    return all_channels


def get_channel_videos(channel: dict, youtube, max_videos: int = 10, min_views: int = 1000, min_duration_minutes: int = 5) -> list:
    """Get top performing videos from a channel."""
    videos = []

    try:
        # Get videos from uploads playlist
        playlist_id = channel.get("uploads_playlist")
        if not playlist_id:
            return videos

        playlist_response = youtube.playlistItems().list(
            playlistId=playlist_id,
            part="snippet,contentDetails",
            maxResults=50
        ).execute()

        video_ids = [item["contentDetails"]["videoId"] for item in playlist_response.get("items", [])]

        if not video_ids:
            return videos

        # Get video details
        videos_response = youtube.videos().list(
            id=",".join(video_ids),
            part="snippet,statistics,contentDetails"
        ).execute()

        for video in videos_response.get("items", []):
            stats = video.get("statistics", {})
            views = int(stats.get("viewCount", 0))

            # Parse duration (PT1H2M3S format)
            duration_str = video.get("contentDetails", {}).get("duration", "PT0S")
            duration_minutes = parse_duration(duration_str)

            if views >= min_views and duration_minutes >= min_duration_minutes:
                videos.append({
                    "id": video["id"],
                    "title": video["snippet"]["title"],
                    "channel_name": channel["name"],
                    "channel_id": channel["id"],
                    "views": views,
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "duration_minutes": duration_minutes,
                    "published_at": video["snippet"]["publishedAt"],
                    "description": video["snippet"].get("description", "")[:500],
                    "url": f"https://youtube.com/watch?v={video['id']}"
                })

        # Sort by views and limit
        videos.sort(key=lambda x: x["views"], reverse=True)
        videos = videos[:max_videos]

    except Exception as e:
        print(f"    Error getting videos for {channel['name']}: {e}")

    return videos


def parse_duration(duration_str: str) -> int:
    """Parse ISO 8601 duration to minutes."""
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 60 + minutes + (1 if seconds > 30 else 0)


# ============================================================================
# TRANSCRIPT API FUNCTIONS
# ============================================================================

def get_transcript_supadata(video_id: str) -> str:
    """Get transcript using Supadata API (primary)."""
    api_key = os.getenv("SUPADATA_API_KEY")
    if not api_key:
        return None

    try:
        response = requests.get(
            f"https://api.supadata.ai/v1/transcript",
            params={"url": f"https://youtube.com/watch?v={video_id}"},
            headers={"x-api-key": api_key},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            # Extract text from transcript segments
            content = data.get("content", [])
            if content:
                full_text = " ".join([segment.get("text", "") for segment in content])
                return full_text.strip()
        elif response.status_code == 404:
            return None  # No transcript available
        else:
            print(f"    Supadata API error: {response.status_code}")
            return None

    except Exception as e:
        print(f"    Supadata error: {e}")
        return None


def get_transcript_transcriptapi(video_id: str) -> str:
    """Get transcript using TranscriptAPI (secondary fallback)."""
    api_key = os.getenv("TRANSCRIPTAPI_KEY")
    if not api_key:
        return None

    try:
        response = requests.get(
            "https://transcriptapi.com/api/v2/youtube/transcript",
            params={
                "video_url": video_id,
                "format": "json"
            },
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        transcript = data.get("transcript", [])

        # Handle list of segments format
        if isinstance(transcript, list):
            return " ".join([t.get("text", "") for t in transcript]).strip()
        elif isinstance(transcript, str):
            return transcript.strip()

        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None  # No transcript available
        print(f"    TranscriptAPI error: {e.response.status_code}")
        return None
    except Exception as e:
        print(f"    TranscriptAPI error: {e}")
        return None


def get_transcript_youtube_api(video_id: str, retries: int = 2) -> str:
    """Get transcript using youtube-transcript-api (final fallback)."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from http.cookiejar import MozillaCookieJar

        # Check for cookies file to bypass rate limiting
        project_root = Path(__file__).parent.parent
        cookies_path = project_root / "youtube_cookies.txt"

        # Create API instance with cookies if available
        if cookies_path.exists():
            try:
                cookie_jar = MozillaCookieJar(str(cookies_path))
                cookie_jar.load(ignore_discard=True, ignore_expires=True)
                session = requests.Session()
                session.cookies = cookie_jar
                api = YouTubeTranscriptApi(http_client=session)
            except Exception:
                api = YouTubeTranscriptApi()
        else:
            api = YouTubeTranscriptApi()

        for attempt in range(retries):
            try:
                # Try to get English transcript first
                try:
                    transcript = api.fetch(video_id, languages=['en', 'en-US', 'en-GB'])
                    full_text = " ".join([snippet.text for snippet in transcript])
                    return full_text
                except Exception:
                    pass

                # Try to list available transcripts
                transcript_list = api.list(video_id)

                # Try any English variant
                for t in transcript_list:
                    if 'en' in t.language_code.lower():
                        transcript = t.fetch()
                        return " ".join([snippet.text for snippet in transcript])

                # Try auto-generated
                for t in transcript_list:
                    if t.is_generated:
                        try:
                            translated = t.translate('en')
                            transcript = translated.fetch()
                            return " ".join([snippet.text for snippet in transcript])
                        except Exception:
                            transcript = t.fetch()
                            return " ".join([snippet.text for snippet in transcript])

            except Exception as e:
                error_str = str(e).lower()
                if "blocking" in error_str or "ip" in error_str:
                    if attempt < retries - 1:
                        time.sleep((attempt + 1) * 3)
                        continue
                break

        return None

    except ImportError:
        return None
    except Exception:
        return None


def get_transcript(video_id: str) -> str:
    """Get transcript using fallback chain: Supadata -> TranscriptAPI -> youtube-transcript-api."""

    # Try Supadata first (primary)
    if os.getenv("SUPADATA_API_KEY"):
        transcript = get_transcript_supadata(video_id)
        if transcript:
            return transcript

    # Try TranscriptAPI second (secondary)
    if os.getenv("TRANSCRIPTAPI_KEY"):
        transcript = get_transcript_transcriptapi(video_id)
        if transcript:
            return transcript

    # Try youtube-transcript-api last (free fallback, may be rate limited)
    transcript = get_transcript_youtube_api(video_id)
    if transcript:
        return transcript

    return None


# ============================================================================
# MANUAL GENERATION FUNCTIONS
# ============================================================================

def convert_to_howto_manual(transcript: str, video_info: dict, use_gemini: bool = False) -> dict:
    """Convert transcript to structured how-to manual using Claude or Gemini."""

    prompt = f"""Convert this video transcript into a comprehensive how-to manual.

VIDEO: {video_info['title']}
CHANNEL: {video_info['channel_name']}
VIEWS: {video_info['views']:,}

TRANSCRIPT:
{transcript[:15000]}

Create a structured how-to manual with:

1. **Executive Summary** (2-3 sentences)
2. **Key Concepts** (bullet list of main ideas)
3. **Step-by-Step Process** (numbered, actionable steps)
4. **Best Practices** (do's and don'ts)
5. **Common Mistakes to Avoid**
6. **Tools/Resources Mentioned**
7. **Actionable Takeaways** (3-5 things to implement immediately)
8. **Skill Rating** (1-10, how valuable is this as a skill to automate?)

Format as clean markdown. Be thorough but concise."""

    if use_gemini and os.getenv("GOOGLE_API_KEY"):
        return call_gemini(prompt, video_info)
    else:
        return call_claude(prompt, video_info)


def call_claude(prompt: str, video_info: dict) -> dict:
    """Call Claude via OpenRouter."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("    Error: OPENROUTER_API_KEY required")
        return None

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 4000
            },
            timeout=120
        )

        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]

            # Extract skill rating
            skill_rating = 5
            if "Skill Rating" in content:
                import re
                match = re.search(r'Skill Rating[:\s]*(\d+)', content)
                if match:
                    skill_rating = int(match.group(1))

            return {
                "video_id": video_info["id"],
                "video_title": video_info["title"],
                "channel_name": video_info["channel_name"],
                "views": video_info["views"],
                "url": video_info["url"],
                "manual_content": content,
                "skill_rating": skill_rating,
                "generated_at": datetime.now().isoformat()
            }
        else:
            print(f"    Claude API error: {response.status_code}")
            return None

    except Exception as e:
        print(f"    Error calling Claude: {e}")
        return None


def call_gemini(prompt: str, video_info: dict) -> dict:
    """Call Gemini Flash (cheaper)."""
    try:
        import google.generativeai as genai

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        content = response.text

        # Extract skill rating
        skill_rating = 5
        import re
        match = re.search(r'Skill Rating[:\s]*(\d+)', content)
        if match:
            skill_rating = int(match.group(1))

        return {
            "video_id": video_info["id"],
            "video_title": video_info["title"],
            "channel_name": video_info["channel_name"],
            "views": video_info["views"],
            "url": video_info["url"],
            "manual_content": content,
            "skill_rating": skill_rating,
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"    Error calling Gemini: {e}")
        return None


def filter_valuable_manuals(manuals: list, min_rating: int = 7) -> list:
    """Filter manuals worth turning into skills."""
    print(f"\n[5/6] Filtering valuable manuals (min rating: {min_rating})...")

    valuable = [m for m in manuals if m and m.get("skill_rating", 0) >= min_rating]

    print(f"  {len(valuable)}/{len(manuals)} manuals rated {min_rating}+ for skill conversion")

    for m in valuable[:5]:
        print(f"    - {m['video_title'][:50]}... (Rating: {m['skill_rating']})")

    return valuable


def generate_skill_bible(manuals: list, niche: str, output_dir: Path) -> Path:
    """Generate a comprehensive skill bible from multiple manuals."""
    print(f"\n[6/6] Generating Skill Bible...")

    if not manuals:
        print("  No manuals to process")
        return None

    # Combine all manual content
    combined_content = "\n\n---\n\n".join([
        f"## From: {m['video_title']}\n**Channel:** {m['channel_name']} | **Views:** {m['views']:,}\n\n{m['manual_content']}"
        for m in manuals[:10]  # Limit to top 10
    ])

    prompt = f"""You are creating a comprehensive SKILL BIBLE for: {niche}

Based on the following how-to manuals extracted from top YouTube experts, create a unified skill bible.

SOURCE MANUALS:
{combined_content[:30000]}

Create a SKILL BIBLE with this structure:

# SKILL BIBLE: {niche.title()}

> Sources: {len(manuals)} expert videos analyzed
> Generated: {datetime.now().strftime("%Y-%m-%d")}

---

## Executive Summary
[2-3 paragraph overview of this skill domain]

---

## Core Principles
[5-7 fundamental principles that underpin success]

---

## Complete Process (Step-by-Step)
[Detailed numbered steps from start to finish]

---

## Best Practices
[Comprehensive list of do's]

---

## Common Mistakes
[What to avoid and why]

---

## Tools & Resources
[Software, platforms, resources mentioned]

---

## Advanced Techniques
[Expert-level tactics for optimization]

---

## Metrics & KPIs
[What to track and benchmark targets]

---

## Quick Reference Checklist
[Actionable checklist for implementation]

---

## Expert Insights
[Notable quotes and wisdom from the source videos]

Make this comprehensive, actionable, and production-ready for an AI agent to execute."""

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("  Error: OPENROUTER_API_KEY required")
        return None

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 8000
            },
            timeout=180
        )

        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]

            # Generate filename
            safe_niche = niche.lower().replace(" ", "_").replace("-", "_")[:30]
            filename = f"SKILL_BIBLE_{safe_niche}.md"
            output_path = output_dir / filename

            # Also save to skills folder
            skills_dir = Path(__file__).parent.parent / "skills"
            skills_path = skills_dir / filename

            # Write to both locations
            output_path.write_text(content, encoding="utf-8")
            skills_path.write_text(content, encoding="utf-8")

            print(f"  Saved: {output_path}")
            print(f"  Saved: {skills_path}")

            return output_path
        else:
            print(f"  API error: {response.status_code}")
            return None

    except Exception as e:
        print(f"  Error generating skill bible: {e}")
        return None


def process_video(video: dict, use_gemini: bool = False) -> dict:
    """Process a single video: get transcript, convert to manual."""

    print(f"    Processing: {video['title'][:50]}...")

    # Add a small delay to avoid rate limiting
    time.sleep(1)

    # Get transcript using fallback chain
    transcript = get_transcript(video["id"])

    if not transcript:
        print(f"    Could not get transcript for {video['id']}")
        return None

    # Convert to how-to manual
    manual = convert_to_howto_manual(transcript, video, use_gemini)

    return manual


def main():
    parser = argparse.ArgumentParser(
        description="Mine knowledge from top YouTube channels in your niche"
    )

    parser.add_argument(
        "--niche", "-n",
        nargs="+",
        required=True,
        help="Niche keywords to search (e.g., 'meta ads' 'facebook advertising')"
    )
    parser.add_argument(
        "--max-channels",
        type=int,
        default=10,
        help="Maximum channels to analyze (default: 10)"
    )
    parser.add_argument(
        "--videos-per-channel",
        type=int,
        default=5,
        help="Videos to analyze per channel (default: 5)"
    )
    parser.add_argument(
        "--min-subscribers",
        type=int,
        default=5000,
        help="Minimum channel subscribers (default: 5000)"
    )
    parser.add_argument(
        "--min-views",
        type=int,
        default=5000,
        help="Minimum video views (default: 5000)"
    )
    parser.add_argument(
        "--min-skill-rating",
        type=int,
        default=7,
        help="Minimum skill rating to include (default: 7)"
    )
    parser.add_argument(
        "--use-gemini",
        action="store_true",
        help="Use Gemini Flash instead of Claude (cheaper)"
    )
    parser.add_argument(
        "--output-dir",
        default=".tmp/knowledge_mine",
        help="Output directory"
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="Parallel video processing (default: 1, increase carefully to avoid rate limits)"
    )

    args = parser.parse_args()

    # Check for at least one transcript API key
    has_transcript_api = (
        os.getenv("SUPADATA_API_KEY") or
        os.getenv("TRANSCRIPTAPI_KEY")
    )

    print("=" * 60)
    print("YouTube Knowledge Miner")
    print("=" * 60)
    print(f"Niche: {' + '.join(args.niche)}")
    print(f"Max Channels: {args.max_channels}")
    print(f"Videos/Channel: {args.videos_per_channel}")
    print(f"Using: {'Gemini Flash' if args.use_gemini else 'Claude'}")
    print(f"Transcript APIs: ", end="")
    apis = []
    if os.getenv("SUPADATA_API_KEY"):
        apis.append("Supadata")
    if os.getenv("TRANSCRIPTAPI_KEY"):
        apis.append("TranscriptAPI")
    apis.append("youtube-transcript-api (fallback)")
    print(" -> ".join(apis))
    print("=" * 60)

    if not has_transcript_api:
        print("\nWarning: No transcript API keys found (SUPADATA_API_KEY or TRANSCRIPTAPI_KEY)")
        print("Falling back to youtube-transcript-api which may be rate limited.\n")

    # Setup output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Find top channels
    channels = find_top_channels(
        args.niche,
        max_channels=args.max_channels,
        min_subscribers=args.min_subscribers
    )

    if not channels:
        print("No channels found. Try different keywords.")
        return 1

    # Save channels list
    channels_file = output_dir / "channels.json"
    with open(channels_file, "w") as f:
        json.dump(channels, f, indent=2)

    # Step 2: Get videos from each channel
    print(f"\n[2/6] Getting top videos from {len(channels)} channels...")

    creds = get_youtube_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    all_videos = []
    for channel in channels:
        print(f"  {channel['name']}...")
        videos = get_channel_videos(
            channel, youtube,
            max_videos=args.videos_per_channel,
            min_views=args.min_views
        )
        all_videos.extend(videos)
        print(f"    Found {len(videos)} qualifying videos")

    print(f"  Total videos to process: {len(all_videos)}")

    # Save videos list
    videos_file = output_dir / "videos.json"
    with open(videos_file, "w") as f:
        json.dump(all_videos, f, indent=2)

    # Step 3: Process videos (get transcripts, convert to manuals)
    print(f"\n[3/6] Processing videos (transcripts + manuals)...")

    manuals = []
    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        futures = {
            executor.submit(process_video, video, args.use_gemini): video
            for video in all_videos
        }

        for future in as_completed(futures):
            video = futures[future]
            try:
                manual = future.result()
                if manual:
                    manuals.append(manual)
                    print(f"      Completed: {video['title'][:40]}... (Rating: {manual.get('skill_rating', 'N/A')})")
            except Exception as e:
                print(f"      Failed: {video['title'][:40]}... ({e})")

    print(f"  Successfully processed: {len(manuals)}/{len(all_videos)} videos")

    # Step 4: Save all manuals
    print(f"\n[4/6] Saving how-to manuals...")

    manuals_dir = output_dir / "manuals"
    manuals_dir.mkdir(exist_ok=True)

    for manual in manuals:
        safe_title = manual["video_title"][:50].replace("/", "-").replace("\\", "-")
        manual_file = manuals_dir / f"{safe_title}.md"
        manual_file.write_text(manual["manual_content"], encoding="utf-8")

    # Save manuals index
    manuals_index = output_dir / "manuals_index.json"
    with open(manuals_index, "w") as f:
        json.dump(manuals, f, indent=2)

    # Step 5: Filter valuable manuals
    valuable_manuals = filter_valuable_manuals(manuals, args.min_skill_rating)

    # Step 6: Generate skill bible
    niche_name = " ".join(args.niche)
    skill_bible_path = generate_skill_bible(valuable_manuals, niche_name, output_dir)

    # Summary
    print("\n" + "=" * 60)
    print("KNOWLEDGE MINING COMPLETE")
    print("=" * 60)
    print(f"Channels analyzed: {len(channels)}")
    print(f"Videos processed: {len(manuals)}")
    print(f"High-value manuals: {len(valuable_manuals)}")
    print(f"\nOutputs:")
    print(f"  Channels: {channels_file}")
    print(f"  Videos: {videos_file}")
    print(f"  Manuals: {manuals_dir}")
    if skill_bible_path:
        print(f"  Skill Bible: {skill_bible_path}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
