#!/usr/bin/env python3
"""
FAQ Chatbot Response Generator - Generate responses for common questions.

Usage:
    python3 execution/generate_faq_responses.py \
        --questions "How do I reset my password?,What's your refund policy?" \
        --business "SaaS Company" \
        --output .tmp/faq_responses.json
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
    parser = argparse.ArgumentParser(description="Generate FAQ responses")
    parser.add_argument("--questions", "-q", required=True, help="Comma-separated questions or file path")
    parser.add_argument("--business", "-b", required=True, help="Business name/description")
    parser.add_argument("--context", "-c", default="", help="Additional context")
    parser.add_argument("--tone", "-t", default="friendly", choices=["friendly", "professional", "casual"])
    parser.add_argument("--output", "-o", default=".tmp/faq_responses.json")
    args = parser.parse_args()

    # Parse questions
    if Path(args.questions).exists():
        questions = Path(args.questions).read_text().strip().split("\n")
    else:
        questions = [q.strip() for q in args.questions.split(",")]

    print(f"\n❓ FAQ Response Generator\n   Questions: {len(questions)}\n")
    client = get_client()

    faqs = []
    for i, q in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {q[:50]}...")
        
        response = client.chat.completions.create(
            model=get_model(),
            messages=[
                {"role": "system", "content": f"You are a helpful customer support agent for {args.business}. Tone: {args.tone}. Be concise but thorough."},
                {"role": "user", "content": f"""Generate an FAQ response:

QUESTION: {q}
BUSINESS: {args.business}
CONTEXT: {args.context or "General customer support"}

PROVIDE:
1. Direct answer (2-3 sentences)
2. Additional helpful info if relevant
3. Next step or CTA

Keep response under 150 words. Be helpful and {args.tone}."""}
            ],
            temperature=0.6,
            max_tokens=300
        ).choices[0].message.content

        faqs.append({
            "question": q,
            "answer": response,
            "category": "general",
            "created_at": datetime.now().isoformat()
        })

    output = {
        "generated_at": datetime.now().isoformat(),
        "business": args.business,
        "tone": args.tone,
        "faqs": faqs
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Generated {len(faqs)} FAQ responses")
    print(f"   📄 Output: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
