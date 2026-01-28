#!/usr/bin/env python3
"""
Win/Loss Analysis - Analyze closed deals to understand patterns.

Usage:
    python3 execution/analyze_win_loss.py \
        --deals deals.json \
        --output .tmp/win_loss_analysis.md
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
    parser = argparse.ArgumentParser(description="Analyze win/loss patterns")
    parser.add_argument("--deals", "-d", required=True, help="Deals JSON file or summary text")
    parser.add_argument("--period", "-p", default="Last Quarter", help="Analysis period")
    parser.add_argument("--output", "-o", default=".tmp/win_loss_analysis.md")
    args = parser.parse_args()

    # Load deals data
    if Path(args.deals).exists():
        deals_data = Path(args.deals).read_text()
    else:
        deals_data = args.deals

    print(f"\n📊 Win/Loss Analyzer\n")
    client = get_client()

    analysis = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are a sales analytics expert who identifies patterns in closed deals."},
            {"role": "user", "content": f"""Analyze these deals for win/loss patterns:

PERIOD: {args.period}

DEALS DATA:
{deals_data[:6000]}

PROVIDE ANALYSIS:

## Executive Summary
- Win rate
- Key findings (3 bullets)

## Wins Analysis
- Total won deals
- Common characteristics of wins
- Winning patterns (industry, size, source, etc.)
- Average deal size won
- Average sales cycle (won)

## Losses Analysis
- Total lost deals
- Top reasons for losses
- Common characteristics of losses
- Competitor losses
- Lost deal patterns

## Key Insights
1. What's working well
2. Where we're losing deals
3. Competitor positioning

## Recommendations
1. To improve win rate
2. To reduce lost deals
3. Process improvements

## Action Items
- Immediate (this week)
- Short-term (this month)
- Long-term (this quarter)"""}
        ],
        temperature=0.5,
        max_tokens=3000
    ).choices[0].message.content

    output = f"""# Win/Loss Analysis

**Period:** {args.period}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{analysis}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Analysis saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
