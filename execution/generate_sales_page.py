#!/usr/bin/env python3
"""
VSL Sales Page Generator

Generates sales page copy to accompany VSL.
Follows directive: directives/vsl_sales_page_writer.md
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


def load_landing_page_skill_bible() -> str:
    """Load landing page skill bible for enhanced sales page generation."""
    skill_path = Path(__file__).parent.parent / "skills" / "SKILL_BIBLE_landing_page_ai_mastery.md"
    if skill_path.exists():
        content = skill_path.read_text(encoding="utf-8")
        # Extract key sections for context
        sections = []
        for section in ["## Core Principles", "## Best Practices", "## Advanced Techniques"]:
            if section in content:
                start = content.find(section)
                next_section = content.find("\n## ", start + len(section))
                if next_section > start:
                    sections.append(content[start:next_section])
                else:
                    sections.append(content[start:start + 1500])
        return "\n".join(sections)[:3500]
    return ""


def generate_sales_page(research_data: dict, vsl_script: str, page_style: str, client: OpenAI) -> str:
    """Generate complete sales page copy"""
    print(f"📄 Generating {page_style} sales page...")

    # Load skill bible for enhanced context
    skill_context = load_landing_page_skill_bible()

    # Use Claude Opus 4.5
    model = "anthropic/claude-opus-4.5" if "openrouter" in str(client.base_url).lower() else "gpt-4o"

    skill_section = ""
    if skill_context:
        skill_section = f"""

APPLY THESE LANDING PAGE BEST PRACTICES:
{skill_context[:2500]}
"""

    system_prompt = f"""You are a master funnel copywriter specializing in long-form sales pages for high-ticket B2B offers.

Your sales pages are comprehensive, persuasive, and hit 1500-3000 words minimum.
You write FULL copy, not outlines or summaries. Every section is fully developed.
{skill_section}"""

    prompt = f"""Generate a complete, long-form sales page to accompany this VSL.

CONTEXT:
Company: {research_data['company']['name']}
Offer: {research_data['offer']['name']}
Target Audience: {research_data.get('targetAudience', {}).get('demographics', 'Business owners')}

VSL KEY POINTS:
{vsl_script[:2000]}

CRITICAL REQUIREMENTS:
✅ MINIMUM 1500 WORDS (long-form sales pages convert better)
✅ Target: 1500-3000 words depending on style
✅ Write FULL copy for every section (not outlines)
✅ Each bullet should be 1-2 sentences explaining the benefit

REQUIREMENTS:
Generate a complete sales page with:

1. **Headline (3 variations for A/B testing)**
   - Curiosity-driven
   - Benefit-driven
   - Social proof-driven

2. **Subheadline** - Expand on promise

3. **Pre-Video Copy** - Pattern interrupt + brief setup (2-3 sentences)

4. **Video Embed Section** - "[VIDEO EMBED HERE]" placeholder

5. **Post-Video Bullets** - 10-15 transformation/benefit bullets
   - Each bullet should be 1-2 sentences (not just a single line)
   - Focus on outcomes with supporting details
   - Use power words and specificity
   - Include numbers where possible

6. **About the Mechanism Section** - 300-500 words
   - Detailed explanation of how it works
   - Why it's different from competitors
   - Proof that it works

7. **Social Proof Section** - 400-600 words
   - 3-5 testimonials with full context
   - Specific results and timeframes
   - Use ALL research data
   - Include company names if available

8. **Offer Details** - 500-700 words
   - What's included (detailed breakdown)
   - Bonus stack (each bonus explained in 2-3 sentences)
   - Total value calculation shown
   - Value justification

8. **Guarantee Section**
   - Risk reversal copy
   - Clear terms

9. **CTA Button Copy** - 3 variations

10. **FAQ Section** - Top 5-7 objections
    - Price concern
    - Time concern
    - "Does it work for me?"
    - Implementation difficulty
    - Results timeline

OUTPUT FORMAT (Markdown):
# Sales Page: [Company] - [Offer]

## Headline Options

### Option 1: Curiosity
[Headline]

### Option 2: Benefit
[Headline]

### Option 3: Social Proof
[Headline]

## Subheadline
[Subheadline text]

## Pre-Video Copy
[2-3 sentences]

## Video Section
[VIDEO EMBED HERE]

## What You'll Discover
- [Bullet point 1]
- [Bullet point 2]
...

[Continue with all sections...]

Style: {page_style}
Tone: Confident, direct, results-focused
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=12000,  # Increased for long-form copy
    )

    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Generate sales page copy")
    parser.add_argument("--research", required=True, help="Research JSON file")
    parser.add_argument("--vsl-script", required=True, help="VSL script markdown file")
    parser.add_argument("--style", default="full", choices=["minimal", "full", "long-form"], help="Page style")
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

    print("🚀 Starting sales page generation...")

    # Load inputs
    with open(args.research, "r") as f:
        research_data = json.load(f)

    with open(args.vsl_script, "r") as f:
        vsl_script = f.read()

    # Generate page
    sales_page = generate_sales_page(research_data, vsl_script, args.style, client)

    # Save output
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        f.write(sales_page)

    print(f"\n✅ Sales page generated!")
    print(f"   Output: {args.output}")
    print(f"   Word count: {len(sales_page.split())}")

    return 0


if __name__ == "__main__":
    exit(main())
