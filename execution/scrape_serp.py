#!/usr/bin/env python3
"""
Google SERP Lead Scraper - Extract business leads from Google search results.

Usage:
    python3 execution/scrape_serp.py \
        --query "marketing agencies in Austin" \
        --num_results 50 \
        --output .tmp/serp_leads.json
"""

import argparse, json, os, sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

def search_serp_api(query, num_results=50):
    """Search using SerpAPI."""
    api_key = os.getenv("SERP_API_KEY") or os.getenv("SERPAPI_KEY")
    if not api_key:
        return None
    
    try:
        resp = requests.get("https://serpapi.com/search", params={
            "q": query,
            "api_key": api_key,
            "num": min(num_results, 100)
        }, timeout=30)
        if resp.ok:
            return resp.json()
    except Exception as e:
        print(f"   SerpAPI error: {e}")
    return None

def search_valueserp(query, num_results=50):
    """Search using ValueSERP."""
    api_key = os.getenv("VALUESERP_API_KEY")
    if not api_key:
        return None
    
    try:
        resp = requests.get("https://api.valueserp.com/search", params={
            "q": query,
            "api_key": api_key,
            "num": min(num_results, 100)
        }, timeout=30)
        if resp.ok:
            return resp.json()
    except Exception as e:
        print(f"   ValueSERP error: {e}")
    return None

def extract_leads(serp_data):
    """Extract lead information from SERP results."""
    leads = []
    
    # Organic results
    for result in serp_data.get("organic_results", []):
        leads.append({
            "type": "organic",
            "title": result.get("title", ""),
            "url": result.get("link", result.get("url", "")),
            "domain": result.get("displayed_link", result.get("domain", "")),
            "snippet": result.get("snippet", ""),
            "position": result.get("position", 0)
        })
    
    # Local results (Google Maps)
    for result in serp_data.get("local_results", {}).get("places", []):
        leads.append({
            "type": "local",
            "name": result.get("title", result.get("name", "")),
            "address": result.get("address", ""),
            "phone": result.get("phone", ""),
            "website": result.get("website", result.get("link", "")),
            "rating": result.get("rating", ""),
            "reviews": result.get("reviews", "")
        })
    
    return leads

def main():
    parser = argparse.ArgumentParser(description="Scrape leads from Google SERP")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--num_results", "-n", type=int, default=50)
    parser.add_argument("--output", "-o", default=".tmp/serp_leads.json")
    args = parser.parse_args()

    print(f"\n🔍 SERP Lead Scraper\n   Query: {args.query}\n")

    # Try SerpAPI first, then ValueSERP
    serp_data = search_serp_api(args.query, args.num_results)
    if not serp_data:
        serp_data = search_valueserp(args.query, args.num_results)
    
    if not serp_data:
        print("   ❌ No SERP API configured. Add SERP_API_KEY or VALUESERP_API_KEY to .env")
        return 1

    leads = extract_leads(serp_data)
    
    output = {
        "scraped_at": datetime.now().isoformat(),
        "query": args.query,
        "total_leads": len(leads),
        "leads": leads
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    organic = len([l for l in leads if l.get("type") == "organic"])
    local = len([l for l in leads if l.get("type") == "local"])
    
    print(f"✅ Found {len(leads)} leads")
    print(f"   Organic: {organic} | Local: {local}")
    print(f"   📄 Output: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
