#!/usr/bin/env python3
"""
LinkedIn DM Generator - Create personalized LinkedIn direct messages.

Usage:
    python3 execution/generate_linkedin_dm.py \
        --name "John Smith" \
        --title "VP of Marketing" \
        --company "Acme Corp" \
        --offer "Marketing automation" \
        --output .tmp/linkedin_dm.md
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
    parser = argparse.ArgumentParser(description="Generate LinkedIn DMs")
    parser.add_argument("--name", "-n", required=True)
    parser.add_argument("--title", "-t", default="")
    parser.add_argument("--company", "-c", default="")
    parser.add_argument("--offer", "-o", required=True, help="What you're offering")
    parser.add_argument("--context", default="", help="Additional context")
    parser.add_argument("--output", default=".tmp/linkedin_dm.md")
    args = parser.parse_args()

    print(f"\n💬 LinkedIn DM Generator\n   To: {args.name}\n")
    client = get_client()

    dms = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You write LinkedIn DMs that get responses. Keep them short, personal, and non-salesy."},
            {"role": "user", "content": f"""Create LinkedIn DMs for:

RECIPIENT: {args.name}
TITLE: {args.title or "Unknown"}
COMPANY: {args.company or "Unknown"}
WHAT I'M OFFERING: {args.offer}
CONTEXT: {args.context or "Cold outreach"}

CREATE 3 DM VARIATIONS:

## DM 1: Connection Request Note
[Under 300 characters - for connection request]

## DM 2: Initial Message (After Connected)
[Under 500 characters - first real message]

## DM 3: Follow-up (If No Response)
[Under 300 characters - gentle nudge]

ALSO PROVIDE:

## Voice Note Script (30 seconds)
[What to say in a LinkedIn voice message]

## Video Message Script (60 seconds)
[For video DM if they have it enabled]

RULES:
- No "I hope this finds you well"
- No pitching in first message
- Lead with curiosity or value
- Reference something specific
- Always have a soft CTA
- Sound human, not templated"""}
        ],
        temperature=0.8,
        max_tokens=1500
    ).choices[0].message.content

    output = f"""# LinkedIn DM: {args.name}

**Title:** {args.title}
**Company:** {args.company}
**Offer:** {args.offer}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{dms}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ DMs saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
