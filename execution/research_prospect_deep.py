#!/usr/bin/env python3
"""
AI Prospect Research Agent - Generate comprehensive dossiers on prospects and companies.

Usage:
    python3 execution/research_prospect_deep.py \
        --name "John Smith" \
        --company "Acme Corp" \
        --domain "acmecorp.com" \
        --output .tmp/dossier.json
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

try:
    import requests
except ImportError:
    print("Error: requests package not installed. Run: pip install requests")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()


def get_client() -> OpenAI:
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    elif os.getenv("OPENAI_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY required")
        sys.exit(1)


def get_model() -> str:
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def call_llm(client: OpenAI, system_prompt: str, user_prompt: str, temperature: float = 0.5) -> str:
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


def search_perplexity(query: str) -> str:
    """Search using Perplexity API if available."""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return ""
    
    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [{"role": "user", "content": query}]
            },
            timeout=30
        )
        if response.ok:
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  Perplexity search failed: {e}")
    return ""


def research_company(client: OpenAI, company: str, domain: str) -> str:
    """Research company using AI."""
    print(f"  🏢 Researching company: {company}")
    
    # Try Perplexity for real-time data
    perplexity_data = search_perplexity(f"Tell me about {company} ({domain}) - recent news, funding, employees, products")
    
    system_prompt = """You are a business intelligence researcher. Create comprehensive company profiles based on available information."""
    
    user_prompt = f"""Research and compile information about this company:

COMPANY: {company}
DOMAIN: {domain}

PERPLEXITY SEARCH RESULTS:
{perplexity_data if perplexity_data else "No real-time search available - use your knowledge"}

COMPILE:

## Company Overview
- Industry and business model
- Founded/headquarters
- Employee count estimate
- Products/services

## Recent Developments
- Recent news or announcements
- Funding history
- Key milestones

## Tech Stack (inferred)
- Likely tools they use
- Based on industry and size

## Market Position
- Key competitors
- Market positioning
- Strengths/weaknesses

## Hiring Signals
- Any known open positions
- Growth indicators

Be specific where possible, clearly label assumptions."""

    return call_llm(client, system_prompt, user_prompt)


def research_person(client: OpenAI, name: str, company: str, linkedin_url: str = "") -> str:
    """Research individual prospect."""
    print(f"  👤 Researching person: {name}")
    
    perplexity_data = search_perplexity(f"{name} {company} LinkedIn background career")
    
    system_prompt = """You are a sales intelligence researcher. Create prospect profiles for sales call preparation."""
    
    user_prompt = f"""Research this prospect:

NAME: {name}
COMPANY: {company}
LINKEDIN: {linkedin_url or "Not provided"}

PERPLEXITY RESULTS:
{perplexity_data if perplexity_data else "No real-time search available"}

COMPILE:

## Person Overview
- Current title (if known)
- Tenure at company
- Career history (inferred)
- Professional background

## Communication Style (inferred)
- Based on role and industry
- Likely priorities

## Potential Pain Points
- Based on role
- Common challenges for this position

## Talking Points
- Conversation starters
- Relevant topics
- Things to avoid

Be specific where possible, clearly label inferences."""

    return call_llm(client, system_prompt, user_prompt)


def synthesize_dossier(client: OpenAI, name: str, company: str, company_research: str, person_research: str) -> dict:
    """Synthesize all research into final dossier."""
    print(f"  📋 Synthesizing dossier...")
    
    system_prompt = """You are a sales strategist. Synthesize research into actionable sales intelligence."""
    
    user_prompt = f"""Create a sales dossier from this research:

PROSPECT: {name}
COMPANY: {company}

COMPANY RESEARCH:
{company_research}

PERSON RESEARCH:
{person_research}

OUTPUT AS JSON:
{{
  "prospect": {{
    "name": "",
    "title": "",
    "company": "",
    "linkedin_url": ""
  }},
  "company": {{
    "name": "",
    "industry": "",
    "size": "",
    "funding": "",
    "location": ""
  }},
  "intelligence": {{
    "recent_news": [""],
    "hiring_signals": [""],
    "tech_stack": [""],
    "pain_points": [""],
    "opportunities": [""]
  }},
  "sales_strategy": {{
    "talking_points": [""],
    "questions_to_ask": [""],
    "objections_to_prepare": [""],
    "value_props_to_lead_with": [""]
  }},
  "priority_score": 0-100,
  "recommended_approach": ""
}}

Return ONLY valid JSON."""

    response = call_llm(client, system_prompt, user_prompt, temperature=0.3)
    
    # Parse JSON
    try:
        if response.startswith("```"):
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        return json.loads(response)
    except:
        return {
            "prospect": {"name": name, "company": company},
            "raw_research": {"company": company_research, "person": person_research}
        }


def format_markdown(dossier: dict) -> str:
    """Format dossier as markdown."""
    p = dossier.get("prospect", {})
    c = dossier.get("company", {})
    i = dossier.get("intelligence", {})
    s = dossier.get("sales_strategy", {})
    
    return f"""# Prospect Dossier: {p.get('name', 'Unknown')}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Prospect Overview
