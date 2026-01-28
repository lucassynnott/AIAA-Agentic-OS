#!/usr/bin/env python3
"""
Email Flow Writer - Generate automated email sequences (welcome, abandoned cart, etc).

Usage:
    python3 execution/generate_email_flow.py \
        --flow_type "welcome" \
        --business "SaaS Company" \
        --product "Project Management Tool" \
        --emails 5 \
        --output .tmp/email_flow.md
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
    parser = argparse.ArgumentParser(description="Generate email flows")
    parser.add_argument("--flow_type", "-t", required=True, 
        choices=["welcome", "abandoned_cart", "onboarding", "nurture", "win_back", "post_purchase"])
    parser.add_argument("--business", "-b", required=True)
    parser.add_argument("--product", "-p", default="")
    parser.add_argument("--emails", "-e", type=int, default=5)
    parser.add_argument("--output", "-o", default=".tmp/email_flow.md")
    args = parser.parse_args()

    flow_contexts = {
        "welcome": "New subscriber welcome sequence",
        "abandoned_cart": "Cart abandonment recovery",
        "onboarding": "New customer onboarding",
        "nurture": "Lead nurturing sequence",
        "win_back": "Re-engagement for inactive users",
        "post_purchase": "Post-purchase follow-up"
    }

    print(f"\n📧 Email Flow Writer\n   Type: {args.flow_type}\n   Emails: {args.emails}\n")
    client = get_client()

    flow = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are an email marketing expert who creates high-converting automated sequences."},
            {"role": "user", "content": f"""Create a {args.emails}-email {args.flow_type} sequence:

BUSINESS: {args.business}
PRODUCT: {args.product or "Not specified"}
FLOW TYPE: {args.flow_type} - {flow_contexts[args.flow_type]}
NUMBER OF EMAILS: {args.emails}

FOR EACH EMAIL PROVIDE:

## Email X: [Name]

**Trigger/Timing:** When this email sends
**Goal:** What this email should achieve

**Subject Lines (3 options):**
1. 
2. 
3. 

**Preview Text:**

**Email Body:**
[Complete email copy]

**CTA:**

**Design Notes:**
- Key visual elements
- Image suggestions

---

SEQUENCE STRATEGY:
- Overall flow logic
- Key conversion points
- Expected metrics

Make emails conversational, value-driven, and action-oriented."""}
        ],
        temperature=0.7,
        max_tokens=4000
    ).choices[0].message.content

    output = f"""# Email Flow: {args.flow_type.replace('_', ' ').title()}

**Business:** {args.business}
**Emails:** {args.emails}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{flow}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Flow saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
