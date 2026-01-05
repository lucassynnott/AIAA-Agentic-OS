# Demo Scheduling Automation

## What This Workflow Is
This workflow automates the entire demo booking process including smart routing to the right rep, automated reminders, and intelligent no-show recovery sequences.

## What It Does
1. Captures booking data from Calendly/Cal.com
2. Routes meetings to appropriate rep based on lead criteria
3. Sends automated confirmation and reminder sequences
4. Detects no-shows and triggers recovery outreach
5. Updates CRM with meeting status

## Prerequisites

### Required API Keys (add to .env)
```
CALENDLY_API_KEY=your_calendly_key        # Or CAL_COM_API_KEY
HUBSPOT_API_KEY=your_hubspot_key          # Or SALESFORCE credentials
TWILIO_SID=your_twilio_sid                # For SMS (optional)
TWILIO_AUTH_TOKEN=your_twilio_token
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Calendly Pro or Cal.com account
- CRM with API access
- Email platform (SendGrid/Gmail)

### Installation
```bash
pip install requests google-api-python-client twilio
```

## How to Run

### Step 1: Set Up Webhook
Configure Calendly/Cal.com to send webhooks to your endpoint when bookings are created.

### Step 2: Process New Booking
When webhook fires:
```bash
python3 execution/process_demo_booking.py \
  --event_data '[webhook payload]' \
  --routing_rules routing.json
```

### Step 3: Handle No-Shows
Run after meeting end time:
```bash
python3 execution/handle_no_show.py --meeting_id "[MEETING_ID]"
```

### Step 4: Manual No-Show Check
```bash
python3 execution/check_no_shows.py --date today
```

### Automated Setup (Recommended)
Set up a cron job or n8n workflow to:
1. Check for meetings ending in last hour
2. Mark no-shows automatically
3. Trigger recovery sequence

## Goal
Automate demo scheduling with smart routing, reminders, and no-show handling.

## Inputs
- **Calendar**: Calendly, Cal.com, or Google Calendar
- **Routing Rules**: By lead score, region, or product interest
- **Reminder Sequence**: Before meeting
- **No-show Follow-up**: After missed meeting

## Process

### 1. Booking Flow
Lead books via scheduling link → Data captured → Routed to right rep → Confirmations sent

### 2. Smart Routing
| Criteria | Route To |
|----------|----------|
| Enterprise (500+ emp) | Senior AE |
| SMB (<100 emp) | SDR/Junior AE |
| Specific product | Product specialist |
| Region | Regional rep |

### 3. Pre-Meeting Automation
**Immediately:**
- Confirmation email with agenda
- Calendar invite
- Add to CRM

**24 hours before:**
- Reminder email
- Prep doc sent
- Research dossier generated

**1 hour before:**
- SMS reminder (optional)
- Meeting link reminder

### 4. No-Show Handling
**If no-show detected:**
```bash
python3 execution/handle_no_show.py --meeting_id "[ID]"
```

**Sequence:**
- 5 min after: "Are you joining?"
- 15 min after: "Let's reschedule" with link
- 24 hours: Follow-up email
- 3 days: Final attempt

### 5. Post-Meeting
- Send summary email
- Update CRM status
- Trigger follow-up sequence

## Integrations
- Calendly/Cal.com API
- CRM (HubSpot, Salesforce)
- Email (Gmail, SendGrid)
- SMS (Twilio)

## Metrics to Track
- Booking rate
- Show rate
- Conversion rate
- Time to book
