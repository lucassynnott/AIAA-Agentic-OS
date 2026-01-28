#!/usr/bin/env python3
"""
Product Description Writer - Generate e-commerce product descriptions.

Usage:
    python3 execution/generate_product_description.py \
        --product "Wireless Headphones" \
        --features "40hr battery, ANC, Bluetooth 5.0" \
        --audience "Remote workers" \
        --tone "premium" \
        --output .tmp/product_desc.md
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
    parser = argparse.ArgumentParser(description="Generate product descriptions")
    parser.add_argument("--product", "-p", required=True)
    parser.add_argument("--features", "-f", required=True, help="Key features")
    parser.add_argument("--audience", "-a", default="", help="Target audience")
    parser.add_argument("--tone", "-t", default="professional", choices=["premium", "casual", "technical", "playful"])
    parser.add_argument("--platform", default="shopify", choices=["shopify", "amazon", "etsy", "general"])
    parser.add_argument("--output", "-o", default=".tmp/product_desc.md")
    args = parser.parse_args()

    print(f"\n🛍️ Product Description Writer\n   Product: {args.product}\n")
    client = get_client()

    desc = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You write high-converting {args.platform} product descriptions in a {args.tone} tone."},
            {"role": "user", "content": f"""Write product copy for:

PRODUCT: {args.product}
FEATURES: {args.features}
TARGET AUDIENCE: {args.audience or "General consumers"}
TONE: {args.tone}
PLATFORM: {args.platform}

PROVIDE:

## Product Title Options (3)
- SEO-optimized titles

## Short Description (50-100 words)
- Hook + key benefit
- For product cards/previews

## Long Description (200-300 words)
- Opening hook
- Problem/solution
- Key features with benefits
- Social proof placeholder
- CTA

## Bullet Points (5-7)
- Feature → Benefit format
- Easy to scan

## SEO Keywords
- Primary keyword
- Secondary keywords (5)
- Long-tail keywords (3)

## Meta Description
- 155 characters max
- Include keyword + CTA

Make it benefit-focused, not just feature-focused."""}
        ],
        temperature=0.7,
        max_tokens=2000
    ).choices[0].message.content

    output = f"""# Product Description: {args.product}

**Platform:** {args.platform.title()}
**Tone:** {args.tone}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{desc}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Description saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
