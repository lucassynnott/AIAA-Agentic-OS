#!/usr/bin/env python3
"""
VSL Funnel Writer - Generate complete VSL (Video Sales Letter) funnel copy
including script, landing page, and email sequence using proven frameworks.

Usage:
    python3 execution/generate_vsl_funnel.py \
        --product "Course Name" \
        --price "$997" \
        --audience "Entrepreneurs" \
        --pain_points "struggling with X, frustrated by Y" \
        --transformation "Go from A to B in 90 days" \
        --mechanism "The XYZ Method" \
        --output_dir ".tmp/vsl_output"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY required in .env")
    sys.exit(1)


def get_client() -> OpenAI:
    """Get OpenAI client configured for OpenRouter or OpenAI."""
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    """Get the model to use."""
    if os.getenv("OPENROUTER_API_KEY"):
        return "anthropic/claude-sonnet-4"
    return "gpt-4o"


def call_llm(client: OpenAI, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """Call LLM with retry logic."""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=get_model(),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                raise e
            print(f"  Retry {attempt + 1}/3: {e}")
    return ""


def generate_vsl_hooks(client: OpenAI, config: dict) -> str:
    """Generate powerful VSL opening hooks."""
    print("🎣 Generating VSL hooks...")
    
    system_prompt = """You are a world-class VSL copywriter who has written scripts that have generated millions in sales. Create irresistible hooks."""
    
    user_prompt = f"""Create 5 powerful VSL opening hooks for this offer:

PRODUCT CONTEXT:
- Product/Service: {config['product']}
- Price Point: {config['price']}
- Target Audience: {config['audience']}
- Main Pain Points: {config['pain_points']}
- Transformation Promise: {config['transformation']}
- Unique Mechanism: {config['mechanism']}
- Guarantee: {config.get('guarantee', '30-day money-back guarantee')}

CREATE 5 HOOKS USING DIFFERENT FRAMEWORKS:

HOOK 1: Pattern Interrupt
- Start with something unexpected that stops the scroll
- Create immediate curiosity
- Example pattern: "What if everything you've been told about X is wrong?"

HOOK 2: Big Promise
- Lead with the transformation
- Be specific with numbers/timeframes
- Example pattern: "How to [achieve result] in [timeframe] without [common obstacle]"

HOOK 3: Enemy/Villain
- Call out what's been holding them back
- Create "us vs them" dynamic
- Example pattern: "The [industry/gurus] don't want you to know this..."

HOOK 4: Story-Based
- Open with a compelling personal story
- Create emotional connection
- Example pattern: "3 years ago, I was exactly where you are now..."

HOOK 5: Curiosity Gap
- Create an information gap they need to fill
- Tease the mechanism
- Example pattern: "There's a hidden [thing] that top [achievers] use..."

For each hook, provide:
1. The hook itself (2-3 sentences)
2. Why it works psychologically
3. The exact opening line for the video

Make hooks specific to this offer, not generic."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.8)


def generate_vsl_story(client: OpenAI, config: dict, hooks: str) -> str:
    """Generate the main VSL story section."""
    print("📖 Writing VSL story section...")
    
    system_prompt = """You are a master storyteller and VSL scriptwriter. Create compelling stories that build trust and desire."""
    
    user_prompt = f"""Create the main story section for this VSL:

PRODUCT CONTEXT:
- Product/Service: {config['product']}
- Price Point: {config['price']}
- Target Audience: {config['audience']}
- Main Pain Points: {config['pain_points']}
- Transformation Promise: {config['transformation']}
- Unique Mechanism: {config['mechanism']}

SELECTED HOOKS:
{hooks[:1500]}

WRITE THE STORY SECTION (spoken script format):

## PART 1: RELATABILITY (2-3 minutes)
- Establish credibility through shared struggle
- "I know exactly how you feel because..."
- Show you understand their world
- Build trust through vulnerability

## PART 2: THE JOURNEY (3-4 minutes)
- Your discovery story
- The breakthrough moment
- What you tried that didn't work
- The "aha" that changed everything

## PART 3: THE MECHANISM REVEAL (2-3 minutes)
- Introduce the unique mechanism
- Why it's different from everything else
- The science/logic behind it
- Why it works when other things don't

## PART 4: PROOF & RESULTS (2-3 minutes)
- Your personal results
- Client/student results (describe scenarios)
- Specific numbers and transformations
- "Before and after" scenarios

Write this as a spoken script with natural language, pauses noted, and emotional beats marked. Use conversational tone - this is meant to be spoken, not read."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_vsl_objections(client: OpenAI, config: dict) -> str:
    """Generate objection handling section."""
    print("🛡️ Creating objection handling...")
    
    system_prompt = """You are an expert at addressing buying objections in VSLs. Handle objections before they become blockers."""
    
    user_prompt = f"""Create a masterful objection handling section for this VSL:

