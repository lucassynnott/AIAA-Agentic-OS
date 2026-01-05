#!/usr/bin/env python3
"""
Cold Email Scriptwriter - Generate personalized cold email sequences with A/B variants.

Usage:
    python3 execution/write_cold_emails.py \
        --leads leads.csv \
        --sender_name "John Smith" \
        --product "AI Cold Email Tool" \
        --value_prop "Book 30+ meetings per month" \
        --output .tmp/email_sequences.json
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
            print(f"    Retry {attempt + 1}/3: {e}")
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
            json={"model": "llama-3.1-sonar-small-128k-online", "messages": [{"role": "user", "content": query}]},
            timeout=30
        )
        if response.ok:
            return response.json()["choices"][0]["message"]["content"]
    except:
        pass
    return ""


def load_leads(path: str) -> list:
    """Load leads from CSV or JSON."""
    p = Path(path)
    if p.suffix == ".csv":
        with open(p) as f:
            return list(csv.DictReader(f))
    elif p.suffix == ".json":
        with open(p) as f:
            data = json.load(f)
            return data if isinstance(data, list) else data.get("leads", data.get("data", []))
    return []


def research_prospect(prospect: dict) -> str:
    """Research a prospect using Perplexity."""
    name = prospect.get("name") or f"{prospect.get('first_name', '')} {prospect.get('last_name', '')}".strip()
    company = prospect.get("company") or prospect.get("company_name", "")
    
    if not company:
        return ""
    
    query = f"Tell me about {company} - recent news, funding, growth, challenges. Also any info on {name} if available."
    return search_perplexity(query)


def generate_first_line(client: OpenAI, prospect: dict, research: str, config: dict) -> str:
    """Generate personalized first line."""
    name = prospect.get("name") or f"{prospect.get('first_name', '')} {prospect.get('last_name', '')}".strip()
    company = prospect.get("company") or prospect.get("company_name", "")
    title = prospect.get("title") or prospect.get("job_title", "")
    
    system_prompt = "You are an expert cold email copywriter. Write short, personalized first lines that feel genuine, not salesy."
    
    user_prompt = f"""Write a personalized first line for a cold email.

PROSPECT:
- Name: {name}
- Title: {title}
- Company: {company}

RESEARCH:
{research[:1000] if research else "No research available - use industry-generic approach"}

MY OFFERING:
- Product/Service: {config['product']}
- Value Proposition: {config['value_prop']}

RULES:
- 8-20 words max
- Be specific, not generic
- Reference something real (news, hiring, content)
- Don't be sycophantic
- Connect to a potential pain point

OUTPUT: Just the first line, nothing else."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.8).strip().strip('"')


def generate_email_sequence(client: OpenAI, prospect: dict, first_line: str, config: dict) -> list:
    """Generate a 4-email sequence."""
    name = prospect.get("name") or f"{prospect.get('first_name', '')} {prospect.get('last_name', '')}".strip()
    company = prospect.get("company") or prospect.get("company_name", "")
    title = prospect.get("title") or prospect.get("job_title", "")
    
    system_prompt = """You are an expert cold email copywriter trained on proven methodologies. 
Write short, conversational emails that achieve >10% response rates. No fluff, no corporate speak."""
    
    user_prompt = f"""Create a 4-email sequence for this prospect.

PROSPECT:
- Name: {name}
- Title: {title}
- Company: {company}

PERSONALIZED FIRST LINE: {first_line}

MY OFFERING:
- Product/Service: {config['product']}
- Value Proposition: {config['value_prop']}
- Sender: {config['sender_name']} ({config.get('sender_title', 'Founder')})

CREATE 4 EMAILS:

EMAIL 1 (Day 0): Problem + Social Proof
- Use the personalized first line
- Present one specific pain point
- Share one specific result
- Soft CTA ("Open to a quick chat?")

EMAIL 2 (Day 3): Follow-up + Value Add
- Short, reference first email
- Share additional insight or resource
- Different angle on the value

EMAIL 3 (Day 7): Case Study
- Share specific client result
- Numbers and outcomes
- "If this resonates..."

EMAIL 4 (Day 10): Breakup
- "Closing the loop"
- Final value reminder
- Easy out CTA

OUTPUT AS JSON:
[
  {{
    "email_number": 1,
    "subject": "subject line",
    "body": "email body with {{{{first_name}}}} placeholder",
    "timing": "Day 0",
    "framework": "Problem + Social Proof"
  }},
  ...
]

Rules:
- 50-100 words per email
- No formal greetings (Hi {{{{first_name}}}}, is fine)
- End with one simple CTA
- Sound human, not robotic"""

    response = call_llm(client, system_prompt, user_prompt, temperature=0.7)
    
    try:
        if "```" in response:
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        return json.loads(response)
    except:
        return []


