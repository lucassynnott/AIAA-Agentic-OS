#!/usr/bin/env python3
"""
Press Release Generator - Generate professional press releases.

Usage:
    python3 execution/generate_press_release.py \
        --company "Acme Corp" \
        --announcement "Launches AI-powered platform" \
        --details "New features include..." \
        --output .tmp/press_release.md
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
    parser = argparse.ArgumentParser(description="Generate press releases")
    parser.add_argument("--company", "-c", required=True)
    parser.add_argument("--announcement", "-a", required=True, help="Main announcement")
    parser.add_argument("--details", "-d", default="", help="Supporting details")
    parser.add_argument("--quote_person", default="", help="Person for quote")
    parser.add_argument("--quote_title", default="CEO", help="Title of quote person")
    parser.add_argument("--contact", default="", help="Media contact info")
    parser.add_argument("--output", "-o", default=".tmp/press_release.md")
    args = parser.parse_args()

    print(f"\n📰 Press Release Generator\n   Company: {args.company}\n")
    client = get_client()

    pr = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You write professional press releases following AP style guidelines."},
            {"role": "user", "content": f"""Write a press release:

COMPANY: {args.company}
ANNOUNCEMENT: {args.announcement}
DETAILS: {args.details or "Not provided"}
QUOTE FROM: {args.quote_person or "[Executive Name]"}, {args.quote_title}
DATE: {datetime.now().strftime("%B %d, %Y")}

FORMAT:

**FOR IMMEDIATE RELEASE**

# [Headline - Compelling, newsworthy]

## [Subheadline - Supporting detail]

**[CITY, STATE]** — [Dateline] — [Opening paragraph: Who, What, When, Where, Why in 2-3 sentences]

[Second paragraph: Expand on the news, key details]

[Quote paragraph: Statement from executive]

[Third paragraph: Additional context, market impact]

[Quote paragraph: Optional second quote or customer quote]

[Boilerplate: About {args.company}]

**Media Contact:**
{args.contact or "[Contact Name]"}
[Email]
[Phone]

###

Make it newsworthy, factual, and quotable."""}
        ],
        temperature=0.6,
        max_tokens=2000
    ).choices[0].message.content

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(pr, encoding="utf-8")
    print(f"✅ Press release saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
