#!/usr/bin/env python3
"""
Booked Meeting Alert + Prospect Research - Generate research when meeting is booked.

Usage:
    python3 execution/alert_booked_meeting.py \
        --name "John Smith" \
        --company "Acme Corp" \
        --meeting_time "2024-01-15 2:00 PM" \
        --output .tmp/meeting_prep.md
"""

import argparse, os, sys
from datetime import datetime
from pathlib import Path
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"

def search_perplexity(query):
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key: return ""
    try:
        resp = requests.post("https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "llama-3.1-sonar-small-128k-online", "messages": [{"role": "user", "content": query}]},
            timeout=30)
        if resp.ok: return resp.json()["choices"][0]["message"]["content"]
    except: pass
    return ""

def main():
    parser = argparse.ArgumentParser(description="Research for booked meeting")
    parser.add_argument("--name", "-n", required=True)
    parser.add_argument("--company", "-c", required=True)
    parser.add_argument("--meeting_time", "-t", required=True)
    parser.add_argument("--meeting_type", default="discovery", help="Meeting type")
    parser.add_argument("--output", "-o", default=".tmp/meeting_prep.md")
    args = parser.parse_args()

    print(f"\n📅 Meeting Booked!\n   {args.name} @ {args.company}\n   Time: {args.meeting_time}\n")

    # Research
    print("   Researching prospect...")
    research = search_perplexity(f"Tell me about {args.company} - what they do, recent news, and any info on {args.name}")

    client = get_client()

    prep = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You prepare sales reps for meetings with actionable intelligence."},
            {"role": "user", "content": f"""Prepare for this meeting:

PROSPECT: {args.name}
COMPANY: {args.company}
MEETING TIME: {args.meeting_time}
MEETING TYPE: {args.meeting_type}

RESEARCH:
{research or "No real-time research available"}

CREATE PREP SHEET:

## Quick Facts
- Company overview
- Recent news
- Key info about prospect

## Pre-Call Checklist
- [ ] Review LinkedIn profile
- [ ] Check company website
- [ ] Prepare demo/materials
- [ ] Test meeting link

## Opening Script
[How to start the call]

## Discovery Questions
1. Question 1
2. Question 2
3. Question 3
4. Question 4
5. Question 5

## Talking Points
- Point 1 to mention
- Point 2 to mention

## Potential Objections
- Objection 1 + response
- Objection 2 + response

## Success Criteria
What makes this meeting successful?

## Post-Meeting
- Follow-up template
- Next steps to propose"""}
        ],
        temperature=0.6,
        max_tokens=2000
    ).choices[0].message.content

    output = f"""# 🎯 Meeting Prep: {args.name} @ {args.company}

**Meeting Time:** {args.meeting_time}
**Type:** {args.meeting_type}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

{prep}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Prep saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
