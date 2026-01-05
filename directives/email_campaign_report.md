# Email Campaign Performance Report

## What This Workflow Is
This workflow automatically pulls data from your cold email platform, generates performance reports with AI-powered insights, and delivers them via email or Slack.

## What It Does
1. Connects to Instantly/Smartlead/Lemlist API
2. Pulls campaign metrics (opens, replies, bounces)
3. Calculates KPIs and compares to benchmarks
4. Generates AI insights and recommendations
5. Delivers formatted report to your inbox/Slack

## Prerequisites

### Required API Keys (add to .env)
```
INSTANTLY_API_KEY=your_instantly_key      # Or SMARTLEAD_API_KEY
OPENAI_API_KEY=your_openai_key            # For AI insights
SENDGRID_API_KEY=your_sendgrid_key        # For email delivery
SLACK_WEBHOOK_URL=your_slack_webhook      # For Slack delivery
```

### Required Tools
- Python 3.10+
- Email platform with API access
- OpenAI API access

### Installation
```bash
pip install openai requests
```

## How to Run

### Step 1: Fetch Campaign Data
```bash
python3 execution/fetch_campaign_stats.py \
  --platform instantly \
  --date_range "last_7_days" \
  --output .tmp/stats.json
```

### Step 2: Generate Report
```bash
python3 execution/generate_campaign_report.py \
  --stats .tmp/stats.json \
  --output .tmp/report.html
```

### Step 3: Deliver Report
```bash
python3 execution/send_report.py \
  --report .tmp/report.html \
  --to "you@company.com" \
  --slack_channel "#cold-email"
```

### Quick One-Liner (Daily Report)
```bash
python3 execution/fetch_campaign_stats.py --platform instantly --date_range "yesterday" && \
python3 execution/generate_campaign_report.py --stats .tmp/stats.json && \
python3 execution/send_report.py --report .tmp/report.html --to "team@company.com"
```

### Automated Daily Report (Cron)
Add to crontab: `0 8 * * * cd /path/to/project && python3 execution/run_daily_report.py`

## Goal
Generate automated daily/weekly reports on cold email campaign performance with insights and recommendations.

## Inputs
- **Platform**: Instantly, Smartlead, or Lemlist
- **Report Frequency**: Daily or Weekly
- **Delivery**: Email, Slack, or Google Sheet
- **Campaigns**: All or specific campaign IDs

## Tools/Scripts
- `execution/fetch_campaign_stats.py` - Pull platform data
- `execution/generate_campaign_report.py` - Create report
- `execution/send_report.py` - Deliver report

## Process

### 1. Fetch Campaign Data
```bash
python3 execution/fetch_campaign_stats.py \
  --platform instantly \
  --date_range "last_7_days" \
  --output .tmp/stats.json
```

### 2. Metrics Collected
- **Sent**: Total emails sent
- **Delivered**: Successfully delivered
- **Opened**: Unique opens
- **Replied**: Total replies
- **Positive Replies**: Interested responses
- **Bounced**: Hard/soft bounces
- **Unsubscribed**: Opt-outs

### 3. Calculate KPIs
| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Delivery Rate | Delivered/Sent | >95% |
| Open Rate | Opens/Delivered | >50% |
| Reply Rate | Replies/Delivered | >5% |
| Positive Rate | Positive/Replies | >30% |
| Bounce Rate | Bounced/Sent | <3% |

### 4. Generate Report
```bash
python3 execution/generate_campaign_report.py \
  --stats .tmp/stats.json \
  --output .tmp/report.html
```

### 5. Report Structure

```markdown
# Campaign Performance Report
**Period:** [Date Range]
**Generated:** [Timestamp]

## Executive Summary
[AI-generated summary of performance]

## Overall Metrics
| Metric | This Period | Previous | Change |
|--------|-------------|----------|--------|
| Sent | 5,000 | 4,500 | +11% |
| Open Rate | 52% | 48% | +4% |
| Reply Rate | 6.2% | 5.8% | +0.4% |

## Campaign Breakdown
### Campaign: [Name]
- Sent: X
- Opens: X (X%)
- Replies: X (X%)
- Status: 🟢 Healthy / 🟡 Warning / 🔴 Critical

## Domain Health
| Domain | Sent | Bounce | Status |
|--------|------|--------|--------|
| domain1.com | 500 | 1.2% | 🟢 |
| domain2.com | 500 | 4.5% | 🔴 |

## Top Performing
- Best subject line: "[Subject]" (58% open)
- Best campaign: "[Name]" (8.2% reply)

## Alerts
⚠️ domain2.com bounce rate above threshold
⚠️ Campaign X reply rate declining

## Recommendations
1. [AI-generated recommendation]
2. [AI-generated recommendation]
```

### 6. Deliver Report
```bash
python3 execution/send_report.py \
  --report .tmp/report.html \
  --to "team@company.com" \
  --slack_channel "#cold-email"
```

## Alerts & Thresholds

### Red Alerts (Immediate Action)
- Bounce rate >5%
- Delivery rate <90%
- Domain blacklisted

### Yellow Warnings
- Bounce rate 3-5%
- Reply rate declining week-over-week
- High unsubscribe rate

### Green (Healthy)
- All metrics within benchmarks
- Positive trend

## Integrations Required
- Email platform API (Instantly/Smartlead)
- Gmail/SendGrid (report delivery)
- Slack (optional)
- Google Sheets (optional)

## Automation
- Daily report: 8am
- Weekly summary: Monday 9am
- Real-time alerts: On threshold breach

## Cost Estimate
- API calls: Free (within platform limits)
- AI analysis: ~$0.05/report
