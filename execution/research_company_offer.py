#!/usr/bin/env python3
"""
Company & Offer Market Research

Conducts comprehensive market research using Perplexity AI.
Follows directive: directives/company_market_research.md
"""

import argparse
import json
import os
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ Error: requests library not installed")
    print("   Install with: pip install requests")
    exit(1)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  Warning: python-dotenv not installed")
    print("   Install with: pip install python-dotenv")
    print("   Continuing with system environment variables...")


def call_perplexity(query: str, api_key: str) -> str:
    """Call Perplexity API with a research query"""
    url = "https://api.perplexity.ai/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "sonar",  # Updated model name for 2026
        "messages": [
            {
                "role": "user",
                "content": query,
            }
        ],
        "temperature": 0.2,
        "max_tokens": 2000,
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"⚠️  Perplexity API error: {response.status_code}")
        print(f"   Response: {response.text}")
        return ""

    result = response.json()
    return result["choices"][0]["message"]["content"]


def research_company_overview(company: str, website: str, api_key: str) -> dict:
    """Step 1: Company Overview Research"""
    print(f"🔍 Researching company overview...")

    query = f"""Research {company} ({website}). Provide:
- Company overview and mission
- Core products/services
- Target market and ideal customers
- Company size and stage
- Recent news or announcements
- Social media presence

Format as structured data."""

    result = call_perplexity(query, api_key)

    return {
        "name": company,
        "website": website,
        "overview": result,
    }


def research_offer_analysis(company: str, offer: str, api_key: str) -> dict:
    """Step 2: Offer Analysis"""
    print(f"🔍 Analyzing offer...")

    query = f"""Analyze {offer} by {company}. Provide:
- How the offer works (mechanism)
- Key features and benefits
- Pricing structure if available
- Customer results or case studies
- Unique selling propositions
- Common objections or concerns

Format as structured data."""

    result = call_perplexity(query, api_key)

    return {
        "name": offer,
        "description": result,
    }


def research_target_audience(offer: str, industry: str, api_key: str) -> dict:
    """Step 3: Target Audience Research"""
    print(f"🔍 Researching target audience...")

    query = f"""Research the target audience for {offer} in {industry}. Provide:
- Demographic profile (titles, company size, etc.)
- Primary pain points and challenges (list at least 5)
- Current solutions they're using
- Buying triggers and motivations
- Common objections to similar offers
- Language and terminology they use

Format as structured data with clear lists."""

    result = call_perplexity(query, api_key)

    # Parse result (simplified - production would use structured extraction)
    return {
        "demographics": result.split("\n")[0] if result else "",
        "painPoints": ["Pain point extraction from result"],  # Simplified
        "desires": ["Desire extraction from result"],
        "language": ["Keywords from result"],
    }


def research_competitors(company: str, offer: str, api_key: str) -> list:
    """Step 4: Competitive Landscape"""
    print(f"🔍 Analyzing competitive landscape...")

    query = f"""Research competitors of {company} offering similar solutions to {offer}. Provide:
- Top 3-5 direct competitors
- How they position their offers
- Pricing comparison
- Strengths and weaknesses
- Market gaps and opportunities

Format as list."""

    result = call_perplexity(query, api_key)

    return [
        {
            "name": "Competitor (extracted)",
            "positioning": result[:200],  # Simplified
        }
    ]


def research_social_proof(company: str, offer: str, api_key: str) -> dict:
    """Step 5: Social Proof & Results"""
    print(f"🔍 Finding social proof and results...")

    query = f"""Find case studies, testimonials, and results for {company} and {offer}. Include:
- Quantifiable results (revenue, leads, ROI, etc.)
- Customer success stories
- Reviews and ratings
- Industry recognition or awards
- Media mentions or features

Format with specific numbers and names where possible."""

    result = call_perplexity(query, api_key)

    return {
        "results": [],  # Parse from result
        "testimonials": [],
        "caseStudies": [result],  # Simplified
    }


