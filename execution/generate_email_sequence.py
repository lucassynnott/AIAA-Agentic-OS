#!/usr/bin/env python3
"""
VSL Email Sequence Generator

Generates 7-email nurture sequence for VSL funnel.
Follows directive: directives/vsl_email_sequence_writer.md
"""

import argparse
import json
import os
from pathlib import Path

try:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()
except ImportError as e:
    print(f"❌ Error: {e}")
    exit(1)


def generate_email_sequence(research_data: dict, vsl_script: str, sales_page: str, sequence_length: int, client: OpenAI) -> str:
    """Generate complete email sequence"""
    print(f"📧 Generating {sequence_length}-email sequence...")

    # Use Claude Opus 4.5
    model = "anthropic/claude-opus-4.5" if "openrouter" in str(client.base_url).lower() else "gpt-4o"

    system_prompt = """You are an expert email copywriter specializing in high-converting nurture sequences for B2B VSL funnels.

Your emails are substantial, value-rich, and hit 300-500 words MINIMUM per email.
You write complete emails with full narratives, not outlines or summaries.
Total sequence should be 2500-3500 words (7 emails × 350-500 words each)."""

    prompt = f"""Generate a high-converting {sequence_length}-email nurture sequence for VSL funnel viewers who didn't book immediately.

CONTEXT:
Company: {research_data['company']['name']}
Offer: {research_data['offer']['name']}

VSL FULL CONTEXT:
{vsl_script[:3000]}

SOCIAL PROOF FROM RESEARCH:
{chr(10).join(research_data.get('socialProof', {}).get('caseStudies', [])[:2])}

CRITICAL REQUIREMENTS:
✅ MINIMUM 300-500 WORDS PER EMAIL (7 emails = 2500-3500 total words)
✅ Each email must be FULLY written (complete paragraphs, stories, examples)
✅ Include specific details from research
✅ Conversational, personal tone

SEQUENCE STRUCTURE (7 emails):
1. **Email 1 (Immediate):** "Did you watch?" - Re-engage (350-400 words)
2. **Email 2 (Day 1):** Indoctrination - Your story/credentials (400-500 words)
3. **Email 3 (Day 2):** Case study deep dive - Specific result (450-500 words)
4. **Email 4 (Day 3):** Mechanism explanation - How it works (400-500 words)
5. **Email 5 (Day 4):** Objection crusher - Address top concern (350-450 words)
6. **Email 6 (Day 5):** Urgency reminder - Spots filling (300-400 words)
7. **Email 7 (Day 6):** Last chance - Final deadline (350-400 words)

REQUIREMENTS FOR EACH EMAIL:
- **Subject Line** (2 variations - both compelling)
- **Preview Text** (50 chars)
- **Body Copy** (300-500 words FULL copy with paragraphs, stories, examples)
- **PS Section** (50-100 words with secondary benefit or urgency)
- **CTA Button Text** (clear action)

EMAIL BEST PRACTICES:
- Conversational tone (like talking to a friend)
- Short paragraphs (2-3 sentences max)
- One clear CTA per email
- Personal story elements
- Specific numbers/results
- Address one core objection per email

OUTPUT FORMAT (Markdown):
# Email Sequence: [Company] - [Offer]

## Email 1: Did You Watch? (Send: Immediately)

### Subject Line A
[Subject line]

### Subject Line B
[Alternative]

### Preview Text
[Preview text - 50 chars]

### Body

[Email body copy]

**P.S.** [Secondary benefit or urgency]

### CTA
[Book Your Call] → [Calendar URL]

---

[Repeat for all 7 emails...]

ABSOLUTELY CRITICAL:
- DO NOT write outlines - write COMPLETE email copy
- Each email must be 300-500 words (check word count mentally)
- Use actual company/offer names
- Include specific results from research with numbers
- Natural, conversational tone (like emailing a friend)
- Each email standalone readable
- Progressive urgency increase from email 1 to 7
- Include full stories and examples (not just bullet points)
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=16000,  # Increased for full sequence (7 long emails)
    )

    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Generate email sequence")
    parser.add_argument("--research", required=True, help="Research JSON file")
    parser.add_argument("--vsl-script", required=True, help="VSL script file")
    parser.add_argument("--sales-page", required=True, help="Sales page file")
    parser.add_argument("--length", type=int, default=7, choices=[5, 7], help="Sequence length")
    parser.add_argument("--output", required=True, help="Output markdown file")

    args = parser.parse_args()

    # Initialize API
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: No API key found")
        return 1

    if os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    else:
        client = OpenAI(api_key=api_key)

    print("🚀 Starting email sequence generation...")

    # Load inputs
    with open(args.research, "r") as f:
        research_data = json.load(f)

    with open(args.vsl_script, "r") as f:
        vsl_script = f.read()

    with open(args.sales_page, "r") as f:
        sales_page = f.read()

    # Generate sequence
    email_sequence = generate_email_sequence(research_data, vsl_script, sales_page, args.length, client)

    # Save output
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        f.write(email_sequence)

    print(f"\n✅ Email sequence generated!")
    print(f"   Output: {args.output}")
    print(f"   Emails: {args.length}")
    print(f"   Word count: {len(email_sequence.split())}")

    return 0


if __name__ == "__main__":
    exit(main())
