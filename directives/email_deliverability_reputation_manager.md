# Email Deliverability & Reputation Manager

## What This Workflow Is
This workflow monitors email deliverability by checking blacklists, SPF, DKIM, DMARC records, and provides AI-powered recommendations for improving email reputation.

## What It Does
1. Receives domain via form or schedule
2. Checks MXToolbox blacklist status
3. Validates SPF, DKIM, DMARC records
4. AI analyzes and scores deliverability
5. Sends alerts for critical issues

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key
AIRTABLE_API_KEY=your_airtable_key        # For storing results
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- MXToolbox access

### Installation
```bash
pip install openai requests
```

## How to Run

### Via N8N Form
Submit form with:
- Domain Name
- IP Address (optional)
- Email Service Provider
- Campaign Volume
- Urgency Level

### Via Python Script
```bash
python3 execution/check_deliverability.py \
  --domain "yourdomain.com" \
  --provider "google_workspace"
```

### Quick One-Liner
```bash
python3 execution/check_deliverability.py --domain "[DOMAIN]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: Form Trigger - Manual Assessment

## Inputs
- **Assessment Type**: dropdown (required)
- **Domain Name**: text (required)
- **IP Address**: text
- **Email Service Provider**: dropdown (required)
- **Campaign Volume (per month)**: number
- **Urgency Level**: dropdown (required)
- **Additional Notes**: textarea

## Integrations Required
- Airtable
- Slack

## Process
### 1. Form Trigger - Manual Assessment
Workflow is triggered via form.

### 2. Schedule Trigger - Continuous Monitoring
Workflow is triggered via form.

### 3. Schedule Trigger - Weekly Audit
Workflow is triggered via form.

### 4. Webhook - Email Provider Events
[Describe what this step does]

### 5. Route by Trigger Type
Workflow is triggered via form.

### 6. Set Manual Assessment Data
Data is normalized/transformed for the next step.

### 7. Set Continuous Monitoring Data
Data is normalized/transformed for the next step.

### 8. Set Weekly Audit Data
Data is normalized/transformed for the next step.

### 9. Set Webhook Event Data
Data is normalized/transformed for the next step.

### 10. MXToolbox Blacklist Check
[Describe what this step does]

### 11. SPF Record Check
[Describe what this step does]

### 12. DKIM Record Check
[Describe what this step does]

### 13. DMARC Policy Check
[Describe what this step does]

### 14. AI Deliverability Analyst
AI agent processes the input with the following instructions:
```
=Analyze the following email deliverability data and provide actionable recommendations:

Domain: {{ $('Route by Trigger Type').item.json.domain }}
Blacklist Status: {{ $('MXToolbox Blacklist Check').item.json.status }}
SPF Status: {{ $('SPF Record Check').item.json.status }}
DKIM Status: {{ $('DKIM Record Check').item.json.status }}
DMARC Status: {{ $('DMARC Policy Check').item.json.status }}

Provide:
1. Overall deliverability score (1-100)
2. Critical issues requiring immediate attention
3. Specific remediation steps
4. Performance optimization recommendations
5. Risk assessment for email campaigns

Always output in this JSON format:
[
  {
    "score": 0,
    "grade": "F",
... [truncated]
```

### 15. Store Assessment Results
[Describe what this step does]

### 16. Check Alert Threshold
[Describe what this step does]

### 17. Send Critical Alert
[Describe what this step does]

### 18. Send Status Report
[Describe what this step does]

### 19. OpenRouter LLM
[Describe what this step does]

## Output Schema
### Structured Output Parser
```json
{}
```

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Cold Email Lead Generation Agency/Domain Health Analyzer.json`
Generated on: 2026-01-02