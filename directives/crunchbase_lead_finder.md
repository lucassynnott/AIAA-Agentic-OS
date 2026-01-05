# Crunchbase Startup Lead Finder

## What This Workflow Is
This workflow finds recently funded startups from Crunchbase based on funding stage, amount, and industry, then enriches with decision-maker contacts.

## What It Does
1. Searches Crunchbase for recently funded companies
2. Filters by stage, amount, industry, location
3. Extracts company and founder data
4. Enriches with verified email contacts
5. Exports to Google Sheets

## Prerequisites

### Required API Keys (add to .env)
```
CRUNCHBASE_API_KEY=your_crunchbase_key    # Or use APIFY_API_TOKEN
APOLLO_API_KEY=your_apollo_key            # For email enrichment
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Crunchbase Pro OR Apify scraper
- Email enrichment service

### Installation
```bash
pip install requests apify-client google-api-python-client
```

## How to Run

### Step 1: Search Funded Companies
```bash
python3 execution/scrape_crunchbase.py \
  --stage "Series A,Series B" \
  --min_funding 1000000 \
  --industry "SaaS,FinTech" \
  --days 30 \
  --output .tmp/funded_companies.json
```

### Step 2: Enrich Contacts
```bash
python3 execution/enrich_contacts.py \
  .tmp/funded_companies.json \
  --output .tmp/enriched.json
```

### Step 3: Export to Sheet
```bash
python3 execution/update_sheet.py .tmp/enriched.json --title "Funded Startups - $(date +%Y-%m-%d)"
```

### Quick One-Liner
```bash
python3 execution/scrape_crunchbase.py --stage "Series A" --days 30 && \
python3 execution/enrich_contacts.py .tmp/funded_companies.json && \
python3 execution/update_sheet.py .tmp/enriched.json
```

## Goal
Find recently funded startups and extract decision-maker contacts for outreach.

## Inputs
- **Funding Stage**: Seed, Series A, B, C+
- **Funding Amount**: Min/max range
- **Industry**: Target sectors
- **Location**: Geographic filter
- **Timeframe**: Funding recency (last 30/60/90 days)

## Process

### 1. Search Crunchbase
```bash
python3 execution/scrape_crunchbase.py \
  --stage "Series A,Series B" \
  --min_funding 1000000 \
  --industry "SaaS,FinTech" \
  --days 30 \
  --output .tmp/funded_companies.json
```

### 2. Data Extracted
- Company name
- Funding amount
- Funding date
- Investors
- Company description
- Website
- Employee count
- Founders/executives

### 3. Enrich Contacts
```bash
python3 execution/enrich_contacts.py .tmp/funded_companies.json
```

### 4. Outreach Angle
```
Subject: Congrats on the Series A

Hi [NAME],

Saw [COMPANY] just raised [AMOUNT] from [INVESTOR] - congrats!

As you scale [specific area], we help companies like yours [value prop].

Worth a quick chat?
```

## Why This Works
- Funded = budget available
- Growth mode = buying tools/services
- Timely = relevant conversation starter

## Integrations
- Crunchbase API or Apify scraper
- Email enrichment (Apollo, Hunter)

## Cost
- Crunchbase Pro: $49-99/mo
- Alternative: Apify scraper ~$0.05/company
