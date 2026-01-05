#!/usr/bin/env python3
"""
Objection Handler - Generate responses to sales objections.

Usage:
    python3 execution/handle_objections.py \
        --objection "It's too expensive" \
        --product "Marketing automation SaaS" \
        --price "$997/month" \
        --output .tmp/objection_response.md
"""

import argparse, os, sys
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
    parser = argparse.ArgumentParser(description="Handle sales objections")
    parser.add_argument("--objection", "-o", required=True, help="The objection to handle")
    parser.add_argument("--product", "-p", required=True, help="Product/service being sold")
    parser.add_argument("--price", default="", help="Price point")
    parser.add_argument("--context", "-c", default="", help="Additional context")
    parser.add_argument("--output", default=".tmp/objection_response.md")
    args = parser.parse_args()

    print(f"\n🎯 Objection Handler\n   Objection: {args.objection}\n")
    client = get_client()

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are an expert sales coach who helps handle objections with empathy and skill."},
            {"role": "user", "content": f"""Help me handle this sales objection:

OBJECTION: "{args.objection}"
PRODUCT: {args.product}
PRICE: {args.price or "Not specified"}
CONTEXT: {args.context or "None"}

PROVIDE:

## Understanding the Objection
- What they're really saying
- Underlying concern
- Type of objection (price, timing, trust, need, authority)

## Response Framework
Use the LAER model:
- **Listen**: Acknowledge statement
- **Acknowledge**: Show understanding  
- **Explore**: Ask clarifying questions
- **Respond**: Address the concern

## Sample Responses (3 variations)

### Response 1: Empathetic + Reframe
[Full response script]

### Response 2: Question-Based
[Response using questions to uncover real objection]

### Response 3: Story/Social Proof
[Response using client success story]

## Follow-up Questions to Ask
- Question 1
- Question 2
- Question 3

## If They Still Object
- Fallback response
- When to walk away

Make responses conversational, not pushy."""}
        ],
        temperature=0.7,
        max_tokens=2000
    ).choices[0].message.content

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(f"# Objection Handler\n\n**Objection:** {args.objection}\n\n---\n\n{response}", encoding="utf-8")
    print(f"✅ Response saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
