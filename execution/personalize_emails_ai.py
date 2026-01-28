#!/usr/bin/env python3
"""
AI Cold Email Personalizer - Generate hyper-personalized first lines and email openers.

Usage:
    python3 execution/personalize_emails_ai.py \
        --input leads.json \
        --service "B2B lead generation" \
        --value_prop "Book 30+ meetings per month" \
        --output personalized_leads.json
"""

import argparse
import csv
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
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o-mini"


def call_llm(client: OpenAI, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=get_model(),
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=temperature,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                raise e
    return ""


def search_perplexity(query: str) -> str:
    """Search using Perplexity API."""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return ""
    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-sonar-small-128k-online", "messages": [{"role": "user", "content": query}]},
            timeout=30
        )
        if response.ok:
            return response.json()["choices"][0]["message"]["content"]
    except:
        pass
    return ""


def load_leads(path: str) -> list:
    """Load leads from file."""
    p = Path(path)
    if p.suffix == ".csv":
        with open(p) as f:
            return list(csv.DictReader(f))
    elif p.suffix == ".json":
        with open(p) as f:
            data = json.load(f)
            return data if isinstance(data, list) else data.get("leads", data.get("data", []))
    return []


def personalize_lead(client: OpenAI, lead: dict, service: str, value_prop: str, depth: str = "medium") -> dict:
    """Generate personalization for a single lead."""
    name = lead.get("name") or f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
    company = lead.get("company") or lead.get("company_name", "")
    title = lead.get("title") or lead.get("job_title", "")
    website = lead.get("website") or lead.get("domain", "")
    
    # Research based on depth
    research = ""
    if depth in ["medium", "deep"] and company:
        query = f"Recent news about {company}. Any funding, hiring, product launches, or challenges?"
        research = search_perplexity(query)
    
    system_prompt = """You are an expert at writing personalized cold email openers. 
Generate specific, relevant first lines that feel genuine and tie to a potential pain point.
Output ONLY valid JSON."""

    user_prompt = f"""Generate personalization for this lead:

PROSPECT:
- Name: {name}
- Title: {title}
- Company: {company}
- Website: {website}

RESEARCH:
{research[:800] if research else "No research available - use role/industry-based personalization"}

MY OFFERING:
- Service: {service}
- Value Prop: {value_prop}

OUTPUT JSON:
{{
  "personalized_first_line": "8-20 word opener referencing something specific",
  "pain_point": "The main pain point this person likely has",
  "personalization_source": "What the first line references (news/hiring/content/role-based)",
  "research_notes": "Key findings in 1-2 sentences",
  "confidence_score": 0-100,
  "alternative_angles": ["angle 1", "angle 2"]
}}

RULES:
- First line must be <25 words
- Be specific, not generic ("Noticed you're hiring" vs "Growing company")
- Tie to potential pain point
- Don't be sycophantic
- If no research, use role-based personalization"""

    response = call_llm(client, system_prompt, user_prompt, temperature=0.7)
    
    try:
        if "```" in response:
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        personalization = json.loads(response)
    except:
        personalization = {
            "personalized_first_line": f"As a {title} at {company}, you probably deal with...",
            "pain_point": "Unknown",
            "personalization_source": "role-based",
            "research_notes": "Could not parse AI response",
            "confidence_score": 30,
            "alternative_angles": []
        }
    
    return {
        **lead,
        **personalization
    }


def main():
    parser = argparse.ArgumentParser(description="Generate personalized email openers")
    parser.add_argument("--input", "-i", required=True, help="Input leads file (CSV or JSON)")
    parser.add_argument("--service", "-s", required=True, help="Your service/offering")
    parser.add_argument("--value_prop", "-v", default="", help="Value proposition")
    parser.add_argument("--depth", "-d", default="medium", choices=["light", "medium", "deep"],
        help="Personalization depth (light=fast, deep=thorough)")
    parser.add_argument("--output", "-o", default=".tmp/personalized_leads.json", help="Output file")
    parser.add_argument("--limit", type=int, default=0, help="Limit leads to process")
    
    args = parser.parse_args()
    
    print(f"\n🎯 AI Email Personalizer")
    print(f"   Input: {args.input}")
    print(f"   Service: {args.service}")
    print(f"   Depth: {args.depth}\n")
    
    leads = load_leads(args.input)
    if args.limit > 0:
        leads = leads[:args.limit]
    print(f"   Processing: {len(leads)} leads\n")
    
    client = get_client()
    results = []
    
    for i, lead in enumerate(leads, 1):
        name = lead.get("name") or f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
        company = lead.get("company") or lead.get("company_name", "")
        print(f"[{i}/{len(leads)}] {name} @ {company}...", end=" ")
        
        personalized = personalize_lead(client, lead, args.service, args.value_prop, args.depth)
        results.append(personalized)
        
        score = personalized.get("confidence_score", 0)
        print(f"✓ (confidence: {score})")
    
    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "personalized_at": datetime.now().isoformat(),
        "config": {"service": args.service, "value_prop": args.value_prop, "depth": args.depth},
        "total_leads": len(results),
        "leads": results
    }
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    # Stats
    high_confidence = sum(1 for r in results if r.get("confidence_score", 0) >= 70)
    print(f"\n✅ Personalization complete!")
    print(f"   High confidence (70+): {high_confidence}/{len(results)}")
    print(f"   📄 Output: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
