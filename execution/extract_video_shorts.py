#!/usr/bin/env python3
"""
Video Shorts Extractor - Identify moments for short-form content from transcripts.

Usage:
    python3 execution/extract_video_shorts.py \
        --transcript transcript.txt \
        --output .tmp/shorts_clips.md
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
    parser = argparse.ArgumentParser(description="Extract shorts from video transcripts")
    parser.add_argument("--transcript", "-t", required=True, help="Transcript file")
    parser.add_argument("--clips", "-c", type=int, default=5, help="Number of clips to identify")
    parser.add_argument("--max_length", "-l", type=int, default=60, help="Max clip length in seconds")
    parser.add_argument("--output", "-o", default=".tmp/shorts_clips.md")
    args = parser.parse_args()

    transcript = Path(args.transcript).read_text()
    print(f"\n🎬 Video Shorts Extractor\n   Finding {args.clips} clips\n")

    client = get_client()

    clips = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You identify viral short-form video moments from long-form content."},
            {"role": "user", "content": f"""Find {args.clips} best moments for short-form video:

TRANSCRIPT:
{transcript[:8000]}

MAX CLIP LENGTH: {args.max_length} seconds

FOR EACH CLIP IDENTIFY:

## Clip {'{n}'}: [Hook Title]

**Timestamp Range:** [start] - [end] (estimate based on position in transcript)

**The Moment:**
[Exact quote or description of the moment]

**Why It Works:**
- Emotional hook
- Standalone value
- Controversy/curiosity factor

**Hook for Short:**
[Suggested opening text/voiceover for the clip]

**Suggested Text Overlay:**
[Key phrase to display]

**Platform Fit:**
- TikTok: [why/why not]
- Reels: [why/why not]
- Shorts: [why/why not]

---

PRIORITIZE:
1. Strong emotional moments
2. Contrarian statements
3. "Aha" insights
4. Funny/relatable moments
5. Quotable lines

Each clip should work as standalone content."""}
        ],
        temperature=0.7,
        max_tokens=2500
    ).choices[0].message.content

    output = f"""# Short-Form Video Clips

**Source:** {args.transcript}
**Clips Identified:** {args.clips}
**Max Length:** {args.max_length}s
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{clips}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Clips saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
