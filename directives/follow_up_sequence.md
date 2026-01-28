# Follow-up Sequence Automation

## What This Workflow Is
This workflow automates multi-touch follow-up sequences across email, LinkedIn, and phone after key sales events like demos or proposals.

## What It Does
1. Triggers sequence based on event (demo, proposal, no response)
2. Sends personalized follow-ups on scheduled days
3. Tracks engagement across channels
4. Stops automatically when prospect responds
5. Updates CRM with sequence status

## Prerequisites

### Required API Keys (add to .env)
```
INSTANTLY_API_KEY=your_instantly_key      # Or SMARTLEAD, LEMLIST
HUBSPOT_API_KEY=your_hubspot_key          # For CRM sync
```

### Required Tools
- Python 3.10+
- Email automation platform
- CRM with API access

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Trigger a Sequence
```bash
python3 execution/trigger_sequence.py \
  --prospect_email "john@acme.com" \
  --sequence "post_demo" \
  --start_date "today"
```

### Step 2: Check Sequence Status
```bash
python3 execution/check_sequence_status.py --email "john@acme.com"
```

### Step 3: Stop Sequence
```bash
python3 execution/stop_sequence.py --email "john@acme.com" --reason "replied"
```

### Quick One-Liner
```bash
python3 execution/trigger_sequence.py --email "prospect@company.com" --sequence "post_demo"
```

## Goal
Automate multi-touch follow-up sequences after initial contact with prospects.

## Inputs
- **Trigger Event**: Demo completed, proposal sent, no response, etc.
- **Sequence Type**: Nurture, close, re-engage
- **Channel**: Email, LinkedIn, phone
- **Timing**: Days between touches

## Sequence Templates

### Post-Demo Follow-up
**Day 0:** Thank you + summary email
**Day 2:** Case study relevant to their use case
**Day 5:** "Any questions?" check-in
**Day 8:** Value-add content
**Day 12:** "Next steps?" with calendar link

### Post-Proposal Follow-up
**Day 0:** Proposal sent confirmation
**Day 3:** "Had a chance to review?"
**Day 7:** Address common objections
**Day 10:** Create urgency (limited offer/timeline)
**Day 14:** Break-up email

### Cold Email No-Response
**Email 2 (Day 3):** Different angle/value prop
**Email 3 (Day 7):** Social proof/case study
**Email 4 (Day 14):** Break-up with value

## Process

### 1. Trigger Sequence
```bash
python3 execution/trigger_sequence.py \
  --prospect_email "[EMAIL]" \
  --sequence "post_demo" \
  --start_date "today"
```

### 2. Personalization
Each email pulls:
- First name
- Company name
- Relevant case study
- Custom notes from CRM

### 3. Stop Conditions
- Prospect replies
- Meeting booked
- Unsubscribe requested
- Manual pause

## Multi-Channel Sequences
Day 1: Email
Day 3: LinkedIn view + connect
Day 5: Email
Day 7: LinkedIn message
Day 10: Email
Day 14: Phone call

## Integrations
- Email platform (Instantly, Lemlist)
- CRM
- LinkedIn automation
- Phone dialer (optional)

## Related Skill Bibles

### PRIMARY: Max Sturtevant's $40M+ Email Methodology

**[SKILL_BIBLE_sturtevant_email_master_system.md](../skills/SKILL_BIBLE_sturtevant_email_master_system.md)** ⭐ ESSENTIAL
- Sequence timing and structure (6,968 words)
- SCE Framework for follow-ups
- 75-word max body copy

**[SKILL_BIBLE_sturtevant_cart_recovery.md](../skills/SKILL_BIBLE_sturtevant_cart_recovery.md)**
- Follow-up timing (1hr, 4hr, 24hr, 48hr, 72hr)
- Urgency without desperation
- Re-engagement tactics

**[SKILL_BIBLE_sturtevant_copywriting.md](../skills/SKILL_BIBLE_sturtevant_copywriting.md)**
- Follow-up email copy formulas
- Subject line variations for sequences

### SUPPLEMENTARY

**[SKILL_BIBLE_hormozi_sales_training.md](../skills/SKILL_BIBLE_hormozi_sales_training.md)**
- Follow-up psychology
- Persistence frameworks
- Closing from follow-up

**[SKILL_BIBLE_cold_email_mastery.md](../skills/SKILL_BIBLE_cold_email_mastery.md)**
- Cold follow-up best practices
- Multi-touch sequences
