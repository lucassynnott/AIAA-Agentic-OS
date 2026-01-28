# Apify Lead Scraper Workflow

> **Version:** 1.0 | **Actor ID:** IoSHqwTR9YGhzccez
> Scrape B2B leads with comprehensive filtering by company, contact, funding, and revenue criteria.

---

## What This Workflow Is

A lead generation workflow that uses Apify's B2B lead scraping actor to find targeted prospects based on:
- Company attributes (industry, keywords, domain, size, funding, revenue)
- Contact attributes (job title, seniority, location, city)
- Email validation status

## What It Does

1. Accepts search criteria via command line arguments or JSON config
2. Calls Apify actor `IoSHqwTR9YGhzccez` with the specified filters
3. Retrieves and saves results as JSON and CSV
4. Returns structured lead data for follow-up workflows

---

## Prerequisites

### Required API Keys
```
APIFY_API_TOKEN     # Apify API access
```

### Required Packages
```bash
pip install apify-client python-dotenv
```

### Skill Bibles
- `SKILL_BIBLE_cold_email_mastery.md` - For follow-up outreach
- `SKILL_BIBLE_lead_gen_strategies.md` - For targeting strategy

---

## How to Run

### Basic Usage
```bash
python3 execution/scrape_leads_apify.py --fetch_count 50 --contact_job_title "CEO" --contact_location "united states"
```

### Full Example with All Filters
```bash
python3 execution/scrape_leads_apify.py \
    --fetch_count 100 \
    --contact_job_title "CEO" "Founder" "CTO" \
    --contact_location "united states" \
    --contact_city "San Francisco" "New York" \
    --company_industry "information technology & services" "marketing & advertising" \
    --company_keywords "SaaS" "AI" \
    --company_not_industry "retail" "manufacturing" \
    --seniority_level "founder" "c_suite" \
    --functional_level "c_suite" \
    --funding "seed" "series_a" "series_b" \
    --size "11-20" "21-50" "51-100" \
    --min_revenue "100K" \
    --max_revenue "10B" \
    --email_status "validated" \
    --output_prefix "saas_founders"
```

### Using JSON Config File
```bash
python3 execution/scrape_leads_apify.py --config my_search.json
```

---

## Inputs

### JSON Input Schema

This is the complete input structure for the Apify actor:

```json
{
    "company_domain": ["www.google.com"],
    "company_industry": [
        "information technology & services",
        "construction",
        "marketing & advertising",
        "real estate",
        "health, wellness & fitness"
    ],
    "company_keywords": ["SaaS"],
    "company_not_industry": [
        "management consulting",
        "computer software",
        "internet",
        "retail"
    ],
    "company_not_keywords": ["Manufacturing"],
    "contact_city": ["San Francisco"],
    "contact_job_title": ["CEO"],
    "contact_location": ["united states"],
    "contact_not_city": ["Dusseldorf"],
    "contact_not_location": ["germany"],
    "email_status": ["validated", "not_validated", "unknown"],
    "fetch_count": 10,
    "functional_level": ["c_suite"],
    "funding": [
        "seed", "angel", "series_a", "series_b", "series_c",
        "series_d", "series_e", "series_f", "debt_financing",
        "convertible_note", "private_equity_round", "other_round",
        "venture_round"
    ],
    "max_revenue": "10B",
    "min_revenue": "100K",
    "seniority_level": ["founder"],
    "size": [
        "1-10", "11-20", "21-50", "51-100", "101-200", "201-500",
        "501-1000", "1001-2000", "2001-5000", "5001-10000",
        "10001-20000", "20001-50000", "50000+"
    ]
}
```

### Command Line Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `--fetch_count` | int | No (default: 10) | Number of leads to fetch |
| `--config` | string | No | Path to JSON config file |
| `--output_prefix` | string | No (default: "leads") | Prefix for output files |

#### Company Filters
| Argument | Type | Description |
|----------|------|-------------|
| `--company_domain` | list | Specific company domains to include |
| `--company_industry` | list | Industries to include |
| `--company_keywords` | list | Keywords companies should match |
| `--company_not_industry` | list | Industries to exclude |
| `--company_not_keywords` | list | Keywords to exclude |

