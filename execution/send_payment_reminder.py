#!/usr/bin/env python3
"""
Payment Reminder Generator - Generate payment reminder emails.

Usage:
    python3 execution/send_payment_reminder.py \
        --client "Acme Corp" \
        --amount 5000 \
        --days_overdue 7 \
        --output .tmp/payment_reminder.md
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
    parser = argparse.ArgumentParser(description="Generate payment reminders")
    parser.add_argument("--client", "-c", required=True)
    parser.add_argument("--amount", "-a", type=float, required=True)
    parser.add_argument("--days_overdue", "-d", type=int, default=0)
    parser.add_argument("--invoice_num", default="")
    parser.add_argument("--output", "-o", default=".tmp/payment_reminder.md")
    args = parser.parse_args()

    # Determine tone based on days overdue
    if args.days_overdue <= 0:
        tone = "friendly"
        urgency = "upcoming"
    elif args.days_overdue <= 7:
        tone = "polite"
        urgency = "gentle reminder"
    elif args.days_overdue <= 14:
        tone = "firm"
        urgency = "second notice"
    else:
        tone = "serious"
        urgency = "urgent final notice"

    print(f"\n💳 Payment Reminder Generator\n   Client: {args.client}\n   Amount: ${args.amount:,.2f}\n   Days overdue: {args.days_overdue}\n")
    
    client = get_client()

    reminder = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You write payment reminder emails. Tone: {tone}. Keep professional while being clear about next steps."},
            {"role": "user", "content": f"""Create a payment reminder email:

CLIENT: {args.client}
AMOUNT DUE: ${args.amount:,.2f}
INVOICE: {args.invoice_num or "Recent invoice"}
DAYS OVERDUE: {args.days_overdue}
URGENCY LEVEL: {urgency}

CREATE:

## Subject Lines (3)

## Email Body
- Professional greeting
- Clear statement of amount due
- Original due date reference
- Payment methods
- Offer to discuss if issues
- Clear next steps
- Professional close

## Follow-up SMS (if applicable)
[Short text version]

Keep under 150 words. Be {tone} but clear."""}
        ],
        temperature=0.6,
        max_tokens=1000
    ).choices[0].message.content

    output = f"""# Payment Reminder: {args.client}

**Amount:** ${args.amount:,.2f}
**Days Overdue:** {args.days_overdue}
**Urgency:** {urgency}
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
