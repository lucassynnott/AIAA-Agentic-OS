# AI WhatsApp Support Bot

## What This Workflow Is
This workflow deploys an AI-powered WhatsApp chatbot that provides 24/7 customer support by answering questions from your knowledge base and escalating to humans when needed.

## What It Does
1. Ingests your knowledge base (FAQs, docs, product info)
2. Sets up WhatsApp Business API integration
3. Responds to customer messages using AI + knowledge
4. Automatically escalates complex issues to humans
5. Logs conversations to your CRM

## Prerequisites

### Required API Keys (add to .env)
```
TWILIO_SID=your_twilio_sid                # WhatsApp provider
TWILIO_AUTH_TOKEN=your_twilio_token
WHATSAPP_PHONE_ID=your_phone_id
OPENAI_API_KEY=your_openai_key            # For AI responses
PINECONE_API_KEY=your_pinecone_key        # Vector DB for knowledge
GOOGLE_APPLICATION_CREDENTIALS=credentials.json  # For Google Docs KB
```

### Required Accounts
- WhatsApp Business Account (verified)
- Twilio or 360dialog account
- Meta Business verification
- Vector database (Pinecone or Supabase)

### Installation
```bash
pip install twilio openai pinecone-client google-api-python-client
```

## How to Run

### Step 1: Prepare Your Knowledge Base
Create a Google Doc or Notion page with:
- Common FAQs and answers
- Product/service descriptions
- Pricing information
- Support policies

### Step 2: Ingest Knowledge
```bash
python3 execution/sync_knowledge_base.py \
  --source "https://docs.google.com/document/d/xxx" \
  --output .tmp/knowledge_vectors.json
```

### Step 3: Deploy Bot
```bash
python3 execution/setup_whatsapp_bot.py \
  --knowledge .tmp/knowledge_vectors.json \
  --business_name "Your Company" \
  --escalation_email "support@yourcompany.com"
```

### Step 4: Configure Webhook
Set your Twilio webhook URL to receive incoming messages.

### Step 5: Test Bot
Send a test message to your WhatsApp Business number.

### Update Knowledge Base
```bash
python3 execution/sync_knowledge_base.py --source "[DOC_URL]" --update
```

## Goal
Deploy an AI-powered WhatsApp chatbot for 24/7 customer support using your knowledge base.

## Inputs
- **Knowledge Base**: Google Docs, Notion, or FAQ document
- **Business Phone**: WhatsApp Business number
- **Escalation Rules**: When to hand off to human
- **Brand Voice**: Tone and style guidelines

## Tools/Scripts
- `execution/setup_whatsapp_bot.py` - Bot configuration
- `execution/sync_knowledge_base.py` - Knowledge ingestion

## Process

### 1. Prepare Knowledge Base
Create document with:
- FAQs and answers
- Product/service information
- Pricing details
- Common objections and responses
- Escalation triggers

### 2. Ingest Knowledge
```bash
python3 execution/sync_knowledge_base.py \
  --source "https://docs.google.com/document/d/xxx" \
  --output .tmp/knowledge_vectors.json
```

### 3. Configure Bot
```bash
python3 execution/setup_whatsapp_bot.py \
  --knowledge .tmp/knowledge_vectors.json \
  --business_name "[YOUR_BUSINESS]" \
  --escalation_email "[EMAIL]"
```

### 4. Bot Behavior

**Greeting**
```
Hi! 👋 I'm [Bot Name], [Company]'s AI assistant.

I can help with:
• Product questions
• Pricing info
• Support issues
• Booking appointments

How can I help you today?
```

**Response Flow**
1. Receive message
2. Search knowledge base
3. Generate contextual response
4. Check if escalation needed
5. Send response

**Escalation Triggers**
- "speak to human" / "real person"
- Billing/refund issues
- Complaints
- Complex technical issues
- 3+ failed answer attempts

### 5. Escalation Message
```
I want to make sure you get the best help possible.

I'm connecting you with a team member who will respond shortly.

Your conversation has been saved, so you won't need to repeat anything.
```

## Features

### Knowledge-Based Answers
Uses RAG to answer from your docs.

### Appointment Booking
Integrates with Calendly/Cal.com.

### Lead Qualification
Asks qualifying questions, logs to CRM.

### Order Status
Connects to order system for tracking.

### Multilingual
Auto-detects and responds in user's language.

## Response Guidelines
- Keep responses under 300 characters
- Use simple language
- Include relevant links when helpful
- Always offer human escalation option
- Don't make promises outside scope

## Integrations Required
- WhatsApp Business API (via Twilio/360dialog)
- OpenAI/Anthropic (AI responses)
- Vector database (Pinecone/Supabase)
- CRM (optional)
- Calendar (optional)

## Cost Estimate
- WhatsApp API: ~$0.005-0.05/message
- AI: ~$0.01/response
- **1000 conversations/month: ~$50-100**

## Setup Requirements
1. WhatsApp Business Account
2. Verified business phone number
3. Meta Business verification
4. API provider account (Twilio recommended)

## Edge Cases
- Spam messages: Rate limit + block
- Off-topic queries: Politely redirect
- Abusive messages: Auto-escalate + log
- After hours: Set expectations on response time