#### Contact Filters
| Argument | Type | Description |
|----------|------|-------------|
| `--contact_job_title` | list | Job titles to target |
| `--contact_location` | list | Countries/regions to include |
| `--contact_city` | list | Cities to include |
| `--contact_not_location` | list | Countries/regions to exclude |
| `--contact_not_city` | list | Cities to exclude |

#### Level Filters
| Argument | Type | Valid Values |
|----------|------|--------------|
| `--seniority_level` | list | founder, c_suite, partner, vp, head, director, manager, senior, entry, training, unpaid |
| `--functional_level` | list | c_suite, vp, director, manager, senior, entry, training, partner, owner, unpaid |

#### Company Characteristics
| Argument | Type | Description |
|----------|------|-------------|
| `--size` | list | Company size ranges (1-10, 11-20, 21-50, etc.) |
| `--funding` | list | Funding stages (seed, angel, series_a, etc.) |
| `--min_revenue` | string | Minimum revenue (100K, 1M, 10B) |
| `--max_revenue` | string | Maximum revenue (100K, 1M, 10B) |

#### Email Filter
| Argument | Type | Valid Values |
|----------|------|--------------|
| `--email_status` | list | validated, not_validated, unknown |

---

## Process

### Step 1: Configure Search Criteria
Either pass arguments directly or create a JSON config file with your target criteria.

### Step 2: Execute Scrape
Run the script. It will:
1. Validate API token
2. Build the request payload
3. Call Apify actor `IoSHqwTR9YGhzccez`
4. Wait for completion

### Step 3: Retrieve Results
Results are automatically:
- Saved to `.tmp/leads/<prefix>_<timestamp>.json`
- Saved to `.tmp/leads/<prefix>_<timestamp>.csv`
- Displayed with sample lead preview

---

## Outputs

| File | Format | Location |
|------|--------|----------|
| Lead data (JSON) | JSON array | `.tmp/leads/<prefix>_<timestamp>.json` |
| Lead data (CSV) | CSV | `.tmp/leads/<prefix>_<timestamp>.csv` |

### Output Fields (typical)
- `first_name`, `last_name`
- `email`, `email_status`
- `title`, `seniority`
- `company_name`, `company_website`
- `linkedin_url`
- `city`, `state`, `country`
- `company_size`, `company_industry`

---

## Quality Gates

- [ ] APIFY_API_TOKEN is set in .env
- [ ] At least one filter criterion is provided
- [ ] fetch_count is reasonable (< 1000 for cost control)
- [ ] Results contain expected fields
- [ ] Email validation status matches request

---

## Edge Cases

| Scenario | Solution |
|----------|----------|
| No results returned | Broaden filters (remove exclusions, expand locations) |
| API rate limit | Wait and retry, or reduce fetch_count |
| Invalid filter values | Script validates against allowed values |
| Empty email fields | Check email_status filter; use "unknown" to include more |

---

## Related Directives

- `cold_email_scriptwriter.md` - Generate outreach for scraped leads
- `company_market_research.md` - Deep dive on specific companies
- `meeting_prep.md` - Prepare for calls with leads

---

## Cost Considerations

Apify charges per result. Monitor usage:
- Start with small `fetch_count` to test filters
- Use specific filters to reduce wasted results
- Track monthly spend in Apify dashboard

---

## Example Config Files

### SaaS Founders in US
```json
{
    "contact_job_title": ["CEO", "Founder", "Co-Founder"],
    "contact_location": ["united states"],
    "company_keywords": ["SaaS", "Software"],
    "seniority_level": ["founder", "c_suite"],
    "funding": ["seed", "series_a", "series_b"],
    "size": ["11-20", "21-50", "51-100"],
    "email_status": ["validated"],
    "fetch_count": 100
}
```

### Marketing Agency Decision Makers
```json
{
    "contact_job_title": ["CEO", "Owner", "Managing Director"],
    "contact_location": ["united states", "united kingdom"],
    "company_industry": ["marketing & advertising"],
    "seniority_level": ["founder", "c_suite", "owner"],
    "size": ["1-10", "11-20", "21-50"],
    "email_status": ["validated", "not_validated"],
    "fetch_count": 200
}
```

### Real Estate Professionals
```json
{
    "contact_job_title": ["Broker", "Agent", "Owner"],
    "contact_location": ["united states"],
    "contact_city": ["Los Angeles", "Miami", "New York"],
    "company_industry": ["real estate"],
    "email_status": ["validated"],
    "fetch_count": 150
}
```
