#!/usr/bin/env python3
"""
Static Ad Generator - Generate static image ad copy and concepts.

Usage:
    python3 execution/generate_static_ad.py \
        --product "SaaS Tool" \
        --offer "50% off" \
        --platform "facebook" \
        --output .tmp/static_ads.md
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
    parser = argparse.ArgumentParser(description="Generate static ad concepts")
    parser.add_argument("--product", "-p", required=True)
    parser.add_argument("--offer", "-o", default="", help="Special offer")
    parser.add_argument("--platform", default="facebook", choices=["facebook", "instagram", "linkedin", "google"])
    parser.add_argument("--audience", "-a", default="", help="Target audience")
    parser.add_argument("--variations", "-v", type=int, default=5)
    parser.add_argument("--output", default=".tmp/static_ads.md")
    args = parser.parse_args()

    print(f"\n🖼️ Static Ad Generator\n   Product: {args.product}\n   Platform: {args.platform}\n")
    client = get_client()

    ads = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You create high-converting static ads for {args.platform}."},
            {"role": "user", "content": f"""Create {args.variations} static ad concepts:

PRODUCT: {args.product}
OFFER: {args.offer or "No special offer"}
PLATFORM: {args.platform}
AUDIENCE: {args.audience or "General"}

FOR EACH AD VARIATION:

## Ad {'{n}'}: [Angle Name]

**Visual Concept:**
- Main image/graphic description
- Color scheme
- Layout (text placement)

**Headline:** (under 5 words)

**Primary Text:** (for feed copy)

**Description:** (for link description)

**CTA Button:** 

**Design Notes:**
- Font style
- Visual elements (icons, arrows, etc.)
- Contrast/readability tips

**Why This Works:**
- Psychology behind it

---

ANGLES TO COVER:
1. Problem-focused
2. Benefit-focused
3. Social proof
4. Urgency/scarcity
5. Curiosity/question

Keep text minimal on images - most impact in fewest words."""}
        ],
        temperature=0.8,
        max_tokens=2500
    ).choices[0].message.content

    output = f"""# Static Ad Concepts

**Product:** {args.product}
**Platform:** {args.platform}
**Offer:** {args.offer or "None"}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{ads}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Ads saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
