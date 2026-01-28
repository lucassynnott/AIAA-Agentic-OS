#!/usr/bin/env python3
"""
Funnel Copywriter - Generate complete funnel copy (sales page, emails, ads)
Uses AI market research and proven copywriting frameworks.

Usage:
    python3 execution/generate_funnel_copy.py \
        --business "Company Name" \
        --industry "SaaS" \
        --audience "B2B founders" \
        --funnel_type "VSL" \
        --benefits "benefit1,benefit2,benefit3" \
        --pain_points "pain1,pain2,pain3" \
        --value_prop "Unique value proposition" \
        --output_dir ".tmp/funnel_output"

    # With pre-researched market data:
    python3 execution/generate_funnel_copy.py \
        --research_file .tmp/market_research.json \
        --funnel_type "VSL" \
        --output_dir ".tmp/funnel_output"
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
        return "anthropic/claude-opus-4"
    return "gpt-4o"


def load_landing_page_skill_bible() -> str:
    """Load landing page skill bible for enhanced funnel copy generation."""
    skill_path = Path(__file__).parent.parent / "skills" / "SKILL_BIBLE_landing_page_ai_mastery.md"
    if skill_path.exists():
        content = skill_path.read_text(encoding="utf-8")
        # Extract key sections for context
        sections = []
        for section in ["## Core Principles", "## Best Practices"]:
            if section in content:
                start = content.find(section)
                next_section = content.find("\n## ", start + len(section))
                if next_section > start:
                    sections.append(content[start:next_section])
                else:
                    sections.append(content[start:start + 1500])
        return "\n".join(sections)[:3000]
    return ""


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


def generate_market_research(client: OpenAI, config: dict) -> str:
    """Generate market research dossier."""
    print("📊 Generating market research...")
    
    system_prompt = """You are an expert audience researcher and market analyst. Create a copywriter-ready market research dossier."""
    
    user_prompt = f"""Analyze this business and create a comprehensive market research dossier:

BUSINESS PROFILE:
- Business/Product Name: {config['business']}
- Industry: {config['industry']}
- Target Audience: {config['audience']}
- Top Benefits: {config['benefits']}
- Pain Points Solved: {config['pain_points']}
- Unique Value Proposition: {config['value_prop']}
- Funnel Type: {config['funnel_type']}

DELIVERABLES:
1. Executive Summary (5-7 key strategic moves)
2. Business Snapshot (facts vs assumptions)
3. Audience Personas (2-3) with:
   - Jobs-to-be-done
   - Pains and gains
   - Purchase triggers
   - Decision criteria
   - Common objections
   - Voice-of-customer phrases (10+)
4. Competitive Landscape Analysis
5. Demand & Intent Signals
6. Positioning Recommendations

Be specific and actionable. Use real market insights where possible."""

    return call_llm(client, system_prompt, user_prompt)


def generate_funnel_strategy(client: OpenAI, config: dict, research: str) -> str:
    """Generate funnel strategy blueprint."""
    print("🎯 Creating funnel strategy...")
    
    system_prompt = """You are an expert funnel strategist who has built million-dollar funnels. Create a comprehensive funnel strategy blueprint."""
    
    user_prompt = f"""Create a funnel strategy for this business:

BUSINESS INTELLIGENCE:
- Business Name: {config['business']}
- Industry: {config['industry']}
- Target Audience: {config['audience']}
- Funnel Type: {config['funnel_type']}
- Benefits: {config['benefits']}
- Pain Points: {config['pain_points']}
- Value Proposition: {config['value_prop']}
- Brand Voice: {config.get('brand_voice', 'Professional but conversational')}
- Special Offers: {config.get('offers', 'None specified')}

MARKET RESEARCH:
{research}

DELIVER A COMPREHENSIVE FUNNEL STRATEGY INCLUDING:

## 1. STRATEGIC FOUNDATION
- Power of One Analysis (One problem, one desire, one method, one promise)
- Primary conversion mechanism
- Traffic temperature strategy

## 2. FUNNEL ARCHITECTURE
- Page flow and sequence
- Entry points and exit points
- Upsell/downsell structure

## 3. MESSAGING FRAMEWORK
- Big idea/hook
- Unique mechanism
- Proof elements needed
- Risk reversal strategy

