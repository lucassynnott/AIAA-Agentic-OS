# Sales Pipeline Dashboard Generator

## What This Workflow Is
This workflow generates visual sales pipeline dashboards from CRM data, showing deal stages, values, and velocity metrics.

## What It Does
1. Pulls deal data from CRM
2. Calculates pipeline metrics
3. Generates stage visualizations
4. Tracks velocity and conversion
5. Outputs to Google Sheets/Slides

## Prerequisites

### Required API Keys (add to .env)
```
HUBSPOT_API_KEY=your_hubspot_key          # Or CRM
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- CRM API access

### Installation
```bash
pip install requests google-api-python-client
```

## How to Run

### Step 1: Generate Dashboard
```bash
python3 execution/generate_pipeline_dashboard.py \
  --source hubspot \
  --output_sheet "[SHEET_URL]"
```

### Quick One-Liner
```bash
python3 execution/generate_pipeline_dashboard.py --source hubspot
```

## Goal
Generate visual sales pipeline dashboards from CRM data.

## Inputs
- **CRM Source**: HubSpot, Salesforce, Pipedrive, GHL
- **Time Period**: This month, quarter, year
- **Metrics**: Revenue, deals, conversion rates

## Process

### 1. Pull Pipeline Data
```bash
python3 execution/generate_pipeline_dashboard.py \
  --crm hubspot \
  --period this_quarter \
  --output .tmp/dashboard.html
```

### 2. Dashboard Sections

**Pipeline Overview:**
- Total pipeline value
- Deals by stage
- Weighted pipeline
- Average deal size

**Stage Funnel:**
```
Lead        │████████████████████│ 100
Qualified   │█████████████       │ 65
Demo        │████████            │ 40
Proposal    │██████              │ 30
Negotiation │███                 │ 15
Closed Won  │██                  │ 10
```

**Key Metrics:**
| Metric | Current | Goal | Status |
|--------|---------|------|--------|
| Pipeline Value | $500K | $600K | 🟡 83% |
| Deals Created | 45 | 50 | 🟡 90% |
| Win Rate | 22% | 25% | 🟡 88% |
| Avg Deal Size | $12K | $15K | 🟡 80% |

**Deal Velocity:**
- Avg days in each stage
- Stage-to-stage conversion
- Bottleneck identification

### 3. Rep Performance
| Rep | Pipeline | Deals | Win Rate |
|-----|----------|-------|----------|
| Jane | $200K | 15 | 28% |
| John | $180K | 18 | 22% |
| Bob | $120K | 12 | 18% |

### 4. Forecast
```
Current Pipeline: $500,000
Expected Close (weighted): $150,000
Quota: $200,000
Gap: $50,000
```

### 5. At-Risk Deals
Deals stalled or at risk:
- [Deal] - $50K - No activity 14 days
- [Deal] - $30K - Pushed twice

### 6. Output Formats
- Interactive HTML
- PDF report
- Google Sheets
- Slack summary

## Integrations
- CRM APIs
- Google Sheets
- Slack

## Cost
- API calls: Free
- Generation: ~$0.05
