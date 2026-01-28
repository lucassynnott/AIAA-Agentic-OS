#!/usr/bin/env python3
"""
Cold Email Pipeline - End-to-End Lead Generation to Campaign

Complete pipeline that:
1. Scrapes leads from Apify (Apollo-style data)
2. Scrapes LinkedIn posts for each lead
3. Generates personalized first lines based on real post content
4. Creates campaign in Instantly
5. Uploads leads with proper variable formatting

IMPORTANT - Location Format:
    --location requires state/country format for Apify: "california, us", "united states"
    --city for city-level filtering: "San Francisco", "New York"

Usage:
    # Basic usage
    python3 execution/cold_email_pipeline.py \
        --industry "SaaS" \
        --location "california, us" \
        --city "San Francisco" \
        --limit 25 \
        --campaign_name "SF SaaS Outreach - Jan 2026"

    # Advanced: SaaS founders, 25-150 employees, $1M+ revenue
    python3 execution/cold_email_pipeline.py \
        --industry "SaaS" \
        --location "california, us" \
        --city "San Francisco" \
        --job_titles "CEO" "Founder" "Co-Founder" \
        --seniority "founder" "c_suite" \
        --sizes "21-50" "51-100" "101-200" \
        --min_revenue "1M" \
        --limit 25 \
        --campaign_name "SF SaaS Founders - Jan 2026"

    # Skip Instantly (just generate leads + personalization)
    python3 execution/cold_email_pipeline.py \
        --industry "SaaS" \
        --location "united states" \
        --limit 50 \
        --skip_instantly
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

# API Constants
APIFY_LEAD_ACTOR = "IoSHqwTR9YGhzccez"  # Apollo-style lead scraper
APIFY_LINKEDIN_ACTOR = "supreme_coder/linkedin-post"  # LinkedIn post scraper
INSTANTLY_API_BASE = "https://api.instantly.ai/api/v2"


def check_api_keys():
    """Verify all required API keys are present."""
    required = {
        "APIFY_API_TOKEN": os.getenv("APIFY_API_TOKEN"),
        "INSTANTLY_API_KEY": os.getenv("INSTANTLY_API_KEY"),
    }

    # Need at least one LLM API
    llm_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not llm_key:
        required["OPENROUTER_API_KEY or OPENAI_API_KEY"] = None

    missing = [k for k, v in required.items() if not v]
    if missing:
        print(f"Error: Missing API keys in .env: {', '.join(missing)}")
        sys.exit(1)

    print("All API keys verified")


def scrape_leads(
    industry: str,
    location: str,
    limit: int,
    city: str = None,
    job_titles: list = None,
    seniority: list = None,
    sizes: list = None,
    min_revenue: str = None
) -> list:
    """Scrape leads using Apify Apollo-style actor with advanced filtering."""
    from apify_client import ApifyClient

    client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

    print(f"\nStep 1: Scraping {limit} leads...")
    print(f"  Industry: {industry}")
    print(f"  Location: {location}")
    if city:
        print(f"  City: {city}")
    if sizes:
        print(f"  Company sizes: {sizes}")
    if min_revenue:
        print(f"  Min revenue: {min_revenue}")
    if job_titles:
        print(f"  Job titles: {job_titles}")
    if seniority:
        print(f"  Seniority: {seniority}")

    # Build Apify input with proper field names
    run_input = {
        "company_keywords": [industry] if industry else [],
        "contact_location": [location] if location else [],
        "fetch_count": limit,
        "email_status": ["validated", "not_validated", "unknown"]
    }

    # Add optional filters
    if city:
        run_input["contact_city"] = [city]
    if job_titles:
        run_input["contact_job_title"] = job_titles
    if seniority:
        run_input["seniority_level"] = seniority
    if sizes:
        run_input["size"] = sizes
    if min_revenue:
        run_input["min_revenue"] = min_revenue

    run = client.actor(APIFY_LEAD_ACTOR).call(run_input=run_input, timeout_secs=600)

    leads = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        leads.append({
            "email": item.get("email", ""),
            "first_name": item.get("firstName", ""),
            "last_name": item.get("lastName", ""),
            "full_name": item.get("fullName", ""),
            "job_title": item.get("jobTitle", ""),
            "headline": item.get("headline", ""),
            "linkedin": item.get("linkedin", ""),
            "company_name": item.get("companyName", ""),
            "company_website": item.get("companyWebsite", ""),
            "industry": item.get("industry", ""),
            "company_size": item.get("companySize", 0),
            "city": item.get("city", ""),
            "state": item.get("state", ""),
            "country": item.get("country", "")
        })

    # Filter to leads with emails
    leads = [l for l in leads if l.get("email")]
    print(f"  Found {len(leads)} leads with emails")

    return leads


def scrape_linkedin_posts(leads: list, posts_per_profile: int = 5) -> dict:
    """Scrape LinkedIn posts for all leads."""
    from apify_client import ApifyClient

    client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

    # Get LinkedIn URLs
    linkedin_urls = [l["linkedin"] for l in leads if l.get("linkedin")]

    print(f"\nStep 2: Scraping LinkedIn posts for {len(linkedin_urls)} profiles...")

    if not linkedin_urls:
        print("  No LinkedIn URLs found")
        return {}

    run_input = {
        "urls": linkedin_urls,
        "deepScrape": True,
        "limitPerSource": posts_per_profile,
        "rawData": False
    }

    run = client.actor(APIFY_LINKEDIN_ACTOR).call(run_input=run_input, timeout_secs=600)

    # Group posts by profile URL
    results = {}
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        url_key = (item.get("inputUrl") or item.get("authorProfileUrl", "")).lower().rstrip("/")

        if url_key:
            if url_key not in results:
                results[url_key] = {"posts": []}

            results[url_key]["posts"].append({
                "text": item.get("text", ""),
                "reactions": item.get("numLikes", 0),
                "time_since": item.get("timeSincePosted", "")
            })

    profiles_with_posts = sum(1 for p in results.values() if p.get("posts"))
    print(f"  Found posts for {profiles_with_posts} profiles")

    return results


def generate_personalized_lines(leads: list, posts_data: dict) -> list:
    """Generate personalized first lines based on LinkedIn posts."""
    from openai import OpenAI

    # Get LLM client
    if os.getenv("OPENROUTER_API_KEY"):
        client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        model = "anthropic/claude-sonnet-4"
    elif os.getenv("OPENAI_API_KEY"):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        model = "gpt-4o"
    else:
        # Use Anthropic directly
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        model = "claude-sonnet-4-5-20250929"

    print(f"\nStep 3: Generating personalized first lines...")

    system_prompt = """You write hyper-personalized cold email first lines based on LinkedIn posts.

