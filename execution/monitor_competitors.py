#!/usr/bin/env python3
"""
Competitor Monitor - Analyze and monitor competitor activity.

Usage:
    python3 execution/monitor_competitors.py \
        --competitors "Competitor1.com,Competitor2.com" \
        --focus "pricing,features,content" \
        --output .tmp/competitor_report.md
"""

import argparse, os, sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
    import requests
except ImportError:
    print("Error: Required packages not installed. Run: pip install openai requests")
    sys.exit(1)

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
    if not api_key:
        return ""
    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "llama-3.1-sonar-small-128k-online", "messages": [{"role": "user", "content": query}]},
            timeout=30
        )
        if resp.ok:
            return resp.json()["choices"][0]["message"]["content"]
    except:
        pass
    return ""

def main():
    parser = argparse.ArgumentParser(description="Monitor competitors")
    parser.add_argument("--competitors", "-c", required=True, help="Comma-separated competitor domains")
    parser.add_argument("--focus", "-f", default="pricing,features,content", help="Focus areas")
    parser.add_argument("--your_company", "-y", default="", help="Your company for comparison")
    parser.add_argument("--output", "-o", default=".tmp/competitor_report.md")
    args = parser.parse_args()

    competitors = [c.strip() for c in args.competitors.split(",")]
    focus_areas = [f.strip() for f in args.focus.split(",")]

    print(f"\n🔍 Competitor Monitor\n   Tracking: {competitors}\n")
    client = get_client()

    # Research each competitor
    research = ""
    for comp in competitors:
        print(f"   Researching {comp}...")
        data = search_perplexity(f"Latest news and updates about {comp} - pricing, features, products, marketing")
        research += f"\n\n## {comp}\n{data or 'No real-time data available'}"

    # Generate analysis
    analysis = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are a competitive intelligence analyst."},
            {"role": "user", "content": f"""Analyze these competitors:

COMPETITORS: {', '.join(competitors)}
FOCUS AREAS: {', '.join(focus_areas)}
YOUR COMPANY: {args.your_company or "Not specified"}

RESEARCH DATA:
{research[:4000]}

PROVIDE:

## Executive Summary
- Key findings (3-5 bullets)

## Competitor Profiles

### [Competitor 1]
- Overview
- Pricing model
- Key features
- Recent moves
- Strengths/Weaknesses

(repeat for each)

## Competitive Landscape
- Market positioning map
- Feature comparison
- Pricing comparison

## Opportunities
- Gaps in competitor offerings
- Underserved segments
- Differentiation opportunities

## Threats
- Competitive risks
- Market changes

## Recommendations
1. Immediate actions
2. Strategic considerations
3. Monitoring priorities

## Track These
- Key metrics to watch
- Signals to monitor"""}
        ],
        temperature=0.5,
        max_tokens=3500
    ).choices[0].message.content

    output = f"""# Competitor Intelligence Report

**Competitors:** {', '.join(competitors)}
**Focus:** {', '.join(focus_areas)}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{analysis}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"\n✅ Report saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
