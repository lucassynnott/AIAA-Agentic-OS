#!/usr/bin/env python3
"""
Ticket Auto-Responder - Generate responses for support tickets.

Usage:
    python3 execution/generate_ticket_response.py \
        --ticket "I can't log into my account" \
        --category "account" \
        --output .tmp/ticket_response.md
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
    parser = argparse.ArgumentParser(description="Generate ticket responses")
    parser.add_argument("--ticket", "-t", required=True, help="Ticket content")
    parser.add_argument("--category", "-c", default="general", 
        choices=["billing", "technical", "account", "feature", "bug", "general"])
    parser.add_argument("--customer_name", "-n", default="")
    parser.add_argument("--tone", default="friendly", choices=["friendly", "formal", "empathetic"])
    parser.add_argument("--output", "-o", default=".tmp/ticket_response.md")
    args = parser.parse_args()

    print(f"\n🎫 Ticket Response Generator\n   Category: {args.category}\n")
    client = get_client()

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You are a helpful support agent. Tone: {args.tone}. Be concise and solution-focused."},
            {"role": "user", "content": f"""Generate a support response:

TICKET: {args.ticket}
CATEGORY: {args.category}
CUSTOMER NAME: {args.customer_name or "Customer"}

PROVIDE:

## Initial Response

[Complete response including:
- Acknowledgment of issue
- Solution steps OR questions to clarify
- Timeframe expectations
- Offer additional help]

## If Issue Not Resolved - Follow-up

[Escalation path or alternative solutions]

## Internal Notes

- Issue summary
- Category tags
- Priority assessment
- Knowledge base article to link (if applicable)

Keep response under 150 words. Be helpful, not robotic."""}
        ],
        temperature=0.6,
        max_tokens=1000
    ).choices[0].message.content

    output = f"""# Support Ticket Response

**Category:** {args.category}
**Tone:** {args.tone}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

**Original Ticket:**
{args.ticket}

---

{response}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Response saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
