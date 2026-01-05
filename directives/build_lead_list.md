# Build Lead List

## What This Workflow Is
This workflow builds qualified lead lists from multiple sources (Google Maps, LinkedIn, Apollo, custom directories), enriches with emails, and delivers to Google Sheets.

## What It Does
1. Scrapes leads from your chosen source
2. Filters by ICP criteria (industry, location, size)
3. Enriches with verified emails
4. Deduplicates and validates
5. Exports to Google Sheets

## Prerequisites

### Required API Keys (add to .env)
```
APIFY_API_TOKEN=your_apify_token          # For scraping
HUNTER_API_KEY=your_hunter_key            # Or APOLLO_API_KEY for enrichment
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Apify account
- Email enrichment service

### Installation
```bash
pip install apify-client requests google-api-python-client gspread
```

## How to Run

### Step 1: Test Scrape (25 leads)
```bash
python3 execution/scrape_apify.py \
  --industry "SaaS" \
  --location "United States" \
  --max_items 25
```

### Step 2: Full Scrape
```bash
python3 execution/scrape_apify.py \
  --industry "SaaS" \
  --location "United States" \
  --max_items 500
```

### Step 3: Upload to Sheets
```bash
python3 execution/update_sheet.py .tmp/leads.json --title "SaaS Leads - $(date +%Y-%m-%d)"
```

### Step 4: Enrich Emails
```bash
python3 execution/enrich_emails.py "[SHEET_URL]"
```

### Quick One-Liner
```bash
python3 execution/scrape_apify.py --industry "SaaS" --location "US" --max_items 500 && \
python3 execution/update_sheet.py .tmp/leads.json && \
python3 execution/enrich_emails.py "[SHEET_URL]"
```

## Goal
Build a qualified lead list from multiple sources, enrich with contact info, and deliver to Google Sheets. This is a flexible directive that can pull from various data sources based on user needs.

## Inputs
- **Target ICP**: Ideal customer profile description
- **Industry**: Target industry/niche
- **Location**: Geographic targeting
- **Company Size**: Employee count or revenue range (optional)
- **Lead Count**: How many leads needed
- **Data Source**: Where to pull leads from (see options below)

## Data Sources

### Option A: Google Maps / Local Businesses
Best for: Local services, brick-and-mortar, SMBs
```bash
python3 execution/scrape_google_maps.py --query "[INDUSTRY] in [LOCATION]" --max_items [COUNT]
```

### Option B: Apollo/LinkedIn (via Apify)
Best for: B2B, specific job titles, company size filters
```bash
python3 execution/scrape_apify.py --industry "[INDUSTRY]" --location "[LOCATION]" --max_items [COUNT]
```

### Option C: Parallel Multi-Region Scrape
Best for: Large lists (1000+), national campaigns
```bash
python3 execution/scrape_apify_parallel.py --industry "[INDUSTRY]" --location "[LOCATION]" --total_count [COUNT] --strategy regions
```

### Option D: Custom Website Scrape
Best for: Niche directories, specific websites
```bash
python3 execution/scrape_single_site.py --url "[DIRECTORY_URL]" --selectors "[CSS_SELECTORS]"
```

## Process

### 1. Define ICP
Before scraping, clarify with user:
- What problem does your service solve?
- Who is the decision maker? (title/role)
- What company size is ideal?
- Any industries to exclude?

### 2. Test Scrape
Run small test (25-50 leads) to verify quality:
```bash
python3 execution/scrape_apify.py --industry "[INDUSTRY]" --location "[LOCATION]" --max_items 25
```

Review `.tmp/test_leads.json`:
- Are companies in the right industry?
- Are contacts the right role/seniority?
- Is location accurate?

### 3. Full Scrape
Once quality verified, run full scrape with chosen data source.

### 4. LLM Classification (Optional)
For nuanced filtering (e.g., "product companies vs agencies"):
```bash
python3 execution/classify_leads_llm.py .tmp/leads.json --classification_type [TYPE] --output .tmp/classified.json
```

### 5. Upload to Sheets
```bash
python3 execution/update_sheet.py .tmp/leads.json --title "[ICP] Lead List - [DATE]"
```

### 6. Enrich Emails
```bash
python3 execution/enrich_emails.py [SHEET_URL]
```

### 7. Deduplicate (if combining sources)
```bash
python3 execution/dedupe_leads.py [SHEET_URL] --key email
```

## Output Schema
Google Sheet with columns:
| Column | Description |
|--------|-------------|
| company_name | Business name |
| website | Company website |
| industry | Business category |
| location | City, State/Country |
| employee_count | Company size |
| first_name | Contact first name |
| last_name | Contact last name |
| title | Job title |
| email | Verified email |
| phone | Phone number (if available) |
| linkedin_url | LinkedIn profile |
| source | Where lead came from |

## Quality Benchmarks
- **Email enrichment rate**: >60% is good, >80% is excellent
- **Industry match rate**: >80% required
- **Contact accuracy**: Verify 5-10 manually

## Edge Cases
- **No results**: Broaden search terms or try different source
- **Wrong industry**: Refine keywords, use LLM classification
- **Missing emails**: Try alternative enrichment sources
- **Duplicates**: Run dedupe script, check against existing lists

## Cost Estimates
- Apify scraping: ~$0.01 per lead
- Email enrichment: ~$0.02-0.05 per email
- LLM classification: ~$0.0003 per lead
- **Total for 1000 leads**: ~$30-50
