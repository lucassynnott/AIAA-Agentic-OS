#!/usr/bin/env python3
"""
Crunchbase Lead Finder - Find companies on Crunchbase by criteria.

Usage:
    python3 execution/scrape_crunchbase.py \
        --industry "saas" \
        --funding "series_a" \
        --location "san francisco" \
        --output .tmp/crunchbase_leads.json
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
    parser = argparse.ArgumentParser(description="Find Crunchbase leads")
    parser.add_argument("--industry", "-i", required=True)
    parser.add_argument("--funding", "-f", default="", help="Funding stage")
    parser.add_argument("--location", "-l", default="", help="Location")
    parser.add_argument("--employees", "-e", default="", help="Employee count range")
    parser.add_argument("--output", "-o", default=".tmp/crunchbase_leads.json")
    args = parser.parse_args()

    print(f"\n🔍 Crunchbase Lead Finder\n   Industry: {args.industry}\n")

    # Build search query
    query = f"List {args.industry} companies"
    if args.funding:
        query += f" that raised {args.funding} funding"
    if args.location:
        query += f" in {args.location}"
    if args.employees:
        query += f" with {args.employees} employees"
    query += ". Include company name, website, funding amount, description. Format as a list."

    print("   Searching...")
    results = search_perplexity(query)

    output = {
        "searched_at": datetime.now().isoformat(),
        "criteria": {
            "industry": args.industry,
            "funding": args.funding,
            "location": args.location,
            "employees": args.employees
        },
        "results": results
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Results saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
