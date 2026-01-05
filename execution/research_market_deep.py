#!/usr/bin/env python3
"""
Deep Market Research Agent - Uses Perplexity Deep Research via OpenRouter for comprehensive market analysis.
Outputs structured research that can feed into funnel, copy, and strategy workflows.

Usage:
    python3 execution/research_market_deep.py \
        --business "Agency Accelerator" \
        --industry "Marketing Agency" \
        --audience "Agency owners doing 10-50k/month" \
        --output .tmp/market_research.json

    # Then feed to funnel workflow:
    python3 execution/generate_funnel_copy.py --research_file .tmp/market_research.json ...
"""

import argparse
import json
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


def get_perplexity_client() -> OpenAI:
    """Get OpenRouter client configured for Perplexity models."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY required in .env")
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")


def deep_research(client: OpenAI, query: str, context: str = "") -> str:
    """Run deep research using Perplexity via OpenRouter."""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="perplexity/sonar-deep-research",
                messages=[
                    {"role": "system", "content": "You are a market research analyst. Provide comprehensive, data-driven research with specific numbers, sources, and actionable insights."},
                    {"role": "user", "content": f"{context}\n\n{query}" if context else query}
                ],
                temperature=0.3,
                max_tokens=8000
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                print(f"   Error: {e}")
                return ""
            print(f"   Retry {attempt + 1}/3...")
    return ""


def research_market(client: OpenAI, config: dict) -> dict:
    """Conduct comprehensive market research."""
    results = {}
    
    business = config["business"]
    industry = config["industry"]
    audience = config["audience"]
    
    # 1. Market Overview
    print("📊 Researching market overview...")
    results["market_overview"] = deep_research(client, f"""
Research the {industry} market for a business called "{business}":

1. Total addressable market (TAM) size and growth rate
2. Key market segments and their sizes
3. Market trends for 2024-2025
4. Regulatory or economic factors affecting the market
5. Technology disruptions impacting the industry

Provide specific numbers, percentages, and cite sources where possible.
""")

    # 2. Target Audience Deep Dive
    print("👥 Researching target audience...")
    results["audience_research"] = deep_research(client, f"""
Deep research on this target audience: {audience}

Research and provide:
1. Demographics (age, income, location, company size)
2. Psychographics (values, motivations, fears)
3. Online behavior (platforms, content consumption, communities)
4. Buying behavior (decision process, budget cycles, stakeholders)
5. Common pain points and frustrations (with specific examples)
6. Goals and aspirations
7. Where they seek information and advice
8. Influencers and thought leaders they follow

Use real data and surveys where available.
""")

    # 3. Competitor Analysis
    print("🔍 Researching competitors...")
    results["competitor_analysis"] = deep_research(client, f"""
Competitive analysis for {industry} targeting {audience}:

1. Top 5-10 direct competitors (names, websites, positioning)
2. Their pricing models and price points
3. Their marketing strategies and channels
4. Their strengths and weaknesses
5. Customer reviews and sentiment (what people love/hate)
6. Market gaps and underserved segments
7. Emerging competitors to watch

Focus on competitors serving: {audience}
""")

    # 4. Voice of Customer
    print("💬 Researching voice of customer...")
    results["voice_of_customer"] = deep_research(client, f"""
Voice of Customer research for {audience} in {industry}:

Find actual language, phrases, and quotes from:
1. Reddit discussions (r/entrepreneur, r/agency, r/marketing, etc.)
2. Facebook groups and communities
3. Twitter/X conversations
4. Review sites and testimonials
5. Forum discussions
6. Podcast interviews with this audience

Provide:
- 10+ exact phrases they use to describe their problems
- 10+ exact phrases they use to describe desired outcomes
- Common objections to solutions like "{business}"
- Trigger events that prompt them to seek solutions
- Emotional language around their frustrations
""")

    # 5. Content & Messaging Research
    print("📝 Researching content landscape...")
    results["content_research"] = deep_research(client, f"""
Content and messaging research for {industry} targeting {audience}:

1. Top performing content topics in this space
2. Most shared articles/videos in the last 12 months
3. Headline formulas that resonate with this audience
4. Hooks and angles that drive engagement
5. Content gaps (topics not well covered)
6. Best performing ad copy examples
7. Email subject lines with high open rates

What messaging resonates most with {audience}?
""")

    # 6. Pricing & Offer Research
    print("💰 Researching pricing and offers...")
    results["pricing_research"] = deep_research(client, f"""
Pricing and offer research for {industry} serving {audience}:

