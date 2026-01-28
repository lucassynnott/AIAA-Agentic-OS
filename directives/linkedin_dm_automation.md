# LinkedIn DM Automation

## What This Workflow Is
This workflow automates personalized LinkedIn outreach including connection requests and follow-up message sequences while staying within platform limits.

## What It Does
1. Takes list of LinkedIn profile URLs
2. Generates personalized connection messages
3. Sends requests within daily limits
4. Follows up after connection acceptance
5. Tracks responses and manages sequences

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For personalization
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- LinkedIn automation tool (Dripify, Expandi) OR browser automation
- Google Sheets for target list

### Installation
```bash
pip install openai google-api-python-client
```

## How to Run

### Step 1: Prepare Target List
Create Google Sheet with columns: linkedin_url, first_name, company, notes

### Step 2: Generate Personalized Messages
```bash
python3 execution/personalize_linkedin_messages.py \
  --sheet "[SHEET_URL]" \
  --template connection_request \
  --output .tmp/messages.json
```

### Step 3: Queue Messages (with automation tool)
```bash
python3 execution/queue_linkedin_messages.py \
  --messages .tmp/messages.json \
  --daily_limit 50
```

### Quick One-Liner
```bash
python3 execution/personalize_linkedin_messages.py --sheet "[SHEET_URL]" --template connection_request
```

## Goal
Send personalized LinkedIn connection requests and follow-up messages at scale.

## Inputs
- **Target List**: LinkedIn profile URLs
- **Connection Message**: Personalized request template
- **Follow-up Sequence**: Messages after connection
- **Daily Limits**: Connections per day (50-100 safe)

## Process

### 1. Prepare Target List
Google Sheet with:
- LinkedIn URL
- First name
- Company
- Personalization notes

### 2. Generate Personalized Messages
```bash
python3 execution/personalize_linkedin_messages.py \
  --sheet "[SHEET_URL]" \
  --template connection_request \
  --output .tmp/messages.json
```

### 3. Connection Request Templates
**Template A: Mutual Interest**
```
Hi [NAME], saw we're both in [INDUSTRY]. 
Would love to connect and exchange ideas on [TOPIC].
```

**Template B: Content Reference**
```
Hi [NAME], your post on [TOPIC] resonated - 
especially [SPECIFIC POINT]. Let's connect!
```

**Template C: Mutual Connection**
```
Hi [NAME], noticed we're both connected to [PERSON]. 
Always good to expand the network!
```

### 4. Follow-up Sequence
**Day 1 (After Accept):**
```
Thanks for connecting, [NAME]! 

Quick question - are you currently [PAIN POINT QUESTION]?
```

**Day 3 (If No Reply):**
```
Hey [NAME], following up on my question about [TOPIC].

[VALUE ADD - insight, resource, or offer]

Worth a quick chat?
```

### 5. Safety Limits
- Connection requests: 50-80/day
- Messages: 100-150/day
- Warmup period: Start low, increase gradually
- Rest days: 1-2 days off per week

## Tools
- Dripify, Expandi, or LinkedHelper
- Or custom via browser automation

## Compliance
- Stay within LinkedIn limits
- Personalize every message
- No spam or hard selling
- Respect opt-outs

## Cost
- Automation tools: $50-100/mo
- Or custom scripts: Free

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_lead_generation.md](../skills/SKILL_BIBLE_hormozi_lead_generation.md)**
- LinkedIn outreach strategy
- Connection building
- Lead qualification

**[SKILL_BIBLE_hormozi_free_customer_acquisition.md](../skills/SKILL_BIBLE_hormozi_free_customer_acquisition.md)**
- Organic outreach tactics
- Relationship building
- Value-first messaging

**[SKILL_BIBLE_cold_email_mastery.md](../skills/SKILL_BIBLE_cold_email_mastery.md)**
- DM personalization frameworks
- Follow-up sequences
- Response optimization
