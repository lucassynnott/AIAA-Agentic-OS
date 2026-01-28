#!/usr/bin/env python3
"""
LinkedIn Lead Scraper - Scrape LinkedIn profiles using Apify.

Usage:
    python3 execution/scrape_linkedin_apify.py \
        --titles "CEO,Founder,VP Sales" \
        --industries "SaaS,Marketing Agency" \
        --locations "United States" \
        --company_size "11-50" \
        --max_items 500 \
        --output .tmp/linkedin_leads.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from apify_client import ApifyClient
except ImportError:
    print("Error: apify-client not installed. Run: pip install apify-client")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN") or os.getenv("APIFY_TOKEN")

def check_apify_token():
    """Check for APIFY token and exit if not found."""
    if not APIFY_TOKEN:
        print("Error: APIFY_API_TOKEN required in .env")
        print("Get your token from: https://console.apify.com/account/integrations")
        sys.exit(1)


def scrape_linkedin_profiles(
    titles: list,
    industries: list = None,
    locations: list = None,
    company_size: str = None,
    max_items: int = 100
) -> list:
    """Scrape LinkedIn profiles using Apify LinkedIn Scraper."""
    
    client = ApifyClient(APIFY_TOKEN)
    
    # Build search URLs based on criteria
    search_queries = []
    for title in titles:
        query = f'"{title}"'
        if industries:
            query += f' AND ({" OR ".join(industries)})'
        search_queries.append(query)
    
    # Use LinkedIn Sales Navigator Scraper actor
    actor_id = "anchor/linkedin-people-profiles-search-scraper"
    
    run_input = {
        "searchUrls": [],
        "keywords": titles,
        "locations": locations or ["United States"],
        "maxItems": max_items,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }
    
    # Add company size filter if specified
    if company_size:
        run_input["companySize"] = [company_size]
    
    if industries:
        run_input["industries"] = industries
    
    print(f"  Starting Apify actor: {actor_id}")
    print(f"  Titles: {titles}")
    print(f"  Locations: {locations}")
    print(f"  Max items: {max_items}")
    
    try:
        # Start the actor
        run = client.actor(actor_id).call(run_input=run_input, timeout_secs=600)
        
        # Get results
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append({
                "first_name": item.get("firstName", ""),
                "last_name": item.get("lastName", ""),
                "full_name": item.get("fullName", ""),
                "title": item.get("headline", "") or item.get("title", ""),
                "company": item.get("companyName", "") or item.get("company", ""),
                "company_linkedin": item.get("companyLinkedInUrl", ""),
                "linkedin_url": item.get("linkedInUrl", "") or item.get("profileUrl", ""),
                "location": item.get("location", ""),
                "connections": item.get("connectionsCount", ""),
                "summary": item.get("summary", "")[:200] if item.get("summary") else "",
                "scraped_at": datetime.now().isoformat()
            })
        
        return results
        
    except Exception as e:
        print(f"  Error with primary actor, trying fallback...")
        # Fallback to simpler actor
        return scrape_linkedin_simple(titles, locations, max_items)


def scrape_linkedin_simple(titles: list, locations: list, max_items: int) -> list:
    """Simpler fallback LinkedIn scraper."""
    client = ApifyClient(APIFY_TOKEN)
    
    # Use a simpler search-based actor
    actor_id = "curious_coder/linkedin-search-export"
    
    search_term = " OR ".join([f'"{t}"' for t in titles])
    
    run_input = {
        "searchTerms": [search_term],
        "locations": locations or ["United States"],
        "maxResultsPerSearch": max_items,
        "outputFields": ["name", "title", "company", "location", "linkedinUrl"]
    }
    
    try:
        run = client.actor(actor_id).call(run_input=run_input, timeout_secs=300)
        
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            name_parts = (item.get("name", "") or "").split(" ", 1)
            results.append({
                "first_name": name_parts[0] if name_parts else "",
                "last_name": name_parts[1] if len(name_parts) > 1 else "",
                "full_name": item.get("name", ""),
                "title": item.get("title", ""),
                "company": item.get("company", ""),
                "linkedin_url": item.get("linkedinUrl", ""),
                "location": item.get("location", ""),
                "scraped_at": datetime.now().isoformat()
            })
        
        return results
    except Exception as e:
        print(f"  Fallback also failed: {e}")
        return []


def dedupe_leads(leads: list) -> list:
    """Remove duplicate leads by LinkedIn URL."""
    seen = set()
    unique = []
    for lead in leads:
        url = lead.get("linkedin_url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(lead)
        elif not url:
            unique.append(lead)  # Keep leads without URL
    return unique


def main():
    parser = argparse.ArgumentParser(description="Scrape LinkedIn profiles via Apify")
    parser.add_argument("--titles", "-t", required=True, help="Comma-separated job titles")
    parser.add_argument("--industries", "-i", default="", help="Comma-separated industries")
    parser.add_argument("--locations", "-l", default="United States", help="Comma-separated locations")
    parser.add_argument("--company_size", "-s", default="", help="Company size filter (e.g., 11-50)")
    parser.add_argument("--max_items", "-m", type=int, default=100, help="Max profiles to scrape")
    parser.add_argument("--output", "-o", default=".tmp/linkedin_leads.json", help="Output file")
    
    args = parser.parse_args()
    
    # Check for API token after argparse (so --help works)
    check_apify_token()
    
    titles = [t.strip() for t in args.titles.split(",")]
    industries = [i.strip() for i in args.industries.split(",") if i.strip()] if args.industries else None
    locations = [l.strip() for l in args.locations.split(",")]
    
    print(f"\n🔗 LinkedIn Lead Scraper")
    print(f"   Titles: {titles}")
    print(f"   Industries: {industries or 'All'}")
    print(f"   Locations: {locations}")
    print(f"   Max items: {args.max_items}\n")
    
    # Scrape
    leads = scrape_linkedin_profiles(
        titles=titles,
        industries=industries,
        locations=locations,
        company_size=args.company_size,
        max_items=args.max_items
    )
    
    # Dedupe
    leads = dedupe_leads(leads)
    print(f"\n   ✅ Scraped: {len(leads)} unique profiles")
    
    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "scraped_at": datetime.now().isoformat(),
        "criteria": {
            "titles": titles,
            "industries": industries,
            "locations": locations,
            "company_size": args.company_size
        },
        "total_leads": len(leads),
        "leads": leads
    }
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"   📄 Output: {output_path}")
    
    # Show sample
    if leads:
        print(f"\n   Sample lead:")
        sample = leads[0]
        print(f"      {sample.get('full_name', 'N/A')} - {sample.get('title', 'N/A')}")
        print(f"      {sample.get('company', 'N/A')} | {sample.get('location', 'N/A')}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
