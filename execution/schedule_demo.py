#!/usr/bin/env python3
"""
Demo Scheduler - Generate demo confirmation and prep materials.

Usage:
    python3 execution/schedule_demo.py \
        --prospect "John Smith" \
        --company "Acme Corp" \
        --datetime "2024-01-15 2:00 PM" \
        --product "Marketing Platform" \
        --output .tmp/demo_prep.md
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
    parser = argparse.ArgumentParser(description="Generate demo prep materials")
    parser.add_argument("--prospect", "-p", required=True)
    parser.add_argument("--company", "-c", required=True)
    parser.add_argument("--datetime", "-d", required=True, help="Demo date/time")
    parser.add_argument("--product", required=True, help="Product being demoed")
    parser.add_argument("--notes", "-n", default="", help="Additional context")
    parser.add_argument("--output", "-o", default=".tmp/demo_prep.md")
    args = parser.parse_args()

    print(f"\n📅 Demo Scheduler\n   Prospect: {args.prospect}\n   Company: {args.company}\n")
    client = get_client()

    prep = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You prepare sales demos for maximum effectiveness."},
            {"role": "user", "content": f"""Prepare demo materials for:

PROSPECT: {args.prospect}
COMPANY: {args.company}
DATE/TIME: {args.datetime}
PRODUCT: {args.product}
NOTES: {args.notes or "Standard discovery call"}

CREATE:

## Confirmation Email
- Subject line
- Body with:
  - Date/time confirmation
  - Meeting link placeholder
  - What to prepare
  - Agenda preview

## Pre-Demo Research Checklist
- [ ] Company website review
- [ ] LinkedIn profile check
- [ ] Recent news
- [ ] Competitor landscape
- [ ] Potential pain points

## Demo Agenda (30-45 min)
1. Intro & rapport (5 min)
2. Discovery questions (10 min)
3. Tailored demo (15-20 min)
4. Q&A (5 min)
5. Next steps (5 min)

## Key Discovery Questions
1. Question about current situation
2. Question about pain points
3. Question about goals
4. Question about decision process
5. Question about timeline

## Features to Highlight
Based on {args.company}'s likely needs:
- Feature 1 and benefit
- Feature 2 and benefit
- Feature 3 and benefit

## Objection Prep
- Common objection 1 + response
- Common objection 2 + response

## Post-Demo Follow-up Template
- Subject line
- Recap key points
- Next steps
- Resources to share"""}
        ],
        temperature=0.6,
        max_tokens=2000
    ).choices[0].message.content

    output = f"""# Demo Prep: {args.prospect} @ {args.company}

**Date/Time:** {args.datetime}
**Product:** {args.product}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{prep}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Demo prep saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
