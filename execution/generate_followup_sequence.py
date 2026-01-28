#!/usr/bin/env python3
"""
Follow-up Sequence Generator - Create follow-up email sequences.

Usage:
    python3 execution/generate_followup_sequence.py \
        --context "Met at conference, discussed marketing automation" \
        --goal "book_call" \
        --emails 4 \
        --output .tmp/followup_sequence.md
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
    parser = argparse.ArgumentParser(description="Generate follow-up sequences")
    parser.add_argument("--context", "-c", required=True, help="Context of initial interaction")
    parser.add_argument("--goal", "-g", default="book_call", choices=["book_call", "get_reply", "close_deal", "reconnect"])
    parser.add_argument("--emails", "-e", type=int, default=4, help="Number of follow-ups")
    parser.add_argument("--tone", "-t", default="professional", choices=["professional", "casual", "friendly"])
    parser.add_argument("--output", "-o", default=".tmp/followup_sequence.md")
    args = parser.parse_args()

    print(f"\n📧 Follow-up Sequence Generator\n   Goal: {args.goal}\n   Emails: {args.emails}\n")
    client = get_client()

    sequence = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You write effective follow-up email sequences. Tone: {args.tone}."},
            {"role": "user", "content": f"""Create a {args.emails}-email follow-up sequence:

CONTEXT: {args.context}
GOAL: {args.goal}
TONE: {args.tone}

FOR EACH EMAIL:

## Follow-up {'{n}'}: [Day X]

**Timing:** Days after previous
**Subject Lines (3):**

**Email Body:**
[Complete email - keep under 100 words]

**CTA:**

---

SEQUENCE STRATEGY:
- Email 1: Reference initial interaction
- Email 2: Add value/insight
- Email 3: Different angle/social proof
- Email 4+: Breakup or reconnect

RULES:
- Each email under 100 words
- Different approach each time
- Never sound desperate
- Always provide easy out
- Reference previous emails subtly"""}
        ],
        temperature=0.7,
        max_tokens=2500
    ).choices[0].message.content

    output = f"""# Follow-up Sequence

**Context:** {args.context}
**Goal:** {args.goal}
**Emails:** {args.emails}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{sequence}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Sequence saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
