# Funding Round Alert Lead Finder

## What This Workflow Is
This workflow monitors funding announcements from Crunchbase and news sources to identify newly funded companies as sales leads with buying signals.

## What It Does
1. Monitors funding sources (Crunchbase, TechCrunch)
2. Filters by stage, industry, amount, location
3. Enriches with decision maker contacts
4. Generates personalized outreach templates
5. Sends daily Slack alerts

## Prerequisites

### Required API Keys (add to .env)
```
CRUNCHBASE_API_KEY=your_crunchbase_key    # For funding data
APOLLO_API_KEY=your_apollo_key            # For contact enrichment
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- Crunchbase API access

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Track Funding
```bash
python3 execution/track_funding.py \
  --stages "Series A,Series B" \
  --industries "SaaS,FinTech" \
  --min_amount 1000000 \
  --days 30 \
  --output .tmp/funded_companies.json
```

### Quick One-Liner (Daily Cron)
```bash
python3 execution/track_funding.py --stages "Series A,Series B" --days 7
```

## Goal
Track recent funding announcements and generate leads from newly funded companies.

## Inputs
- **Funding Stage**: Seed, Series A, B, C, etc.
- **Industry**: Target sectors
- **Location**: Geographic filter
- **Amount Range**: Min/max funding amount
- **Timeframe**: Last 7, 30, 90 days

## Process

### 1. Monitor Funding Sources
```bash
python3 execution/track_funding.py \
  --stages "Series A,Series B" \
  --industries "SaaS,FinTech" \
  --min_amount 1000000 \
  --days 30 \
  --output .tmp/funded_companies.json
```

### 2. Data Sources
- Crunchbase
- TechCrunch
- PitchBook
- Twitter/X announcements
- Press releases
- LinkedIn funding posts

### 3. Data Collected
- Company name
- Funding amount
- Round type
- Lead investor
- Other investors
- Company website
- Industry
- Announcement date
- Growth signals

### 4. Lead Enrichment
For each funded company:
- Decision maker contacts
- Email addresses
- LinkedIn profiles
- Tech stack
- Employee count

### 5. Why Funding = Buying Signal
| Funding Stage | Typical Needs |
|---------------|---------------|
| Seed | Product, early customers |
| Series A | Scale sales, marketing |
| Series B | Operations, expansion |
| Series C+ | Enterprise tools, efficiency |

### 6. Outreach Template
```
Subject: Congrats on the [ROUND]!

Hi [NAME],

Saw [COMPANY] just raised [AMOUNT] from [INVESTOR] - 
congrats! Exciting times.

As you scale [SPECIFIC AREA], we help companies 
like yours [VALUE PROP].

[RELEVANT CASE STUDY]

Worth a quick call to see if we can help?
```

### 7. Daily Alert
```markdown
# Funding Alert - [DATE]

## Today's Rounds
| Company | Amount | Stage | Industry |
|---------|--------|-------|----------|
| [Name] | $XM | Series A | SaaS |

## Your Match Score
[Company]: 85/100 - Good fit because [reasons]
```

## Integrations
- Crunchbase API
- News APIs
- Email enrichment
- Slack alerts

## Cost
- Crunchbase: $49-199/mo
- Or scraping: ~$0.05/company
