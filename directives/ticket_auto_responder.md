# Support Ticket Auto-Responder

## What This Workflow Is
This workflow automatically acknowledges support tickets, classifies them by category/priority, and drafts AI responses from your knowledge base.

## What It Does
1. Receives ticket via webhook/email
2. AI classifies by category, priority, sentiment
3. Sends immediate acknowledgment
4. Drafts AI response from knowledge base
5. Routes to appropriate team

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For AI classification/response
ZENDESK_API_KEY=your_zendesk_key          # Or help desk platform
PINECONE_API_KEY=your_pinecone_key        # For knowledge base
```

### Required Tools
- Python 3.10+
- Help desk API
- Vector database with KB

### Installation
```bash
pip install openai pinecone-client requests
```

## How to Run

### Step 1: Process Incoming Ticket
```bash
python3 execution/process_support_ticket.py \
  --ticket_id "[ID]" \
  --knowledge_base .tmp/kb_vectors.json
```

### Step 2: Ingest Knowledge Base (setup)
```bash
python3 execution/ingest_knowledge.py \
  --source "[DOCS_URL]" \
  --output .tmp/kb_vectors.json
```

### Quick One-Liner
```bash
python3 execution/process_support_ticket.py --ticket_id "[ID]"
```

## Goal
Automatically acknowledge and triage incoming support tickets with AI-powered initial responses.

## Inputs
- **Ticket Source**: Email, form, chat
- **Knowledge Base**: FAQ/documentation
- **Routing Rules**: By category, priority, team

## Process

### 1. Ticket Receipt
```bash
python3 execution/process_support_ticket.py \
  --ticket_id "[ID]" \
  --knowledge_base .tmp/kb_vectors.json
```

### 2. Auto-Classification
AI classifies ticket by:
- **Category**: Billing, Technical, General, Feature Request
- **Priority**: Urgent, High, Medium, Low
- **Sentiment**: Frustrated, Neutral, Positive

### 3. Immediate Acknowledgment
```
Subject: Re: [Original Subject] [Ticket #XXXX]

Hi [NAME],

Thanks for reaching out! We've received your message 
and a team member will respond within [SLA TIME].

Ticket #: [NUMBER]
Priority: [PRIORITY]

In the meantime, you might find these helpful:
[RELEVANT KB ARTICLES]

If urgent, call us at [PHONE].

Best,
[COMPANY] Support
```

### 4. AI-Suggested Response
For common questions, AI drafts response:
```
[DRAFTED RESPONSE BASED ON KB]

---
Agent: Review and send, or edit as needed.
Confidence: [X%]
KB Source: [Article link]
```

### 5. Routing Rules
| Category | Route To | SLA |
|----------|----------|-----|
| Billing | Finance | 4h |
| Technical | Engineering | 2h |
| Urgent | On-call | 30m |
| General | Support | 24h |

### 6. Escalation
Auto-escalate if:
- No response within SLA
- Customer replies 3+ times
- Negative sentiment detected
- VIP customer

## Integrations
- Help desk (Zendesk, Intercom, Freshdesk)
- Knowledge base
- Slack (alerts)
- CRM

## Cost
- AI responses: ~$0.01/ticket
- Automation: Free
