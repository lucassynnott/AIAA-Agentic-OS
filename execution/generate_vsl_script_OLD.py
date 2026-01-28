#!/usr/bin/env python3
"""
VSL Script Generator

Generates high-converting VSL scripts using proven frameworks from skill bibles.
Follows directive: directives/vsl_script_writer.md
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
    print(f"❌ Error: Required library not installed: {e}")
    print("   Install with: pip install openai python-dotenv")
    exit(1)


def load_skill_bibles() -> str:
    """Load VSL skill bibles for context"""
    skill_bibles = []

    skill_paths = [
        "skills/SKILL_BIBLE_vsl_writing_production.md",
        "skills/SKILL_BIBLE_vsl_script_mastery_fazio.md",
        "skills/SKILL_BIBLE_funnel_copywriting_mastery.md",
    ]

    for path in skill_paths:
        try:
            with open(path, "r") as f:
                content = f.read()
                skill_bibles.append(f"# {Path(path).stem}\n\n{content}")
                print(f"✅ Loaded: {path}")
        except FileNotFoundError:
            print(f"⚠️  Skill bible not found: {path}")

    return "\n\n---\n\n".join(skill_bibles)


def generate_hooks(research_data: dict, client: OpenAI) -> list:
    """Generate 3 hook options using proven formulas"""
    print("🎯 Generating 3 hook options...")

    prompt = f"""Generate 3 powerful VSL opening hooks for this offer using different psychological frameworks.

RESEARCH CONTEXT:
Company: {research_data['company']['name']}
Offer: {research_data['offer']['name']}
Target Audience: {research_data.get('targetAudience', {}).get('demographics', 'Agency owners')}
Key Pain Points: {', '.join(research_data.get('targetAudience', {}).get('painPoints', ['scaling challenges'])[:3])}
Top Result: {research_data.get('socialProof', {}).get('caseStudies', ['Customer success'])[0][:200] if research_data.get('socialProof', {}).get('caseStudies') else 'N/A'}

REQUIREMENTS:
- Hook 1: Bold Claim + Curiosity Gap
- Hook 2: Pattern Interrupt + Question
- Hook 3: Social Proof + Promise

Each hook should:
- Stop the scroll in 3 seconds
- Identify the specific avatar
- Create curiosity
- Be 2-3 sentences max

