#!/usr/bin/env python3
"""
Funding Round Tracker - Find recently funded companies for outreach.

Usage:
    python3 execution/track_funding_rounds.py \
        --stage "seed,series_a" \
        --industry "saas" \
        --output .tmp/funded_companies.json
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
    parser = argparse.ArgumentParser(description="Track funding rounds")
    parser.add_argument("--stage", "-s", default="seed,series_a,series_b", help="Funding stages")
    parser.add_argument("--industry", "-i", default="", help="Industry filter")
    parser.add_argument("--days", "-d", type=int, default=30, help="Days to look back")
    parser.add_argument("--output", "-o", default=".tmp/funded_companies.json")
    args = parser.parse_args()

    stages = [s.strip() for s in args.stage.split(",")]
    print(f"\n💰 Funding Round Tracker\n   Stages: {stages}\n")

    query = f"Companies that raised {', '.join(stages)} funding in the last {args.days} days"
    if args.industry: query += f" in {args.industry} industry"
    query += ". List company name, funding amount, stage, investors, and what they do."

    print("   Searching funding news...")
    results = search_perplexity(query)

    if not results:
        print("   ❌ Add PERPLEXITY_API_KEY for real-time funding data")
        return 1

    output = {
        "searched_at": datetime.now().isoformat(),
        "criteria": {"stages": stages, "industry": args.industry, "days": args.days},
        "raw_results": results
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Results saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
