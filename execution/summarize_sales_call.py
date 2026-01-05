#!/usr/bin/env python3
"""
Sales Call Summarizer - Summarize sales calls and extract action items.

Usage:
    python3 execution/summarize_sales_call.py \
        --transcript call_transcript.txt \
        --output .tmp/call_summary.md
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
    parser = argparse.ArgumentParser(description="Summarize sales calls")
    parser.add_argument("--transcript", "-t", required=True, help="Transcript file or text")
    parser.add_argument("--prospect", "-p", default="", help="Prospect name")
    parser.add_argument("--company", "-c", default="", help="Company name")
    parser.add_argument("--output", "-o", default=".tmp/call_summary.md")
    args = parser.parse_args()

    # Load transcript
    if Path(args.transcript).exists():
        transcript = Path(args.transcript).read_text()
    else:
        transcript = args.transcript

    print(f"\n📞 Sales Call Summarizer\n")
    client = get_client()

    summary = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are an expert at analyzing sales calls and extracting key insights."},
            {"role": "user", "content": f"""Analyze this sales call transcript:

PROSPECT: {args.prospect or "Unknown"}
COMPANY: {args.company or "Unknown"}

TRANSCRIPT:
{transcript[:8000]}

PROVIDE:

## Call Summary
- 2-3 sentence overview
- Call duration estimate
- Call type (discovery, demo, closing, etc.)

## Key Points Discussed
- Main topics covered (bullet points)

## Prospect Pain Points
- Challenges they mentioned
- Problems they want solved

## Objections Raised
- Any concerns or pushback
- How they were addressed

## Interest Level
- Score 1-10 with reasoning
- Buying signals observed

## Next Steps
- What was agreed upon
- Follow-up actions needed

## Action Items
- [ ] Item 1 (owner, deadline)
- [ ] Item 2 (owner, deadline)

## Recommended Follow-up
- Suggested next touchpoint
- Key points to address"""}
        ],
        temperature=0.5,
        max_tokens=2000
    ).choices[0].message.content

    output = f"""# Sales Call Summary

**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Prospect:** {args.prospect or "Unknown"}
**Company:** {args.company or "Unknown"}

---

{summary}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Summary saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
