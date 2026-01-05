#!/usr/bin/env python3
"""
Monthly Report Generator - Generate client monthly performance reports.

Usage:
    python3 execution/generate_monthly_report.py \
        --client "Acme Corp" \
        --metrics '{"leads": 500, "meetings": 50, "closed": 10, "revenue": 50000}' \
        --output .tmp/monthly_report.md
"""

import argparse, json, os, sys
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
    parser = argparse.ArgumentParser(description="Generate monthly reports")
    parser.add_argument("--client", "-c", required=True)
    parser.add_argument("--metrics", "-m", required=True, help="Metrics JSON")
    parser.add_argument("--highlights", "-h", default="", help="Key highlights")
    parser.add_argument("--challenges", default="", help="Challenges faced")
    parser.add_argument("--month", default="", help="Report month (default: last month)")
    parser.add_argument("--output", "-o", default=".tmp/monthly_report.md")
    args = parser.parse_args()

    try:
        metrics = json.loads(args.metrics)
    except:
        print("Error: Invalid JSON")
        return 1

    month = args.month or datetime.now().strftime("%B %Y")
    print(f"\n📊 Monthly Report Generator\n   Client: {args.client}\n   Month: {month}\n")

    client = get_client()

    report = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You create professional client monthly reports with actionable insights."},
            {"role": "user", "content": f"""Create a monthly report:

CLIENT: {args.client}
MONTH: {month}

METRICS:
{json.dumps(metrics, indent=2)}

HIGHLIGHTS: {args.highlights or "Not specified"}
CHALLENGES: {args.challenges or "None noted"}

CREATE REPORT WITH:

## Executive Summary
- Overall performance
- Key wins
- Areas of focus

## Performance Metrics
- Table of all metrics
- Comparison to goals
- Month-over-month trends

## Activities & Deliverables
- What was completed
- Key milestones

## Wins & Highlights
- Top achievements
- Success stories

## Challenges & Solutions
- Issues encountered
- How they were addressed

## Next Month Focus
- Priorities
- Goals
- Planned activities

## Recommendations
- Strategic suggestions
- Optimization opportunities

Keep it professional, data-driven, and actionable."""}
        ],
        temperature=0.6,
        max_tokens=2500
    ).choices[0].message.content

    output = f"""# Monthly Report: {args.client}

**Period:** {month}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{report}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Report saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
