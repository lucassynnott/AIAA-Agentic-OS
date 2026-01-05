# AI Email Reply Classifier

## What This Workflow Is
This workflow uses AI to classify email replies by intent (interested, meeting request, not interested, etc.) and routes them for appropriate follow-up.

## What It Does
1. Receives email reply content
2. AI classifies by intent and sentiment
3. Assigns priority level
4. Suggests response or auto-responds
5. Updates CRM with classification

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
INSTANTLY_API_KEY=your_instantly_key      # Or email platform
```

### Required Tools
- Python 3.10+
- Email platform API

### Installation
```bash
pip install openai requests
```

## How to Run

### Step 1: Classify Reply
```bash
python3 execution/classify_email_reply.py \
  --email_id "[ID]" \
  --output .tmp/classification.json
```

### Step 2: Process Classification
```bash
python3 execution/process_reply_classification.py \
  --classification .tmp/classification.json
```

### Quick One-Liner
```bash
python3 execution/classify_email_reply.py --email_id "[ID]"
```

## Goal
Automatically classify email replies by intent to prioritize and route appropriately.

## Inputs
- **Email Content**: Subject + body
- **Context**: Campaign, sender info
- **Classification Rules**: Custom categories

## Process

### 1. Classify Reply
```bash
python3 execution/classify_email_reply.py \
  --email_id "[ID]" \
  --output .tmp/classification.json
```

### 2. Classification Categories

**Positive (High Priority):**
- Interested - wants to learn more
- Meeting request - wants to schedule
- Question - asking about offer
- Referral - pointing to someone else

**Neutral:**
- Out of office - auto-reply
- More info - needs details first
- Timing - not now, maybe later
- Wrong person - redirect needed

**Negative:**
- Not interested - clear rejection
- Unsubscribe - wants off list
- Competitor - using alternative
- Do not contact - strong rejection

### 3. Response Routing
| Classification | Action |
|----------------|--------|
| Interested | Priority response, send calendar |
| Meeting request | Auto-send scheduling link |
| Question | Queue for personalized response |
| Out of office | Pause sequence, resume later |
| Not interested | Remove from sequence |
| Unsubscribe | Unsubscribe immediately |

### 4. Classification Output
```json
{
  "email_id": "12345",
  "classification": "interested",
  "confidence": 0.92,
  "sentiment": "positive",
  "key_phrases": ["love to learn more", "sounds interesting"],
  "suggested_response": "[Draft response]",
  "priority": "high",
  "action": "send_calendar_link"
}
```

### 5. Auto-Responses

**Interested:**
```
Great to hear from you, [NAME]!

Here's my calendar to find a time that works:
[CALENDAR_LINK]

Looking forward to connecting!
```

**Question:**
```
Great question, [NAME]!

[ANSWER TO SPECIFIC QUESTION]

Would you like to discuss further? [CALENDAR_LINK]
```

### 6. Reporting
```markdown
# Reply Classification Report

## This Week
- Total replies: 150
- Positive: 45 (30%)
- Neutral: 60 (40%)
- Negative: 45 (30%)

## Top Categories
1. Interested: 28
2. Not interested: 35
3. Out of office: 42
4. Questions: 17
```

## Integrations
- Email platform (Instantly, Smartlead)
- OpenAI (classification)
- CRM

## Cost
- ~$0.01 per email classified
