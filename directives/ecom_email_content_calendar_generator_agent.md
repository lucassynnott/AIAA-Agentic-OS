# Ecom Email Content Calendar Generator Agent

## What This Workflow Is
This workflow generates a 30-day email content calendar for e-commerce brands with campaign themes, send dates, and strategies.

## What It Does
1. Receives brand info and key dates via form
2. Researches brand with Perplexity
3. Generates 30-day calendar with AI
4. Creates Google Sheet with schedule
5. Organizes in client folder and notifies Slack

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key
PERPLEXITY_API_KEY=your_perplexity_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- Google OAuth

### Installation
```bash
pip install openai google-api-python-client requests
```

## How to Run

### Via N8N Form (Recommended)
Submit form with:
- Brand Name, Website, Industry/Niche
- Existing Client (yes/no)
- Personalization Notes
- Upcoming Key Dates

### Via Python Script
```bash
python3 execution/generate_email_calendar.py \
  --brand "Brand Name" \
  --website "https://brand.com" \
  --niche "fashion" \
  --key_dates "Black Friday: Nov 29, Cyber Monday: Dec 2"
```

### Quick One-Liner
```bash
python3 execution/generate_email_calendar.py --brand "[BRAND]" --website "[URL]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: Calendar Request Form

## Inputs
- **Brand Name**: text (required)
- **Brand Website**: text (required)
- **Industry / Niche**: text (required)
- **Existing Client?**: dropdown (required)
- **Personalization Notes**: textarea
- **Upcoming Key Dates**: textarea

## Integrations Required
- Google Sheets
- Slack

## Process
### 1. Calendar Request Form
Workflow is triggered via form.

### 2. Format Brand Data
[Describe what this step does]

### 3. Content Calendar AI Agent
AI agent processes the input with the following instructions:
```
=Create a high-converting, comprehensive 30-day email campaign calendar for the following brand, using proven strategies from 8-figure e-commerce email marketers:

BRAND DETAILS:

Brand Name: {{ $json.brandName }}
Website: {{ $json.brandWebsite }}
Industry: {{ $json.industry }}
Existing Client: {{ $json.existingClient }}
Personalization Notes: {{ $json.personalizationNotes }}
Upcoming Key Dates: {{ $json.upcomingKeyDates }}

CALENDAR REQUIREMENTS:

Build a 30-day email campaign calendar starting from tomorrow’s date.
Schedule 3-4 emails per week (never more than one per day), using optimal send days (Tues/Wed/Thurs) and avoiding Mondays/Fridays unless a key date or launch requires it.
Strategically mix campaign types to maximize engagement, education, and conversion—avoid repetitive themes and ensure variety.
Anchor the calendar around the provided upcoming key dates (holidays, launches, sales, etc.), layering supplementary emails (teasers, reminders, last-chance) as needed for those events.
Fill remaining gaps with value-driven, non-discount content (educational, social proof, tips, behind-the-scenes, etc.) to nurture and build trust.
Build a narrative arc across the month—move from education and engagement to conversion and retention, considering the customer journey.
Follow industry-specific best practices for content, frequency, and segmentation.
... [truncated]
```

### 4. Parse Calendar Data
[Describe what this step does]

### 5. Populate Calendar Data
[Describe what this step does]

### 6. Split Calendar Rows
[Describe what this step does]

### 7. Prepare Summary Data
[Describe what this step does]

### 8. Populate Summary
[Describe what this step does]

### 9. OpenRouter Chat Model
[Describe what this step does]

### 10. Message a model in Perplexity
[Describe what this step does]

### 11. Create spreadsheet
[Describe what this step does]

### 12. Create Calendar Sheet
[Describe what this step does]

### 13. Create Summary Sheet
[Describe what this step does]

### 14. Aggregate
[Describe what this step does]

### 15. Edit Fields
Data is normalized/transformed for the next step.

### 16. Check If Returning Client
[Describe what this step does]

### 17. Search for Existing Folder
[Describe what this step does]

### 18. Create New Client Folder
[Describe what this step does]

### 19. Move to Existing Folder
[Describe what this step does]

### 20. Move to New Folder
[Describe what this step does]

### 21. Slack Notification
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Ecom Email Marketing Agency/Ecom Email Content Calendar Generator Agent.json`
Generated on: 2026-01-02