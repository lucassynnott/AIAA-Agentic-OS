#!/usr/bin/env python3
"""
Fast Lead Pipeline - Quick SaaS founder scraping using Perplexity + Instantly upload.
Optimized for speed over deep personalization.

Usage:
    python3 execution/fast_lead_pipeline.py --location "San Francisco" --limit 50
"""

import os
import sys
import json
import argparse
import time
import re
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from dotenv import load_dotenv

load_dotenv()

INSTANTLY_API_BASE = "https://api.instantly.ai/api/v2"


def find_saas_founders(location: str, batch: int, total_batches: int) -> list:
    """Find SaaS founders via Perplexity search."""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return []

    # Different search terms per batch to get variety
    search_variants = [
        "B2B SaaS", "enterprise software", "cloud software",
        "software startup", "tech company", "SaaS platform"
    ]
    variant = search_variants[batch % len(search_variants)]

    query = f"""Find 15 real {variant} company founders/CEOs in {location}:
- Company has 50+ employees
- Established companies with revenue
- Different from common well-known ones if batch {batch}

Return as JSON array only, no explanation:
[{{"name": "First Last", "title": "CEO", "company": "Company", "website": "example.com"}}]"""

    resp = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "sonar", "messages": [{"role": "user", "content": query}]},
        timeout=60
    )

    if not resp.ok:
        print(f"  Perplexity error: {resp.status_code}")
        return []

    content = resp.json()["choices"][0]["message"]["content"]

    # Extract JSON from response
    leads = []
    try:
        # Find JSON array in response
        json_match = re.search(r'\[[\s\S]*\]', content)
        if json_match:
            data = json.loads(json_match.group())
            for item in data:
                name = item.get("name", "")
                name_parts = name.split(" ", 1)
                first_name = name_parts[0] if name_parts else ""
                last_name = name_parts[1] if len(name_parts) > 1 else ""
                website = item.get("website", "").replace("https://", "").replace("http://", "").replace("www.", "")

                if first_name:
                    leads.append({
                        "first_name": first_name,
                        "last_name": last_name,
                        "full_name": name,
                        "job_title": item.get("title", "CEO"),
                        "company_name": item.get("company", ""),
                        "company_website": website,
                        "email": f"{first_name.lower()}@{website}" if website else "",
                        "location": location
                    })
    except json.JSONDecodeError:
        pass

    return leads


def generate_icebreakers_batch(leads: list) -> list:
    """Generate icebreakers for all leads in one LLM call."""

    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        # Fallback to template
        for lead in leads:
            lead["icebreaker"] = f"Saw {lead['company_name']} is scaling fast in the SaaS space."
        return leads

    # Build batch prompt
    lead_list = "\n".join([
        f"{i+1}. {lead['full_name']}, {lead['job_title']} at {lead['company_name']}"
        for i, lead in enumerate(leads)
    ])

    prompt = f"""Write a short, personalized cold email opening line (10-15 words) for each person below.
Rules:
- Reference their company or role specifically
- Sound like a peer, not salesy
- Don't start with "I noticed" or "I saw"
- Don't use generic compliments

People:
{lead_list}

Output format (one per line, numbered):
1. [opening line for person 1]
2. [opening line for person 2]
..."""

    if os.getenv("OPENROUTER_API_KEY"):
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"},
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=60
        )
        if resp.ok:
            content = resp.json()["choices"][0]["message"]["content"]
        else:
            content = ""
    else:
        import anthropic
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        content = resp.content[0].text

    # Parse responses
    lines = content.strip().split("\n")
    for i, lead in enumerate(leads):
        for line in lines:
            if line.strip().startswith(f"{i+1}."):
                icebreaker = line.split(".", 1)[1].strip() if "." in line else line
                lead["icebreaker"] = icebreaker.strip('"').strip("'")
                break
        if "icebreaker" not in lead:
            lead["icebreaker"] = f"Scaling a SaaS company like {lead['company_name']} is no small feat."

    return leads


