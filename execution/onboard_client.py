#!/usr/bin/env python3
"""
Client Onboarding Generator - Generate onboarding materials for new clients.

Usage:
    python3 execution/onboard_client.py \
        --client "Acme Corp" \
        --service "Marketing Automation" \
        --start_date "2024-01-15" \
        --output .tmp/onboarding/
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
    parser = argparse.ArgumentParser(description="Generate client onboarding")
    parser.add_argument("--client", "-c", required=True)
    parser.add_argument("--service", "-s", required=True, help="Service being delivered")
    parser.add_argument("--start_date", "-d", default="", help="Start date")
    parser.add_argument("--contact", default="", help="Primary contact name")
    parser.add_argument("--output", "-o", default=".tmp/onboarding/")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    start_date = args.start_date or datetime.now().strftime("%Y-%m-%d")

    print(f"\n🚀 Client Onboarding Generator\n   Client: {args.client}\n   Service: {args.service}\n")
    client = get_client()

    # Welcome email
    print("   Creating welcome email...")
    welcome = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You write warm, professional client welcome emails."},
            {"role": "user", "content": f"""Write a welcome email for:
CLIENT: {args.client}
SERVICE: {args.service}
START DATE: {start_date}
CONTACT: {args.contact or "the team"}

Include:
- Warm welcome
- What to expect in first week
- Key contacts
- Next steps
- How to reach support"""}
        ],
        temperature=0.7, max_tokens=1000
    ).choices[0].message.content
    (output_dir / "01_welcome_email.md").write_text(f"# Welcome Email\n\n{welcome}")

    # Onboarding checklist
    print("   Creating onboarding checklist...")
    checklist = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You create comprehensive onboarding checklists."},
            {"role": "user", "content": f"""Create an onboarding checklist for:
CLIENT: {args.client}
SERVICE: {args.service}

Include sections:
- Pre-kickoff (access, logins, docs)
- Week 1 (kickoff, discovery, setup)
- Week 2 (implementation begins)
- Week 3-4 (review, optimization)
- Ongoing (reporting, communication)

Format as checkboxes."""}
        ],
        temperature=0.6, max_tokens=1500
    ).choices[0].message.content
    (output_dir / "02_onboarding_checklist.md").write_text(f"# Onboarding Checklist\n\n{checklist}")

    # Kickoff agenda
    print("   Creating kickoff agenda...")
    agenda = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You create effective meeting agendas."},
            {"role": "user", "content": f"""Create a kickoff meeting agenda:
CLIENT: {args.client}
SERVICE: {args.service}
DURATION: 60 minutes

Include:
- Introductions
- Goals alignment
- Scope review
- Timeline
- Communication plan
- Q&A
- Next steps"""}
        ],
        temperature=0.6, max_tokens=1000
    ).choices[0].message.content
    (output_dir / "03_kickoff_agenda.md").write_text(f"# Kickoff Meeting Agenda\n\n{agenda}")

    print(f"\n✅ Onboarding package created!")
    print(f"   📁 Output: {output_dir}")
    print(f"   Files: welcome_email, onboarding_checklist, kickoff_agenda")
    return 0

if __name__ == "__main__":
    sys.exit(main())