PRODUCT CONTEXT:
- Product/Service: {config['product']}
- Price Point: {config['price']}
- Target Audience: {config['audience']}
- Transformation Promise: {config['transformation']}
- Guarantee: {config.get('guarantee', '30-day money-back guarantee')}

ADDRESS THESE COMMON OBJECTIONS:

1. "IT'S TOO EXPENSIVE"
- Reframe the investment
- Compare to cost of NOT solving
- Show ROI

2. "I DON'T HAVE TIME"
- Address time concerns
- Show efficiency
- Minimal time commitment

3. "I'VE TRIED THINGS BEFORE"
- Why this is different
- What makes your approach unique
- Address skepticism

4. "I'M NOT SURE IT WILL WORK FOR ME"
- Social proof for "people like them"
- Range of success stories
- The guarantee safety net

5. "I NEED TO THINK ABOUT IT"
- Cost of waiting
- Why now is the time
- Urgency element

For each objection:
1. Acknowledge it ("I get it...")
2. Reframe it
3. Provide proof/logic
4. Transition to next point

Write as spoken script, conversational tone."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_vsl_close(client: OpenAI, config: dict) -> str:
    """Generate VSL closing and CTA section."""
    print("🎬 Writing closing and CTA...")
    
    system_prompt = """You are a master closer who writes VSL endings that convert. Create urgency and make the decision feel inevitable."""
    
    user_prompt = f"""Create a powerful VSL close and call-to-action:

PRODUCT CONTEXT:
- Product/Service: {config['product']}
- Price Point: {config['price']}
- Target Audience: {config['audience']}
- Transformation Promise: {config['transformation']}
- Guarantee: {config.get('guarantee', '30-day money-back guarantee')}
- Urgency Element: {config.get('urgency', 'Limited enrollment')}
- Bonuses: {config.get('bonuses', 'Not specified')}

CREATE THE CLOSING SECTION:

## OFFER RECAP (1-2 minutes)
- Everything they're getting
- Value stack with specific values
- Bonus breakdown
- Total value vs. price

## GUARANTEE SECTION (1 minute)
- Risk reversal
- Make it feel completely safe
- "Try it, and if..."

## URGENCY/SCARCITY (1 minute)
- Why they need to act now
- What happens if they wait
- Limited time/spots element

## FINAL CTA (2-3 minutes)
- The two paths (with/without)
- Future pacing success
- Clear next step
- "Click the button below..."

## CLOSING STATEMENT
- Powerful final words
- Leave them inspired
- Call to action one more time

Write as spoken script. Make it emotional but not manipulative. Create genuine urgency."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_landing_page(client: OpenAI, config: dict, vsl_content: str) -> str:
    """Generate landing page copy to accompany the VSL."""
    print("🖥️ Creating landing page copy...")
    
    system_prompt = """You are a landing page copywriter. Create copy that complements a VSL and drives conversions."""
    
    user_prompt = f"""Create landing page copy to accompany this VSL:

PRODUCT CONTEXT:
- Product/Service: {config['product']}
- Price Point: {config['price']}
- Target Audience: {config['audience']}
- Transformation Promise: {config['transformation']}

VSL SUMMARY:
{vsl_content[:1000]}

CREATE LANDING PAGE SECTIONS:

## ABOVE THE FOLD
- Headline (attention-grabbing)
- Subheadline (clarifies the promise)
- VSL embed area
- Primary CTA button text

## BELOW VSL SECTION
- "What You'll Discover" bullets (5-7)
- Social proof section
- "This is for you if..." section
- "This is NOT for you if..." section

## OFFER SECTION
- What's included (value stack)
- Bonus descriptions
- Price presentation
- Payment options text

## FAQ SECTION
- 5 common questions with answers
- Address objections subtly

## FINAL CTA SECTION
- Urgency reminder
- Final headline
- CTA button text
- Guarantee reminder

