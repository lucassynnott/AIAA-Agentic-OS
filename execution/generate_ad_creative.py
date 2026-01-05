#!/usr/bin/env python3
"""
Ad Creative Generator - Generate ad copy for Facebook, Google, LinkedIn ads.

Usage:
    python3 execution/generate_ad_creative.py \
        --product "SaaS Tool" \
        --platform "facebook" \
        --goal "conversions" \
        --audience "B2B marketers" \
        --output .tmp/ad_creative.md
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv()


def get_client() -> OpenAI:
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def call_llm(client: OpenAI, system: str, user: str, temp: float = 0.7) -> str:
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=get_model(),
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=temp, max_tokens=3000
            )
            return resp.choices[0].message.content
        except Exception as e:
            if attempt == 2: raise e
    return ""


def generate_ads(client: OpenAI, product: str, platform: str, goal: str, audience: str, offer: str) -> str:
    """Generate ad creative for specified platform."""
    
    platform_specs = {
        "facebook": {
            "headline_chars": 40,
            "primary_text": 125,
            "description": 30,
            "formats": ["Single image", "Carousel", "Video"]
        },
        "google": {
            "headline_chars": 30,
            "description": 90,
            "formats": ["Search", "Display", "Performance Max"]
        },
        "linkedin": {
            "headline_chars": 70,
            "intro_text": 150,
            "formats": ["Sponsored Content", "Message Ad", "Text Ad"]
        }
    }
    
    specs = platform_specs.get(platform, platform_specs["facebook"])
    
    system_prompt = f"""You are an expert {platform} ads copywriter with proven ROAS results.
Create high-converting ad copy that follows platform best practices and character limits."""
    
    user_prompt = f"""Create ad creative for {platform}:

PRODUCT/SERVICE: {product}
TARGET AUDIENCE: {audience}
CAMPAIGN GOAL: {goal}
OFFER: {offer or "Not specified"}

PLATFORM SPECS:
- Headline max: {specs.get('headline_chars', 40)} chars
- Body text max: {specs.get('primary_text', specs.get('description', 90))} chars
- Available formats: {', '.join(specs['formats'])}

CREATE 3 AD VARIATIONS:

## AD 1: Pain Point Focus
- Headlines (3 options)
- Primary text/body
- Call to action
- Image/video concept suggestion

## AD 2: Benefit/Outcome Focus
- Headlines (3 options)
- Primary text/body
- Call to action
- Image/video concept suggestion

## AD 3: Social Proof/Urgency Focus
- Headlines (3 options)
- Primary text/body
- Call to action
- Image/video concept suggestion

FOR EACH AD INCLUDE:
- Character counts for each element
- A/B testing hypothesis
- Audience targeting suggestion

Make copy specific, benefit-driven, and action-oriented.
Follow {platform}'s ad policies (no exaggerated claims, misleading content)."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.8)


def main():
    parser = argparse.ArgumentParser(description="Generate ad creative")
    parser.add_argument("--product", "-p", required=True, help="Product/service")
    parser.add_argument("--platform", "-l", default="facebook",
        choices=["facebook", "google", "linkedin", "tiktok"])
    parser.add_argument("--goal", "-g", default="conversions",
        choices=["conversions", "leads", "traffic", "awareness", "engagement"])
    parser.add_argument("--audience", "-a", required=True, help="Target audience")
    parser.add_argument("--offer", "-f", default="", help="Special offer/discount")
    parser.add_argument("--output", "-o", default=".tmp/ad_creative.md")
    
    args = parser.parse_args()
    
    print(f"\n📢 Ad Creative Generator")
    print(f"   Product: {args.product}")
    print(f"   Platform: {args.platform}")
    print(f"   Goal: {args.goal}")
    print(f"   Audience: {args.audience}\n")
    
    client = get_client()
    
    print("🎨 Generating ad variations...")
    ads = generate_ads(client, args.product, args.platform, args.goal, args.audience, args.offer)
    
    output = f"""# Ad Creative: {args.product}

**Platform:** {args.platform.title()}
**Goal:** {args.goal}
**Audience:** {args.audience}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{ads}
"""
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    
    print(f"\n✅ Ad creative complete!")
    print(f"   📄 Output: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
