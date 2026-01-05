# Lead Notification

## What This Workflow Is
This workflow sends instant Slack/email notifications when a new lead is captured from form submissions, calendar bookings, or email replies to ensure fast follow-up.

## What It Does
1. Receives webhook from form/calendar/email platform
2. Parses and validates lead data
3. Optionally enriches with company data
4. Sends instant Slack + email notifications
5. Logs lead to tracking sheet

## Prerequisites

### Required API Keys (add to .env)
```
SLACK_WEBHOOK_URL=your_slack_webhook
SENDGRID_API_KEY=your_sendgrid_key        # For email alerts
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Slack webhook configured
- Google Sheets for logging

### Installation
```bash
pip install requests google-api-python-client
```

## How to Run

### Webhook Endpoint
Configure your form/calendar to POST to:
```
POST https://[your-webhook-url]/lead-notification
```

### Manual Test
```bash
python3 execution/send_lead_notification.py \
  --name "John Smith" \
  --email "john@acme.com" \
  --company "Acme Corp" \
  --source "website_form"
```

### Quick One-Liner
```bash
python3 execution/send_lead_notification.py --name "[NAME]" --email "[EMAIL]" --source "[SOURCE]"
```

## Goal
Send instant notifications when a new lead is captured (form submission, booked call, email reply). Ensures fast follow-up.

## Trigger
Webhook called when:
- New form submission
- Calendar booking
- Positive email reply detected
- Lead score threshold reached

## Inputs (webhook payload)
```json
{
  "lead_name": "John Smith",
  "lead_email": "john@company.com",
  "company": "Acme Corp",
  "source": "website_form | calendar | email_reply",
  "details": "Additional context",
  "timestamp": "2024-01-02T10:30:00Z"
}
```

## Process

### 1. Parse Lead Data
Extract from webhook:
- Contact info (name, email, phone)
- Company name
- Lead source
- Any form responses or context

### 2. Enrich Lead (Optional)
If company domain available:
- Lookup company size
- Industry classification
- Recent news/funding

### 3. Send Notifications
**Slack Alert:**
```
🔥 New Lead Alert!

Name: [lead_name]
Company: [company]
Email: [lead_email]
Source: [source]

Details: [details]

⏰ Captured: [timestamp]
```

**Email Alert (to sales team):**
Subject: `🔥 New Lead: [lead_name] from [company]`

### 4. Log to Sheet
Append to lead tracker:
```bash
python3 execution/append_to_sheet.py \
  --sheet_id "[LEAD_TRACKER_ID]" \
  --data '{"name": "[NAME]", "email": "[EMAIL]", "company": "[COMPANY]", "source": "[SOURCE]", "date": "[DATE]", "status": "New"}'
```

### 5. Trigger Follow-up (Optional)
If source is "calendar":
- Send confirmation email
- Add to CRM pipeline

If source is "email_reply":
- Route to inbox owner
- Update campaign status

## Response Time Targets
- Notification sent: <30 seconds
- First human response: <5 minutes (business hours)
- Follow-up if no response: 15 minutes

## Webhook Endpoint
```
POST https://[your-modal-url]/directive?slug=lead-notification
```

## Edge Cases
- **Duplicate lead**: Check email against existing records, merge if duplicate
- **Spam submission**: Basic validation (email format, company exists)
- **After hours**: Queue for morning notification batch
