#!/usr/bin/env python3
"""
Twitter Thread Writer - Generate viral Twitter/X threads.

Usage:
    python3 execution/generate_twitter_thread.py \
        --topic "How I grew from 0 to 10k followers" \
        --style "story" \
        --length 10 \
        --output .tmp/twitter_thread.md
"""

import argparse, os, sys
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"

def main():
    parser = argparse.ArgumentParser(description="Generate Twitter threads")
    parser.add_argument("--topic", "-t", required=True)
    parser.add_argument("--style", "-s", default="educational", choices=["story", "educational", "listicle", "contrarian"])
    parser.add_argument("--length", "-l", type=int, default=10, help="Number of tweets")
    parser.add_argument("--output", "-o", default=".tmp/twitter_thread.md")
    args = parser.parse_args()

    print(f"\n🐦 Twitter Thread Writer\n   Topic: {args.topic}\n   Style: {args.style}\n")
    client = get_client()

    thread = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are a Twitter expert who writes viral threads with high engagement."},
            {"role": "user", "content": f"""Write a {args.length}-tweet thread:

TOPIC: {args.topic}
STYLE: {args.style}

THREAD STRUCTURE:
- Tweet 1: Hook (must stop scroll, create curiosity)
- Tweets 2-{args.length-1}: Value delivery
- Tweet {args.length}: CTA + summary

RULES:
- Each tweet max 280 characters
- Use line breaks for readability
- Include engagement hooks throughout
- End with retweet/follow CTA
- Number format: "1/" or use emojis

FORMAT OUTPUT AS:

**Tweet 1 (Hook)**
[Tweet text]

**Tweet 2**
[Tweet text]

...

**Tweet {args.length} (CTA)**
[Tweet text]

---

**Thread Summary:** One line description
**Best Time to Post:** Recommendation
**Engagement Tip:** How to maximize reach

Make it specific, valuable, and shareable."""}
        ],
        temperature=0.8,
        max_tokens=2500
    ).choices[0].message.content

    output = f"""# Twitter Thread: {args.topic}

**Style:** {args.style}
**Length:** {args.length} tweets
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{thread}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Thread saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