def create_instantly_campaign(campaign_name: str) -> str:
    """Create Instantly campaign."""
    api_key = os.getenv("INSTANTLY_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "name": campaign_name,
        "sequences": [{
            "steps": [
                {
                    "type": "email",
                    "delay": 0,
                    "variants": [{
                        "subject": "quick question, {{firstName}}",
                        "body": "<p>Hi {{firstName}},</p><p>{{icebreaker}}</p><p>We help SaaS companies like {{companyName}} automate outbound and book more meetings without hiring more SDRs.</p><p>Worth a quick chat?</p>"
                    }]
                },
                {
                    "type": "email",
                    "delay": 3,
                    "variants": [{
                        "subject": "Re: quick question",
                        "body": "<p>Hi {{firstName}},</p><p>Bumping this up - happy to share how we helped similar companies 3x their pipeline.</p><p>15 min this week?</p>"
                    }]
                }
            ]
        }],
        "email_gap": 10,
        "daily_limit": 50
    }

    resp = requests.post(f"{INSTANTLY_API_BASE}/campaigns", headers=headers, json=payload)

    if resp.status_code in [200, 201]:
        return resp.json().get("id")
    print(f"  Campaign error: {resp.status_code} - {resp.text[:200]}")
    return None


def upload_leads_parallel(campaign_id: str, leads: list) -> dict:
    """Upload leads to Instantly in parallel."""
    api_key = os.getenv("INSTANTLY_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    success = 0
    errors = 0

    def upload_one(lead):
        payload = {
            "campaign": campaign_id,
            "email": lead.get("email", ""),
            "first_name": lead.get("first_name", ""),
            "last_name": lead.get("last_name", ""),
            "company_name": lead.get("company_name", ""),
            "custom_variables": {
                "icebreaker": lead.get("icebreaker", ""),
                "companyName": lead.get("company_name", "")
            }
        }
        resp = requests.post(f"{INSTANTLY_API_BASE}/leads", headers=headers, json=payload)
        return resp.status_code in [200, 201]

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(upload_one, lead): lead for lead in leads if lead.get("email")}
        for future in as_completed(futures):
            if future.result():
                success += 1
            else:
                errors += 1

    return {"success": success, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description="Fast lead pipeline")
    parser.add_argument("--location", default="San Francisco", help="Target location")
    parser.add_argument("--limit", type=int, default=50, help="Number of leads")
    parser.add_argument("--campaign_name", help="Instantly campaign name")
    parser.add_argument("--skip_instantly", action="store_true", help="Skip Instantly upload")

    args = parser.parse_args()

    print("=" * 50)
    print("FAST LEAD PIPELINE")
    print("=" * 50)

    # Step 1: Find founders in parallel batches
    print(f"\n[1/4] Finding SaaS founders in {args.location}...")

    all_leads = []
    batches_needed = (args.limit // 12) + 1

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(find_saas_founders, args.location, i+1, batches_needed)
            for i in range(batches_needed)
        ]
        for future in as_completed(futures):
            all_leads.extend(future.result())
            print(f"  Found {len(all_leads)} leads so far...")

    # Dedupe by company name
    seen = set()
    unique_leads = []
    for lead in all_leads:
        key = lead.get("company_name", "").lower()
        if key and key not in seen:
            seen.add(key)
            unique_leads.append(lead)

    leads = unique_leads[:args.limit]
    print(f"  Final: {len(leads)} unique leads")

    if not leads:
        print("No leads found. Exiting.")
        return 1

    # Step 2: Generate icebreakers in batch
    print(f"\n[2/4] Generating personalized icebreakers...")
    leads = generate_icebreakers_batch(leads)
    print(f"  Generated {len([l for l in leads if l.get('icebreaker')])} icebreakers")

    # Step 3: Save leads
    output_path = f".tmp/leads/fast_{args.location.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump({"leads": leads, "generated_at": datetime.now().isoformat()}, f, indent=2)
    print(f"\n[3/4] Saved to: {output_path}")

    # Step 4: Upload to Instantly
    if not args.skip_instantly:
        campaign_name = args.campaign_name or f"Fast {args.location} SaaS | {datetime.now().strftime('%b %d')}"
        print(f"\n[4/4] Creating Instantly campaign: {campaign_name}")

        campaign_id = create_instantly_campaign(campaign_name)
        if campaign_id:
            print(f"  Campaign ID: {campaign_id}")
            print(f"  Uploading {len(leads)} leads...")

            results = upload_leads_parallel(campaign_id, leads)
            print(f"  Uploaded: {results['success']}, Errors: {results['errors']}")
        else:
            print("  Failed to create campaign")

    print("\n" + "=" * 50)
    print("DONE!")
    print("=" * 50)
    print(f"Leads: {len(leads)}")
    print(f"File: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
