#!/usr/bin/env python3
"""
Carousel Post Creator - Generate LinkedIn/Instagram carousel content.

Usage:
    python3 execution/generate_carousel.py \
        --topic "5 Cold Email Mistakes" \
        --slides 8 \
        --platform linkedin \
        --output .tmp/carousel.md
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
    parser = argparse.ArgumentParser(description="Generate carousel posts")
    parser.add_argument("--topic", "-t", required=True)
    parser.add_argument("--slides", "-s", type=int, default=8)
    parser.add_argument("--platform", "-p", default="linkedin", choices=["linkedin", "instagram"])
    parser.add_argument("--output", "-o", default=".tmp/carousel.md")
    args = parser.parse_args()

    print(f"\n📱 Carousel Creator\n   Topic: {args.topic}\n   Slides: {args.slides}\n")
    client = get_client()

    carousel = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You create high-engagement {args.platform} carousel posts."},
            {"role": "user", "content": f"""Create a {args.slides}-slide carousel:

TOPIC: {args.topic}
PLATFORM: {args.platform}
SLIDES: {args.slides}

CAROUSEL STRUCTURE:
- Slide 1: Hook/Title (grab attention)
- Slides 2-{args.slides-1}: Value slides
- Slide {args.slides}: CTA slide

FOR EACH SLIDE PROVIDE:

## Slide X: [Title]
**Headline:** (5-8 words, bold)
**Body:** (15-25 words supporting text)
**Visual:** (Design suggestion)

---

RULES:
- Each slide = ONE idea only
- Use simple language
- Create visual contrast
- Include numbers where possible
- End with clear CTA

Also provide:
- Caption for the post (with hashtags)
- Best posting time
- Engagement strategy"""}
        ],
        temperature=0.8,
        max_tokens=2500
    ).choices[0].message.content

    output = f"""# Carousel: {args.topic}

**Platform:** {args.platform.title()}
**Slides:** {args.slides}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{carousel}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Carousel saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
