#!/usr/bin/env python3
"""
Content Calendar Generator - Create monthly content calendars.

Usage:
    python3 execution/generate_content_calendar.py \
        --niche "B2B SaaS Marketing" \
        --platforms "linkedin,twitter,blog" \
        --weeks 4 \
        --output .tmp/content_calendar.md
"""

import argparse, os, sys
from datetime import datetime, timedelta
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
    parser = argparse.ArgumentParser(description="Generate content calendars")
    parser.add_argument("--niche", "-n", required=True, help="Industry/niche")
    parser.add_argument("--platforms", "-p", default="linkedin,twitter", help="Comma-separated platforms")
    parser.add_argument("--weeks", "-w", type=int, default=4, help="Number of weeks")
    parser.add_argument("--pillars", default="", help="Content pillars (comma-separated)")
    parser.add_argument("--output", "-o", default=".tmp/content_calendar.md")
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",")]
    start_date = datetime.now()

    print(f"\n📅 Content Calendar Generator\n   Niche: {args.niche}\n   Platforms: {platforms}\n")
    client = get_client()

    calendar = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are a content strategist who creates engaging content calendars."},
            {"role": "user", "content": f"""Create a {args.weeks}-week content calendar:

NICHE: {args.niche}
PLATFORMS: {', '.join(platforms)}
START DATE: {start_date.strftime("%Y-%m-%d")}
CONTENT PILLARS: {args.pillars or "Educational, Behind-the-scenes, Case studies, Tips, Engagement"}

FOR EACH WEEK, PROVIDE:

## Week X (Date Range)

### Content Themes
- Theme for the week

### Posts by Platform

{'### LinkedIn' if 'linkedin' in platforms else ''}
{'- Mon: [Post type] - Topic' if 'linkedin' in platforms else ''}
{'- Wed: [Post type] - Topic' if 'linkedin' in platforms else ''}
{'- Fri: [Post type] - Topic' if 'linkedin' in platforms else ''}

{'### Twitter/X' if 'twitter' in platforms else ''}
{'- Daily tweet ideas (5)' if 'twitter' in platforms else ''}
{'- Thread topic' if 'twitter' in platforms else ''}

{'### Blog' if 'blog' in platforms else ''}
{'- Article topic and angle' if 'blog' in platforms else ''}

{'### Newsletter' if 'newsletter' in platforms else ''}
{'- Topic and key sections' if 'newsletter' in platforms else ''}

### Key Dates/Events to Leverage
- Relevant dates this week

---

INCLUDE FOR EACH POST:
- Content type (story, tips, question, etc.)
- Topic/hook
- Best posting time
- Engagement prompt/CTA

Make content specific and actionable, not generic."""}
        ],
        temperature=0.8,
        max_tokens=4000
    ).choices[0].message.content

    output = f"""# Content Calendar

**Niche:** {args.niche}
**Platforms:** {', '.join(platforms)}
**Period:** {start_date.strftime("%Y-%m-%d")} to {(start_date + timedelta(weeks=args.weeks)).strftime("%Y-%m-%d")}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{calendar}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Calendar saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