## 4. CONVERSION TRIGGERS
- Urgency elements
- Scarcity tactics
- Social proof requirements
- Trust builders

## 5. EMAIL STRATEGY
- Sequence structure
- Key email themes
- Timing recommendations

Be specific with copy angles, not generic advice."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.6)


def generate_sales_page(client: OpenAI, config: dict, research: str, strategy: str) -> str:
    """Generate complete sales page copy."""
    print("📝 Writing sales page copy...")

    # Load skill bible for enhanced context
    skill_context = load_landing_page_skill_bible()

    skill_section = ""
    if skill_context:
        skill_section = f"""

APPLY THESE LANDING PAGE BEST PRACTICES:
{skill_context[:2000]}
"""

    system_prompt = f"""You are a world-class direct response copywriter who has written millions in sales. Write high-converting sales page copy.
{skill_section}"""
    
    user_prompt = f"""Write a complete high-converting sales page for this business:

BUSINESS INTELLIGENCE:
- Business Name: {config['business']}
- Industry: {config['industry']}
- Target Audience: {config['audience']}
- Funnel Type: {config['funnel_type']}
- Benefits: {config['benefits']}
- Pain Points: {config['pain_points']}
- Value Proposition: {config['value_prop']}
- Brand Voice: {config.get('brand_voice', 'Professional but conversational')}
- Special Offers: {config.get('offers', 'None specified')}

MARKET RESEARCH:
{research[:2000]}

FUNNEL STRATEGY:
{strategy[:2000]}

WRITE A COMPLETE SALES PAGE INCLUDING:

## HEADLINE OPTIONS (3 variations)
- Pattern interrupt headlines
- Curiosity-driven headlines
- Benefit-focused headlines

## OPENING SECTION
- Hook that calls out the reader
- Problem agitation
- Empathy builder

## PROBLEM SECTION
- Deep pain point exploration
- Future pacing the problem
- "If nothing changes" scenario

## SOLUTION INTRODUCTION
- Unique mechanism reveal
- Why this is different
- Big promise

## BENEFITS SECTION
- Feature-to-benefit transformations
- Outcome-focused bullets
- Emotional benefits

## PROOF SECTION
- Credibility builders
- Results framework
- Social proof placeholders

## OFFER SECTION
- Value stack
- Bonus breakdown
- Price anchoring

## OBJECTION HANDLING
- Top 5 objections addressed
- Risk reversal/guarantee

## CTA SECTION
- Primary CTA copy
- Urgency elements
- Final push

Write complete copy, not outlines. Use conversational, punchy language."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_email_sequence(client: OpenAI, config: dict, research: str, strategy: str) -> str:
    """Generate email sequence."""
    print("📧 Creating email sequence...")
    
    system_prompt = """You are an email marketing expert who writes high-converting sequences. Write complete emails, not outlines."""
    
    user_prompt = f"""Create a complete email sequence for this funnel:

BUSINESS INTELLIGENCE:
- Business Name: {config['business']}
- Industry: {config['industry']}
- Target Audience: {config['audience']}
- Funnel Type: {config['funnel_type']}
- Benefits: {config['benefits']}
- Pain Points: {config['pain_points']}
- Value Proposition: {config['value_prop']}

FUNNEL STRATEGY CONTEXT:
{strategy[:1500]}

CREATE A 7-EMAIL SEQUENCE:

EMAIL 1: Welcome + Quick Win
- Subject line options (3)
- Preview text
- Complete email body
- CTA

EMAIL 2: Problem Agitation
- Subject line options (3)
- Complete email body highlighting main pain point
- Story or example

EMAIL 3: Solution Introduction
- Subject line options (3)
- Introduce the solution/mechanism
- Create curiosity

EMAIL 4: Social Proof
- Subject line options (3)
- Case study or testimonial focus
- Results-driven

EMAIL 5: Objection Crusher
- Subject line options (3)
- Address top objection
- Reframe the concern

EMAIL 6: Urgency/Scarcity
- Subject line options (3)
- Create legitimate urgency
- Deadline or limited availability

EMAIL 7: Last Chance
- Subject line options (3)
- Final push
- What they'll miss

Write complete emails (150-300 words each), not summaries. Make them conversational and value-packed."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def save_output(output_dir: Path, filename: str, content: str) -> str:
    """Save content to file."""
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def load_research_file(filepath: str) -> dict:
    """Load pre-generated market research from JSON file."""
    with open(filepath) as f:
        data = json.load(f)
    return data


