#!/usr/bin/env python3
"""
Campaign Report Generator - Generate email/ad campaign performance reports.

Usage:
    python3 execution/generate_campaign_report.py \
        --campaign "Q1 Cold Email" \
        --metrics '{"sent": 5000, "opens": 2500, "clicks": 250, "replies": 125, "meetings": 25}' \
        --output .tmp/campaign_report.md
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

def calculate_rates(metrics):
    """Calculate conversion rates."""
    sent = metrics.get("sent", 0)
    rates = {}
    if sent > 0:
        rates["open_rate"] = round(metrics.get("opens", 0) / sent * 100, 2)
        rates["click_rate"] = round(metrics.get("clicks", 0) / sent * 100, 2)
        rates["reply_rate"] = round(metrics.get("replies", 0) / sent * 100, 2)
        rates["meeting_rate"] = round(metrics.get("meetings", 0) / sent * 100, 2)
    if metrics.get("opens", 0) > 0:
        rates["click_to_open"] = round(metrics.get("clicks", 0) / metrics["opens"] * 100, 2)
    if metrics.get("replies", 0) > 0:
        rates["reply_to_meeting"] = round(metrics.get("meetings", 0) / metrics["replies"] * 100, 2)
    return rates

def main():
    parser = argparse.ArgumentParser(description="Generate campaign reports")
    parser.add_argument("--campaign", "-c", required=True, help="Campaign name")
    parser.add_argument("--metrics", "-m", required=True, help="Metrics JSON")
    parser.add_argument("--period", "-p", default="Last 30 days", help="Reporting period")
    parser.add_argument("--output", "-o", default=".tmp/campaign_report.md")
    args = parser.parse_args()

    try:
        metrics = json.loads(args.metrics)
    except:
        print("Error: Invalid JSON for metrics")
        return 1

    print(f"\n📈 Campaign Report Generator\n   Campaign: {args.campaign}\n")

    rates = calculate_rates(metrics)
    client = get_client()

    analysis = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You analyze email marketing campaigns and provide actionable insights."},
            {"role": "user", "content": f"""Analyze this campaign performance:

CAMPAIGN: {args.campaign}
PERIOD: {args.period}

METRICS:
- Sent: {metrics.get('sent', 0):,}
- Opens: {metrics.get('opens', 0):,} ({rates.get('open_rate', 0)}%)
- Clicks: {metrics.get('clicks', 0):,} ({rates.get('click_rate', 0)}%)
- Replies: {metrics.get('replies', 0):,} ({rates.get('reply_rate', 0)}%)
- Meetings: {metrics.get('meetings', 0):,} ({rates.get('meeting_rate', 0)}%)

INDUSTRY BENCHMARKS:
- Open rate: 20-30%
- Click rate: 2-5%
- Reply rate: 1-5%

PROVIDE:

## Performance Summary
- Overall assessment
- Key wins
- Areas for improvement

## Metric Analysis
- Open rate analysis vs benchmark
- Click rate analysis
- Reply rate analysis
- Conversion funnel

## Recommendations
1. To improve open rates
2. To improve reply rates
3. To improve conversions

## Next Steps
- Immediate actions
- Tests to run"""}
        ],
        temperature=0.6,
        max_tokens=1500
    ).choices[0].message.content

    output = f"""# Campaign Report: {args.campaign}

**Period:** {args.period}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

## Key Metrics

| Metric | Value | Rate |
|--------|-------|------|
| Sent | {metrics.get('sent', 0):,} | - |
| Opens | {metrics.get('opens', 0):,} | {rates.get('open_rate', 0)}% |
| Clicks | {metrics.get('clicks', 0):,} | {rates.get('click_rate', 0)}% |
| Replies | {metrics.get('replies', 0):,} | {rates.get('reply_rate', 0)}% |
| Meetings | {metrics.get('meetings', 0):,} | {rates.get('meeting_rate', 0)}% |

---

{analysis}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Report saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
