# Cold Email Mass Personalizer

## What This Workflow Is
This workflow takes a cold email script and lead list CSV, then generates personalized icebreakers for each prospect using AI research.

## What It Does
1. Receives email script and lead CSV via form
2. Researches each prospect (LinkedIn, news, etc.)
3. Generates custom icebreaker for each lead
4. Appends personalized line to email body
5. Outputs to Google Sheet

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key
PERPLEXITY_API_KEY=your_perplexity_key    # For prospect research
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
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
- Sender Name, Sender Title
- Cold Email Script Body
- Lead List CSV

### Via Python Script
```bash
python3 execution/personalize_cold_emails.py \
  --leads leads.csv \
  --email_body "Your base email script here..." \
  --output_sheet "[SHEET_URL]"
```

### Quick One-Liner
```bash
python3 execution/personalize_cold_emails.py --leads leads.csv --email_body "[SCRIPT]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: Campaign Request Form

## Inputs
- **Sender Name**: text (required)
- **Sender Title**: text (required)
- **Your Cold Email Script Body**: textarea (required)
- **Upload Lead List CSV**: file (required)

## Integrations Required
- Slack
- Google Sheets

## Process
### 1. Process CSV Upload
[Describe what this step does]

### 2. Normalize CSV Data
Data is normalized/transformed for the next step.

### 3. Prospect Research Agent
AI agent processes the input with the following instructions:
```
=You are an elite prospect research specialist tasked with conducting comprehensive intelligence gathering on a specific business prospect. Your goal is to uncover actionable insights that will enable highly personalized outreach.
TARGET PROSPECT:

Name: {{ $('Normalize CSV Data').first().json.prospect_name }}
Title: {{ $('Normalize CSV Data').first().json.prospect_title }}
Company: {{ $('Normalize CSV Data').first().json.company_name }}
Domain: {{ $('Normalize CSV Data').first().json.company_website }}

RESEARCH OBJECTIVES:
1. PUBLIC ACHIEVEMENTS & CONTENT (Priority #1)
Find recent public-facing activities:

LinkedIn posts, comments, and engagement (last 90 days)
Podcast appearances, interviews, webinar participation
Speaking engagements, conference presentations
Published articles, blog posts, thought leadership content
Social media activity across platforms
Awards, recognition, press mentions
Public milestones, company announcements they've shared

... [truncated]
```

### 4. OpenRouter Chat Model
[Describe what this step does]

### 5. Notify: Returning Customer
[Describe what this step does]

### 6. Loop Over Items
[Describe what this step does]

### 7. Create spreadsheet
[Describe what this step does]

### 8. Format Final Email
Data is normalized/transformed for the next step.

### 9. Update Google Sheet
[Describe what this step does]

### 10. Perplexity
[Describe what this step does]

### 11. OpenRouter Chat Model5
[Describe what this step does]

### 12. Icebreaker Writer
AI agent processes the input with the following instructions:
```
=You are a master cold email copywriter specializing in crafting compelling icebreakers that achieve 80%+ open rates. Your task is to create a single, powerful opening line that follows the greeting in a cold email.
Prospect Intelligence Report
Target Prospect:

Name: {{ $('Process CSV Upload').first().json['First Name'] }} {{ $('Process CSV Upload').first().json['Last Name'] }}
Company: {{ $('Process CSV Upload').first().json.Company }}

Research Analysis: {{ $json.output }}

Cold Email Body You Are Appending The Icebreaker Above:
{{ $('Campaign Request Form').first().json['Your Cold Email Script Body'] }}

Source Priority: Use PUBLIC achievements first. Only reference INTERNAL intelligence if no public details exist, and frame them generally (not specific metrics).

Icebreaker Requirements
Length: 8-22 words maximum
Focus: 100% about them, 0% about you
Tone: Observational and conversational
Format: Single sentence, no questions

... [truncated]
```

### 13. Campaign Request Form
Workflow is triggered via form.

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Cold Email Lead Generation Agency/Cold Email Mass Personalizer.json`
Generated on: 2026-01-02