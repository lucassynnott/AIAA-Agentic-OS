#!/usr/bin/env python3
"""
Contract Renewal Reminder - Generate renewal outreach for expiring contracts.

Usage:
    python3 execution/remind_contract_renewal.py \
        --client "Acme Corp" \
        --days_until 30 \
        --value 50000 \
        --output .tmp/renewal_reminder.md
"""

import argparse, os, sys
from datetime import datetime, timedelta
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
    parser = argparse.ArgumentParser(description="Generate renewal reminders")
    parser.add_argument("--client", "-c", required=True)
    parser.add_argument("--days_until", "-d", type=int, required=True, help="Days until expiry")
    parser.add_argument("--value", "-v", type=float, default=0, help="Contract value")
    parser.add_argument("--wins", "-w", default="", help="Key wins/results achieved")
    parser.add_argument("--output", "-o", default=".tmp/renewal_reminder.md")
    args = parser.parse_args()

    expiry_date = (datetime.now() + timedelta(days=args.days_until)).strftime("%Y-%m-%d")
    
    print(f"\n📋 Contract Renewal Reminder\n   Client: {args.client}\n   Expires in: {args.days_until} days\n")
    client = get_client()

    reminder = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You write compelling contract renewal outreach that highlights value delivered."},
            {"role": "user", "content": f"""Create renewal outreach for:

CLIENT: {args.client}
CONTRACT EXPIRES: {expiry_date} ({args.days_until} days)
CONTRACT VALUE: ${args.value:,.2f if args.value else "Not specified"}
KEY WINS: {args.wins or "Review account for wins"}

CREATE:

## Email 1: Initial Renewal Outreach ({args.days_until} days out)
- Subject lines (3)
- Body: Value recap, renewal benefits, next steps
- CTA: Schedule renewal discussion

## Email 2: Follow-up (if no response)
- Subject lines (3)
- Shorter, more direct

## Talking Points for Renewal Call
- Value delivered recap
- ROI metrics to highlight
- New features/improvements
- Upsell opportunities
- Objection handling

## Renewal Proposal Outline
- Executive summary
- Results delivered
- Continued partnership benefits
- Pricing/terms
- Next steps

Make it value-focused, not pushy."""}
        ],
        temperature=0.7,
        max_tokens=2000
    ).choices[0].message.content

    output = f"""# Contract Renewal: {args.client}

**Expiry Date:** {expiry_date}
**Days Until:** {args.days_until}
**Value:** ${args.value:,.2f if args.value else "TBD"}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{reminder}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Reminder saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