Write ONE line (8-18 words) that references something SPECIFIC from their posts.

RULES:
1. Reference their ACTUAL content - quote or paraphrase their ideas
2. Never use "I noticed" or "I came across"
3. Sound like a peer who genuinely found their content interesting
4. Don't start with "I" - start with something about THEM
5. Be conversational, not salesy

Output ONLY the first line. No quotes. No explanation."""

    results = []
    high_confidence = 0

    for i, lead in enumerate(leads, 1):
        name = lead.get("full_name") or f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
        linkedin_url = lead.get("linkedin", "").lower().rstrip("/")
        profile_posts = posts_data.get(linkedin_url, {}).get("posts", [])

        # Build posts text
        posts_text = ""
        for j, post in enumerate(profile_posts[:5]):
            if post.get("text"):
                posts_text += f"\n--- Post {j+1} ---\n{post['text'][:500]}\n"

        has_posts = bool(posts_text.strip())

        if has_posts:
            user_prompt = f"""Write a first line for {name}, {lead.get('job_title', '')} at {lead.get('company_name', '')}.

THEIR POSTS:
{posts_text}

Pick ONE idea from their posts to reference naturally."""
        else:
            user_prompt = f"""Write a first line for {name}, {lead.get('job_title', '')} at {lead.get('company_name', '')}.
Headline: {lead.get('headline', '')}

