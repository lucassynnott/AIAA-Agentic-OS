#!/usr/bin/env python3
"""
Client QBR Generator - Generate quarterly business review presentations.

Usage:
    python3 execution/generate_qbr.py \
        --client "Acme Corp" \
        --metrics "Revenue: $50k, Leads: 500, Conversion: 5%" \
        --wins "Launched 3 campaigns, 2x pipeline" \
        --challenges "Deliverability issues" \
        --next_quarter "Scale to 1000 leads/month" \
        --output .tmp/qbr.md
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

def call_llm(client, system, user, temp=0.6):
    resp = client.chat.completions.create(model=get_model(), messages=[
        {"role": "system", "content": system}, {"role": "user", "content": user}
    ], temperature=temp, max_tokens=4000)
    return resp.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Generate QBR presentations")
    parser.add_argument("--client", "-c", required=True)
    parser.add_argument("--metrics", "-m", required=True, help="Key metrics achieved")
    parser.add_argument("--wins", "-w", default="", help="Key wins this quarter")
    parser.add_argument("--challenges", "-h", default="", help="Challenges faced")
    parser.add_argument("--next_quarter", "-n", default="", help="Next quarter goals")
    parser.add_argument("--output", "-o", default=".tmp/qbr.md")
    args = parser.parse_args()

    print(f"\n📊 QBR Generator\n   Client: {args.client}\n")
    client = get_client()

    qbr = call_llm(client,
        "You create professional quarterly business review presentations.",
        f"""Create a QBR presentation outline for:

CLIENT: {args.client}
QUARTER: Q{((datetime.now().month-1)//3)+1} {datetime.now().year}
KEY METRICS: {args.metrics}
WINS: {args.wins or "Not specified"}
CHALLENGES: {args.challenges or "None noted"}
NEXT QUARTER GOALS: {args.next_quarter or "To be discussed"}

CREATE QBR WITH SLIDES:

## SLIDE 1: Executive Summary
- Overall performance summary
- Key metric highlights

## SLIDE 2: Goals vs Actuals
- What we set out to achieve
- What we actually achieved
- Variance analysis

## SLIDE 3: Key Wins
- Top 3-5 achievements
- Impact of each win

## SLIDE 4: Metrics Deep Dive
- Detailed breakdown of each metric
- Trends and insights

## SLIDE 5: Challenges & Learnings
- What didn't work
- Lessons learned
- How we'll improve

## SLIDE 6: Next Quarter Roadmap
- Goals for next quarter
- Key initiatives
- Success metrics

## SLIDE 7: Discussion & Questions
- Open items
- Decisions needed

Include talking points for each slide.""", 0.6)

    output = f"""# Quarterly Business Review: {args.client}

**Quarter:** Q{((datetime.now().month-1)//3)+1} {datetime.now().year}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{qbr}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ QBR saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
