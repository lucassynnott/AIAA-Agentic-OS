#!/usr/bin/env python3
"""
Brand Mention Monitor - Track brand mentions across the web.

Usage:
    python3 execution/monitor_brand_mentions.py \
        --brand "Company Name" \
        --output .tmp/brand_mentions.json
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
    parser = argparse.ArgumentParser(description="Monitor brand mentions")
    parser.add_argument("--brand", "-b", required=True, help="Brand name to monitor")
    parser.add_argument("--competitors", "-c", default="", help="Competitor brands")
    parser.add_argument("--output", "-o", default=".tmp/brand_mentions.json")
    args = parser.parse_args()

    print(f"\n📡 Brand Mention Monitor\n   Brand: {args.brand}\n")

    queries = [
        f"Recent mentions of {args.brand} in news articles and blogs",
        f"Social media discussions about {args.brand}",
        f"Reviews and feedback about {args.brand}"
    ]

    results = {}
    for q in queries:
        print(f"   Searching: {q[:40]}...")
        results[q] = search_perplexity(q)

    output = {
        "monitored_at": datetime.now().isoformat(),
        "brand": args.brand,
        "results": results
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Mentions saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