No posts found. Use their headline creatively."""

        try:
            if hasattr(client, 'chat'):  # OpenAI-style client
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.85,
                    max_tokens=100
                )
                first_line = response.choices[0].message.content.strip().strip('"').strip("'")
            else:  # Anthropic client
                response = client.messages.create(
                    model=model,
                    max_tokens=100,
                    messages=[{"role": "user", "content": f"{system_prompt}\n\n{user_prompt}"}]
                )
                first_line = response.content[0].text.strip().strip('"').strip("'")

            confidence = "high" if has_posts else "medium"
            if has_posts:
                high_confidence += 1

        except Exception as e:
            first_line = f"Error: {e}"
            confidence = "none"

        lead["personalized_first_line"] = first_line
        lead["confidence"] = confidence
        lead["posts_found"] = len(profile_posts)
        results.append(lead)

        status = "+" if confidence == "high" else "~" if confidence == "medium" else "x"
        print(f"  [{i}/{len(leads)}] {status} {name[:30]}")

        time.sleep(0.3)

    print(f"  High confidence (from posts): {high_confidence}/{len(leads)}")

    return results


def create_instantly_campaign(campaign_name: str, email_template: dict = None) -> str:
    """Create a campaign in Instantly and return the campaign ID."""
    api_key = os.getenv("INSTANTLY_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"\nStep 4: Creating Instantly campaign '{campaign_name}'...")

    # Default email template
    if not email_template:
        email_template = {
            "sequences": [{
                "steps": [
                    {
                        "type": "email",
                        "delay": 0,
                        "variants": [
                            {
                                "subject": "quick question",
                                "body": "<p>Hi {{firstName}},</p><p>{{icebreaker}}</p><p>We help companies like {{companyName}} automate their outbound and book more meetings without hiring more SDRs.</p><p>Worth a quick chat?</p><p>{{sendingAccountFirstName}}</p>"
                            },
                            {
                                "subject": "{{firstName}} - quick thought",
                                "body": "<p>Hi {{firstName}},</p><p>{{icebreaker}}</p><p>We recently helped a similar company 5x their meeting volume using AI-powered outbound.</p><p>15 min to see if we can do the same for you?</p><p>{{sendingAccountFirstName}}</p>"
                            }
                        ]
                    },
                    {
                        "type": "email",
                        "delay": 3,
                        "variants": [{
                            "subject": "Re: quick question",
                            "body": "<p>Hi {{firstName}},</p><p>Bumping this up.</p><p>Happy to share exactly how we helped similar companies if helpful.</p><p>Either way, no worries.</p><p>{{sendingAccountFirstName}}</p>"
                        }]
                    },
                    {
                        "type": "email",
                        "delay": 4,
                        "variants": [{
                            "subject": "Re: quick question",
                            "body": "<p>Hi {{firstName}},</p><p>Last one from me on this.</p><p>If outbound isn't a priority right now, totally get it. But if pipeline ever becomes a focus, happy to chat.</p><p>{{sendingAccountFirstName}}</p>"
                        }]
                    }
                ]
            }]
        }

    payload = {
        "name": campaign_name,
        "sequences": email_template["sequences"],
        "campaign_schedule": {
            "schedules": [{
                "name": "Weekday Schedule",
                "days": {"1": True, "2": True, "3": True, "4": True, "5": True},
                "timing": {"from": "09:00", "to": "17:00"},
                "timezone": "America/Chicago"
            }]
        },
        "email_gap": 10,
        "daily_limit": 50,
        "stop_on_reply": True,
        "stop_on_auto_reply": True
    }

    resp = requests.post(f"{INSTANTLY_API_BASE}/campaigns", headers=headers, json=payload)

    if resp.status_code not in [200, 201]:
        print(f"  Error creating campaign: {resp.status_code} - {resp.text[:200]}")
        return None

    campaign_id = resp.json().get("id")
    print(f"  Created campaign: {campaign_id}")

    return campaign_id


def upload_leads_to_instantly(campaign_id: str, leads: list) -> dict:
    """Upload leads to Instantly campaign with proper variable formatting."""
    api_key = os.getenv("INSTANTLY_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"\nStep 5: Uploading {len(leads)} leads to campaign...")

    success = 0
    errors = 0

    for i, lead in enumerate(leads, 1):
        email = lead.get("email")
        if not email:
            continue

        personalization = lead.get("personalized_first_line", "")
        company = lead.get("company_name", "")

        payload = {
            "campaign": campaign_id,  # IMPORTANT: Use 'campaign' not 'campaign_id'
            "email": email,
            "first_name": lead.get("first_name", ""),
            "last_name": lead.get("last_name", ""),
            "company_name": company,
            "personalization": personalization,
            "custom_variables": {
                "icebreaker": personalization,
                "companyName": company
            }
        }

        resp = requests.post(f"{INSTANTLY_API_BASE}/leads", headers=headers, json=payload)

        if resp.status_code in [200, 201]:
            success += 1
        else:
            errors += 1

        if i % 10 == 0:
            print(f"  Progress: {i}/{len(leads)}")

        time.sleep(0.3)

    # Update personalization via PATCH (in case it wasn't set on POST)
    print("  Updating personalization fields...")
    resp = requests.post(
        f"{INSTANTLY_API_BASE}/leads/list",
        headers=headers,
        json={"campaign": campaign_id, "limit": 100}
    )
    campaign_leads = resp.json().get("items", [])

    email_to_pers = {l["email"].lower(): l.get("personalized_first_line", "") for l in leads if l.get("email")}

    updated = 0
    for lead in campaign_leads:
        email = lead.get("email", "").lower()
        if email in email_to_pers and not lead.get("personalization"):
            pers = email_to_pers[email]
            if pers:
                patch_resp = requests.patch(
                    f"{INSTANTLY_API_BASE}/leads/{lead['id']}",
                    headers=headers,
                    json={"personalization": pers}
                )
                if patch_resp.status_code == 200:
                    updated += 1
                time.sleep(0.2)

    print(f"  Uploaded: {success}, Updated: {updated}, Errors: {errors}")

    return {"success": success, "updated": updated, "errors": errors}


def main():
    parser = argparse.ArgumentParser(
        description="End-to-end cold email pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Required arguments
    parser.add_argument("--industry", required=True, help="Target industry/keywords (e.g., 'SaaS')")
    parser.add_argument("--location", required=True,
                       help="Location - state/country format (e.g., 'california, us', 'united states')")

    # Optional filters
    parser.add_argument("--city", help="City filter (e.g., 'San Francisco')")
    parser.add_argument("--job_titles", nargs='+', help="Job titles to target (e.g., 'CEO' 'Founder')")
    parser.add_argument("--seniority", nargs='+',
                       help="Seniority levels: founder, c_suite, vp, director, manager, senior, entry")
    parser.add_argument("--sizes", nargs='+',
                       help="Company size ranges: 1-10, 11-20, 21-50, 51-100, 101-200, 201-500, etc.")
    parser.add_argument("--min_revenue", help="Minimum revenue (e.g., '1M', '100K', '10B')")

    # Pipeline options
    parser.add_argument("--limit", type=int, default=50, help="Number of leads to scrape")
    parser.add_argument("--campaign_name", help="Instantly campaign name (auto-generated if not provided)")
    parser.add_argument("--output", "-o", help="Output JSON file for leads")
    parser.add_argument("--skip_instantly", action="store_true", help="Skip Instantly upload (just generate leads)")

    args = parser.parse_args()

    print("="*60)
    print("COLD EMAIL PIPELINE")
    print("="*60)

    # Check API keys
    check_api_keys()

    # Generate campaign name if not provided
    city_part = f"{args.city} " if args.city else ""
    campaign_name = args.campaign_name or f"{city_part}{args.industry} | {datetime.now().strftime('%b %Y')}"

    # Step 1: Scrape leads
    leads = scrape_leads(
        industry=args.industry,
        location=args.location,
        limit=args.limit,
        city=args.city,
        job_titles=args.job_titles,
        seniority=args.seniority,
        sizes=args.sizes,
        min_revenue=args.min_revenue
    )

    if not leads:
        print("No leads found. Exiting.")
        sys.exit(1)

    # Step 2: Scrape LinkedIn posts
    posts_data = scrape_linkedin_posts(leads)

    # Step 3: Generate personalized lines
    personalized_leads = generate_personalized_lines(leads, posts_data)

    # Filter to high-confidence leads only
    high_confidence_leads = [l for l in personalized_leads if l.get("confidence") == "high"]
    print(f"\nFiltered to {len(high_confidence_leads)} high-confidence leads")

    # Save output
    location_slug = args.location.lower().replace(' ', '_').replace(',', '')
    city_slug = f"_{args.city.lower().replace(' ', '_')}" if args.city else ""
    output_path = args.output or f".tmp/leads/{location_slug}{city_slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "filters": {
            "industry": args.industry,
            "location": args.location,
            "city": args.city,
            "job_titles": args.job_titles,
            "seniority": args.seniority,
            "sizes": args.sizes,
            "min_revenue": args.min_revenue
        },
        "total_scraped": len(leads),
        "high_confidence": len(high_confidence_leads),
        "leads": high_confidence_leads
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"\nSaved leads to: {output_path}")

    # Steps 4-5: Instantly campaign and upload
    if not args.skip_instantly and high_confidence_leads:
        campaign_id = create_instantly_campaign(campaign_name)

        if campaign_id:
            upload_results = upload_leads_to_instantly(campaign_id, high_confidence_leads)

            print("\n" + "="*60)
            print("PIPELINE COMPLETE")
            print("="*60)
            print(f"Campaign: {campaign_name}")
            print(f"Campaign ID: {campaign_id}")
            print(f"Leads uploaded: {upload_results['success']}")
            print(f"Personalization set: {upload_results['updated']}")
            print(f"\nNext steps:")
            print(f"  1. Review campaign at https://app.instantly.ai")
            print(f"  2. Add sending accounts")
            print(f"  3. Activate when ready")
    else:
        print("\n" + "="*60)
        print("LEAD GENERATION COMPLETE")
        print("="*60)
        print(f"Leads saved to: {output_path}")
        print(f"High-confidence leads: {len(high_confidence_leads)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
