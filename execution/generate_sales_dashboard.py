#!/usr/bin/env python3
"""
Sales Pipeline Dashboard - Generate sales pipeline summary and insights.

Usage:
    python3 execution/generate_sales_dashboard.py \
        --deals deals.json \
        --output .tmp/sales_dashboard.md
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
    parser = argparse.ArgumentParser(description="Generate sales dashboard")
    parser.add_argument("--deals", "-d", required=True, help="Deals JSON")
    parser.add_argument("--period", "-p", default="Current Month")
    parser.add_argument("--output", "-o", default=".tmp/sales_dashboard.md")
    args = parser.parse_args()

    # Load deals
    if Path(args.deals).exists():
        with open(args.deals) as f:
            deals = json.load(f)
    else:
        deals = json.loads(args.deals)

    if isinstance(deals, dict):
        deals = deals.get("deals", [deals])

    print(f"\n📊 Sales Dashboard\n   Deals: {len(deals)}\n   Period: {args.period}\n")

    # Calculate metrics
    stages = {}
    total_value = 0
    for deal in deals:
        stage = deal.get("stage", "Unknown")
        value = deal.get("value", deal.get("amount", 0))
        stages[stage] = stages.get(stage, {"count": 0, "value": 0})
        stages[stage]["count"] += 1
        stages[stage]["value"] += value
        total_value += value

    client = get_client()

    analysis = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You analyze sales pipelines and provide actionable insights."},
            {"role": "user", "content": f"""Analyze this sales pipeline:

PERIOD: {args.period}
TOTAL DEALS: {len(deals)}
TOTAL VALUE: ${total_value:,.2f}

BY STAGE:
{json.dumps(stages, indent=2)}

DEAL DETAILS:
{json.dumps(deals[:10], indent=2)}

PROVIDE:

## Pipeline Health Assessment
- Overall health (healthy/needs attention/critical)
- Key observations

## Stage Analysis
- Bottlenecks
- Conversion concerns
- Opportunities

## Top Priority Deals
- Deals to focus on this week
- Why each matters

## Risks
- Deals at risk
- Stalled deals

## Recommendations
1. Immediate actions
2. This week priorities
3. Process improvements

## Forecast
- Expected closes this period
- Confidence level"""}
        ],
        temperature=0.5,
        max_tokens=2000
    ).choices[0].message.content

    # Build output
    output = f"""# Sales Pipeline Dashboard

**Period:** {args.period}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Summary Metrics

| Metric | Value |
|--------|-------|
| Total Deals | {len(deals)} |
| Total Pipeline Value | ${total_value:,.2f} |
| Average Deal Size | ${total_value/len(deals):,.2f if deals else 0} |

---

## By Stage

| Stage | Deals | Value |
|-------|-------|-------|
"""
    for stage, data in stages.items():
        output += f"| {stage} | {data['count']} | ${data['value']:,.2f} |\n"

    output += f"""

---

{analysis}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Dashboard saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
