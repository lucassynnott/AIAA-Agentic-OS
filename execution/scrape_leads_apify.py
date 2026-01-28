#!/usr/bin/env python3
"""
Apify Lead Scraper - Actor ID: IoSHqwTR9YGhzccez

Scrapes B2B leads using the specified Apify actor with comprehensive filtering.
Supports company, contact, funding, and revenue filters.

IMPORTANT - Location Format:
    --contact_location requires country or state-level values (NOT city names):
    - Countries: "united states", "germany", "united kingdom", "canada"
    - US States: "california, us", "new york, us", "texas, us", "florida, us"

    For city-level filtering, use --contact_city:
    - Cities: "San Francisco", "New York", "Los Angeles", "Chicago"

Usage:
    # Basic usage with defaults
    python3 execution/scrape_leads_apify.py --fetch_count 50

    # SaaS founders in San Francisco, 25-150 employees, $1M+ revenue
    python3 execution/scrape_leads_apify.py \
        --fetch_count 25 \
        --contact_job_title "CEO" "Founder" "Co-Founder" \
        --contact_location "california, us" \
        --contact_city "San Francisco" \
        --company_keywords "SaaS" \
        --seniority_level "founder" "c_suite" \
        --size "21-50" "51-100" "101-200" \
        --min_revenue "1M" \
        --output_prefix "sf_saas_founders"

    # Full example with all filters
    python3 execution/scrape_leads_apify.py \
        --fetch_count 100 \
        --contact_job_title "CEO" "Founder" \
        --contact_location "united states" \
        --company_industry "information technology & services" "marketing & advertising" \
        --company_keywords "SaaS" \
        --seniority_level "founder" "c_suite" \
        --min_revenue "100K" \
        --max_revenue "10B"

    # Load from JSON config file
    python3 execution/scrape_leads_apify.py --config my_search.json
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from apify_client import ApifyClient

# Load environment variables
load_dotenv()

# The specific Apify actor for lead scraping
ACTOR_ID = "IoSHqwTR9YGhzccez"

# Default input structure (based on user-provided schema)
DEFAULT_INPUT = {
    "company_domain": [],
    "company_industry": [],
    "company_keywords": [],
    "company_not_industry": [],
    "company_not_keywords": [],
    "contact_city": [],
    "contact_job_title": [],
    "contact_location": [],
    "contact_not_city": [],
    "contact_not_location": [],
    "email_status": ["validated", "not_validated", "unknown"],
    "fetch_count": 10,
    "functional_level": [],
    "funding": [],
    "max_revenue": "",
    "min_revenue": "",
    "seniority_level": [],
    "size": []
}

# Valid options for enum fields
VALID_EMAIL_STATUS = ["validated", "not_validated", "unknown"]
VALID_FUNCTIONAL_LEVELS = ["c_suite", "vp", "director", "manager", "senior", "entry", "training", "partner", "owner", "unpaid"]
VALID_SENIORITY_LEVELS = ["founder", "c_suite", "partner", "vp", "head", "director", "manager", "senior", "entry", "training", "unpaid"]
VALID_FUNDING = ["seed", "angel", "series_a", "series_b", "series_c", "series_d", "series_e", "series_f",
                 "debt_financing", "convertible_note", "private_equity_round", "other_round", "venture_round"]
VALID_SIZES = ["1-10", "11-20", "21-50", "51-100", "101-200", "201-500", "501-1000", "1001-2000",
               "2001-5000", "5001-10000", "10001-20000", "20001-50000", "50000+"]


def scrape_leads(input_config: dict) -> list:
    """
    Run the Apify actor to scrape leads.

    Args:
        input_config: Dictionary matching the Apify actor input schema

    Returns:
        List of lead results or empty list on failure
    """
    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        print("Error: APIFY_API_TOKEN not found in .env", file=sys.stderr)
        return []

    client = ApifyClient(api_token)

    # Clean up the input - remove empty arrays and empty strings
    clean_input = {}
    for key, value in input_config.items():
        if isinstance(value, list) and len(value) > 0:
            clean_input[key] = value
        elif isinstance(value, str) and value:
            clean_input[key] = value
        elif isinstance(value, int):
            clean_input[key] = value

    print(f"Starting lead scrape with actor {ACTOR_ID}...")
    print(f"Configuration: {json.dumps(clean_input, indent=2)}")

    try:
        # Run the actor and wait for it to finish
        run = client.actor(ACTOR_ID).call(run_input=clean_input)
    except Exception as e:
        print(f"Error running actor: {e}", file=sys.stderr)
        return []

    if not run:
        print("Error: Actor run failed to start", file=sys.stderr)
        return []

    print(f"Scrape finished. Run ID: {run.get('id')}")
    print(f"Fetching results from dataset {run['defaultDatasetId']}...")

    # Fetch results from the actor's default dataset
    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)

    return results


def save_results(results: list, prefix: str = "leads") -> str:
    """
    Save results to JSON and CSV files.

    Args:
        results: List of lead dictionaries
        prefix: Prefix for the output filename

    Returns:
        Path to the saved JSON file
    """
    if not results:
        print("No results to save.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(".tmp/leads")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON
    json_file = output_dir / f"{prefix}_{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"JSON results saved to {json_file}")

    # Save CSV for easy viewing
    csv_file = output_dir / f"{prefix}_{timestamp}.csv"
    if results:
        # Get all unique keys from results
        all_keys = set()
        for item in results:
            all_keys.update(item.keys())

        # Prioritize common fields
        priority_fields = ['first_name', 'last_name', 'email', 'title', 'company_name',
                          'company_website', 'linkedin_url', 'city', 'state', 'country']
        headers = [f for f in priority_fields if f in all_keys]
        headers.extend([k for k in sorted(all_keys) if k not in headers])

        with open(csv_file, "w") as f:
            # Write header
            f.write(",".join(headers) + "\n")
            # Write rows
            for item in results:
                row = []
                for h in headers:
                    val = str(item.get(h, "")).replace(",", ";").replace("\n", " ")
                    row.append(f'"{val}"')
                f.write(",".join(row) + "\n")
        print(f"CSV results saved to {csv_file}")

    return str(json_file)


def build_input_from_args(args) -> dict:
    """
    Build the Apify input configuration from command line arguments.
    """
    config = DEFAULT_INPUT.copy()

    # Company filters
    if args.company_domain:
        config["company_domain"] = args.company_domain
    if args.company_industry:
        config["company_industry"] = args.company_industry
    if args.company_keywords:
        config["company_keywords"] = args.company_keywords
    if args.company_not_industry:
        config["company_not_industry"] = args.company_not_industry
    if args.company_not_keywords:
        config["company_not_keywords"] = args.company_not_keywords

    # Contact filters
    if args.contact_city:
        config["contact_city"] = args.contact_city
    if args.contact_job_title:
        config["contact_job_title"] = args.contact_job_title
    if args.contact_location:
        config["contact_location"] = args.contact_location
    if args.contact_not_city:
        config["contact_not_city"] = args.contact_not_city
    if args.contact_not_location:
        config["contact_not_location"] = args.contact_not_location

    # Email and seniority
    if args.email_status:
        config["email_status"] = args.email_status
    if args.functional_level:
        config["functional_level"] = args.functional_level
    if args.seniority_level:
        config["seniority_level"] = args.seniority_level

    # Company size and funding
    if args.size:
        config["size"] = args.size
    if args.funding:
        config["funding"] = args.funding

    # Revenue
    if args.min_revenue:
        config["min_revenue"] = args.min_revenue
    if args.max_revenue:
        config["max_revenue"] = args.max_revenue

    # Count
    config["fetch_count"] = args.fetch_count

    return config


def main():
    parser = argparse.ArgumentParser(
        description="Scrape B2B leads using Apify actor IoSHqwTR9YGhzccez",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic search for CEOs in the US
    python3 execution/scrape_leads_apify.py --fetch_count 50 --contact_job_title "CEO" --contact_location "united states"

    # SaaS companies with funding
    python3 execution/scrape_leads_apify.py --fetch_count 100 --company_keywords "SaaS" --funding seed series_a series_b

    # Load from config file
    python3 execution/scrape_leads_apify.py --config search_config.json
        """
    )

    # Config file option
    parser.add_argument("--config", type=str, help="Path to JSON config file with full input schema")

    # Company filters
    parser.add_argument("--company_domain", nargs='+', help="Company domains to include (e.g., google.com)")
    parser.add_argument("--company_industry", nargs='+', help="Industries to include")
    parser.add_argument("--company_keywords", nargs='+', help="Company keywords to match")
    parser.add_argument("--company_not_industry", nargs='+', help="Industries to exclude")
    parser.add_argument("--company_not_keywords", nargs='+', help="Company keywords to exclude")

    # Contact filters
    parser.add_argument("--contact_city", nargs='+', help="Cities to include")
    parser.add_argument("--contact_job_title", nargs='+', help="Job titles to target (e.g., CEO Founder)")
    parser.add_argument("--contact_location", nargs='+', help="Locations/countries to include")
    parser.add_argument("--contact_not_city", nargs='+', help="Cities to exclude")
    parser.add_argument("--contact_not_location", nargs='+', help="Locations to exclude")

    # Email and level filters
    parser.add_argument("--email_status", nargs='+', choices=VALID_EMAIL_STATUS,
                       default=["validated", "not_validated", "unknown"],
                       help="Email validation status filter")
    parser.add_argument("--functional_level", nargs='+', choices=VALID_FUNCTIONAL_LEVELS,
                       help="Functional levels (c_suite, vp, director, etc.)")
    parser.add_argument("--seniority_level", nargs='+', choices=VALID_SENIORITY_LEVELS,
                       help="Seniority levels (founder, c_suite, partner, etc.)")

    # Company characteristics
    parser.add_argument("--size", nargs='+', choices=VALID_SIZES, help="Company size ranges")
    parser.add_argument("--funding", nargs='+', choices=VALID_FUNDING, help="Funding stages")
    parser.add_argument("--min_revenue", type=str, help="Minimum revenue (e.g., 100K, 1M, 10B)")
    parser.add_argument("--max_revenue", type=str, help="Maximum revenue (e.g., 100K, 1M, 10B)")

    # Count and output
    parser.add_argument("--fetch_count", type=int, default=10, help="Number of leads to fetch")
    parser.add_argument("--output_prefix", default="leads", help="Prefix for output files")

    args = parser.parse_args()

    # Build input config
    if args.config:
        # Load from JSON config file
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Error: Config file not found: {args.config}", file=sys.stderr)
            sys.exit(1)
        with open(config_path) as f:
            input_config = json.load(f)
        print(f"Loaded configuration from {args.config}")
    else:
        # Build from command line arguments
        input_config = build_input_from_args(args)

    # Run the scrape
    results = scrape_leads(input_config)

    if results:
        print(f"\nFound {len(results)} leads.")
        saved_file = save_results(results, prefix=args.output_prefix)

        # Print sample of first result
        if results:
            print("\nSample lead:")
            sample = results[0]
            for key in ['first_name', 'last_name', 'email', 'title', 'company_name']:
                if key in sample:
                    print(f"  {key}: {sample[key]}")
    else:
        print("No leads found or error occurred.")
        sys.exit(1)


if __name__ == "__main__":
    main()
