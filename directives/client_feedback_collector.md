# Client Feedback Collector

## What This Workflow Is
This workflow automates NPS/CSAT surveys to clients at key moments, with automatic follow-up based on response scores.

## What It Does
1. Sends surveys at configured trigger points
2. Collects NPS/CSAT scores
3. Routes follow-up by score (promoters vs detractors)
4. Alerts team on low scores
5. Generates feedback analysis reports

## Prerequisites

### Required API Keys (add to .env)
```
TYPEFORM_API_KEY=your_typeform_key         # Or survey tool
HUBSPOT_API_KEY=your_hubspot_key           # For client data
SLACK_WEBHOOK_URL=your_slack_webhook       # For alerts
```

### Required Tools
- Python 3.10+
- Survey platform (Typeform, SurveyMonkey)
- CRM

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Send Survey
```bash
python3 execution/send_nps_survey.py \
  --client_email "client@company.com" \
  --survey_type nps
```

### Step 2: Process Response (via webhook)
```bash
python3 execution/process_survey_response.py \
  --response_data '[webhook payload]'
```

### Step 3: Generate Report
```bash
python3 execution/generate_feedback_report.py --period last_month
```

### Quick One-Liner
```bash
python3 execution/send_nps_survey.py --client_email "[EMAIL]" --survey_type nps
```

## Goal
Systematically collect and analyze client feedback to improve service delivery.

## Inputs
- **Survey Type**: NPS, CSAT, or custom
- **Trigger**: Milestone, time-based, or ad-hoc
- **Follow-up**: Based on response

## Process

### 1. Survey Types

**NPS (Net Promoter Score):**
"On a scale of 0-10, how likely are you to recommend us?"
- Promoters: 9-10
- Passives: 7-8
- Detractors: 0-6

**CSAT (Customer Satisfaction):**
"How satisfied are you with [specific thing]?"
- Very satisfied to Very dissatisfied

**Custom Questions:**
- Service quality
- Communication
- Results delivered
- Value for money

### 2. Survey Timing
- After onboarding (30 days)
- After project milestone
- Quarterly check-in
- After support ticket resolved
- Pre-renewal

### 3. Survey Email
```
Subject: Quick feedback? (1 minute)

Hi [NAME],

How are we doing?

One quick question:

On a scale of 0-10, how likely are you to recommend 
[COMPANY] to a colleague?

[0] [1] [2] [3] [4] [5] [6] [7] [8] [9] [10]

Takes 30 seconds - your feedback helps us improve!

Thanks,
[YOUR NAME]
```

### 4. Follow-up by Score

**Promoters (9-10):**
- Thank you message
- Request review/testimonial
- Ask for referrals

**Passives (7-8):**
- Ask what would make it a 10
- Schedule check-in call
- Identify improvements

**Detractors (0-6):**
- Immediate alert to AM
- Personal outreach within 24h
- Issue resolution process
- Follow-up after resolution

### 5. Feedback Analysis
```markdown
# Feedback Report - [Month]

## NPS Summary
- Responses: X
- Score: [X]
- Trend: ↑/↓/→

## Breakdown
- Promoters: X%
- Passives: X%
- Detractors: X%

## Common Themes
[Positive themes]
[Areas for improvement]

## Action Items
1. [Action based on feedback]
2. [Action based on feedback]
```

## Integrations
- Survey tool (Typeform, SurveyMonkey)
- CRM
- Slack alerts
- Google Sheets

## Cost
- Survey tools: Free-$50/mo
- Automation: Free
