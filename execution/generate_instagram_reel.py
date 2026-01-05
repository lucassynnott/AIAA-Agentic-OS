#!/usr/bin/env python3
"""
Instagram Reel Script Generator - Create scripts for short-form video.

Usage:
    python3 execution/generate_instagram_reel.py \
        --topic "5 Cold Email Mistakes" \
        --length 30 \
        --style "educational" \
        --output .tmp/reel_script.md
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
    parser = argparse.ArgumentParser(description="Generate Instagram Reel scripts")
    parser.add_argument("--topic", "-t", required=True)
    parser.add_argument("--length", "-l", type=int, default=30, choices=[15, 30, 60, 90])
    parser.add_argument("--style", "-s", default="educational", choices=["educational", "entertaining", "motivational", "story"])
    parser.add_argument("--output", "-o", default=".tmp/reel_script.md")
    args = parser.parse_args()

    print(f"\n🎬 Reel Script Generator\n   Topic: {args.topic}\n   Length: {args.length}s\n")
    client = get_client()

    script = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You create viral Instagram Reel scripts. Style: {args.style}. Focus on hooks and retention."},
            {"role": "user", "content": f"""Create a {args.length}-second Reel script:

TOPIC: {args.topic}
LENGTH: {args.length} seconds
STYLE: {args.style}

PROVIDE:

## HOOK (First 3 seconds)
- Visual: [What's on screen]
- Audio: [Exact words]
- Text overlay: [On-screen text]

## MAIN CONTENT ({args.length - 8} seconds)
- [Second-by-second breakdown]
- Visual cues
- Exact script

## CTA (Last 5 seconds)
- What to say
- On-screen text

## CAPTION
- Hook line
- Value summary
- CTA
- Hashtags (10-15)

## AUDIO SUGGESTIONS
- Trending sound recommendation
- Voice-over tips

## THUMBNAIL FRAME
- Best frame for cover
- Text overlay suggestion

RULES:
- Hook must stop scroll in 1 second
- One idea per reel
- Clear value or entertainment
- End with CTA"""}
        ],
        temperature=0.8,
        max_tokens=1500
    ).choices[0].message.content

    output = f"""# Instagram Reel Script

**Topic:** {args.topic}
**Length:** {args.length} seconds
**Style:** {args.style}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{script}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Script saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
