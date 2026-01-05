# Onboard New Client

## What This Workflow Is
This workflow automates the client onboarding process from contract signing through kickoff call, ensuring consistent, professional onboarding every time.

## What It Does
1. Sends welcome email with onboarding form
2. Creates client infrastructure (Slack, Drive, tracking)
3. Schedules kickoff call
4. Sends post-kickoff summary with action items
5. Updates client tracker

## Prerequisites

### Required API Keys (add to .env)
```
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
SLACK_WEBHOOK_URL=your_slack_webhook
SENDGRID_API_KEY=your_sendgrid_key
```

### Required Tools
- Python 3.10+
- Google OAuth credentials
- Slack workspace admin access

### Installation
```bash
pip install google-api-python-client gspread requests
```

## How to Run

### Step 1: Send Welcome Communications
```bash
python3 execution/welcome_client_emails.py \
  --client_name "John Smith" \
  --client_email "john@acme.com" \
  --company "Acme Corp" \
  --service "Cold Email" \
  --start_date "2024-01-15"
```

### Step 2: Create Client Infrastructure
```bash
python3 execution/setup_client_folder.py --company "Acme Corp" --service "Cold Email"
```

### Step 3: Post-Kickoff Automation
```bash
python3 execution/onboarding_post_kickoff.py \
  --client_email "john@acme.com" \
  --next_steps "Action item 1, Action item 2" \
  --first_deliverable_date "2024-01-22"
```

### Quick One-Liner
```bash
python3 execution/welcome_client_emails.py --client_name "[NAME]" --client_email "[EMAIL]" --company "[COMPANY]" --service "[SERVICE]"
```

## Goal
Automate the client onboarding process: send welcome communications, set up project infrastructure, and schedule kickoff call. Ensures consistent, professional onboarding every time.

## Inputs
- **Client Name**: Full name of primary contact
- **Client Email**: Email address
- **Company Name**: Client's business name
- **Service Type**: What service they purchased (e.g., "Cold Email", "Content Marketing")
- **Deal Value**: Monthly retainer amount
- **Start Date**: When engagement begins
- **Account Manager**: Who's assigned to this client (optional)

## Tools/Scripts
- `execution/welcome_client_emails.py` - Sends templated welcome emails
- `execution/onboarding_post_kickoff.py` - Post-kickoff automation
- `execution/update_sheet.py` - Update client tracker
- Google Calendar API - Schedule calls

## Process

### 1. Trigger Onboarding
When a new client signs, run:
```bash
python3 execution/welcome_client_emails.py \
  --client_name "[CLIENT_NAME]" \
  --client_email "[EMAIL]" \
  --company "[COMPANY]" \
  --service "[SERVICE_TYPE]" \
  --start_date "[YYYY-MM-DD]"
```

This sends:
- Welcome email with onboarding form link
- Calendar invite for kickoff call
- Access credentials (if applicable)

### 2. Create Client Infrastructure
Set up project management:
- [ ] Create client Slack channel: `#client-[company-slug]`
- [ ] Create Google Drive folder structure
- [ ] Add to client tracking sheet
- [ ] Set up reporting dashboard (if applicable)

```bash
python3 execution/setup_client_folder.py --company "[COMPANY]" --service "[SERVICE_TYPE]"
```

### 3. Pre-Kickoff Checklist
Before the kickoff call, ensure:
- [ ] Onboarding form completed by client
- [ ] Review client's business/website
- [ ] Prepare first 30-day plan
- [ ] Set up any required accounts (Instantly, Smartlead, etc.)

### 4. Kickoff Call Agenda (60 min)
Run the kickoff call following this structure:

**First 10 min - Rapport & Expectations**
- Re-confirm goals and success metrics
- Review timeline and milestones
- Clarify communication preferences

**Next 30 min - Strategy Deep Dive**
- Walk through the service delivery plan
- Review any onboarding form responses
- Identify quick wins for first week

**Next 15 min - Access & Setup**
- Collect any missing credentials
- Walk through dashboards/reporting
- Confirm all systems connected

**Final 5 min - Next Steps**
- Summarize action items
- Confirm first deliverable date
- Schedule first check-in call

### 5. Post-Kickoff Automation
After kickoff call:
```bash
python3 execution/onboarding_post_kickoff.py \
  --client_email "[EMAIL]" \
  --next_steps "[ACTION_ITEMS]" \
  --first_deliverable_date "[DATE]"
```

This sends:
- Call summary with action items
- Link to shared project tracker
- First deliverable timeline

### 6. Update Client Tracker
```bash
python3 execution/update_sheet.py \
  --sheet_id "[CLIENT_TRACKER_ID]" \
  --data '{"company": "[COMPANY]", "status": "Onboarded", "kickoff_date": "[DATE]", "am": "[ACCOUNT_MANAGER]"}'
```

## Onboarding Timeline
| Day | Action |
|-----|--------|
| 0 | Contract signed, welcome email sent |
| 1-2 | Kickoff call scheduled |
| 3-5 | Kickoff call completed |
| 5-7 | First deliverable/milestone |
| 14 | First results check-in |
| 30 | Month 1 review call |

## Success Metrics
- Kickoff call within 5 days of signing
- First deliverable within 7 days
- Client responds to first check-in within 48h
- No missed communications in first 30 days

## Templates

### Welcome Email Subject
`Welcome to [Your Agency] - Let's Get Started! 🚀`

### Kickoff Call Summary Subject
`[Company] Kickoff Summary + Next Steps`

### First Deliverable Subject
`[Company] - Your First [Deliverable] is Ready`

## Edge Cases
- **Client unresponsive**: 3-touch sequence, then escalate to sales
- **Missing credentials**: Send credential checklist, block until received
- **Scope creep**: Refer back to contract, log for upsell opportunity
- **Delayed start**: Adjust timeline, communicate proactively

## Related Workflows
- `directives/setup_client_communication.md` - Detailed comms setup
- `directives/create_proposal.md` - Pre-sale proposal creation
- `directives/launch_cold_email_campaign.md` - If service is cold email
