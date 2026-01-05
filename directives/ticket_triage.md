# Support Ticket Triage

## What This Workflow Is
This workflow uses AI to classify support tickets by type, priority, and sentiment, then routes them to the appropriate team with SLA tracking.

## What It Does
1. Analyzes ticket content with AI
2. Classifies by type (bug, feature, billing)
3. Assigns priority (P0-P3)
4. Detects customer sentiment
5. Routes to correct team with SLA

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For AI classification
ZENDESK_API_KEY=your_zendesk_key          # Or help desk platform
SLACK_WEBHOOK_URL=your_slack_webhook      # For alerts
PAGERDUTY_API_KEY=your_pagerduty_key      # For P0 escalation
```

### Required Tools
- Python 3.10+
- Help desk API
- Alerting platform

### Installation
```bash
pip install openai requests
```

## How to Run

### Step 1: Triage Ticket
```bash
python3 execution/triage_ticket.py \
  --ticket_id "[ID]" \
  --output .tmp/triage_result.json
```

### Step 2: Apply Routing
```bash
python3 execution/route_ticket.py \
  --triage .tmp/triage_result.json
```

### Quick One-Liner
```bash
python3 execution/triage_ticket.py --ticket_id "[ID]" && python3 execution/route_ticket.py
```

## Goal
Automatically categorize, prioritize, and route support tickets to the right team.

## Inputs
- **Ticket Content**: Subject + body
- **Customer Data**: Account tier, history
- **Team Structure**: Who handles what

## Process

### 1. Analyze Ticket
```bash
python3 execution/triage_ticket.py \
  --ticket_id "[ID]" \
  --output .tmp/triage_result.json
```

### 2. Classification Categories

**By Type:**
- Bug report
- Feature request
- How-to question
- Billing inquiry
- Account issue
- Complaint
- Integration help

**By Priority:**
- P0 (Urgent): Production down, security issue
- P1 (High): Major feature broken
- P2 (Medium): Minor issue with workaround
- P3 (Low): General questions, nice-to-haves

**By Sentiment:**
- Angry/Frustrated
- Confused
- Neutral
- Happy

### 3. Priority Matrix
| Impact | Urgency | Priority |
|--------|---------|----------|
| High | High | P0 |
| High | Low | P1 |
| Low | High | P2 |
| Low | Low | P3 |

### 4. Routing Rules
```json
{
  "billing": {"team": "finance", "sla": "4h"},
  "technical": {"team": "engineering", "sla": "2h"},
  "bug_p0": {"team": "on-call", "sla": "30m"},
  "feature_request": {"team": "product", "sla": "48h"},
  "general": {"team": "support", "sla": "24h"}
}
```

### 5. Auto-Actions

**P0 Tickets:**
- Page on-call engineer
- Slack alert to leadership
- Auto-acknowledge customer

**VIP Customers:**
- Route to senior support
- Alert account manager
- Expedited SLA

**Repeat Issues:**
- Link to related tickets
- Suggest known solution
- Flag for bug tracking

### 6. Triage Output
```json
{
  "ticket_id": "12345",
  "category": "technical",
  "priority": "P1",
  "sentiment": "frustrated",
  "route_to": "engineering",
  "sla_hours": 2,
  "suggested_response": "[Draft response]",
  "related_tickets": ["12300", "12280"]
}
```

## Integrations
- Help desk API
- Slack (alerts)
- PagerDuty (P0)
- CRM (customer data)

## Cost
- AI classification: ~$0.01/ticket
