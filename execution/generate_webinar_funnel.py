#!/usr/bin/env python3
"""
Webinar Funnel Generator - Generate complete webinar funnel assets
including registration page, webinar script, slides outline, and email sequences.

Usage:
    python3 execution/generate_webinar_funnel.py \
        --topic "How to Scale Your Agency to 7 Figures" \
        --offer "Agency Accelerator Program" \
        --price "$2,997" \
        --audience "Agency owners doing $10-50k/month" \
        --duration "90" \
        --output_dir ".tmp/webinar_output"
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


def generate_registration_page(client: OpenAI, config: dict) -> str:
    """Generate webinar registration page copy."""
    print("📝 Creating registration page...")
    
    system_prompt = """You are an expert at writing high-converting webinar registration pages. Your pages consistently achieve 40%+ conversion rates."""
    
    user_prompt = f"""Create a high-converting webinar registration page:

WEBINAR DETAILS:
- Topic: {config['topic']}
- Offer: {config['offer']}
- Price Point: {config['price']}
- Target Audience: {config['audience']}
- Duration: {config['duration']} minutes
- Date/Time: {config.get('datetime', 'TBD')}
- Fast Action Bonus: {config.get('fast_action_bonus', 'None')}

CREATE COMPLETE REGISTRATION PAGE:

## HEADLINE OPTIONS (3)
- Benefit-driven headlines
- Curiosity-driven headlines
- Problem-solution headlines

## SUBHEADLINE
- Clarifies the promise
- Adds specificity

## ABOVE THE FOLD SECTION
- Registration form headline
- Bullet points of what they'll learn (5-7)
- CTA button text

## HOST CREDIBILITY SECTION
- Brief bio positioning
- Key credentials
- Social proof indicators

## "ON THIS FREE TRAINING, YOU'LL DISCOVER" SECTION
- 5-7 specific takeaways
- Each with outcome attached
- Curiosity-inducing language

## "THIS IS FOR YOU IF" SECTION
- 5 qualifying statements
- Creates self-identification

## "THIS IS NOT FOR YOU IF" SECTION
- 3 disqualifying statements
- Weeds out bad fits

## URGENCY/SCARCITY ELEMENTS
- Limited spots
- Fast action bonus
- Replay availability note

## FOOTER CTA
- Final push
- CTA button text
- Last reminder of value

Write complete copy, not outlines. Make it compelling and specific."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_thank_you_page(client: OpenAI, config: dict) -> str:
    """Generate thank you page copy."""
    print("🎉 Creating thank you page...")
    
    system_prompt = """You are an expert at maximizing webinar show rates. Create thank you pages that ensure high attendance."""
    
    user_prompt = f"""Create a webinar thank you page that maximizes show rates:

WEBINAR DETAILS:
- Topic: {config['topic']}
- Date/Time: {config.get('datetime', 'TBD')}
- Duration: {config['duration']} minutes
- Fast Action Bonus: {config.get('fast_action_bonus', 'None')}

CREATE THANK YOU PAGE:

## CONFIRMATION SECTION
- "You're In!" headline
- Confirmation of what they registered for
- Date/time reminder
- Add to calendar buttons text

## "WHAT TO DO RIGHT NOW" SECTION
- Step 1: Add to calendar
- Step 2: Set a reminder
- Step 3: Prepare questions
- Step 4: Clear your schedule

## PRIME THEIR EXPECTATIONS
- "Come ready to learn..."
- What to have ready
- How to get the most value

## FAST ACTION BONUS (if applicable)
- What the bonus is
- How to claim it
- Creates commitment

## "WHAT WE'LL COVER" PREVIEW
- Brief outline
- Creates anticipation
- Shows value

## SHARE SECTION
- Social share buttons
- Share copy suggestions

## PS SECTION
- Reminder of key benefit
- Urgency element

Write complete copy that builds excitement and commitment."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_webinar_script(client: OpenAI, config: dict) -> str:
    """Generate complete webinar script."""
    print("🎤 Writing webinar script...")
    
    system_prompt = """You are a master webinar presenter who has done millions in webinar sales. Create engaging, high-converting webinar scripts."""
    
    user_prompt = f"""Create a complete webinar script:

WEBINAR DETAILS:
- Topic: {config['topic']}
- Offer: {config['offer']}
- Price Point: {config['price']}
- Target Audience: {config['audience']}
- Duration: {config['duration']} minutes
- Teaching Style: {config.get('teaching_style', 'Educational with soft pitch')}

