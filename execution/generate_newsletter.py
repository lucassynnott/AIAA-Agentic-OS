#!/usr/bin/env python3
"""
Newsletter Writer - Generate engaging email newsletters.

Usage:
    python3 execution/generate_newsletter.py \
        --topic "Weekly Marketing Tips" \
        --style "educational" \
        --length "short" \
        --output .tmp/newsletter.md
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv()


def get_client() -> OpenAI:
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def call_llm(client: OpenAI, system: str, user: str, temp: float = 0.7) -> str:
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=get_model(),
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=temp, max_tokens=3000
            )
            return resp.choices[0].message.content
        except Exception as e:
            if attempt == 2: raise e
    return ""


def generate_newsletter(client: OpenAI, topic: str, style: str, length: str, cta: str) -> dict:
    """Generate newsletter content."""
    
    length_words = {"short": 300, "medium": 500, "long": 800}
    word_count = length_words.get(length, 500)
    
    # Generate subject lines
    print("📧 Generating subject lines...")
    subjects = call_llm(client,
        "You are an email marketing expert with 40%+ open rates.",
        f"""Generate 5 subject line options for a newsletter about:
TOPIC: {topic}
STYLE: {style}

Use different frameworks:
1. Curiosity gap
2. Number/list
3. How-to/benefit
4. Question
5. Urgency/FOMO

Each should be under 50 characters.""", 0.8)
    
    # Generate newsletter body
    print("📝 Writing newsletter...")
    body = call_llm(client,
        f"You are an expert newsletter writer. Style: {style}. Be valuable and engaging.",
        f"""Write a {word_count}-word newsletter:

TOPIC: {topic}
STYLE: {style}
CTA: {cta}

STRUCTURE:
1. Hook (1-2 sentences that grab attention)
2. Main Value (the key insight/tip/story)
3. Supporting Content (examples, data, actionable steps)
4. CTA Section (what you want them to do)
5. Sign-off

RULES:
- Short paragraphs (1-3 sentences)
- Use "you" language
- Include one actionable takeaway
- Conversational but valuable
- End with clear CTA""", 0.7)
    
    # Generate preview text
    preview = call_llm(client, "You are an email expert.",
        f"Write a 40-60 character preview text for this newsletter that complements the subject line and creates curiosity:\n\n{body[:500]}", 0.6)
    
    return {"subjects": subjects, "body": body, "preview": preview}


def main():
    parser = argparse.ArgumentParser(description="Generate email newsletters")
    parser.add_argument("--topic", "-t", required=True, help="Newsletter topic")
    parser.add_argument("--style", "-s", default="educational",
        choices=["educational", "inspirational", "story", "curated", "promotional"])
    parser.add_argument("--length", "-l", default="medium", choices=["short", "medium", "long"])
    parser.add_argument("--cta", "-c", default="reply", help="Call to action (reply, link, share)")
    parser.add_argument("--output", "-o", default=".tmp/newsletter.md")
    
    args = parser.parse_args()
    
    print(f"\n📬 Newsletter Writer")
    print(f"   Topic: {args.topic}")
    print(f"   Style: {args.style}")
    print(f"   Length: {args.length}\n")
    
    client = get_client()
    result = generate_newsletter(client, args.topic, args.style, args.length, args.cta)
    
    output = f"""# Newsletter: {args.topic}

**Generated:** {datetime.now().strftime("%Y-%m-%d")}
**Style:** {args.style}

---

## SUBJECT LINE OPTIONS

{result['subjects']}

---

## PREVIEW TEXT

{result['preview']}

---

## NEWSLETTER BODY

{result['body']}
"""
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    
    print(f"\n✅ Newsletter complete!")
    print(f"   📄 Output: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
