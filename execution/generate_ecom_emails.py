#!/usr/bin/env python3
"""
E-commerce Email Campaign Generator - Create email campaigns for e-commerce.

Usage:
    python3 execution/generate_ecom_emails.py \
        --campaign_type "product_launch" \
        --product "New Summer Collection" \
        --brand "Fashion Brand" \
        --output .tmp/ecom_emails.md
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
    parser = argparse.ArgumentParser(description="Generate e-commerce email campaigns")
    parser.add_argument("--campaign_type", "-t", required=True,
        choices=["product_launch", "sale", "abandoned_cart", "back_in_stock", "loyalty", "seasonal", "vip"])
    parser.add_argument("--product", "-p", required=True)
    parser.add_argument("--brand", "-b", required=True)
    parser.add_argument("--discount", "-d", default="")
    parser.add_argument("--urgency", default="")
    parser.add_argument("--output", "-o", default=".tmp/ecom_emails.md")
    args = parser.parse_args()

    campaign_configs = {
        "product_launch": {"emails": 3, "desc": "New product announcement"},
        "sale": {"emails": 4, "desc": "Sale/promotion campaign"},
        "abandoned_cart": {"emails": 3, "desc": "Cart recovery sequence"},
        "back_in_stock": {"emails": 2, "desc": "Back in stock notification"},
        "loyalty": {"emails": 3, "desc": "Customer loyalty/rewards"},
        "seasonal": {"emails": 4, "desc": "Seasonal promotion"},
        "vip": {"emails": 3, "desc": "VIP/exclusive access"}
    }

    config = campaign_configs[args.campaign_type]
    print(f"\n🛒 E-commerce Email Generator\n   Type: {args.campaign_type}\n   Product: {args.product}\n")
    client = get_client()

    campaign = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You create high-converting e-commerce email campaigns with proven frameworks."},
            {"role": "user", "content": f"""Create a {args.campaign_type} email campaign:

BRAND: {args.brand}
PRODUCT: {args.product}
CAMPAIGN TYPE: {args.campaign_type} - {config['desc']}
DISCOUNT: {args.discount or "Not specified"}
URGENCY: {args.urgency or "Standard"}
NUMBER OF EMAILS: {config['emails']}

FOR EACH EMAIL PROVIDE:

## Email X: [Name]

**Timing:** When to send
**Goal:** Primary objective

**Subject Lines (3):**
1. 
2. 
3. 

**Preview Text:**

**Email Structure:**
- Header/Hero image description
- Headline
- Body copy
- Product showcase section
- CTA button text
- Secondary CTA

**Design Notes:**
- Color recommendations
- Image suggestions
- Mobile considerations

---

CAMPAIGN STRATEGY:
- Optimal send times
- Segmentation suggestions
- A/B test recommendations
- Expected metrics

Make emails brand-appropriate, conversion-focused, and visually engaging."""}
        ],
        temperature=0.7,
        max_tokens=3500
    ).choices[0].message.content

    output = f"""# E-commerce Email Campaign

**Brand:** {args.brand}
**Campaign Type:** {args.campaign_type}
**Product:** {args.product}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{campaign}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Campaign saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