CREATE COMPLETE WEBINAR SCRIPT:

## OPENING (5-7 minutes)
- Pattern interrupt opening
- Set expectations
- Big promise for the webinar
- Quick credibility
- "Stay until the end" hook

## CONTENT SECTION 1 (15-20 minutes)
- First major teaching point
- Framework or concept
- Examples/stories
- Quick win for attendees

## CONTENT SECTION 2 (15-20 minutes)
- Second major teaching point
- Builds on section 1
- Common mistakes to avoid
- Another example/story

## CONTENT SECTION 3 (10-15 minutes)
- Third teaching point
- Advanced insight
- Transition to "the problem"

## THE BRIDGE (5-10 minutes)
- "But here's what I've realized..."
- Why content alone isn't enough
- The missing piece
- Natural transition to offer

## THE OFFER (15-20 minutes)
- Introduction of the offer
- What's included (detailed)
- Value stack
- Bonuses
- Price reveal
- Guarantee
- CTA

## Q&A FRAMEWORK (10 minutes)
- Prepared questions to answer
- Objection-handling responses
- Final push
- Closing CTA

Write as a spoken script with transitions, pauses noted, and slide cues marked [SLIDE: description]."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_slide_outline(client: OpenAI, config: dict, script: str) -> str:
    """Generate slide deck outline."""
    print("📊 Creating slide outline...")
    
    system_prompt = """You are a presentation designer. Create clear slide-by-slide outlines for webinars."""
    
    user_prompt = f"""Create a slide-by-slide outline for this webinar:

WEBINAR DETAILS:
- Topic: {config['topic']}
- Duration: {config['duration']} minutes

WEBINAR SCRIPT SUMMARY:
{script[:2000]}

CREATE SLIDE OUTLINE:

For each slide, provide:
- Slide number
- Slide title
- Key content/bullets (3-5 max)
- Visual suggestion
- Presenter notes (1 sentence)

STRUCTURE:
- Title slide
- Agenda slide
- "Who am I" slide
- Promise slide
- Content section 1 slides (5-8 slides)
- Content section 2 slides (5-8 slides)
- Content section 3 slides (5-8 slides)
- Bridge/transition slides (2-3 slides)
- Offer introduction slide
- What's included slides (3-5 slides)
- Bonus slides (2-4 slides)
- Pricing slide
- Guarantee slide
- CTA slide
- FAQ slides (3-5 slides)
- Final CTA slide

Keep slides simple - one idea per slide. Include visual recommendations."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.6)


def generate_pre_webinar_emails(client: OpenAI, config: dict) -> str:
    """Generate pre-webinar email sequence."""
    print("📧 Writing pre-webinar emails...")
    
    system_prompt = """You are an email marketing expert. Write pre-webinar sequences that maximize show rates."""
    
    user_prompt = f"""Create a pre-webinar email sequence:

WEBINAR DETAILS:
- Topic: {config['topic']}
- Offer: {config['offer']}
- Target Audience: {config['audience']}

CREATE 5 PRE-WEBINAR EMAILS:

EMAIL 1: Confirmation (Immediately)
- Welcome and excitement
- What they'll learn
- Add to calendar CTA

EMAIL 2: Content Tease (48 hours before)
- Share a quick tip
- Build anticipation
- Remind them to attend

EMAIL 3: Social Proof (24 hours before)
- Share a result/testimonial
- Create FOMO
- What others are saying

EMAIL 4: Reminder (4 hours before)
- Simple reminder
- Link to join
- Come prepared note

EMAIL 5: "We're Live!" (At start time)
- Very short
- Direct link
- Urgency

For each email:
- 3 subject line options
- Preview text
- Complete email body
- CTA"""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_post_webinar_emails(client: OpenAI, config: dict) -> str:
    """Generate post-webinar email sequence."""
    print("📧 Writing post-webinar emails...")
    
    system_prompt = """You are an email marketing expert. Write post-webinar sequences that maximize conversions."""
    
    user_prompt = f"""Create a post-webinar email sequence:

WEBINAR DETAILS:
- Topic: {config['topic']}
- Offer: {config['offer']}
- Price: {config['price']}
- Target Audience: {config['audience']}
- Guarantee: {config.get('guarantee', '30-day guarantee')}

CREATE 6 POST-WEBINAR EMAILS:

EMAIL 1: Replay Available (Immediately after)
- Thank attendees/non-attendees
- Replay link
- Summary of what was covered
- Offer reminder