def generate_ab_variants(client: OpenAI, email1: dict, prospect: dict, config: dict) -> list:
    """Generate A/B/C variants for email 1."""
    system_prompt = "You are an A/B testing specialist for cold emails. Create variants using different psychological frameworks."
    
    user_prompt = f"""Create 2 additional variants of this email for split testing:

ORIGINAL EMAIL:
Subject: {email1.get('subject', '')}
Body: {email1.get('body', '')}

PROSPECT CONTEXT:
- Name: {prospect.get('name', '')}
- Company: {prospect.get('company', '')}
- Title: {prospect.get('title', '')}

OFFER: {config['product']} - {config['value_prop']}

CREATE VARIANTS:

VARIANT B: Before/After/Bridge framework
- Show the before state (their problem)
- Show the after state (desired outcome)  
- Bridge with your solution

VARIANT C: Curiosity + Question
- Lead with an intriguing observation
- Ask a thought-provoking question
- Tease the solution

OUTPUT AS JSON:
[
  {{"variant": "B", "subject": "", "body": "", "framework": "Before/After/Bridge"}},
  {{"variant": "C", "subject": "", "body": "", "framework": "Curiosity + Question"}}
]"""

    response = call_llm(client, system_prompt, user_prompt, temperature=0.8)
    
    try:
        if "```" in response:
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        return json.loads(response)
    except:
        return []


def main():
    parser = argparse.ArgumentParser(description="Generate personalized cold email sequences")
    parser.add_argument("--leads", "-l", required=True, help="Leads file (CSV or JSON)")
    parser.add_argument("--sender_name", "-s", required=True, help="Sender name")
    parser.add_argument("--sender_title", default="", help="Sender title")
    parser.add_argument("--product", "-p", required=True, help="Product/service being offered")
    parser.add_argument("--value_prop", "-v", default="", help="Value proposition")
    parser.add_argument("--output", "-o", default=".tmp/email_sequences.json", help="Output file")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of leads to process")
    parser.add_argument("--skip_research", action="store_true", help="Skip Perplexity research")
    
    args = parser.parse_args()
    
    config = {
        "sender_name": args.sender_name,
        "sender_title": args.sender_title or "Founder",
        "product": args.product,
        "value_prop": args.value_prop or f"Transform your results with {args.product}"
    }
    
    print(f"\n📧 Cold Email Scriptwriter")
    print(f"   Leads: {args.leads}")
    print(f"   Product: {config['product']}")
    
    # Load leads
    leads = load_leads(args.leads)
    if args.limit > 0:
        leads = leads[:args.limit]
    print(f"   Processing: {len(leads)} leads\n")
    
    client = get_client()
    results = []
    
    for i, prospect in enumerate(leads, 1):
        name = prospect.get("name") or f"{prospect.get('first_name', '')} {prospect.get('last_name', '')}".strip()
        company = prospect.get("company") or prospect.get("company_name", "")
        
        print(f"[{i}/{len(leads)}] {name} @ {company}")
        
        # Research
        research = "" if args.skip_research else research_prospect(prospect)
        
        # Generate first line
        first_line = generate_first_line(client, prospect, research, config)
        print(f"   First line: {first_line[:50]}...")
        
        # Generate sequence
        sequence = generate_email_sequence(client, prospect, first_line, config)
        
        # Generate A/B variants for email 1
        variants = []
        if sequence:
            variants = generate_ab_variants(client, sequence[0], prospect, config)
        
        results.append({
            "prospect": {
                "name": name,
                "company": company,
                "title": prospect.get("title", ""),
                "email": prospect.get("email", "")
            },
            "first_line": first_line,
            "research_notes": research[:500] if research else "",
            "email_sequence": sequence,
            "ab_variants": variants
        })
    
    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "config": config,
        "total_prospects": len(results),
        "sequences": results
    }
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n✅ Generated {len(results)} email sequences")
    print(f"   📄 Output: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
