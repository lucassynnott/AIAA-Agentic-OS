# Job Board Lead Finder

## What This Workflow Is
This workflow scrapes job boards to find companies hiring for roles that indicate buying intent (e.g., hiring SDRs = need lead generation help), then enriches with decision maker contacts.

## What It Does
1. Scrapes job listings from LinkedIn, Indeed, Glassdoor
2. Filters by job titles and keywords
3. Extracts company information
4. Enriches with decision maker contacts
5. Scores leads by hiring signals

## Prerequisites

### Required API Keys (add to .env)
```
APIFY_API_TOKEN=your_apify_token          # For job scraping
APOLLO_API_KEY=your_apollo_key            # For enrichment
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Apify account
- Apollo or Hunter for enrichment

### Installation
```bash
pip install apify-client requests google-api-python-client
```

## How to Run

### Step 1: Scrape Job Listings
```bash
python3 execution/scrape_job_boards.py \
  --titles "SDR,BDR,Sales Development" \
  --keywords "cold email,outbound" \
  --location "United States" \
  --sources "linkedin,indeed" \
  --output .tmp/jobs.json
```

### Step 2: Extract Company Data
```bash
python3 execution/extract_company_info.py \
  --input .tmp/jobs.json \
  --enrich true \
  --output .tmp/companies.json
```

### Step 3: Export to Sheet
```bash
python3 execution/update_sheet.py \
  .tmp/companies.json \
  --title "Job Board Leads - $(date +%Y-%m-%d)"
```

### Quick One-Liner
```bash
python3 execution/scrape_job_boards.py --titles "SDR" --location "US" && \
python3 execution/extract_company_info.py --input .tmp/jobs.json --enrich true && \
python3 execution/update_sheet.py .tmp/companies.json --title "Job Board Leads"
```

### Daily Automated Scrape (Cron)
```bash
0 7 * * * cd /path/to/project && python3 execution/run_job_scraper.py --alert_on_new
```

## Goal
Find companies actively hiring for roles that indicate buying intent for your services.

## Inputs
- **Job Titles**: Roles to monitor (e.g., "SDR", "Marketing Manager")
- **Keywords**: Job description keywords (e.g., "cold email", "lead generation")
- **Locations**: Geographic filter
- **Company Size**: Employee count filter

## Hiring = Buying Signal Logic
| They're Hiring | They Likely Need |
|----------------|------------------|
| SDR/BDR | Lead generation, sales tools |
| Marketing Manager | Content, ads, SEO |
| Demand Gen | Lead gen, marketing automation |
| RevOps | CRM, sales ops, data |
| Content Writer | Content services, SEO |
| Growth Marketer | Paid ads, funnels |

## Tools/Scripts
- `execution/scrape_job_boards.py` - Job listing scraper
- `execution/extract_company_info.py` - Company enrichment

## Process

### 1. Scrape Job Listings
```bash
python3 execution/scrape_job_boards.py \
  --titles "SDR,BDR,Sales Development" \
  --keywords "cold email,outbound" \
  --location "United States" \
  --sources "linkedin,indeed,glassdoor" \
  --output .tmp/jobs.json
```

### 2. Extract Company Data
For each job listing:
- Company name
- Company website
- Job posting URL
- Date posted
- Job requirements (tech stack clues)

### 3. Enrich Companies
```bash
python3 execution/extract_company_info.py \
  --input .tmp/jobs.json \
  --output .tmp/companies.json
```

Adds:
- Company size
- Industry
- Funding stage
- Decision maker contacts

### 4. Score & Prioritize
| Signal | Score |
|--------|-------|
| Multiple relevant job posts | +20 |
| Recent funding | +15 |
| Fast-growing (hiring 5+ roles) | +10 |
| Tech stack match | +10 |
| Decision maker identified | +10 |

### 5. Output to Sheet
```bash
python3 execution/update_sheet.py .tmp/companies.json --title "Job Board Leads - [DATE]"
```

## Output Schema
| Column | Description |
|--------|-------------|
| company_name | Company |
| website | Domain |
| job_title | Role they're hiring |
| job_url | Posting link |
| posted_date | When listed |
| company_size | Employee count |
| industry | Business category |
| score | Lead score |
| contact_name | Decision maker |
| contact_email | Email |

## Job Boards to Monitor
- LinkedIn Jobs
- Indeed
- Glassdoor
- AngelList/Wellfound
- BuiltIn
- Y Combinator Jobs

## Automation
- Daily scrape for new postings
- Alert on high-score leads
- Auto-add to outreach sequence

## Integrations Required
- Apify (job board scrapers)
- Enrichment API (Apollo, Hunter)
- Google Sheets

## Cost Estimate
- Scraping: ~$0.01/job
- Enrichment: ~$0.03/company
- **100 leads: ~$5**

## Outreach Angle
```
Subject: Saw you're hiring [ROLE]

Hi [NAME],

Noticed [COMPANY] is scaling the sales team - congrats on the growth.

We help companies like yours [VALUE PROP] so new hires can 
hit quota faster.

[CASE STUDY/PROOF]

Worth a quick chat?
```
