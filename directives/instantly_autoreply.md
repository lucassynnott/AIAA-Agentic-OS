# Instantly Autoreply

## What This Workflow Is
This workflow receives Instantly email reply webhooks and generates AI-powered contextual responses using campaign-specific knowledge bases.

## What It Does
1. Receives reply webhook from Instantly
2. Looks up campaign knowledge base
3. Researches prospect and company
4. Generates contextual reply with AI
5. Sends reply via Instantly API

## Prerequisites

### Required API Keys (add to .env)
```
INSTANTLY_API_KEY=your_instantly_key
OPENAI_API_KEY=your_openai_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json  # For KB sheet
```

### Required Tools
- Python 3.10+
- Instantly account with webhook

### Installation
```bash
pip install openai requests google-api-python-client
```

## How to Run

### Via Instantly Webhook (Recommended)
Configure Instantly to send reply events to your webhook endpoint.

### Knowledge Base Setup
Add campaign knowledge bases to Sheet: `1QS7MYDm6RUTzzTWoMfX-0G9NzT5EoE2KiCE7iR1DBLM`
- Column A: Campaign ID
- Column B: Campaign Name
- Column C: Knowledge Base
- Column D: Reply Examples

### Quick One-Liner (Manual Test)
```bash
python3 execution/instantly_autoreply.py --campaign_id "[ID]" --email_id "[EMAIL_ID]"
```

## Purpose
Automatically generate and send intelligent replies to incoming emails from Instantly campaigns, using campaign-specific knowledge bases and web research.

## Inputs
The webhook receives this payload from Instantly (reply event):
- `timestamp`: ISO timestamp when the event occurred
- `event_type`: Type of event (e.g., "reply")
- `campaign_id`: UUID of the campaign
- `campaign_name`: Name of the campaign (format: "CAMPAIGN_ID | Campaign Name")
- `lead_email`: The prospect's email address
- `email_account`: The sending account (eaccount)
- `email_id`: UUID of the email to reply to (use as reply_to_uuid)
- `reply_subject`: Subject line of the incoming reply
- `reply_text`: Full plain text content of the incoming reply
- `reply_html`: Full HTML content of the incoming reply
- `reply_text_snippet`: Short preview of the reply content
- Additional lead data fields may be present

## Process

### Step 1: Parse Incoming Reply
The incoming email content is already in the payload:
- `reply_text` or `reply_html`: The full content of their reply
- `reply_subject`: Their subject line
Use this directly - no need to fetch.

### Step 2: Get Full Conversation History (Optional)
If more context is needed, call `instantly_get_emails` with the lead_email to retrieve prior emails (limit 10).

### Step 3: Extract Campaign ID
Parse the campaign_name to get the ID (everything before the "|"). Or use `campaign_id` directly if available.

### Step 4: Lookup Knowledge Base
Call `read_sheet` on spreadsheet `1QS7MYDm6RUTzzTWoMfX-0G9NzT5EoE2KiCE7iR1DBLM` to find the row where column "ID" matches the campaign ID. Extract:
- `Knowledge Base`: Campaign-specific context and talking points
- `Reply Examples`: Example replies to match tone

### Step 5: Skip if No Knowledge Base
If no knowledge base found for this campaign, skip processing and return empty.

### Step 6: Generate Reply
Using extended thinking, generate a reply following these rules:

**Role & Tone:**
- Write as the email_account (first person: 'I', 'we')
- Concise, confident, friendly, non-corporate, outcome-focused
- No em dashes (—), no over-explaining, no hype, no filler
- If followup: be light but persistent, illustrate value props

**Research (use web_search tool):**
- Research the sender and their company/clinic thoroughly
- Look up any products, tools, locations, acronyms you don't recognize
- Use research to tailor the reply (don't mention you searched)

**When to Return Empty (no reply):**
- If additional email would be needless (they confirmed call, logistics done)
- If explicitly negative: "DO NOT EMAIL", "UNSUBSCRIBE", "remove me from list"
- If no knowledge base found

**Output Format:**
- 3-8 sentences unless thread requires more
- HTML with `<br>` for line breaks, `<br><br>` between paragraphs
- No `<html>`, `<body>`, `<p>` tags
- Sign off with first name from email_account

### Step 7: Filter Empty Replies
If the generated reply is empty or just whitespace, do NOT send. Return success with `skipped: true`.

### Step 8: Send Reply
Call `instantly_send_reply` with:
- `eaccount`: The email_account from input
- `reply_to_uuid`: The email_id from input
- `subject`: The reply_subject from input
- `html_body`: The generated reply

## Output
Return:
- `status`: "success" or "error"
- `skipped`: true if reply was intentionally empty
- `reply_sent`: true if reply was actually sent
- `message_id`: ID from Instantly if sent

## Error Handling
- If Instantly API fails: Log error, return error status
- If knowledge base lookup fails: Skip this email (no KB = no reply)
- If AI generation fails: Log error, do not send partial reply

## Knowledge Base Sheet Structure
Spreadsheet ID: `1QS7MYDm6RUTzzTWoMfX-0G9NzT5EoE2KiCE7iR1DBLM`

| ID | Campaign Name | Knowledge Base | Reply Examples |
|----|---------------|----------------|----------------|
| abc123 | Dental Outreach | [context...] | [examples...] |