EMAIL 2: "Did You Have Questions?" (24 hours)
- Address common questions
- Overcome objections
- Soft pitch

EMAIL 3: Case Study (48 hours)
- Share a success story
- Results breakdown
- "Imagine if you..."

EMAIL 4: FAQ (72 hours)
- Address objections as FAQs
- Risk reversal
- Price anchoring

EMAIL 5: Urgency (96 hours)
- Deadline approaching
- What they'll miss
- Final bonuses

EMAIL 6: Last Chance (120 hours)
- Final email
- Replay coming down
- Last opportunity
- Strong close

For each email:
- 3 subject line options
- Preview text
- Complete email body
- CTA"""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def save_output(output_dir: Path, filename: str, content: str) -> str:
    """Save content to file."""
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Generate complete webinar funnel")
    parser.add_argument("--topic", required=True, help="Webinar topic/title")
    parser.add_argument("--offer", required=True, help="Product/service being offered")
    parser.add_argument("--price", required=True, help="Price point")
    parser.add_argument("--audience", required=True, help="Target audience")
    parser.add_argument("--duration", default="90", help="Webinar duration in minutes")
    parser.add_argument("--datetime", default="", help="Webinar date/time")
    parser.add_argument("--fast_action_bonus", default="", help="Fast action bonus")
    parser.add_argument("--teaching_style", default="Educational with soft pitch", help="Teaching style")
    parser.add_argument("--guarantee", default="30-day money-back guarantee", help="Guarantee")
    parser.add_argument("--output_dir", default=".tmp/webinar_output", help="Output directory")
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build config
    config = {
        "topic": args.topic,
        "offer": args.offer,
        "price": args.price,
        "audience": args.audience,
        "duration": args.duration,
        "datetime": args.datetime or "Date TBD",
        "fast_action_bonus": args.fast_action_bonus,
        "teaching_style": args.teaching_style,
        "guarantee": args.guarantee
    }
    
    print(f"\n🎥 Webinar Funnel Generator")
    print(f"   Topic: {config['topic']}")
    print(f"   Offer: {config['offer']}")
    print(f"   Price: {config['price']}")
    print(f"   Duration: {config['duration']} minutes")
    print(f"   Output: {output_dir}\n")
    
    client = get_client()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Step 1: Registration Page
    reg_page = generate_registration_page(client, config)
    reg_file = save_output(output_dir, f"01_registration_page_{timestamp}.md",
        f"# Webinar Registration Page: {config['topic']}\n\n{reg_page}")
    print(f"   ✅ Saved: {reg_file}")
    
    # Step 2: Thank You Page
    ty_page = generate_thank_you_page(client, config)
    ty_file = save_output(output_dir, f"02_thank_you_page_{timestamp}.md",
        f"# Webinar Thank You Page: {config['topic']}\n\n{ty_page}")
    print(f"   ✅ Saved: {ty_file}")
    
    # Step 3: Webinar Script
    script = generate_webinar_script(client, config)
    script_file = save_output(output_dir, f"03_webinar_script_{timestamp}.md",
        f"# Webinar Script: {config['topic']}\n\n{script}")
    print(f"   ✅ Saved: {script_file}")
    
    # Step 4: Slide Outline
    slides = generate_slide_outline(client, config, script)
    slides_file = save_output(output_dir, f"04_slide_outline_{timestamp}.md",
        f"# Webinar Slide Outline: {config['topic']}\n\n{slides}")
    print(f"   ✅ Saved: {slides_file}")
    
    # Step 5: Pre-Webinar Emails
    pre_emails = generate_pre_webinar_emails(client, config)
    pre_file = save_output(output_dir, f"05_pre_webinar_emails_{timestamp}.md",
        f"# Pre-Webinar Email Sequence: {config['topic']}\n\n{pre_emails}")
    print(f"   ✅ Saved: {pre_file}")
    
    # Step 6: Post-Webinar Emails
    post_emails = generate_post_webinar_emails(client, config)
    post_file = save_output(output_dir, f"06_post_webinar_emails_{timestamp}.md",
        f"# Post-Webinar Email Sequence: {config['topic']}\n\n{post_emails}")
    print(f"   ✅ Saved: {post_file}")
    
    # Summary
    print(f"\n✅ Webinar funnel generation complete!")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   📄 Files generated: 6")
    print(f"\n   Files:")
    for f in sorted(output_dir.glob(f"*{timestamp}.md")):
        print(f"      - {f.name}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
