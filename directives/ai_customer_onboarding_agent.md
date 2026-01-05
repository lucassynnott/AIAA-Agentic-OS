# AI Customer Onboarding Agent

## What This Workflow Is
This workflow automates new client onboarding by creating Slack channels, Google Drive folders, CRM contacts, and tasks from a form submission.

## What It Does
1. Receives onboarding form submission
2. Creates Slack channel and posts welcome
3. Creates client folder in Google Drive
4. Extracts tasks from proposal document
5. Creates tasks in project management

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key    # For AI processing
SLACK_BOT_TOKEN=your_slack_token
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Slack app with permissions
- Google OAuth

### Installation
```bash
pip install slack-sdk google-api-python-client openai
```

## How to Run

### Via N8N Webhook (Recommended)
Submit form to n8n webhook endpoint with fields:
- Name, Email, Company Name, Website
- Proposal/Scope Document (file)
- Client Information/Tasks

### Via Python Script
```bash
python3 execution/onboard_client.py \
  --name "John Smith" \
  --email "john@company.com" \
  --company "Company Inc" \
  --website "https://company.com" \
  --proposal "[PATH_TO_FILE]"
```

### Quick One-Liner
```bash
python3 execution/onboard_client.py --name "[NAME]" --email "[EMAIL]" --company "[COMPANY]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Name**: text (required)
- **Email**: text (required)
- **Company Name**: text (required)
- **Website**: text (required)
- **Proposal/Scope Document**: file
- **Client Information / Tasks**: textarea

## Integrations Required
- Gmail
- Slack

## Process
### 1. Send Welcome Email
[Describe what this step does]

### 2. On form submission
Workflow is triggered via form.

### 3. Slack | Create Channel
[Describe what this step does]

### 4. Slack | Post Message
[Describe what this step does]

### 5. Segment Tasks
AI agent processes the input with the following instructions:
```
={{ $("On form submission").first().json['Client Information / Tasks'] }}
```

### 6. Split Out1
[Describe what this step does]

### 7. Loop Over Items
[Describe what this step does]

### 8. Rename Doc
Data is normalized/transformed for the next step.

### 9. Extract from File
[Describe what this step does]

### 10. Rename Folder ID
Data is normalized/transformed for the next step.

### 11. Create or update a contact
[Describe what this step does]

### 12. OpenRouter Chat Model
[Describe what this step does]

### 13. OpenRouter Chat Model1
[Describe what this step does]

### 14. Create Main Client Folder
[Describe what this step does]

### 15. Create a task
[Describe what this step does]

### 16. If
[Describe what this step does]

### 17. If1
[Describe what this step does]

### 18. OpenRouter Chat Model2
[Describe what this step does]

### 19. OpenRouter Chat Model3
[Describe what this step does]

### 20. Segment Tasks (PDF)
AI agent processes the input with the following instructions:
```
=

```

### 21. Aggregate
[Describe what this step does]

## Output Schema
### Structured Output Parser
```json
{}
```
### Structured Output Parser1
```json
{}
```

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Cold Email Lead Generation Agency/AI Customer Onboarding Agent.json`
Generated on: 2026-01-02