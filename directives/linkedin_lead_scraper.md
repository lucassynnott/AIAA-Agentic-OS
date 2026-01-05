# LinkedIn Lead Scraper + Email Finder

## What This Workflow Is
This workflow automates the process of finding B2B leads on LinkedIn by scraping public profile data based on your targeting criteria, then enriching those leads with verified email addresses for cold outreach campaigns.

## What It Does
1. Searches LinkedIn for profiles matching your ideal customer profile (job titles, industries, locations)
2. Extracts public profile data (name, title, company, location, LinkedIn URL)
3. Enriches leads with verified business email addresses using email finder APIs
4. Exports the complete lead list to Google Sheets for use in outreach campaigns
5. Handles deduplication and data validation automatically

## Prerequisites

### Required API Keys (add to .env)
```
APIFY_API_TOKEN=your_apify_token          # Get from console.apify.com
HUNTER_API_KEY=your_hunter_key            # Get from hunter.io (or use Apollo)
APOLLO_API_KEY=your_apollo_key            # Alternative to Hunter
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Google OAuth credentials (`credentials.json`)
- Active Apify account with credits

### Installation
```bash
pip install apify-client google-api-python-client gspread
```

## How to Run

### Step 1: Define Your Target Audience
Decide on your ICP criteria:
- Job titles (e.g., "CEO", "VP Sales", "Marketing Director")
- Industries (e.g., "SaaS", "Marketing Agency", "E-commerce")
- Locations (e.g., "United States", "United Kingdom")
- Company size (e.g., "11-50", "51-200" employees)

### Step 2: Test Scrape (Recommended)
Run a small test to verify quality:
```bash
python3 execution/scrape_linkedin_apify.py \
  --titles "CEO,Founder" \
  --industries "SaaS" \
  --locations "United States" \
  --company_size "11-50" \
  --max_items 25 \
  --output .tmp/test_leads.json
```

Review `.tmp/test_leads.json` - ensure 80%+ match your target criteria.

### Step 3: Full Scrape
```bash
python3 execution/scrape_linkedin_apify.py \
  --titles "CEO,Founder,Marketing Director" \
  --industries "SaaS,Marketing Agency" \
  --locations "United States" \
  --company_size "11-50" \
  --max_items 500 \
  --output .tmp/linkedin_leads.json
```

### Step 4: Enrich with Emails
```bash
python3 execution/enrich_emails.py \
  .tmp/linkedin_leads.json \
  --provider hunter \
  --output .tmp/enriched_leads.json
```

### Step 5: Export to Google Sheets
```bash
python3 execution/update_sheet.py \
  .tmp/enriched_leads.json \
  --title "LinkedIn Leads - $(date +%Y-%m-%d)"
```

### Quick One-Liner (After Testing)
```bash
python3 execution/scrape_linkedin_apify.py --titles "CEO" --industries "SaaS" --locations "US" --max_items 500 && \
python3 execution/enrich_emails.py .tmp/linkedin_leads.json && \
python3 execution/update_sheet.py .tmp/enriched_leads.json --title "LinkedIn Leads"
```

## Goal
Scrape LinkedIn profiles by job title, industry, and location, then enrich with verified emails for cold outreach.

## Inputs
- **Job Titles**: Target roles (e.g., "CEO", "Marketing Director")
- **Industries**: Target industries (e.g., "SaaS", "Marketing Agency")
- **Locations**: Geographic targets (e.g., "United States", "London")
- **Company Size**: Employee count filter (e.g., "11-50", "51-200")
- **Lead Count**: Number of leads to scrape

## Tools/Scripts
- `execution/scrape_linkedin_apify.py` - LinkedIn profile scraper via Apify
- `execution/enrich_emails.py` - Email enrichment
- `execution/update_sheet.py` - Google Sheets export

## Process

### 1. Configure Search Parameters
```bash
python3 execution/scrape_linkedin_apify.py \
  --titles "CEO,Founder,Marketing Director" \
  --industries "SaaS,Marketing Agency" \
  --locations "United States" \
  --company_size "11-50" \
  --max_items 500
```

### 2. Test Scrape (25 profiles)
Run small batch to verify quality:
- Check job titles match
- Verify company industries
- Confirm location accuracy

### 3. Full Scrape
Execute full scrape with verified parameters.

Output fields:
- First Name, Last Name
- Job Title
- Company Name
- Company Website
- LinkedIn URL
- Location

### 4. Email Enrichment
```bash
python3 execution/enrich_emails.py .tmp/linkedin_leads.json --provider hunter
```

Enrichment sources:
- Hunter.io (primary)
- Apollo.io (fallback)
- AnyMailFinder (bulk)

### 5. Export to Google Sheets
```bash
python3 execution/update_sheet.py .tmp/enriched_leads.json --title "LinkedIn Leads - [DATE]"
```

## Output Schema
| Column | Description |
|--------|-------------|
| first_name | Contact first name |
| last_name | Contact last name |
| title | Job title |
| company | Company name |
| website | Company domain |
| linkedin_url | Profile URL |
| email | Verified email |
| location | City/Country |

## Integrations Required
- Apify (LinkedIn scraper)
- Hunter.io or Apollo.io (email enrichment)
- Google Sheets API

## Cost Estimate
- Apify: ~$0.02/profile
- Email enrichment: ~$0.03/email
- **500 leads: ~$25**

## Edge Cases
- LinkedIn rate limits: Use Apify's managed proxies
- Low email match rate: Try multiple enrichment providers
- Duplicate profiles: Dedupe by LinkedIn URL

## Compliance
- Respect LinkedIn ToS by using Apify's compliant scraper
- Only scrape public profile data
- Honor opt-out requests
