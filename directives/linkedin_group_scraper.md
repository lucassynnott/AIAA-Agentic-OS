# LinkedIn Group Member Extractor

## What This Workflow Is
This workflow extracts member profiles from LinkedIn groups with filtering by job title, company, and location.

## What It Does
1. Takes LinkedIn group URL
2. Scrapes member profiles
3. Filters by criteria (titles, companies)
4. Extracts name, title, company, URL
5. Outputs to CSV/JSON

## Prerequisites

### Required API Keys (add to .env)
```
PHANTOMBUSTER_API_KEY=your_key            # Or scraping tool
```

### Required Tools
- Python 3.10+
- LinkedIn scraping tool

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Scrape Group Members
```bash
python3 execution/scrape_linkedin_group.py \
  --group_url "[GROUP_URL]" \
  --filters '{"titles": ["CEO", "Founder"]}' \
  --max_members 500 \
  --output .tmp/group_members.json
```

### Quick One-Liner
```bash
python3 execution/scrape_linkedin_group.py --group_url "[URL]" --max_members 500
```

## Goal
Extract members from LinkedIn groups for targeted outreach.

## Inputs
- **Group URL**: LinkedIn group to scrape
- **Filters**: Job titles, companies, locations
- **Lead Count**: Number of members to extract

## Process

### 1. Access Group
```bash
python3 execution/scrape_linkedin_group.py \
  --group_url "[GROUP_URL]" \
  --filters '{"titles": ["CEO", "Founder"]}' \
  --max_members 500 \
  --output .tmp/group_members.json
```

### 2. Data Extracted
- Full name
- Job title
- Company
- Location
- LinkedIn URL
- Profile headline
- Connection status

### 3. Filtering Options
- By job title keywords
- By company size
- By location
- By activity level
- Premium members only

### 4. Enrichment
```bash
python3 execution/enrich_linkedin_leads.py \
  --input .tmp/group_members.json \
  --add_emails true \
  --output .tmp/enriched_members.json
```

### 5. Outreach Angle
```
Subject: Fellow [GROUP NAME] member

Hi [NAME],

Noticed we're both in [GROUP NAME] - great group 
for [TOPIC]!

I saw your work at [COMPANY] and thought you might 
be interested in [VALUE PROP].

[SPECIFIC RELEVANCE]

Worth connecting?
```

### 6. Best Practices
- Join group first (legitimacy)
- Reference group in outreach
- Don't mass-spam group members
- Engage in group first if possible

## Compliance
- Respect LinkedIn limits
- Use compliant tools
- Don't scrape private info
- Personalize outreach

## Integrations
- Apify LinkedIn Group Scraper
- Email enrichment (Hunter, Apollo)
- Google Sheets

## Cost
- Scraping: ~$0.05/member
- Enrichment: ~$0.03/email