Make copy scannable, benefit-focused, and action-oriented."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_email_sequence(client: OpenAI, config: dict) -> str:
    """Generate email sequence for VSL funnel."""
    print("📧 Writing email sequence...")
    
    system_prompt = """You are an email marketing expert for VSL funnels. Write emails that drive people to watch the VSL and buy."""
    
    user_prompt = f"""Create a 5-email sequence for this VSL funnel:

PRODUCT CONTEXT:
- Product/Service: {config['product']}
- Price Point: {config['price']}
- Target Audience: {config['audience']}
- Transformation Promise: {config['transformation']}
- Unique Mechanism: {config['mechanism']}

CREATE 5 EMAILS:

EMAIL 1: "Watch This" (Immediately after opt-in)
- Get them to watch the VSL
- Create curiosity
- Low-friction ask

EMAIL 2: "Did You Catch This?" (24 hours later)
- For non-watchers: drive to VSL
- For watchers: highlight key moment
- Social proof

EMAIL 3: "The Truth About [Topic]" (48 hours)
- Value-driven content
- Address a key objection
- Soft pitch

EMAIL 4: "Quick Question" (72 hours)
- Engagement email
- Address "sitting on the fence"
- Urgency hint

EMAIL 5: "Last Chance" (96 hours)
- Final push
- Deadline/scarcity
- FOMO

For each email provide:
- 3 subject line options
- Preview text
- Complete email body (150-250 words)
- CTA

Write complete emails, conversational tone."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def save_output(output_dir: Path, filename: str, content: str) -> str:
    """Save content to file."""
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Generate complete VSL funnel copy")
    parser.add_argument("--product", required=True, help="Product/service name")
    parser.add_argument("--price", required=True, help="Price point (e.g., $997)")
    parser.add_argument("--audience", required=True, help="Target audience")
    parser.add_argument("--pain_points", default="", help="Main pain points")
    parser.add_argument("--transformation", default="", help="Transformation promise")
    parser.add_argument("--mechanism", default="", help="Unique mechanism/method name")
    parser.add_argument("--guarantee", default="30-day money-back guarantee", help="Guarantee offered")
    parser.add_argument("--urgency", default="Limited enrollment", help="Urgency element")
    parser.add_argument("--bonuses", default="", help="Bonus stack description")
    parser.add_argument("--output_dir", default=".tmp/vsl_output", help="Output directory")
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build config
    config = {
        "product": args.product,
        "price": args.price,
        "audience": args.audience,
        "pain_points": args.pain_points or "Not specified",
        "transformation": args.transformation or f"Transform your results with {args.product}",
        "mechanism": args.mechanism or "Our proven method",
        "guarantee": args.guarantee,
        "urgency": args.urgency,
        "bonuses": args.bonuses
    }
    
    print(f"\n🎬 VSL Funnel Writer")
    print(f"   Product: {config['product']}")
    print(f"   Price: {config['price']}")
    print(f"   Audience: {config['audience']}")
    print(f"   Output: {output_dir}\n")
    
    client = get_client()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Step 1: Generate Hooks
    hooks = generate_vsl_hooks(client, config)
    hooks_file = save_output(output_dir, f"01_vsl_hooks_{timestamp}.md",
        f"# VSL Hooks: {config['product']}\n\n{hooks}")
    print(f"   ✅ Saved: {hooks_file}")
    
    # Step 2: Generate Story Section
    story = generate_vsl_story(client, config, hooks)
    story_file = save_output(output_dir, f"02_vsl_story_{timestamp}.md",
        f"# VSL Story Section: {config['product']}\n\n{story}")
    print(f"   ✅ Saved: {story_file}")
    
    # Step 3: Generate Objection Handling
    objections = generate_vsl_objections(client, config)
    objections_file = save_output(output_dir, f"03_vsl_objections_{timestamp}.md",
        f"# VSL Objection Handling: {config['product']}\n\n{objections}")
    print(f"   ✅ Saved: {objections_file}")
    
    # Step 4: Generate Close
    close = generate_vsl_close(client, config)
    close_file = save_output(output_dir, f"04_vsl_close_{timestamp}.md",
        f"# VSL Close & CTA: {config['product']}\n\n{close}")
    print(f"   ✅ Saved: {close_file}")
    
    # Step 5: Compile Complete VSL Script
    complete_vsl = f"""# Complete VSL Script: {config['product']}

## PRODUCT DETAILS
- Product: {config['product']}
- Price: {config['price']}
- Audience: {config['audience']}
- Transformation: {config['transformation']}

---

## SECTION 1: HOOKS

{hooks}

---

## SECTION 2: STORY

{story}

---

## SECTION 3: OBJECTION HANDLING

{objections}

---

## SECTION 4: CLOSE & CTA

{close}
"""
    vsl_file = save_output(output_dir, f"05_complete_vsl_script_{timestamp}.md", complete_vsl)
    print(f"   ✅ Saved: {vsl_file}")
    
    # Step 6: Generate Landing Page
    landing = generate_landing_page(client, config, complete_vsl[:2000])
    landing_file = save_output(output_dir, f"06_landing_page_{timestamp}.md",
        f"# Landing Page Copy: {config['product']}\n\n{landing}")
    print(f"   ✅ Saved: {landing_file}")
    
    # Step 7: Generate Email Sequence
    emails = generate_email_sequence(client, config)
    email_file = save_output(output_dir, f"07_email_sequence_{timestamp}.md",
        f"# Email Sequence: {config['product']}\n\n{emails}")
    print(f"   ✅ Saved: {email_file}")
    
    # Summary
    print(f"\n✅ VSL funnel generation complete!")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   📄 Files generated: 7")
    print(f"\n   Files:")
    for f in sorted(output_dir.glob(f"*{timestamp}.md")):
        print(f"      - {f.name}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