def main():
    parser = argparse.ArgumentParser(description="Generate complete funnel copy")
    parser.add_argument("--business", default="", help="Business/product name")
    parser.add_argument("--industry", default="", help="Industry/business type")
    parser.add_argument("--audience", default="", help="Target audience description")
    parser.add_argument("--funnel_type", default="Sales Page", help="Type of funnel (VSL, Webinar, Sales Page)")
    parser.add_argument("--benefits", default="", help="Comma-separated benefits")
    parser.add_argument("--pain_points", default="", help="Comma-separated pain points")
    parser.add_argument("--value_prop", default="", help="Unique value proposition")
    parser.add_argument("--brand_voice", default="Professional but conversational", help="Brand voice/tone")
    parser.add_argument("--offers", default="", help="Special offers or urgency elements")
    parser.add_argument("--output_dir", default=".tmp/funnel_output", help="Output directory")
    parser.add_argument("--skip_research", action="store_true", help="Skip market research step")
    parser.add_argument("--research_file", default="", help="Pre-generated market research JSON file")
    
    args = parser.parse_args()
    
    # Load from research file if provided
    pre_research = None
    if args.research_file and Path(args.research_file).exists():
        print(f"📂 Loading pre-generated research from: {args.research_file}")
        research_data = load_research_file(args.research_file)
        config_from_research = research_data.get("config", {})
        pre_research = research_data.get("synthesis", {}).get("synthesis", "")
        
        # Use research file config as defaults
        args.business = args.business or config_from_research.get("business", "")
        args.industry = args.industry or config_from_research.get("industry", "")
        args.audience = args.audience or config_from_research.get("audience", "")
    
    if not args.business or not args.industry:
        parser.error("--business and --industry are required (or provide --research_file)")
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build config
    config = {
        "business": args.business,
        "industry": args.industry,
        "audience": args.audience or f"{args.industry} professionals",
        "funnel_type": args.funnel_type,
        "benefits": args.benefits or "Not specified",
        "pain_points": args.pain_points or "Not specified",
        "value_prop": args.value_prop or "Not specified",
        "brand_voice": args.brand_voice,
        "offers": args.offers
    }
    
    print(f"\n🚀 Funnel Copywriter")
    print(f"   Business: {config['business']}")
    print(f"   Industry: {config['industry']}")
    print(f"   Funnel Type: {config['funnel_type']}")
    print(f"   Output: {output_dir}\n")
    
    client = get_client()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Step 1: Market Research
    if pre_research:
        research = pre_research
        print("   ✅ Using pre-generated market research")
    elif not args.skip_research:
        research = generate_market_research(client, config)
        research_file = save_output(output_dir, f"01_market_research_{timestamp}.md", 
            f"# Market Research: {config['business']}\n\n{research}")
        print(f"   ✅ Saved: {research_file}")
    else:
        research = "Market research skipped."
        print("   ⏭️  Skipped market research")
    
    # Step 2: Funnel Strategy
    strategy = generate_funnel_strategy(client, config, research)
    strategy_file = save_output(output_dir, f"02_funnel_strategy_{timestamp}.md",
        f"# Funnel Strategy: {config['business']}\n\n{strategy}")
    print(f"   ✅ Saved: {strategy_file}")
    
    # Step 3: Sales Page Copy
    sales_page = generate_sales_page(client, config, research, strategy)
    sales_file = save_output(output_dir, f"03_sales_page_{timestamp}.md",
        f"# Sales Page Copy: {config['business']}\n\n{sales_page}")
    print(f"   ✅ Saved: {sales_file}")
    
    # Step 4: Email Sequence
    emails = generate_email_sequence(client, config, research, strategy)
    email_file = save_output(output_dir, f"04_email_sequence_{timestamp}.md",
        f"# Email Sequence: {config['business']}\n\n{emails}")
    print(f"   ✅ Saved: {email_file}")
    
    # Summary
    print(f"\n✅ Funnel copy generation complete!")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   📄 Files generated: 4")
    print(f"\n   Files:")
    for f in sorted(output_dir.glob(f"*{timestamp}.md")):
        print(f"      - {f.name}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
