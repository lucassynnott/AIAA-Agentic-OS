# Daily Campaign Reports, Health Metrics & Bounce Rate Alerts

## What This Workflow Is
This workflow pulls daily cold email campaign metrics from your sending platform, logs them to Google Sheets, and sends Slack alerts when bounce rates exceed thresholds.

## What It Does
1. Runs on schedule (daily)
2. Fetches campaign metrics via API
3. Logs to Google Sheets for tracking
4. Checks bounce rates against thresholds
5. Sends Slack alert if bounces too high

## Prerequisites

### Required API Keys (add to .env)
```
INSTANTLY_API_KEY=your_instantly_key      # Or email sending platform
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- Email platform API
- Google OAuth

### Installation
```bash
pip install requests google-api-python-client
```

## How to Run

### Via N8N Schedule (Recommended)
Schedule runs daily at set time. Configure in n8n.

### Via Python Script
```bash
python3 execution/daily_campaign_report.py \
  --platform instantly \
  --bounce_threshold 3
```

### Quick One-Liner (Cron)
```bash
python3 execution/daily_campaign_report.py --bounce_threshold 3
```

## Goal
[Describe the purpose of this workflow]

## Trigger
- **Type**: Schedule
- **Node**: Schedule Trigger1

## Inputs
- [Define inputs based on trigger type]

## Integrations Required
- Google Sheets
- Slack

## Process
### 1. HTTP Request5
[Describe what this step does]

### 2. Split Out5
[Describe what this step does]

### 3. HTTP Request6
[Describe what this step does]

### 4. Split Out6
[Describe what this step does]

### 5. Schedule Trigger1
Workflow is triggered via schedule.

### 6. HTTP Request
[Describe what this step does]

### 7. Split Out
[Describe what this step does]

### 8. Schedule Trigger
Workflow is triggered via schedule.

### 9. HTTP Request1
[Describe what this step does]

### 10. Append or update row in sheet1
[Describe what this step does]

### 11. Split Out1
[Describe what this step does]

### 12. Append or update row in sheet
[Describe what this step does]

### 13. Append or update row in sheet6
[Describe what this step does]

### 14. Append or update row in sheet5
[Describe what this step does]

### 15. Send a message
[Describe what this step does]

### 16. If
[Describe what this step does]

### 17. BOUNCE ALERT
[Describe what this step does]

### 18. Bounce Ok
Data is normalized/transformed for the next step.

### 19. BOUNCE ALERT1
[Describe what this step does]

### 20. Bounce Ok1
Data is normalized/transformed for the next step.

### 21. If1
[Describe what this step does]

### 22. Schedule Trigger3
Workflow is triggered via schedule.

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Cold Email Lead Generation Agency/Daily Campaign Reports, Health Metrics & Bounce Rate Alerts.json`
Generated on: 2026-01-02