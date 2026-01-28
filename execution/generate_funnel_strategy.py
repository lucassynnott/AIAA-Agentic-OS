#!/usr/bin/env python3
"""
Funnel Outline & Strategy Agent - Generate comprehensive funnel strategy blueprint
with architecture recommendations, page outlines, and implementation roadmap.

Usage:
    python3 execution/generate_funnel_strategy.py \
        --business "Company Name" \
        --business_type "info_product" \
        --industry "Marketing" \
        --audience "Agency owners" \
        --objective "lead_gen" \
        --price "$997" \
        --pain_points "pain1,pain2,pain3" \
        --differentiator "Unique approach" \
        --output_dir ".tmp/funnel_strategy"
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

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY required in .env")
    sys.exit(1)


def get_client() -> OpenAI:
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def call_llm(client: OpenAI, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=get_model(),
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=temperature,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                raise e
            print(f"  Retry {attempt + 1}/3: {e}")
    return ""


def generate_research(client: OpenAI, config: dict) -> str:
    """Research optimal funnel strategy."""
    print("🔍 Researching funnel strategy...")
    
    system_prompt = """You are a funnel strategist who has built 7-figure funnels. Analyze businesses and recommend optimal funnel architectures."""
    
    user_prompt = f"""Research and analyze the optimal funnel strategy for:

BUSINESS PROFILE:
- Business/Product Name: {config['business']}
- Business Type: {config['business_type']}
- Industry/Niche: {config['industry']}
- Target Audience: {config['audience']}
- Funnel Objective: {config['objective']}
- Offer Price: {config['price']}
- Business Stage: {config.get('stage', 'Growth')}
- Pain Points: {config['pain_points']}
- Differentiator: {config['differentiator']}
- Traffic Sources: {config.get('traffic_sources', 'Not specified')}
- Existing Assets: {config.get('existing_assets', 'Not specified')}
- Competitors: {config.get('competitors', 'Not specified')}
- Timeline: {config.get('timeline', 'Flexible')}
- Budget: {config.get('budget', 'Not specified')}

PROVIDE COMPREHENSIVE ANALYSIS:

## 1. FUNNEL ARCHITECTURE RECOMMENDATION
- Primary funnel type (VSL, Webinar, Challenge, Application, Book, SLO, Product Launch, etc.)
- Why this funnel type is optimal for this business
- Expected conversion benchmarks
- Risk factors and mitigations

## 2. TRAFFIC STRATEGY ALIGNMENT
- How each traffic source will feed into funnel
- Cold vs warm traffic handling
- Retargeting strategy

## 3. OFFER POSITIONING
- Main offer presentation strategy
- Price anchoring approach
- Upsell/downsell recommendations
- Guarantee positioning

## 4. COMPETITIVE DIFFERENTIATION
- How to stand out in the market
- Unique mechanism positioning
- Authority building elements

## 5. KEY SUCCESS FACTORS
- Critical elements for this specific funnel
- Potential bottlenecks
- Optimization priorities

Be specific and actionable, not generic."""

    return call_llm(client, system_prompt, user_prompt)


def generate_architecture(client: OpenAI, config: dict, research: str) -> str:
    """Generate funnel architecture and implementation roadmap."""
    print("📐 Building funnel architecture...")
    
    system_prompt = """You are a funnel architect. Create detailed funnel blueprints with page-by-page specifications."""
    
    user_prompt = f"""Based on this research, create a strategic funnel architecture:

BUSINESS PROFILE:
- Business: {config['business']}
- Business Type: {config['business_type']}
- Industry: {config['industry']}
- Audience: {config['audience']}
- Objective: {config['objective']}
- Price: {config['price']}
- Pain Points: {config['pain_points']}
- Differentiator: {config['differentiator']}

RESEARCH FINDINGS:
{research[:2500]}

CREATE DETAILED FUNNEL ARCHITECTURE:

## 1. FUNNEL FLOW DIAGRAM
- Page 1 → Page 2 → Page 3...
- Decision points and branches
- Exit points and retargeting triggers

## 2. PAGE-BY-PAGE SPECIFICATIONS

### PAGE 1: [Name]
- Purpose and goal
- Key elements required
- Copy angle/hook
- Primary CTA
- Success metrics

### PAGE 2: [Name]
(repeat for each page)