- **Name:** {p.get('name', 'Unknown')}
- **Title:** {p.get('title', 'Unknown')}
- **Company:** {p.get('company', 'Unknown')}
- **LinkedIn:** {p.get('linkedin_url', 'Not provided')}

## Company Overview
- **Company:** {c.get('name', 'Unknown')}
- **Industry:** {c.get('industry', 'Unknown')}
- **Size:** {c.get('size', 'Unknown')}
- **Funding:** {c.get('funding', 'Unknown')}
- **Location:** {c.get('location', 'Unknown')}

## Intelligence

### Recent News
{chr(10).join(['- ' + n for n in i.get('recent_news', ['None found'])])}

### Hiring Signals
{chr(10).join(['- ' + h for h in i.get('hiring_signals', ['None detected'])])}

### Tech Stack
{chr(10).join(['- ' + t for t in i.get('tech_stack', ['Unknown'])])}

### Pain Points
{chr(10).join(['- ' + pp for pp in i.get('pain_points', ['Unknown'])])}

### Opportunities
{chr(10).join(['- ' + o for o in i.get('opportunities', ['Unknown'])])}

## Sales Strategy

### Talking Points
{chr(10).join(['- ' + tp for tp in s.get('talking_points', [])])}

### Questions to Ask
{chr(10).join(['- ' + q for q in s.get('questions_to_ask', [])])}

### Objections to Prepare For
{chr(10).join(['- ' + obj for obj in s.get('objections_to_prepare', [])])}

### Value Props to Lead With
{chr(10).join(['- ' + vp for vp in s.get('value_props_to_lead_with', [])])}

---

**Priority Score:** {dossier.get('priority_score', 'N/A')}/100

**Recommended Approach:** {dossier.get('recommended_approach', 'Standard outreach')}
"""


def main():
    parser = argparse.ArgumentParser(description="Research prospects and generate dossiers")
    parser.add_argument("--name", "-n", help="Prospect name")
    parser.add_argument("--company", "-c", help="Company name")
    parser.add_argument("--domain", "-d", default="", help="Company domain")
    parser.add_argument("--linkedin", "-l", default="", help="LinkedIn URL")
    parser.add_argument("--input", "-i", help="Input JSON/CSV file for batch processing")
    parser.add_argument("--output", "-o", default=".tmp/dossier.json", help="Output file or directory")
    parser.add_argument("--format", "-f", default="both", choices=["json", "markdown", "both"], help="Output format")
    
    args = parser.parse_args()
    
    if not args.name and not args.input:
        parser.error("Either --name or --input is required")
    
    client = get_client()
    
    # Single prospect
    if args.name:
        print(f"\n🔍 Prospect Research Agent")
        print(f"   Prospect: {args.name}")
        print(f"   Company: {args.company or 'Unknown'}\n")
        
        company_research = research_company(client, args.company or "Unknown", args.domain)
        person_research = research_person(client, args.name, args.company or "Unknown", args.linkedin)
        dossier = synthesize_dossier(client, args.name, args.company or "Unknown", company_research, person_research)
        
        # Save output
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if args.format in ["json", "both"]:
            json_path = output_path.with_suffix(".json")
            with open(json_path, "w") as f:
                json.dump(dossier, f, indent=2)
            print(f"\n   ✅ JSON: {json_path}")
        
        if args.format in ["markdown", "both"]:
            md_path = output_path.with_suffix(".md")
            with open(md_path, "w") as f:
                f.write(format_markdown(dossier))
            print(f"   ✅ Markdown: {md_path}")
        
        print(f"\n✅ Dossier complete!")
        return 0
    
    # Batch processing
    if args.input:
        print(f"\n🔍 Batch Prospect Research")
        print(f"   Input: {args.input}\n")
        
        # Load prospects
        input_path = Path(args.input)
        if input_path.suffix == ".json":
            with open(input_path) as f:
                prospects = json.load(f)
                if isinstance(prospects, dict):
                    prospects = prospects.get("data", prospects.get("leads", [prospects]))
        elif input_path.suffix == ".csv":
            import csv
            with open(input_path) as f:
                prospects = list(csv.DictReader(f))
        else:
            print(f"Unsupported format: {input_path.suffix}")
            return 1
        
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, prospect in enumerate(prospects, 1):
            name = prospect.get("name") or prospect.get("first_name", "") + " " + prospect.get("last_name", "")
            company = prospect.get("company") or prospect.get("company_name", "Unknown")
            domain = prospect.get("domain") or prospect.get("website", "")
            
            print(f"\n[{i}/{len(prospects)}] {name} @ {company}")
            
            company_research = research_company(client, company, domain)
            person_research = research_person(client, name, company)
            dossier = synthesize_dossier(client, name, company, company_research, person_research)
            
            # Save
            safe_name = "".join(c if c.isalnum() else "_" for c in name)
            json_path = output_dir / f"{safe_name}.json"
            with open(json_path, "w") as f:
                json.dump(dossier, f, indent=2)
            
            md_path = output_dir / f"{safe_name}.md"
            with open(md_path, "w") as f:
                f.write(format_markdown(dossier))
        
        print(f"\n✅ Batch complete! {len(prospects)} dossiers in {output_dir}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