Format as JSON:
{{
  "hooks": [
    {{
      "type": "Bold Claim + Curiosity",
      "text": "...",
      "whyItWorks": "..."
    }},
    ...
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    hooks_json = response.choices[0].message.content
    # Extract JSON from markdown code blocks if present
    if "```json" in hooks_json:
        hooks_json = hooks_json.split("```json")[1].split("```")[0].strip()

    return json.loads(hooks_json)["hooks"]


def generate_vsl_script(research_data: dict, skill_bibles: str, vsl_length: str, vsl_style: str, client: OpenAI) -> str:
    """Generate complete VSL script following 10-part framework"""
    print(f"📝 Generating {vsl_length} VSL script ({vsl_style} style)...")

    # Determine MINIMUM word count based on length
    min_word_counts = {
        "short": 2000,  # Minimum 2000 words (13 minutes)
        "medium": 2500,  # Minimum 2500 words (16 minutes)
        "long": 3500    # Minimum 3500 words (23 minutes)
    }
    min_words = min_word_counts.get(vsl_length, 2500)

    word_count_ranges = {
        "short": "2000-2500 words (13-17 minutes)",
        "medium": "2500-3000 words (16-20 minutes)",
        "long": "3500-4000 words (23-27 minutes)"
    }
    target_length = word_count_ranges.get(vsl_length, word_count_ranges["medium"])

    # Use Claude Opus 4.5 (as instructed in AGENTS.MD)
    model = "anthropic/claude-opus-4.5" if "openrouter" in str(client.base_url).lower() else "gpt-4o"

    # Build system prompt with full skill bible context
    system_prompt = f"""You are an expert VSL scriptwriter trained on the most advanced direct response frameworks.

SKILL BIBLE EXPERTISE (YOUR TRAINING):
{skill_bibles}  # Load FULL skill bibles, not truncated

You MUST follow the 10-part VSL structure from the skill bibles EXACTLY.
Each section must be fully developed with specific examples, stories, and proof."""

    user_prompt = f"""Generate a complete, high-converting VSL script for this offer.

RESEARCH DATA:
Company: {research_data['company']['name']}
Offer: {research_data['offer']['name']}

FULL OFFER DETAILS:
{research_data['offer']['description']}

TARGET AUDIENCE:
{research_data.get('targetAudience', {}).get('demographics', 'Business owners')}

PAIN POINTS (from research):
{chr(10).join('- ' + p for p in research_data.get('targetAudience', {}).get('painPoints', []))}

SOCIAL PROOF (from research):
{chr(10).join(research_data.get('socialProof', {}).get('caseStudies', []))}

CRITICAL REQUIREMENTS:
✅ MINIMUM {min_words} WORDS (this is NON-NEGOTIABLE)
✅ Target Range: {target_length}
✅ Style: {vsl_style}
✅ Follow 10-part VSL structure from skill bible

SCRIPT STRUCTURE (with approximate word counts per section):

1. **HOOK (0:00-0:30)** - 100-150 words
   - Pattern interrupt
   - Avatar identification
   - Curiosity gap

2. **PROBLEM IDENTIFICATION (0:30-2:00)** - 300-400 words
   - Mirror internal dialogue
   - Agitate top 3 pain points from research
   - "You've probably tried..." (list failed solutions)
   - Make them feel understood

3. **CREDIBILITY (2:00-3:00)** - 200-250 words
   - Brief authority establishment
   - Results you've achieved for others
   - "I've been where you are"

4. **SOLUTION INTRODUCTION (3:00-4:00)** - 200-250 words
   - Name the mechanism/system
   - High-level overview
   - Why it works differently

5. **MECHANISM DEEP DIVE (4:00-8:00)** - 600-800 words
   - The "how it works" section (LONGEST section)
   - Break into 3-5 clear steps
   - Proof for each step
   - Address objections pre-emptively

6. **SOCIAL PROOF STACK (8:00-10:00)** - 400-500 words
   - Case study 1 (most impressive)
   - Case study 2-3 (relatable)
   - Specific numbers and results
   - Testimonial quotes

7. **OFFER REVEAL (10:00-12:00)** - 400-500 words
   - What's included (core offer breakdown)
   - Bonus stack (itemized with value)
   - Total value calculation
   - Price reveal with justification

8. **URGENCY & SCARCITY (12:00-13:00)** - 200-250 words
   - Why spots are limited
   - What happens if they wait
   - Opportunity cost

9. **GUARANTEE (13:00-13:30)** - 150-200 words
   - Risk reversal
   - Clear terms
   - Confidence statement

10. **CALL TO ACTION (13:30-15:00)** - 200-250 words
    - Clear next step
    - What happens on the call
    - Final urgency reminder
    - Button text

OUTPUT FORMAT:
# VSL Script: [Company] - [Offer]

**Target Length:** {target_length}
**Style:** {vsl_style}

---

## HOOK (0:00-0:30)

[Full hook script - 100-150 words]

**Graphics:** [Specific visuals]
**Tone:** [Delivery notes]
**Emphasis:** [Words to emphasize]

---

## PROBLEM IDENTIFICATION (0:30-2:00)

[Full problem section - 300-400 words minimum]

[Continue for ALL 10 parts with FULL development]

ABSOLUTELY CRITICAL:
- DO NOT summarize or abbreviate sections
- Each section must hit its word count target
- Total script MUST be at least {min_words} words
- Use ALL social proof from research
- Include specific numbers and names
- Write complete sentences and paragraphs (not outlines)
- This is a SCRIPT to be READ, not bullet points
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=16000,  # Increased to allow full script generation
    )

    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Generate VSL script from research")
    parser.add_argument("--research", required=True, help="Path to research JSON file")
    parser.add_argument("--length", default="medium", choices=["short", "medium", "long"], help="VSL length")
    parser.add_argument("--style", default="education", choices=["education", "story", "case-study"], help="VSL style")
    parser.add_argument("--output", required=True, help="Output markdown file path")
    parser.add_argument("--hooks-output", help="Optional separate hooks output file")

    args = parser.parse_args()

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY or OPENROUTER_API_KEY not found")
        return 1

    # Use OpenRouter if that's what we have
    if os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        print("🔧 Using OpenRouter API")
    else:
        client = OpenAI(api_key=api_key)
        print("🔧 Using OpenAI API")

    print(f"🚀 Starting VSL script generation...")

    # Load research data
    with open(args.research, "r") as f:
        research_data = json.load(f)

    print(f"✅ Loaded research for: {research_data['company']['name']}")

    # Load skill bibles
    skill_bibles = load_skill_bibles()

    # Generate hooks
    hooks = generate_hooks(research_data, client)

    if args.hooks_output:
        hooks_doc = "# Hook Options\n\n"
        for i, hook in enumerate(hooks, 1):
            hooks_doc += f"## Option {i}: {hook['type']}\n\n"
            hooks_doc += f"{hook['text']}\n\n"
            hooks_doc += f"**Why this works:** {hook['whyItWorks']}\n\n---\n\n"

        Path(args.hooks_output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.hooks_output, "w") as f:
            f.write(hooks_doc)
        print(f"✅ Hooks saved: {args.hooks_output}")

    # Generate full VSL script
    script = generate_vsl_script(research_data, skill_bibles, args.length, args.style, client)

    # Save output
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        f.write(script)

    # Calculate stats
    word_count = len(script.split())
    estimated_minutes = round(word_count / 150, 1)  # 150 words per minute average

    print(f"\n✅ VSL Script generated!")
    print(f"   Output: {args.output}")
    print(f"   Word count: {word_count}")
    print(f"   Estimated length: {estimated_minutes} minutes")
    print(f"   Hooks generated: {len(hooks)}")

    return 0


if __name__ == "__main__":
    exit(main())