## 3. EMAIL SEQUENCES REQUIRED
- Sequence names and triggers
- Number of emails each
- Primary purpose of each sequence

## 4. AUTOMATION TRIGGERS
- When leads enter sequences
- Behavioral triggers
- Tag/segment management

## 5. TECH STACK RECOMMENDATIONS
- Landing page builder
- Email platform
- Payment processor
- Analytics tools

## 6. IMPLEMENTATION ROADMAP

### Week 1: Foundation
- Tasks to complete
- Dependencies

### Week 2: Core Build
- Tasks to complete

### Week 3: Copy & Content
- Tasks to complete

### Week 4: Testing & Launch
- Tasks to complete

## 7. KPI DASHBOARD
- Metrics to track
- Benchmark targets
- Warning indicators

Be specific with page names, copy angles, and exact specifications."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.6)


def save_output(output_dir: Path, filename: str, content: str) -> str:
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Generate funnel strategy blueprint")
    parser.add_argument("--business", required=True, help="Business/product name")
    parser.add_argument("--business_type", default="info_product", 
        choices=["info_product", "saas", "service", "ecommerce", "agency", "coaching"],
        help="Type of business")
    parser.add_argument("--industry", default="", help="Industry/niche")
    parser.add_argument("--audience", default="", help="Target audience description")
    parser.add_argument("--objective", default="lead_gen",
        choices=["lead_gen", "direct_sale", "application", "webinar", "challenge"],
        help="Primary funnel objective")
    parser.add_argument("--price", default="", help="Core offer price")
    parser.add_argument("--stage", default="Growth", help="Business stage")
    parser.add_argument("--pain_points", default="", help="Top customer pain points")
    parser.add_argument("--differentiator", default="", help="What makes you different")
    parser.add_argument("--traffic_sources", default="", help="Primary traffic sources")
    parser.add_argument("--existing_assets", default="", help="What you already have")
    parser.add_argument("--competitors", default="", help="Successful competitors")
    parser.add_argument("--timeline", default="4 weeks", help="Implementation timeline")
    parser.add_argument("--budget", default="", help="Implementation budget")
    parser.add_argument("--output_dir", default=".tmp/funnel_strategy", help="Output directory")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    config = {
        "business": args.business,
        "business_type": args.business_type,
        "industry": args.industry or "Not specified",
        "audience": args.audience or "Not specified",
        "objective": args.objective,
        "price": args.price or "Not specified",
        "stage": args.stage,
        "pain_points": args.pain_points or "Not specified",
        "differentiator": args.differentiator or "Not specified",
        "traffic_sources": args.traffic_sources,
        "existing_assets": args.existing_assets,
        "competitors": args.competitors,
        "timeline": args.timeline,
        "budget": args.budget
    }
    
    print(f"\n📋 Funnel Strategy Generator")
    print(f"   Business: {config['business']}")
    print(f"   Type: {config['business_type']}")
    print(f"   Objective: {config['objective']}")
    print(f"   Output: {output_dir}\n")
    
    client = get_client()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Step 1: Research
    research = generate_research(client, config)
    research_file = save_output(output_dir, f"01_funnel_research_{timestamp}.md",
        f"# Funnel Research: {config['business']}\n\n{research}")
    print(f"   ✅ Saved: {research_file}")
    
    # Step 2: Architecture
    architecture = generate_architecture(client, config, research)
    arch_file = save_output(output_dir, f"02_funnel_architecture_{timestamp}.md",
        f"# Funnel Architecture: {config['business']}\n\n{architecture}")
    print(f"   ✅ Saved: {arch_file}")
    
    # Step 3: Complete Strategy Document
    complete = f"""# Complete Funnel Strategy Blueprint
## {config['business']}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Business Overview
- **Business:** {config['business']}
- **Type:** {config['business_type']}
- **Industry:** {config['industry']}
- **Audience:** {config['audience']}
- **Objective:** {config['objective']}
- **Price Point:** {config['price']}

---

# Part 1: Strategic Research

{research}

---

# Part 2: Funnel Architecture

{architecture}
"""
    complete_file = save_output(output_dir, f"03_complete_strategy_{timestamp}.md", complete)
    print(f"   ✅ Saved: {complete_file}")
    
    print(f"\n✅ Funnel strategy complete!")
    print(f"   📁 Output: {output_dir}")
    print(f"   📄 Files: 3")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
