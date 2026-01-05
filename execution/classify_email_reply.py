#!/usr/bin/env python3
"""
Email Reply Classifier - Classify email replies (interested, not interested, OOO, etc).

Usage:
    python3 execution/classify_email_reply.py \
        --email "Thanks for reaching out, I'd love to learn more..." \
        --output .tmp/classification.json
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

def classify_email(client, email_text):
    """Classify an email reply."""
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You classify email replies for sales teams. Return JSON only."},
            {"role": "user", "content": f"""Classify this email reply:

EMAIL:
{email_text}

RETURN JSON:
{{
  "classification": "interested|soft_interested|not_interested|unsubscribe|ooo|bounce|referral|question|other",
  "confidence": 0-100,
  "sentiment": "positive|neutral|negative",
  "priority": "high|medium|low",
  "suggested_action": "What to do next",
  "key_points": ["Point 1", "Point 2"],
  "reply_needed": true|false,
  "urgency": "immediate|soon|can_wait|none"
}}

Classifications:
- interested: Wants to learn more, book a call
- soft_interested: Positive but non-committal
- not_interested: Clear decline
- unsubscribe: Wants to be removed
- ooo: Out of office auto-reply
- bounce: Email bounced/delivery failure
- referral: Forwarded to someone else
- question: Has questions before deciding
- other: Doesn't fit categories"""}
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
        return {"classification": "other", "confidence": 0, "error": "Parse failed"}

def main():
    parser = argparse.ArgumentParser(description="Classify email replies")
    parser.add_argument("--email", "-e", help="Email text to classify")
    parser.add_argument("--file", "-f", help="File containing email text")
    parser.add_argument("--batch", "-b", help="JSON file with multiple emails")
    parser.add_argument("--output", "-o", default=".tmp/classification.json")
    args = parser.parse_args()

    if not args.email and not args.file and not args.batch:
        parser.error("Provide --email, --file, or --batch")

    client = get_client()
    
    if args.batch:
        # Batch processing
        with open(args.batch) as f:
            emails = json.load(f)
        
        results = []
        for i, item in enumerate(emails, 1):
            text = item.get("body", item.get("email", item.get("text", "")))
            print(f"[{i}/{len(emails)}] Classifying...", end=" ")
            result = classify_email(client, text)
            result["original"] = item
            results.append(result)
            print(f"→ {result.get('classification', 'unknown')}")
        
        output = {"classified_at": datetime.now().isoformat(), "results": results}
    else:
        # Single email
        if args.file:
            email_text = Path(args.file).read_text()
        else:
            email_text = args.email
        
        print(f"\n📧 Email Classifier\n")
        result = classify_email(client, email_text)
        output = {"classified_at": datetime.now().isoformat(), **result}
        
        print(f"Classification: {result.get('classification', 'unknown').upper()}")
        print(f"Confidence: {result.get('confidence', 0)}%")
        print(f"Priority: {result.get('priority', 'unknown')}")
        print(f"Action: {result.get('suggested_action', 'N/A')}")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
