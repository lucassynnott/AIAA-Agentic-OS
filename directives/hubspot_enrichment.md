# HubSpot Lead Enrichment

## What This Workflow Is
This workflow enriches HubSpot contacts with data from Apollo, Clearbit, or People Data Labs including job titles, company info, and verified contact details.

## What It Does
1. Exports contacts from HubSpot list
2. Enriches via Apollo/Clearbit/PDL
3. Adds title, company size, industry
4. Updates HubSpot with new fields
5. Generates quality report

## Prerequisites

### Required API Keys (add to .env)
```
HUBSPOT_API_KEY=your_hubspot_key
APOLLO_API_KEY=your_apollo_key            # Or CLEARBIT/PDL
```

### Required Tools
- Python 3.10+
- HubSpot account
- Enrichment provider

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Export HubSpot Contacts
```bash
python3 execution/hubspot_export.py \
  --list_id "[LIST_ID]" \
  --output .tmp/contacts.json
```

### Step 2: Enrich Data
```bash
python3 execution/enrich_hubspot.py \
  --contacts .tmp/contacts.json \
  --provider apollo \
  --output .tmp/enriched.json
```

### Step 3: Update HubSpot
```bash
python3 execution/hubspot_update.py \
  --contacts .tmp/enriched.json \
  --fields "title,company_size,industry"
```

### Quick One-Liner
```bash
python3 execution/hubspot_export.py --list_id "[ID]" && \
python3 execution/enrich_hubspot.py --provider apollo && \
python3 execution/hubspot_update.py
```

## Goal
Automatically enrich HubSpot contacts with additional data from external sources.

## Inputs
- **HubSpot List**: Contacts to enrich
- **Enrichment Sources**: Apollo, Clearbit, People Data Labs
- **Fields to Add**: Title, company size, industry, etc.

## Process

### 1. Export HubSpot Contacts
```bash
python3 execution/hubspot_export.py \
  --list_id "[LIST_ID]" \
  --output .tmp/contacts.json
```

### 2. Enrich Data
```bash
python3 execution/enrich_hubspot.py \
  --contacts .tmp/contacts.json \
  --provider apollo \
  --output .tmp/enriched.json
```

### 3. Fields to Enrich

**Person Data:**
- Job title (accurate)
- LinkedIn URL
- Phone number
- Verified email

**Company Data:**
- Industry
- Employee count
- Revenue range
- Funding stage
- Tech stack
- Website

### 4. Update HubSpot
```bash
python3 execution/hubspot_update.py \
  --contacts .tmp/enriched.json \
  --fields "title,company_size,industry"
```

### 5. Enrichment Rules
- Only enrich if field is empty
- Don't overwrite manual entries
- Flag low-confidence data
- Log all changes

### 6. Automation Triggers
- New contact created
- Lead score reaches threshold
- Contact added to list
- Weekly batch job

### 7. Quality Report
```markdown
# Enrichment Report

## Summary
- Contacts processed: 500
- Successfully enriched: 423 (85%)
- No match found: 77 (15%)

## Fields Updated
| Field | Updated | No Data |
|-------|---------|---------|
| Title | 412 | 88 |
| Industry | 398 | 102 |
| Phone | 234 | 266 |
```

## Integrations
- HubSpot API
- Apollo/Clearbit/PDL
- Webhook (real-time)

## Cost
- Enrichment: $0.03-0.10/contact
- HubSpot API: Free
