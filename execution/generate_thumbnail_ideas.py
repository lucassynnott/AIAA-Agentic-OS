#!/usr/bin/env python3
"""
AI Thumbnail Generator - Generate YouTube thumbnail concepts.

Usage:
    python3 execution/generate_thumbnail_ideas.py \
        --title "How I Made $100k in 30 Days" \
        --niche "business" \
        --output .tmp/thumbnail_ideas.md
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
    parser = argparse.ArgumentParser(description="Generate thumbnail ideas")
    parser.add_argument("--title", "-t", required=True, help="Video title")
    parser.add_argument("--niche", "-n", default="general", help="Content niche")
    parser.add_argument("--style", "-s", default="", help="Thumbnail style preference")
    parser.add_argument("--output", "-o", default=".tmp/thumbnail_ideas.md")
    args = parser.parse_args()

    print(f"\n🖼️ Thumbnail Generator\n   Title: {args.title}\n")
    client = get_client()

    ideas = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You create high-CTR YouTube thumbnail concepts based on proven patterns."},
            {"role": "user", "content": f"""Create 5 thumbnail concepts for:

VIDEO TITLE: {args.title}
NICHE: {args.niche}
STYLE PREFERENCE: {args.style or "Open to suggestions"}

FOR EACH THUMBNAIL CONCEPT:

## Concept {'{n}'}: [Name]

**Visual Layout:**
- Main element
- Background
- Composition (rule of thirds, etc.)

**Text Overlay:**
- Main text (3-4 words MAX)
- Font style
- Color

**Facial Expression:** (if applicable)
- Emotion to convey
- Eye direction

**Color Scheme:**
- Primary colors
- Contrast elements

**Design Elements:**
- Arrows, circles, etc.
- Before/after split
- Props

**Why It Works:**
- Psychology behind it

---

THUMBNAIL BEST PRACTICES:
- Bright, contrasting colors
- Large, readable text (readable at small size)
- Clear focal point
- Emotional faces perform well
- Create curiosity gap
- Don't repeat the title exactly"""}
        ],
        temperature=0.8,
        max_tokens=2000
    ).choices[0].message.content

    output = f"""# YouTube Thumbnail Ideas

**Video:** {args.title}
**Niche:** {args.niche}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{ideas}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Ideas saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
