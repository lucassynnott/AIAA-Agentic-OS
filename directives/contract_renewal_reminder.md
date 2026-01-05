# Contract Renewal Reminder

## What This Workflow Is
This workflow tracks contract end dates and automates renewal outreach starting 90 days before expiration to maximize retention.

## What It Does
1. Scans CRM for upcoming renewals
2. Alerts account managers at 90/60/30 days
3. Sends renewal outreach emails
4. Tracks renewal status
5. Escalates at-risk renewals

## Prerequisites

### Required API Keys (add to .env)
```
HUBSPOT_API_KEY=your_hubspot_key          # Or CRM with contract data
SENDGRID_API_KEY=your_sendgrid_key
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- CRM with contract data
- Email platform

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Check Upcoming Renewals
```bash
python3 execution/check_renewals.py \
  --lookahead_days 90 \
  --output .tmp/upcoming_renewals.json
```

### Step 2: Send Renewal Outreach
```bash
python3 execution/send_renewal_emails.py \
  --renewals .tmp/upcoming_renewals.json
```

### Quick One-Liner (Weekly Cron)
```bash
python3 execution/check_renewals.py --lookahead_days 90 && \
python3 execution/send_renewal_emails.py --renewals .tmp/upcoming_renewals.json
```

## Goal
Automate contract renewal notifications and processes to retain clients.

## Inputs
- **Contract Data**: Client, end date, value
- **Lead Time**: How far in advance to start (60/90 days)
- **Renewal Terms**: Same, upgrade, or custom

## Process

### 1. Track Contracts
```bash
python3 execution/check_renewals.py \
  --lookahead_days 90 \
  --output .tmp/upcoming_renewals.json
```

### 2. Renewal Timeline

**90 Days Out:**
- Internal alert to account manager
- Review account health
- Prepare renewal strategy

**60 Days Out:**
- Initial renewal outreach
- Schedule review meeting
- Prepare renewal proposal

**30 Days Out:**
- Follow up if no response
- Send formal renewal offer
- Discuss any changes

**14 Days Out:**
- Urgency reminder
- Finalize terms

**7 Days Out:**
- Final notice
- Escalate if no response

### 3. Email: 60 Days Out
```
Subject: [CLIENT] Partnership Renewal

Hi [NAME],

Your agreement with us renews on [DATE] - just 60 days away!

I'd love to schedule a quick call to:
- Review our results together
- Discuss your goals for next year
- Share what's new

[CALENDAR LINK]

Looking forward to continuing our partnership!

[YOUR NAME]
```

### 4. Renewal Strategies

**Healthy Account (High NPS):**
- Propose upgrade/expansion
- Lock in multi-year deal
- Early renewal incentive

**At-Risk Account:**
- Address concerns first
- Offer concessions if needed
- Involve leadership

**Standard Renewal:**
- Review + adjust scope
- Price increase (if applicable)
- Sign and continue

### 5. Tracking
- Days until renewal
- Renewal status (pending/renewed/churned)
- Renewal value vs original
- Retention rate

## Integrations
- CRM (contract data)
- Email platform
- Calendar
- Slack alerts

## Cost
- Automation: Free
- ROI: Prevents churn
