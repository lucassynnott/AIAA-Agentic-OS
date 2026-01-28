#!/usr/bin/env python3
"""
AI Lead Scorer - Score and qualify leads based on ICP criteria using AI.

Usage:
    python3 execution/score_leads_ai.py \
        --input leads.json \
        --icp_criteria criteria.json \
        --output scored_leads.json
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


def load_leads(input_path: str) -> list:
    """Load leads from JSON or CSV."""
    path = Path(input_path)
    if path.suffix == ".json":
        with open(path) as f:
            data = json.load(f)
            return data if isinstance(data, list) else data.get("leads", data.get("data", []))
    elif path.suffix == ".csv":
        import csv
        with open(path) as f:
            return list(csv.DictReader(f))
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")


def load_icp_criteria(criteria_path: Optional[str]) -> dict:
    """Load ICP criteria from JSON file or return defaults."""
    if criteria_path and Path(criteria_path).exists():
        with open(criteria_path) as f:
            return json.load(f)
    return {
        "company_size": {"ideal": "50-500", "weight": 0.25},
        "industry": {"ideal": ["SaaS", "Technology", "Marketing"], "weight": 0.20},
        "job_title": {"ideal": ["CEO", "Founder", "VP", "Director", "Head of"], "weight": 0.25},
        "location": {"ideal": ["United States", "US", "UK", "Canada"], "weight": 0.15},
        "funding": {"ideal": "Funded", "weight": 0.15}
    }


def score_lead_batch(client: OpenAI, leads: list, icp_criteria: dict, batch_size: int = 5) -> list:
    """Score a batch of leads using AI."""
    scored_leads = []
    total = len(leads)
    
    for i in range(0, total, batch_size):
        batch = leads[i:i+batch_size]
        print(f"  Scoring leads {i+1}-{min(i+batch_size, total)} of {total}...")
        
        leads_text = "\n".join([
            f"Lead {j+1}: {json.dumps(lead, indent=2)}" 
            for j, lead in enumerate(batch)
        ])
        
        prompt = f"""Score these leads against the ICP criteria and return JSON.

ICP CRITERIA:
{json.dumps(icp_criteria, indent=2)}

LEADS TO SCORE:
{leads_text}

For each lead, analyze and return a JSON array with:
{{
  "original_data": {{...original lead data...}},
  "lead_score": 0-100,
  "icp_fit": 0-100,
  "intent_score": 0-100,
  "classification": "Hot|Warm|Cool|Cold",
  "reasoning": "Brief explanation",
  "recommended_action": "Specific next step"
}}

Classification rules:
- Hot (80-100): Prioritize immediate outreach
- Warm (60-79): Standard sequence
- Cool (40-59): Nurture campaign  
- Cold (0-39): Deprioritize

Return ONLY valid JSON array, no markdown."""

        try:
            response = client.chat.completions.create(
                model=get_model(),
                messages=[
                    {"role": "system", "content": "You are an expert lead qualification AI. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            result = response.choices[0].message.content.strip()
            # Clean up response
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
            
            batch_scores = json.loads(result)
            if isinstance(batch_scores, dict):
                batch_scores = [batch_scores]
            scored_leads.extend(batch_scores)
            
        except json.JSONDecodeError as e:
            print(f"    Warning: JSON parse error, scoring individually...")
            for lead in batch:
                scored_leads.append({
                    "original_data": lead,
                    "lead_score": 50,
                    "icp_fit": 50,
                    "intent_score": 50,
                    "classification": "Cool",
                    "reasoning": "Could not parse AI response",
                    "recommended_action": "Manual review"
                })
        except Exception as e:
            print(f"    Error: {e}")
            for lead in batch:
                scored_leads.append({
                    "original_data": lead,
                    "lead_score": 0,
                    "classification": "Cold",
                    "reasoning": f"Error: {e}",
                    "recommended_action": "Manual review"
                })
    
    return scored_leads


def main():
    parser = argparse.ArgumentParser(description="Score leads using AI")
    parser.add_argument("--input", "-i", required=True, help="Input leads file (JSON or CSV)")
    parser.add_argument("--icp_criteria", "-c", help="ICP criteria JSON file")
    parser.add_argument("--output", "-o", default=".tmp/scored_leads.json", help="Output file")
    parser.add_argument("--batch_size", type=int, default=5, help="Leads per API call")
    
    args = parser.parse_args()
    
    print(f"\n🎯 AI Lead Scorer")
    print(f"   Input: {args.input}")
    
    # Load data
    leads = load_leads(args.input)
    print(f"   Leads loaded: {len(leads)}")
    
    icp_criteria = load_icp_criteria(args.icp_criteria)
    print(f"   ICP criteria: {len(icp_criteria)} factors")
    
    # Score leads
    client = get_client()
    scored = score_lead_batch(client, leads, icp_criteria, args.batch_size)
    
    # Calculate stats
    hot = sum(1 for l in scored if l.get("classification") == "Hot")
    warm = sum(1 for l in scored if l.get("classification") == "Warm")
    cool = sum(1 for l in scored if l.get("classification") == "Cool")
    cold = sum(1 for l in scored if l.get("classification") == "Cold")
    
    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "scored_at": datetime.now().isoformat(),
        "total_leads": len(scored),
        "summary": {"hot": hot, "warm": warm, "cool": cool, "cold": cold},
        "leads": scored
    }
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n✅ Scoring complete!")
    print(f"   🔥 Hot: {hot} | 🟡 Warm: {warm} | 🔵 Cool: {cool} | ❄️ Cold: {cold}")
    print(f"   📄 Output: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
