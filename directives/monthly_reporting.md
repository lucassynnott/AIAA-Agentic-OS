# Monthly Client Reporting Automation

## What This Workflow Is
This workflow automates monthly client report generation by pulling metrics from all platforms and producing professional PDF/Google Doc reports.

## What It Does
1. Gathers data from analytics, CRM, ad platforms
2. Calculates MoM and YoY comparisons
3. Generates AI insights
4. Creates formatted report
5. Delivers via email or shared doc

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
HUBSPOT_API_KEY=your_hubspot_key
META_API_KEY=your_meta_key                # For ad data
```

### Required Tools
- Python 3.10+
- Analytics/CRM APIs
- Google Docs API

### Installation
```bash
pip install openai google-api-python-client requests
```

## How to Run

### Step 1: Gather Data
```bash
python3 execution/gather_report_data.py \
  --client "[CLIENT]" \
  --period "last_month" \
  --sources "analytics,crm,ads" \
  --output .tmp/data.json
```

### Step 2: Generate Report
```bash
python3 execution/generate_monthly_report.py \
  --data .tmp/data.json \
  --template executive \
  --output .tmp/report.pdf
```

### Quick One-Liner
```bash
python3 execution/gather_report_data.py --client "[CLIENT]" --period last_month && \
python3 execution/generate_monthly_report.py --data .tmp/data.json
```

## Goal
Generate and deliver professional monthly reports to clients with metrics, insights, and recommendations.

## Inputs
- **Client**: Company name
- **Data Sources**: Analytics, CRM, platform APIs
- **Report Type**: Executive summary or detailed
- **Delivery**: Email, Google Doc, or PDF

## Process

### 1. Gather Data
```bash
python3 execution/gather_report_data.py \
  --client "[CLIENT]" \
  --period "last_month" \
  --sources "analytics,crm,ads" \
  --output .tmp/data.json
```

### 2. Generate Report
```bash
python3 execution/generate_monthly_report.py \
  --data .tmp/data.json \
  --template executive \
  --output .tmp/report.pdf
```

### 3. Report Structure
```markdown
# Monthly Report: [CLIENT]
**Period:** [Month Year]
**Prepared by:** [Your Agency]

## Executive Summary
[2-3 paragraph overview of performance]

## Key Metrics
| Metric | This Month | Last Month | Goal | Status |
|--------|------------|------------|------|--------|
| [KPI 1] | X | Y | Z | 🟢/🟡/🔴 |
| [KPI 2] | X | Y | Z | 🟢/🟡/🔴 |

## Performance Highlights
✅ [Win 1]
✅ [Win 2]
✅ [Win 3]

## Challenges & Solutions
⚠️ [Challenge 1] → [How we're addressing]

## Campaign Breakdown
### [Campaign/Channel 1]
[Detailed metrics and analysis]

### [Campaign/Channel 2]
[Detailed metrics and analysis]

## ROI Analysis
- Investment: $X
- Revenue generated: $Y
- ROI: X%

## Next Month Plan
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Recommendations
[Strategic recommendations based on data]
```

### 4. Delivery Options
- **Email**: Attachment + summary
- **Google Doc**: Shared link
- **PDF**: Professional formatted
- **Dashboard**: Live link

### 5. Automation Schedule
- Data pulled: 1st of month
- Report generated: 2nd of month
- Review period: 2nd-3rd
- Delivered: 4th of month

## Integrations
- Google Analytics
- Ad platforms (Meta, Google)
- CRM
- Email platform

## Cost
- Data gathering: API costs
- Report generation: ~$0.10-0.20

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_profit_maximization.md](../skills/SKILL_BIBLE_hormozi_profit_maximization.md)**
- Performance metrics that matter
- ROI analysis frameworks
- Growth indicators

**[SKILL_BIBLE_hormozi_customer_retention.md](../skills/SKILL_BIBLE_hormozi_customer_retention.md)**
- Client communication
- Success metrics presentation
- Relationship building through reports

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Marketing metrics analysis
- Campaign performance evaluation
- Data-driven recommendations
