#!/usr/bin/env python3
"""
Video Transcription & Summary - Transcribe video/audio and generate summary.

Usage:
    python3 execution/transcribe_video.py \
        --file video.mp4 \
        --output .tmp/transcript.md
"""

import argparse, os, sys
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    parser = argparse.ArgumentParser(description="Transcribe video/audio")
    parser.add_argument("--file", "-f", required=True, help="Audio/video file path")
    parser.add_argument("--summarize", "-s", action="store_true", help="Also generate summary")
    parser.add_argument("--output", "-o", default=".tmp/transcript.md")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY required for Whisper transcription")
        sys.exit(1)

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    print(f"\n🎤 Video Transcription\n   File: {file_path.name}\n")
    client = get_client()

    # Transcribe with Whisper
    print("   Transcribing...")
    with open(file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text"
        )

    output = f"""# Transcript: {file_path.name}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Full Transcript

{transcript}
"""

    # Generate summary if requested
    if args.summarize:
        print("   Generating summary...")
        summary = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize this transcript with key points and action items."},
                {"role": "user", "content": f"""Summarize this transcript:

{transcript[:8000]}

Provide:
1. Executive Summary (2-3 sentences)
2. Key Points (bullet list)
3. Action Items (if any)
4. Notable Quotes"""}
            ],
            temperature=0.5,
            max_tokens=1000
        ).choices[0].message.content

        output += f"""

---

## Summary

{summary}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    
    print(f"\n✅ Transcript saved to: {args.output}")
    print(f"   Words: ~{len(transcript.split())}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
