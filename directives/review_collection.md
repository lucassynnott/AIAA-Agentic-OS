# Review Collection Automation

## What This Workflow Is
This workflow automates review collection by sending timed requests to satisfied clients across Google, G2, Capterra, and other platforms.

## What It Does
1. Identifies happy clients (NPS 9-10, project complete)
2. Sends personalized review request email
3. Follows up if no response
4. Rotates platforms across clients
5. Tracks collection rates

## Prerequisites

### Required API Keys (add to .env)
```
SENDGRID_API_KEY=your_sendgrid_key        # Or email platform
HUBSPOT_API_KEY=your_hubspot_key          # For client/NPS data
```

### Required Tools
- Python 3.10+
- Email platform
- CRM with NPS data

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Trigger Review Request
```bash
python3 execution/request_review.py \
  --client_email "happy@client.com" \
  --client_name "John Smith" \
  --platform google \
  --review_link "[YOUR_GOOGLE_REVIEW_LINK]"
```

### Step 2: Check Pending Follow-ups
```bash
python3 execution/check_review_followups.py --days_since_request 3
```

### Quick One-Liner
```bash
python3 execution/request_review.py --client_email "[EMAIL]" --platform google
```

## Goal
Automatically request reviews from satisfied clients at optimal times.

## Inputs
- **Client List**: Active/completed clients
- **Review Platforms**: Google, G2, Capterra, Trustpilot
- **Trigger**: Project completion, milestone, or NPS score

## Process

### 1. Identify Happy Clients
Trigger review request when:
- NPS score 9-10
- Project completed successfully
- Positive feedback received
- X days after onboarding

### 2. Review Request Sequence

**Day 0 (Trigger):**
```
Subject: Quick favor? (30 seconds)

Hey [NAME],

Thrilled with the results we've achieved together!

Would you mind leaving a quick review? It really helps 
other [ROLE]s find us.

👉 [GOOGLE REVIEW LINK]

Just 2-3 sentences about your experience is perfect.

Thanks so much!
[YOUR NAME]
```

**Day 3 (If no review):**
```
Subject: Re: Quick favor?

Hey [NAME],

Just a gentle nudge on the review - would mean a lot!

Here's the link again: [LINK]

If you're short on time, here's a template:
"[COMPANY] helped us [RESULT]. [NAME] was [QUALITY]. 
Highly recommend!"

Thanks!
```

**Day 7 (Final):**
```
Subject: Last ask about this

[NAME],

No pressure at all - just wanted to send this one 
last time.

[LINK]

Either way, thanks for being a great client!
```

### 3. Review Incentives (Optional)
- Feature in case study
- Extended support
- Discount on renewal
- Gift card (where allowed)

### 4. Platform Rotation
Rotate review requests across platforms:
- Week 1 clients → Google
- Week 2 clients → G2
- Week 3 clients → Trustpilot

### 5. Track & Report
- Reviews requested
- Reviews received
- Response rate
- Average rating

## Integrations
- CRM (trigger data)
- Email platform
- Review platform links

## Best Practices
- Ask at peak satisfaction
- Make it easy (direct link)
- Provide template/guidance
- Thank publicly
