# Booked Meeting Alert + Prospect Research

## What This Workflow Is
This workflow triggers when a meeting is booked via Calendly, researches the prospect with AI, and creates a prep doc in Google Drive with Slack notification.

## What It Does
1. Receives Calendly booking event
2. Enriches prospect via Explorium API
3. Researches LinkedIn profile with AI
4. Generates meeting prep document
5. Notifies via Slack with Google Doc link

## Prerequisites

### Required API Keys (add to .env)
```
EXPLORIUM_API_KEY=your_explorium_key      # For prospect enrichment
OPENROUTER_API_KEY=your_openrouter_key
PERPLEXITY_API_KEY=your_perplexity_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
SLACK_BOT_TOKEN=your_slack_token
```

### Required Tools
- Python 3.10+
- Calendly webhook
- Explorium account

### Installation
```bash
pip install openai google-api-python-client slack-sdk requests
```

## How to Run

### Via Calendly Webhook (Recommended)
Configure Calendly to send webhook on booking. Workflow auto-triggers.

### Via Python Script
```bash
python3 execution/research_booked_meeting.py \
  --prospect_name "John Smith" \
  --prospect_email "john@company.com" \
  --meeting_time "2026-01-03 10:00"
```

### Quick One-Liner
```bash
python3 execution/research_booked_meeting.py --prospect_email "[EMAIL]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Manual
- **Node**: Manual Trigger

## Inputs
- [Define inputs based on trigger type]

## Integrations Required
- Gmail
- Slack

## Process
### 1. Calendly Events
Workflow is triggered via manual.

### 2. Map needed fields
Data is normalized/transformed for the next step.

### 3. create json
Data is normalized/transformed for the next step.

### 4. Edit bio
Data is normalized/transformed for the next step.

### 5. Notify admin
[Describe what this step does]

### 6. create HTML
[Describe what this step does]

### 7. Explorium Match Prospects
[Describe what this step does]

### 8. Extract Prospect IDs from Matched Results
[Describe what this step does]

### 9. Explorium Enrich Contacts Information
[Describe what this step does]

### 10. Merge
[Describe what this step does]

### 11. Explorium Enrich Profiles
[Describe what this step does]

### 12. Code
[Describe what this step does]

### 13. Filter non-matched
[Describe what this step does]

### 14. Create or update a contact
[Describe what this step does]

### 15. AI Agent
AI agent processes the input with the following instructions:
```
=You are an AI assistant specializing in generating meeting preparation documents for business professionals. Your goal is to analyze provided data (specifically LinkedIn profiles and meeting agendas) and synthesize it into actionable insights to facilitate productive introductory calls. You are detail-oriented, organized, and capable of extracting key information and identifying relevant connections.

**Task:**

Generate a comprehensive meeting preparation document for an introductory call with a prospect, based on the LinkedIn profile data and meeting agenda provided. The output should follow the format described below and be tailored to the specific information in the input data.

**Input Format:**

You will receive a JSON object containing a LinkedIn profile and a string containing the meeting agenda. The LinkedIn profile will contain fields such as `name`, `position`, `about`, `experience`, `activity` and other relevant details.  The `experience` field is an array of job objects, each containing `title`, `company`, `description`, etc. The `activity` field is an array of the users' recent LinkedIn likes.

**Output Format:**

The output should be a well-formatted document, easily readable and actionable, adhering to the following structure:

**Prospect Information**

Name: {{ $json.name }}
LinkedIn Profile: {{ $json.url }}
City: {{ $json.city }}
Country: {{ $json.country }}
... [truncated]
```

### 16. OpenRouter Chat Model1
[Describe what this step does]

### 17. Code1
[Describe what this step does]

### 18. Aggregate
[Describe what this step does]

### 19. Code2
[Describe what this step does]

### 20. Aggregate1
[Describe what this step does]

### 21. Perplexity
[Describe what this step does]

### 22. Google Doc Creator
[Describe what this step does]

### 23. Move file
[Describe what this step does]

### 24. Send a message
[Describe what this step does]

### 25. Get many contacts
[Describe what this step does]

### 26. If
[Describe what this step does]

### 27. Create Contact
[Describe what this step does]

### 28. Create an opportunity
[Describe what this step does]

### 29. Search For Existing Opportunity
[Describe what this step does]

### 30. Update an opportunity
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Cold Email Lead Generation Agency/Booked Meeting Alert + Prospect Research.json`
Generated on: 2026-01-02