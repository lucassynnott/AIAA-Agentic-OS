# Dream 100 Instagram Personalized DM Automation

## What This Workflow Is
This workflow fetches Instagram accounts from your Dream 100 list, analyzes their latest post, and generates personalized DM openers using AI.

## What It Does
1. Pulls Dream 100 accounts from Google Sheet
2. Fetches latest post for each account
3. Analyzes post image with vision AI
4. Generates personalized compliment DM
5. Adds DM to sheet for manual sending

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key    # For AI/vision
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Instagram API access (or scraping)
- Google OAuth

### Installation
```bash
pip install openai google-api-python-client requests
```

## How to Run

### Via N8N Manual Trigger
Click "Execute workflow" in n8n UI.

### Via Python Script
```bash
python3 execution/dream_100_dm_generator.py \
  --sheet_url "[GOOGLE_SHEET_URL]" \
  --booking_link "https://cal.com/your-link/30min"
```

### Quick One-Liner
```bash
python3 execution/dream_100_dm_generator.py --sheet_url "[SHEET_URL]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Manual
- **Node**: When clicking ‘Execute workflow’

## Inputs
- [Define inputs based on trigger type]

## Integrations Required
- Google Sheets

## Process
### 1. When clicking ‘Execute workflow’
Workflow is triggered via manual.

### 2. Loop Over Items
[Describe what this step does]

### 3. Analyze image
[Describe what this step does]

### 4. Get Instagram accounts
[Describe what this step does]

### 5. Fetch Instagram Account Data
[Describe what this step does]

### 6. Get Instagram Account Data
[Describe what this step does]

### 7. Fetch Image of latest post
[Describe what this step does]

### 8. Add message to Account
[Describe what this step does]

### 9. Fetch Instagram Account Data1
[Describe what this step does]

### 10. Get Instagram Account Data1
[Describe what this step does]

### 11. Aggregate
[Describe what this step does]

### 12. Generate Personalized DM
AI agent processes the input with the following instructions:
```
={
  "USER_PROMPT_V2": {
    "task": "Write a three sentence Instagram DM as plain text only using a compliment first opener.",
    "inputs": {
      "recipient": {
        "full_name": "{{ $('Get Instagram accounts').first().json['Full Name'] }}",
        "username": "{{ $('Get Instagram Account Data').first().json.username }}",
        "bio": "{{ $('Get Instagram accounts').first().json.Biography }}"
      },
      "post_context": {
        "image_description": "{{ $json.choices[0].message.content }}",
        "caption": "{{ $('Get Instagram Account Data').first().json.latestPosts[0].caption }}",
      },
      "agency": {
        "primary_service": "ecom_email",
        "booking_link": "https://cal.com/your-link/30min",
        "incentive_policy": {
          "enabled": true,
          "options": [
            { "type": "early_access", "copy": "early access to a quick audit" },
... [truncated]
```

### 13. OpenRouter Chat Model
[Describe what this step does]

### 14. Schedule Trigger
Workflow is triggered via manual.

### 15. If
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/Dream 100 Instagram Personalized DM Automation.json`
Generated on: 2026-01-02