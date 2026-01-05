# Payment Reminder Automation

## What This Workflow Is
This workflow automates payment reminder emails based on invoice due dates, with escalation rules for overdue accounts.

## What It Does
1. Checks invoice status from billing system
2. Sends reminders at scheduled intervals
3. Escalates overdue accounts to team
4. Updates CRM with payment status
5. Alerts on seriously overdue accounts

## Prerequisites

### Required API Keys (add to .env)
```
STRIPE_API_KEY=your_stripe_key            # Or QUICKBOOKS credentials
SENDGRID_API_KEY=your_sendgrid_key
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- Billing platform API
- Email platform

### Installation
```bash
pip install stripe requests
```

## How to Run

### Step 1: Check Invoice Status
```bash
python3 execution/check_invoices.py \
  --source stripe \
  --output .tmp/overdue.json
```

### Step 2: Send Reminders
```bash
python3 execution/send_payment_reminders.py \
  --invoices .tmp/overdue.json
```

### Quick One-Liner (Daily Cron)
```bash
python3 execution/check_invoices.py --source stripe && \
python3 execution/send_payment_reminders.py --invoices .tmp/overdue.json
```

## Goal
Automate payment reminders to reduce late payments and improve cash flow.

## Inputs
- **Invoice Data**: From billing system
- **Payment Terms**: Net 15, Net 30, etc.
- **Escalation Rules**: When to involve humans

## Process

### 1. Track Invoice Status
```bash
python3 execution/check_invoices.py \
  --source stripe \
  --output .tmp/overdue.json
```

### 2. Reminder Schedule

**5 Days Before Due:**
```
Subject: Friendly reminder: Invoice #[NUMBER] due soon

Hi [NAME],

Quick reminder that invoice #[NUMBER] for $[AMOUNT] 
is due on [DATE].

Pay now: [PAYMENT_LINK]

Let me know if you have any questions!
```

**Day of Due Date:**
```
Subject: Invoice #[NUMBER] due today

Hi [NAME],

Invoice #[NUMBER] for $[AMOUNT] is due today.

Pay now: [PAYMENT_LINK]

Thanks!
```

**3 Days Overdue:**
```
Subject: Payment overdue: Invoice #[NUMBER]

Hi [NAME],

Invoice #[NUMBER] for $[AMOUNT] was due on [DATE] 
and is now 3 days overdue.

Please process payment at your earliest convenience:
[PAYMENT_LINK]

If there's an issue, please let us know.
```

**7 Days Overdue:**
```
Subject: Urgent: Invoice #[NUMBER] - 7 days overdue

Hi [NAME],

This is a reminder that invoice #[NUMBER] is now 
7 days past due.

Total due: $[AMOUNT]

Please arrange payment immediately or contact us 
to discuss.

[PAYMENT_LINK]
```

**14+ Days Overdue:**
- Personal call from account manager
- Service pause warning
- Escalate to leadership

### 3. Escalation Matrix
| Days Overdue | Action |
|--------------|--------|
| -5 | Email reminder |
| 0 | Email reminder |
| 3 | Email + task to AM |
| 7 | Email + call |
| 14 | Service warning |
| 30 | Collection process |

### 4. Auto-Actions
- Send reminders automatically
- Update CRM with payment status
- Alert team on escalation
- Pause services if needed

## Integrations
- Stripe/QuickBooks (invoices)
- Email platform
- CRM
- Slack (alerts)

## Cost
- Automation: Free
- Improves cash flow significantly
