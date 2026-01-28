#!/usr/bin/env python3
"""
Yelp Review Scraper - Extract reviews for analysis.

Usage:
    python3 execution/scrape_yelp_reviews.py \
        --business "restaurant name" \
        --location "new york" \
        --output .tmp/yelp_reviews.json
"""

import argparse, json, os, sys
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

def search_perplexity(query):
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key: return ""
    try:
        resp = requests.post("https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "llama-3.1-sonar-small-128k-online", "messages": [{"role": "user", "content": query}]},
            timeout=30)
        if resp.ok: return resp.json()["choices"][0]["message"]["content"]
    except: pass
    return ""

def main():
    parser = argparse.ArgumentParser(description="Scrape Yelp reviews")
    parser.add_argument("--business", "-b", required=True)
    parser.add_argument("--location", "-l", required=True)
    parser.add_argument("--output", "-o", default=".tmp/yelp_reviews.json")
    args = parser.parse_args()

    print(f"\n⭐ Yelp Review Analyzer\n   Business: {args.business}\n   Location: {args.location}\n")

    query = f"What are customers saying about {args.business} in {args.location} on Yelp? Summarize the main positive and negative themes from reviews. Include overall rating if available."

    print("   Searching reviews...")
    results = search_perplexity(query)

    output = {
        "searched_at": datetime.now().isoformat(),
        "business": args.business,
        "location": args.location,
        "review_summary": results
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Reviews saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