1. Price ranges for similar solutions ($X - $Y)
2. Common pricing models (subscription, one-time, retainer)
3. What's included at different price points
4. Bonus structures that convert well
5. Guarantee types commonly offered
6. Payment plan options
7. Price sensitivity of this audience
8. ROI expectations and benchmarks
""")

    return results


def synthesize_research(client: OpenAI, research: dict, config: dict) -> dict:
    """Synthesize all research into actionable insights."""
    print("🧠 Synthesizing research into actionable insights...")
    
    # Combine all research
    all_research = "\n\n---\n\n".join([
        f"## {k.replace('_', ' ').title()}\n\n{v}" 
        for k, v in research.items() if v
    ])
    
    # Use Claude for synthesis (better reasoning)
    synthesis_client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    
    synthesis = synthesis_client.chat.completions.create(
        model="anthropic/claude-sonnet-4",
        messages=[
            {"role": "system", "content": "You synthesize market research into actionable marketing and sales insights."},
            {"role": "user", "content": f"""
Synthesize this market research for {config['business']} targeting {config['audience']}:

{all_research[:15000]}

Provide a structured synthesis:

## EXECUTIVE SUMMARY
- 3-5 key insights
- Biggest opportunity
- Primary risk/challenge

## IDEAL CUSTOMER PROFILE
- Demographics
- Psychographics
- Buying triggers
- Decision criteria

## POSITIONING RECOMMENDATION
- Unique angle to take
- Key differentiators
- Positioning statement

## MESSAGING FRAMEWORK
- Primary hook
- Supporting messages
- Proof points needed
- Objections to address

## FUNNEL RECOMMENDATIONS
- Best funnel type for this audience
- Key conversion points
- Traffic sources to prioritize

## CONTENT THEMES
- Top 5 content topics
- Hooks that will resonate
- Stories to tell

## PRICING GUIDANCE
- Recommended price range
- Offer structure
- Guarantee recommendation

## VOICE OF CUSTOMER SNIPPETS
- 10 phrases to use in copy
- Pain point language
- Desire language
"""}
        ],
        temperature=0.5,
        max_tokens=4000
    ).choices[0].message.content
    
    return {
        "synthesis": synthesis,
        "raw_research": research
    }


def save_output(output_path: Path, data: dict, format: str = "both"):
    """Save research output."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save JSON for programmatic use
    json_path = output_path.with_suffix(".json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"   ✅ JSON: {json_path}")
    
    # Save Markdown for reading
    md_path = output_path.with_suffix(".md")
    md_content = f"""# Market Research: {data['config']['business']}

**Industry:** {data['config']['industry']}
**Target Audience:** {data['config']['audience']}
**Generated:** {data['generated_at']}
**Research Model:** Perplexity Deep Research

---

{data['synthesis']['synthesis']}

---

# RAW RESEARCH DATA

"""
    for section, content in data['synthesis']['raw_research'].items():
        md_content += f"\n## {section.replace('_', ' ').title()}\n\n{content}\n\n---\n"
    
    md_path.write_text(md_content, encoding="utf-8")
    print(f"   ✅ Markdown: {md_path}")


def main():
    parser = argparse.ArgumentParser(description="Deep market research using Perplexity")
    parser.add_argument("--business", "-b", required=True, help="Business/product name")
    parser.add_argument("--industry", "-i", required=True, help="Industry/market")
    parser.add_argument("--audience", "-a", required=True, help="Target audience description")
    parser.add_argument("--competitors", "-c", default="", help="Known competitors (comma-separated)")
    parser.add_argument("--output", "-o", default=".tmp/market_research", help="Output path (without extension)")
    parser.add_argument("--quick", "-q", action="store_true", help="Quick mode (fewer research queries)")
    
    args = parser.parse_args()
    
    config = {
        "business": args.business,
        "industry": args.industry,
        "audience": args.audience,
        "competitors": args.competitors
    }
    
    print(f"\n🔬 Deep Market Research Agent")
    print(f"   Business: {config['business']}")
    print(f"   Industry: {config['industry']}")
    print(f"   Audience: {config['audience']}")
    print(f"   Model: Perplexity Deep Research via OpenRouter\n")
    
    client = get_perplexity_client()
    
    # Conduct research
    research = research_market(client, config)
    
    # Synthesize findings
    synthesis = synthesize_research(client, research, config)
    
    # Prepare output
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "config": config,
        "synthesis": synthesis
    }
    
    # Save
    print("\n💾 Saving research...")
    save_output(Path(args.output), output_data)
    
    print(f"\n✅ Market research complete!")
    print(f"   Use with other workflows:")
    print(f"   python3 execution/generate_funnel_copy.py --research_file {args.output}.json ...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
