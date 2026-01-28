#!/usr/bin/env python3
"""
Ticket Triage - Auto-classify and prioritize support tickets.

Usage:
    python3 execution/triage_tickets.py \
        --ticket "My payment won't go through" \
        --output .tmp/triage.json
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
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o-mini"

def triage_ticket(client, subject, body, customer_tier="standard"):
    """Triage a support ticket."""
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You triage support tickets for a SaaS company. Return JSON only."},
            {"role": "user", "content": f"""Triage this support ticket:

SUBJECT: {subject}
BODY: {body}
CUSTOMER TIER: {customer_tier}

RETURN JSON:
{{
  "category": "billing|technical|feature_request|account|bug|general|urgent",
  "priority": "critical|high|medium|low",
  "sentiment": "angry|frustrated|neutral|positive",
  "complexity": "simple|moderate|complex",
  "estimated_resolution": "minutes|hours|days",
  "suggested_assignee": "billing_team|support_l1|support_l2|engineering|account_manager",
  "suggested_tags": ["tag1", "tag2"],
  "auto_response_possible": true|false,
  "suggested_response": "Brief response to start with",
  "escalation_needed": true|false,
  "key_issues": ["Issue 1", "Issue 2"]
}}

Category definitions:
- billing: Payment, subscription, invoice issues
- technical: How-to, setup, integration
- feature_request: Wants new functionality
- account: Login, access, permissions
- bug: Something broken
- general: Other inquiries
- urgent: Outage, security, critical"""}
        ],
        temperature=0.3,
        max_tokens=500
    ).choices[0].message.content

    try:
        if "```" in response:
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        return json.loads(response)
    except:
        return {"category": "general", "priority": "medium", "error": "Parse failed"}

def main():
    parser = argparse.ArgumentParser(description="Triage support tickets")
    parser.add_argument("--ticket", "-t", help="Ticket text")
    parser.add_argument("--subject", "-s", default="", help="Ticket subject")
    parser.add_argument("--file", "-f", help="File with ticket")
    parser.add_argument("--batch", "-b", help="JSON file with multiple tickets")
    parser.add_argument("--tier", default="standard", help="Customer tier")
    parser.add_argument("--output", "-o", default=".tmp/triage.json")
    args = parser.parse_args()

    client = get_client()
    
    if args.batch:
        with open(args.batch) as f:
            tickets = json.load(f)
        
        results = []
        for i, t in enumerate(tickets, 1):
            print(f"[{i}/{len(tickets)}] Triaging...", end=" ")
            result = triage_ticket(client, t.get("subject", ""), t.get("body", t.get("text", "")), args.tier)
            result["original"] = t
            results.append(result)
            print(f"→ {result.get('category')}/{result.get('priority')}")
        
        output = {"triaged_at": datetime.now().isoformat(), "results": results}
    else:
        if args.file:
            body = Path(args.file).read_text()
        else:
            body = args.ticket or ""
        
        print(f"\n🎫 Ticket Triage\n")
        result = triage_ticket(client, args.subject, body, args.tier)
        output = {"triaged_at": datetime.now().isoformat(), **result}
        
        print(f"Category: {result.get('category', 'unknown').upper()}")
        print(f"Priority: {result.get('priority', 'unknown').upper()}")
        print(f"Assign to: {result.get('suggested_assignee', 'N/A')}")
        print(f"Auto-response: {'Yes' if result.get('auto_response_possible') else 'No'}")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
