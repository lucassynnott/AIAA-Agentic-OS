#!/usr/bin/env python3
"""
Webinar Follow-up Generator - Create post-webinar follow-up sequences.

Usage:
    python3 execution/generate_webinar_followup.py \
        --webinar "Marketing Automation Masterclass" \
        --offer "Automation Course" \
        --price "$997" \
        --output .tmp/webinar_followup.md
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
    parser = argparse.ArgumentParser(description="Generate webinar follow-up")
    parser.add_argument("--webinar", "-w", required=True, help="Webinar title")
    parser.add_argument("--offer", "-o", required=True, help="Offer being made")
    parser.add_argument("--price", "-p", required=True, help="Price point")
    parser.add_argument("--deadline", "-d", default="72 hours", help="Offer deadline")
    parser.add_argument("--output", default=".tmp/webinar_followup.md")
    args = parser.parse_args()

    print(f"\n📧 Webinar Follow-up Generator\n   Webinar: {args.webinar}\n")
    client = get_client()

    followup = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You create high-converting post-webinar email sequences."},
            {"role": "user", "content": f"""Create webinar follow-up sequence:

WEBINAR: {args.webinar}
OFFER: {args.offer}
PRICE: {args.price}
DEADLINE: {args.deadline}

CREATE SEQUENCES FOR TWO SEGMENTS:

## SEGMENT A: ATTENDED LIVE

### Email 1: Immediate (within 1 hour)
- Subject lines (3)
- Replay link + key takeaways
- Offer reminder with deadline

### Email 2: Next Day
- Address common questions
- Social proof
- Urgency

### Email 3: Day 2
- Case study focus
- Objection handling
- Scarcity

### Email 4: Final Hours
- Last chance
- Bonus stack reminder
- Clear deadline

---

## SEGMENT B: REGISTERED BUT DIDN'T ATTEND

### Email 1: Immediate
- "You missed it" - create FOMO
- Replay link (limited time)
- Highlight best moment

### Email 2: Next Day
- What they missed
- Replay expiring
- Special offer for non-attendees?

### Email 3: Final Notice
- Replay coming down
- Offer deadline
- Last chance

---

## SMS MESSAGES (for both segments)
- Immediate reminder
- 24-hour warning
- Final hours

Make emails urgency-driven but value-focused."""}
        ],
        temperature=0.7,
        max_tokens=3000
    ).choices[0].message.content

    output = f"""# Webinar Follow-up: {args.webinar}

**Offer:** {args.offer}
**Price:** {args.price}
**Deadline:** {args.deadline}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{followup}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Follow-up saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
