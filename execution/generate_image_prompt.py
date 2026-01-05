#!/usr/bin/env python3
"""
AI Image Generator - Generate image prompts for AI image tools.

Usage:
    python3 execution/generate_image_prompt.py \
        --concept "Professional headshot for LinkedIn" \
        --style "photorealistic" \
        --output .tmp/image_prompts.md
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
    parser = argparse.ArgumentParser(description="Generate AI image prompts")
    parser.add_argument("--concept", "-c", required=True, help="What you want to create")
    parser.add_argument("--style", "-s", default="photorealistic", 
        choices=["photorealistic", "illustration", "3d", "cartoon", "abstract", "minimalist"])
    parser.add_argument("--platform", "-p", default="midjourney", 
        choices=["midjourney", "dalle", "stable_diffusion", "ideogram"])
    parser.add_argument("--variations", "-v", type=int, default=5)
    parser.add_argument("--output", "-o", default=".tmp/image_prompts.md")
    args = parser.parse_args()

    print(f"\n🎨 AI Image Prompt Generator\n   Concept: {args.concept}\n   Style: {args.style}\n")
    client = get_client()

    prompts = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You create detailed prompts for {args.platform} that produce stunning images."},
            {"role": "user", "content": f"""Create {args.variations} image prompts for:

CONCEPT: {args.concept}
STYLE: {args.style}
PLATFORM: {args.platform}

FOR EACH PROMPT PROVIDE:

## Prompt {'{n}'}

**Full Prompt:**
[Detailed prompt with style, lighting, composition, mood]

**Negative Prompt:** (what to avoid)

**Settings:**
- Aspect ratio
- Quality settings
- Style parameters

---

PROMPT WRITING TIPS FOR {args.platform.upper()}:
{'- Use --ar for aspect ratio, --v 6 for version, --s for stylize' if args.platform == 'midjourney' else ''}
{'- Be very descriptive, include lighting and mood' if args.platform == 'dalle' else ''}
{'- Use negative prompts to avoid unwanted elements' if args.platform == 'stable_diffusion' else ''}

Make prompts specific, detailed, and optimized for the platform."""}
        ],
        temperature=0.9,
        max_tokens=2000
    ).choices[0].message.content

    output = f"""# AI Image Prompts

**Concept:** {args.concept}
**Style:** {args.style}
**Platform:** {args.platform}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{prompts}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Prompts saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
