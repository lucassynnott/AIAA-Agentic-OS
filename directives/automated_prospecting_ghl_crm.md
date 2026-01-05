# Automated Prospecting > GHL CRM

## What This Workflow Is
This workflow automates prospect research and imports enriched leads into GoHighLevel CRM, using Surfe API for email enrichment.

## What It Does
1. Receives form with ICP criteria
2. Searches for matching companies
3. Finds people at those companies
4. Enriches with email via Surfe API
5. Imports contacts to GHL CRM

## Prerequisites

### Required API Keys (add to .env)
```
SURFE_API_KEY=your_surfe_key              # For email enrichment
GHL_API_KEY=your_ghl_key                  # GoHighLevel API
```

### Required Tools
- Python 3.10+
- Surfe account
- GoHighLevel CRM

### Installation
```bash
pip install requests
```

## How to Run

### Via N8N Webhook
Submit form with:
- Industry Research
- Max Employee Count
- Country Code (Alpha-2)
- Name, Email

### Via Python Script
```bash
python3 execution/prospect_to_ghl.py \
  --industry "SaaS" \
  --max_employees 500 \
  --country "US"
```

### Quick One-Liner
```bash
python3 execution/prospect_to_ghl.py --industry "[INDUSTRY]" --country "US"
```

## Goal
[Describe the purpose of this workflow]

## Trigger
- **Type**: Form
- **Node**: Build Prospect Lists

## Inputs
- **Industry Research**: textarea
- **Max Employee Count**: number
- **Country Code (Alpha-2) **: text
- **What is your name?**: text (required)
- **What is your email?**: email (required)

## Integrations Required
- Gmail

## Process
### 1. Search ICP Companies
[Describe what this step does]

### 2. Search People in Companies
[Describe what this step does]

### 3. Prepare JSON Payload Enrichment Request
[Describe what this step does]

### 4. Surfe Bulk Enrichments API
[Describe what this step does]

### 5. Surfe check enrichement status
[Describe what this step does]

### 6. Is enrichment complete ?
[Describe what this step does]

### 7. Wait 3 secondes
[Describe what this step does]

### 8. Extract list of peoples from Surfe API response
[Describe what this step does]

### 9. Gmail
[Describe what this step does]

### 10. prepare JSON PAYLOAD WITH Company Domains
[Describe what this step does]

### 11. Build Prospect Lists
Workflow is triggered via form.

### 12. Set Prospect Data
Data is normalized/transformed for the next step.

### 13. Create or update a contact
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Cold Email Lead Generation Agency/Automated Prospecting _ GHL CRM.json`
Generated on: 2026-01-02