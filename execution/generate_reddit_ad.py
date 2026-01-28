#!/usr/bin/env python3
"""
Reddit to Ad Scripts - Convert Reddit discussions into ad scripts.

Usage:
    python3 execution/generate_reddit_ad.py \
        --subreddit "entrepreneur" \
        --topic "marketing challenges" \
        --product "Marketing SaaS" \
        --output .tmp/reddit_ads.md
"""

import argparse, os, sys
from datetime import datetime
from pathlib import Path
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"

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
    parser = argparse.ArgumentParser(description="Reddit insights to ad scripts")
    parser.add_argument("--subreddit", "-s", default="", help="Subreddit to research")
    parser.add_argument("--topic", "-t", required=True, help="Topic to research")
    parser.add_argument("--product", "-p", required=True, help="Your product/service")
    parser.add_argument("--output", "-o", default=".tmp/reddit_ads.md")
    args = parser.parse_args()

    print(f"\n🎯 Reddit to Ad Scripts\n   Topic: {args.topic}\n")

    # Research Reddit discussions
    query = f"Common complaints and discussions about {args.topic}"
    if args.subreddit:
        query += f" on Reddit r/{args.subreddit}"
    query += ". What are the main pain points people discuss?"

    print("   Researching Reddit discussions...")
    research = search_perplexity(query)

    client = get_client()

    ads = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You turn customer pain points into compelling ad scripts."},
            {"role": "user", "content": f"""Create ad scripts from these Reddit insights:

TOPIC: {args.topic}
PRODUCT: {args.product}

REDDIT RESEARCH:
{research or "Use common pain points for this topic"}

CREATE 3 AD SCRIPTS:

## Ad 1: Pain Point Hook
- Hook (first 3 seconds)
- Problem agitation
- Solution intro
- CTA

## Ad 2: "I Tried Everything" Story
- Relatable struggle
- Discovery moment
- Transformation
- CTA

## Ad 3: Social Proof Angle
- Specific result
- "Here's how" explanation
- CTA

FOR EACH INCLUDE:
- Video script (30-60 seconds)
- Static ad headline + copy
- Thumbnail/image suggestion

Use actual language patterns from the research."""}
        ],
        temperature=0.8,
        max_tokens=2500
    ).choices[0].message.content

    output = f"""# Reddit-Informed Ad Scripts

**Topic:** {args.topic}
**Product:** {args.product}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

## Reddit Research Summary

{research or "No real-time research available"}

---

{ads}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Ad scripts saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
