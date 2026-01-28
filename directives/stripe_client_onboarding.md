# Stripe Client Onboarding Automation

> **Status:** ✅ Tested & Working | **Last Updated:** January 6, 2026

## What This Workflow Is
Automated client onboarding triggered by Stripe subscription payment. Creates Slack channel, sends branded HTML welcome email, researches the client via Perplexity, searches Fathom for past conversations, generates internal client report, and posts formatted summary to Slack.

## What It Does
1. Creates private Slack channel "{CLIENT NAME} - VIP"
2. Adds owner to channel with welcome message
3. Sends branded HTML welcome email via Gmail
4. Searches Fathom for past call transcripts (by company domain)
5. Runs real-time market research via Perplexity API
6. Generates AI internal client report combining research + Fathom data
7. Creates formatted Google Doc with full research
8. Posts rich Slack blocks to #content-approval with summary

## Prerequisites

### Required API Keys (configured in .env)
```bash
# Slack
SLACK_BOT_TOKEN=xoxb-...              # Bot token with scopes below
SLACK_WORKSPACE_ID=T05D5C7RCTF
SLACK_OWNER_USER_ID=U05D1LH2JG6
SLACK_CONTENT_CHANNEL_ID=C090GHU1YGG  # #content-approval

# Stripe
STRIPE_API_KEY=sk_live_...            # SECRET key (not publishable)
STRIPE_WEBHOOK_SECRET=whsec_...

# Gmail & Google Docs (OAuth via credentials.json)
GMAIL_SENDER=stopmoclay@gmail.com
GOOGLE_DRIVE_FOLDER_ID=1Xhgr63LTNqRI8ofFaVE-_zXYJLgjbBiF

# Fathom
FATHOM_API_KEY=...

# AI Research
PERPLEXITY_API_KEY=pplx-...           # For real-time web research
OPENROUTER_API_KEY=...                # For report generation
```

### Required Slack Bot Scopes
- `channels:manage` - Create channels
- `channels:write.invites` - Invite users
- `groups:write` - Create private channels
- `chat:write` - Post messages
- `users:read.email` - Look up users by email

### Google OAuth Setup
1. Place `client_secrets.json` in project root
2. Create symlink: `ln -s client_secrets.json credentials.json`
3. First run will prompt for OAuth authorization
4. Tokens saved to `token_gmail.json` and `token_docs.json`

### Installation
```bash
pip install slack-sdk google-api-python-client google-auth-oauthlib requests openai python-dotenv
```

## How to Run

### Manual Test
```bash
python3 execution/stripe_client_onboarding.py \
  --client_name "Client Name" \
  --client_email "client@company.com" \
  --company_website "company.com"
```

### Test with Different Email (for testing)
```bash
# Use real client's company for research, but route emails/Slack to test address
python3 execution/stripe_client_onboarding.py \
  --client_name "Mark Lucas" \
  --client_email "stopmoclay@gmail.com" \
  --company_website "marklucas.info"
```

### Via Stripe Webhook (Production)
Configure Stripe webhook to POST to Modal endpoint on:
- `customer.subscription.created`
- `invoice.payment_succeeded`

## Inputs
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client_name | string | Yes | Client's full name |
| client_email | string | Yes | Client's email address |
| company_website | string | No | Client's company domain (defaults to email domain) |

## Process Flow

### 1. Slack Channel Setup
- Creates private channel: `{client_name} - VIP` (sanitized)
- Adds owner (SLACK_OWNER_USER_ID) to channel
- Attempts to invite client by email (requires admin token)
- Posts welcome message with next steps

### 2. Welcome Email (Gmail)
Branded HTML email including:
- INOVATIV branding and 30% revenue guarantee
- What to expect (24hr Slack invite, 48hr kickoff call, Week 1 audit)
- Services overview (CRO, Email/SMS, Creative)
- Professional HTML formatting with plain text fallback

### 3. Fathom Call Search
- Searches by **company website domain** (not email domain)
- Retrieves transcripts and AI summaries
- Extracts action items from past calls
- API: `GET /meetings?calendar_invitees_domains[]={domain}`

### 4. Market Research (Perplexity)
Real-time web research including:
- Company overview and business model
- Products/services and pricing
- Online presence assessment
- Market position and competitors
- Opportunities for INOVATIV (CRO, email, creative)
- Key contacts

### 5. Internal Report Generation
AI synthesizes all data into actionable report:
- Client summary
- Key insights from research and Fathom calls
- Identified opportunities
- Potential challenges
- Recommended approach
- Questions for kickoff call
- Priority actions for Week 1

### 6. Google Doc Creation
- Creates formatted document with all research
- Moves to configured Drive folder
- Returns shareable URL

### 7. Slack Notification (#content-approval)
Rich block formatting with:
- Header with client name
- Fields: Email, Website, Fathom calls count, VIP channel
- Past conversation titles (from Fathom)
- Clickable link to Google Doc
- Clean summary excerpt

## Output
| Output | Location |
|--------|----------|
| Slack VIP Channel | `#{client-name}-vip` |
| Welcome Email | Client's inbox |
| Research Google Doc | Drive folder |
| Slack Summary | #content-approval |
| JSON Results | `.tmp/onboarding_{name}_{timestamp}.json` |

## Error Handling
| Scenario | Behavior |
|----------|----------|
| Slack channel exists | Uses existing channel |
| Client not in Slack | Logs warning, continues |
| Fathom no calls | Notes "No prior calls found" |
| Perplexity fails | Falls back to basic AI research |
| Google OAuth needed | Prompts for browser auth (first run only) |

## Company Context: INOVATIV
E-commerce growth agency that:
- Works with Shopify + Klaviyo brands ($50k-$250k+/month)
- Combines CRO + Email/SMS + Creative (integrated, not siloed)
- **Guarantees 30% revenue increase** or works free until achieved
- Focuses on: conversion optimization, lifecycle email flows, funnel assets

## Known Limitations
- **Slack workspace invites** require Enterprise Grid admin token
- **Fathom API** only returns meetings from past ~2 months
- **First run** requires browser OAuth for Gmail and Google Docs

## Related Files
- `execution/stripe_client_onboarding.py` - Main 850-line automation script
- `credentials.json` → `client_secrets.json` - Google OAuth credentials
- `token_gmail.json` - Gmail OAuth token (auto-generated)
- `token_docs.json` - Google Docs OAuth token (auto-generated)
