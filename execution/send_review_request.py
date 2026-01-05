#!/usr/bin/env python3
"""
Review Collection / Testimonial Request Generator - Generate review request emails.

Usage:
    python3 execution/send_review_request.py \
        --client "John Smith" \
        --company "Acme Corp" \
        --product "Marketing Services" \
        --output .tmp/review_request.md
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
    parser = argparse.ArgumentParser(description="Generate review request emails")
    parser.add_argument("--client", "-c", required=True, help="Client name")
    parser.add_argument("--company", default="", help="Client company")
    parser.add_argument("--product", "-p", required=True, help="Product/service they used")
    parser.add_argument("--platform", default="google", help="Review platform (google, g2, capterra, etc)")
    parser.add_argument("--results", "-r", default="", help="Specific results achieved")
    parser.add_argument("--output", "-o", default=".tmp/review_request.md")
    args = parser.parse_args()

    print(f"\n⭐ Review Request Generator\n   Client: {args.client}\n")
    client = get_client()

    request = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You write personalized review request emails that get responses."},
            {"role": "user", "content": f"""Create a review request email:

CLIENT: {args.client}
COMPANY: {args.company or "N/A"}
PRODUCT/SERVICE: {args.product}
REVIEW PLATFORM: {args.platform}
RESULTS ACHIEVED: {args.results or "General positive experience"}

CREATE:

## Email Version 1: Direct Ask
- Subject lines (3)
- Email body (short, personal)
- Clear CTA with review link placeholder

## Email Version 2: Soft Ask with Testimonial
- Subject lines (3)
- Email asking for quick testimonial quote
- Option to leave full review

## Follow-up Email (If No Response)
- Subject line
- Short reminder

## SMS Version (Optional)
- Brief text message version

RULES:
- Keep emails under 100 words
- Be genuine, not pushy
- Reference specific results if provided
- Make it easy to say yes"""}
        ],
        temperature=0.7,
        max_tokens=1500
    ).choices[0].message.content

    output = f"""# Review Request: {args.client}

**Product:** {args.product}
**Platform:** {args.platform}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{request}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Request saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
