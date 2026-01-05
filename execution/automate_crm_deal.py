#!/usr/bin/env python3
"""
CRM Deal Automator - Generate deal stage updates and next actions.

Usage:
    python3 execution/automate_crm_deal.py \
        --deal "Acme Corp - Enterprise Plan" \
        --current_stage "demo_completed" \
        --notes "Great demo, asked about pricing" \
        --output .tmp/deal_update.md
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

STAGES = ["lead", "qualified", "demo_scheduled", "demo_completed", "proposal_sent", "negotiation", "closed_won", "closed_lost"]

def main():
    parser = argparse.ArgumentParser(description="Automate CRM deal updates")
    parser.add_argument("--deal", "-d", required=True, help="Deal name")
    parser.add_argument("--current_stage", "-s", required=True, choices=STAGES)
    parser.add_argument("--notes", "-n", default="", help="Recent notes/activity")
    parser.add_argument("--value", "-v", type=float, default=0, help="Deal value")
    parser.add_argument("--output", "-o", default=".tmp/deal_update.md")
    args = parser.parse_args()

    print(f"\n🔄 CRM Deal Automator\n   Deal: {args.deal}\n   Stage: {args.current_stage}\n")
    
    # Determine next stage
    current_idx = STAGES.index(args.current_stage)
    next_stage = STAGES[current_idx + 1] if current_idx < len(STAGES) - 2 else args.current_stage

    client = get_client()

    automation = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You help sales reps manage CRM deals effectively."},
            {"role": "user", "content": f"""Recommend next actions for this deal:

DEAL: {args.deal}
CURRENT STAGE: {args.current_stage}
NEXT STAGE: {next_stage}
DEAL VALUE: ${args.value:,.2f if args.value else "TBD"}
RECENT NOTES: {args.notes or "No recent notes"}

PROVIDE:

## Deal Assessment
- Current status
- Momentum (hot/warm/cold)
- Win probability estimate

## Recommended Next Actions
1. Immediate action (today)
2. This week
3. Follow-up schedule

## Tasks to Create
- [ ] Task 1 (due date)
- [ ] Task 2 (due date)
- [ ] Task 3 (due date)

## Email/Call Script
[Brief script for next touchpoint]

## Stage Advancement Criteria
What needs to happen to move to {next_stage}

## Risk Factors
- Potential blockers
- Competitive threats

## CRM Update Notes
[Formatted notes to paste into CRM]"""}
        ],
        temperature=0.6,
        max_tokens=1500
    ).choices[0].message.content

    output = f"""# CRM Deal Update: {args.deal}

**Current Stage:** {args.current_stage}
**Next Stage:** {next_stage}
**Value:** ${args.value:,.2f if args.value else "TBD"}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{automation}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Update saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