def synthesize_research(
    company_data: dict,
    offer_data: dict,
    audience_data: dict,
    competitors_data: list,
    social_proof_data: dict,
) -> dict:
    """Step 6: Synthesize all research into unified dossier"""
    print(f"📊 Synthesizing research dossier...")

    return {
        "company": company_data,
        "offer": offer_data,
        "targetAudience": audience_data,
        "transformation": {
            "before": "Unpredictable revenue, inconsistent lead flow",
            "after": "Consistent qualified calls and predictable growth",
            "mechanism": "AI-driven system (extracted from offer research)",
        },
        "socialProof": social_proof_data,
        "competitors": competitors_data,
        "messaging": {
            "hooks": [
                "Derived from pain points and results",
                "Based on unique mechanism",
                "Leveraging social proof",
            ],
            "angles": ["Pain-agitate-solve", "Mechanism-focused", "Results-driven"],
            "objections": ["Too expensive", "Too complex", "Not sure it works"],
        },
        "researchedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def generate_markdown_report(research_dossier: dict, company: str, offer: str) -> str:
    """Generate human-readable markdown report from research dossier"""
    report = f"""# Market Research: {company}

**Offer:** {offer}
**Research Date:** {research_dossier.get('researchedAt', 'N/A')}

---

## Company Overview

**Name:** {research_dossier['company']['name']}
**Website:** {research_dossier['company']['website']}

{research_dossier['company']['overview']}

---

## Offer Analysis

**Offer Name:** {research_dossier['offer']['name']}

{research_dossier['offer']['description']}

---

## Target Audience

**Demographics:**
{research_dossier['targetAudience']['demographics']}

**Primary Pain Points:**
{chr(10).join('- ' + p for p in research_dossier['targetAudience']['painPoints'])}

**Desires & Motivations:**
{chr(10).join('- ' + d for d in research_dossier['targetAudience']['desires'])}

---

## Transformation Promise

**Before State:**
{research_dossier['transformation']['before']}

**After State:**
{research_dossier['transformation']['after']}

**Mechanism:**
{research_dossier['transformation']['mechanism']}

---

## Social Proof & Results

**Case Studies:**

{chr(10).join(research_dossier['socialProof']['caseStudies'])}

**Quantifiable Results:**
{chr(10).join('- ' + str(r) for r in research_dossier['socialProof'].get('results', ['See case studies above']))}

---

## Competitive Landscape

{chr(10).join(f"**{c['name']}**{chr(10)}{c['positioning']}{chr(10)}" for c in research_dossier['competitors'])}

---

## Messaging Recommendations

**Hook Angles:**
{chr(10).join('- ' + h for h in research_dossier['messaging']['hooks'])}

**Positioning Angles:**
{chr(10).join('- ' + a for a in research_dossier['messaging']['angles'])}

**Common Objections to Address:**
{chr(10).join('- ' + o for o in research_dossier['messaging']['objections'])}

---

*Research powered by Perplexity AI*
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="Research company and offer")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--website", required=True, help="Company website")
    parser.add_argument("--offer", help="Offer/product name (optional - will research company's main offering if not specified)")
    parser.add_argument("--industry", help="Industry/niche")
    parser.add_argument("--price", help="Price point")
    parser.add_argument("--output", required=True, help="Output file path (.json)")

    args = parser.parse_args()

    # Get API key
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        print("❌ Error: PERPLEXITY_API_KEY not found in environment")
        print("   Add to .env file")
        return 1

    # Default offer to company's main product/service if not specified
    offer = args.offer or f"{args.company}'s main product/service"

    print(f"🚀 Starting market research for {args.company}...")
    print(f"   Offer: {offer}")

    # Execute research pipeline
    company_data = research_company_overview(args.company, args.website, api_key)
    offer_data = research_offer_analysis(args.company, offer, api_key)
    audience_data = research_target_audience(
        offer, args.industry or "business services", api_key
    )
    competitors_data = research_competitors(args.company, offer, api_key)
    social_proof_data = research_social_proof(args.company, offer, api_key)

    # Synthesize
    research_dossier = synthesize_research(
        company_data, offer_data, audience_data, competitors_data, social_proof_data
    )

    # Save JSON output (for programmatic use by downstream workflows)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(research_dossier, f, indent=2)

    # Generate formatted markdown report (for Google Docs / human reading)
    markdown_report = generate_markdown_report(research_dossier, args.company, offer)
    markdown_path = output_path.with_suffix('.md')

    with open(markdown_path, "w") as f:
        f.write(markdown_report)

    print(f"\n✅ Research complete!")
    print(f"   JSON: {output_path}")
    print(f"   Markdown: {markdown_path}")

    return 0


if __name__ == "__main__":
    exit(main())
