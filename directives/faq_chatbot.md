# FAQ Chatbot (Slack/Telegram)

## What This Workflow Is
This workflow deploys an AI-powered FAQ chatbot in Slack or Telegram that answers questions from your knowledge base with human escalation.

## What It Does
1. Ingests your knowledge base (docs, FAQs)
2. Deploys bot to Slack/Telegram channel
3. Answers questions using RAG
4. Cites sources for transparency
5. Escalates to humans when unsure

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For AI responses
PINECONE_API_KEY=your_pinecone_key        # Vector database
SLACK_BOT_TOKEN=your_slack_bot_token      # Or TELEGRAM_BOT_TOKEN
```

### Required Tools
- Python 3.10+
- Slack/Telegram bot configured
- Vector database

### Installation
```bash
pip install openai pinecone-client slack-sdk
```

## How to Run

### Step 1: Ingest Knowledge Base
```bash
python3 execution/ingest_knowledge.py \
  --source "https://docs.yourcompany.com" \
  --output .tmp/kb_vectors.json
```

### Step 2: Deploy Bot
```bash
python3 execution/deploy_faq_bot.py \
  --platform slack \
  --knowledge .tmp/kb_vectors.json \
  --channel "#support"
```

### Quick One-Liner
```bash
python3 execution/ingest_knowledge.py --source "[DOCS_URL]" && \
python3 execution/deploy_faq_bot.py --platform slack --channel "#support"
```

## Goal
Deploy an AI chatbot that answers FAQs from your knowledge base in Slack or Telegram.

## Inputs
- **Platform**: Slack or Telegram
- **Knowledge Base**: FAQ document, docs, or website
- **Scope**: What it should/shouldn't answer
- **Escalation**: When to hand off to human

## Process

### 1. Prepare Knowledge Base
```bash
python3 execution/ingest_knowledge.py \
  --source "https://docs.yourcompany.com" \
  --output .tmp/kb_vectors.json
```

### 2. Deploy Bot
```bash
python3 execution/deploy_faq_bot.py \
  --platform slack \
  --knowledge .tmp/kb_vectors.json \
  --channel "#support"
```

### 3. Bot Behavior

**On Question:**
1. Search knowledge base
2. Generate answer if confident
3. Cite source
4. Offer human escalation

**Response Format:**
```
Based on our documentation:

[ANSWER]

📚 Source: [Link to doc]

Was this helpful? React with 👍 or 👎
Need more help? Type "human" for team support.
```

### 4. Commands
- `/faq [question]` - Ask a question
- `/search [topic]` - Search docs
- `/human` - Request human help
- `/feedback` - Give feedback

### 5. Confidence Handling
| Confidence | Action |
|------------|--------|
| >90% | Answer directly |
| 70-90% | Answer + offer human |
| <70% | "I'm not sure" + escalate |

### 6. Escalation Message
```
I want to make sure you get accurate help.

Let me get a team member. @support-team can you 
assist with this question?

Your question has been logged and someone will 
respond shortly.
```

## Integrations
- Slack/Telegram API
- Vector database (Pinecone, Supabase)
- OpenAI/Anthropic

## Cost
- AI: ~$0.01/question
- Slack: Free (basic)
