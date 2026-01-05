#!/usr/bin/env python3
"""
Job Board Lead Finder - Find companies hiring for specific roles.

Usage:
    python3 execution/find_job_board_leads.py \
        --role "Marketing Manager" \
        --location "Remote" \
        --output .tmp/job_leads.json
"""

import argparse, json, os, sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

def search_perplexity(query):
    """Search using Perplexity for job listings."""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return ""
    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [{"role": "user", "content": query}]
            },
            timeout=30
        )
        if resp.ok:
            return resp.json()["choices"][0]["message"]["content"]
    except:
        pass
    return ""

def main():
    parser = argparse.ArgumentParser(description="Find companies from job boards")
    parser.add_argument("--role", "-r", required=True, help="Job role to search")
    parser.add_argument("--location", "-l", default="", help="Location filter")
    parser.add_argument("--industry", "-i", default="", help="Industry filter")
    parser.add_argument("--output", "-o", default=".tmp/job_leads.json")
    args = parser.parse_args()

    print(f"\n💼 Job Board Lead Finder\n   Role: {args.role}\n")

    # Build search query
    query_parts = [f"companies currently hiring {args.role}"]
    if args.location:
        query_parts.append(f"in {args.location}")
    if args.industry:
        query_parts.append(f"in {args.industry} industry")
    
    query = " ".join(query_parts) + ". List company names, job titles, and company websites."
    
    print("   Searching job boards...")
    results = search_perplexity(query)
    
    if not results:
        print("   ❌ No results. Add PERPLEXITY_API_KEY to .env for real-time job search.")
        return 1

    # Parse results with AI
    from openai import OpenAI
    
    def get_client():
        if os.getenv("OPENROUTER_API_KEY"):
            return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    client = get_client()
    model = "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o-mini"
    
    parsed = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Extract company leads from job board data. Return JSON array."},
            {"role": "user", "content": f"""Extract leads from this job board data:

{results}

Return JSON array:
[
  {{
    "company": "Company Name",
    "role": "Job Title",
    "location": "Location",
    "website": "company website if found",
    "source": "job board name if mentioned"
  }}
]

Return only valid JSON."""}
        ],
        temperature=0.3,
        max_tokens=2000
    ).choices[0].message.content

    try:
        if "```" in parsed:
            parsed = parsed.split("```")[1]
            if parsed.startswith("json"):
                parsed = parsed[4:]
        leads = json.loads(parsed)
    except:
        leads = []

    output = {
        "searched_at": datetime.now().isoformat(),
        "search_criteria": {
            "role": args.role,
            "location": args.location,
            "industry": args.industry
        },
        "total_leads": len(leads),
        "leads": leads,
        "raw_results": results
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Found {len(leads)} companies hiring")
    print(f"   📄 Output: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
