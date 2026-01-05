# Client Health Score Calculator

## What This Workflow Is
This workflow calculates health scores for each client based on engagement, results, relationship quality, and payment history to predict churn risk and prioritize retention efforts.

## What It Does
1. Pulls data from CRM, billing, and support platforms
2. Scores each client on 4 dimensions (engagement, results, relationship, financial)
3. Classifies clients as Healthy, Stable, At Risk, or Critical
4. Generates dashboard with prioritized action items
5. Alerts team when scores drop significantly

## Prerequisites

### Required API Keys (add to .env)
```
HUBSPOT_API_KEY=your_hubspot_key          # Or SALESFORCE credentials
STRIPE_API_KEY=your_stripe_key            # For payment data
INTERCOM_API_KEY=your_intercom_key        # For support data
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- CRM with API access
- Billing platform API

### Installation
```bash
pip install requests google-api-python-client
```

## How to Run

### Step 1: Gather Client Data
```bash
python3 execution/gather_client_metrics.py \
  --source "hubspot,stripe,intercom" \
  --output .tmp/client_metrics.json
```

### Step 2: Calculate Health Scores
```bash
python3 execution/calculate_health_scores.py \
  --data .tmp/client_metrics.json \
  --weights default \
  --output .tmp/health_scores.json
```

### Step 3: Generate Dashboard
```bash
python3 execution/generate_health_dashboard.py \
  --scores .tmp/health_scores.json \
  --output .tmp/health_dashboard.html
```

### Quick One-Liner
```bash
python3 execution/gather_client_metrics.py --source "hubspot,stripe" && \
python3 execution/calculate_health_scores.py --data .tmp/client_metrics.json && \
python3 execution/generate_health_dashboard.py --scores .tmp/health_scores.json
```

### Daily Automated Run (Cron)
```bash
0 8 * * * cd /path/to/project && python3 execution/run_health_check.py --slack_alert
```

## Goal
Calculate client health scores to predict churn risk and prioritize retention efforts.

## Inputs
- **Client List**: Active clients with engagement data
- **Metrics**: Usage, communication, results, payments
- **Thresholds**: What defines healthy vs at-risk

## Health Score Components

### 1. Engagement Score (25%)
| Factor | Points | Criteria |
|--------|--------|----------|
| Login frequency | 0-25 | Daily=25, Weekly=15, Monthly=5, Never=0 |
| Feature adoption | 0-25 | Using 80%+ features=25 |
| Support tickets | 0-25 | Few=25, Many unresolved=5 |

### 2. Results Score (30%)
| Factor | Points | Criteria |
|--------|--------|----------|
| KPI achievement | 0-30 | Meeting goals=30 |
| ROI positive | 0-30 | Clear ROI=30 |
| Improvement trend | 0-30 | Improving=30, Declining=5 |

### 3. Relationship Score (25%)
| Factor | Points | Criteria |
|--------|--------|----------|
| NPS score | 0-25 | Promoter=25, Passive=15, Detractor=5 |
| Communication | 0-25 | Responsive=25, Slow/None=5 |
| Meeting attendance | 0-25 | Always=25, Sometimes=15, Rarely=5 |

### 4. Financial Score (20%)
| Factor | Points | Criteria |
|--------|--------|----------|
| Payment history | 0-20 | On-time=20, Late=10, Missed=0 |
| Contract length | 0-20 | Annual=20, Monthly=10 |
| Expansion potential | 0-20 | High=20, Low=5 |

## Process

### 1. Gather Client Data
```bash
python3 execution/gather_client_metrics.py \
  --source "hubspot,stripe,intercom" \
  --output .tmp/client_metrics.json
```

### 2. Calculate Scores
```bash
python3 execution/calculate_health_scores.py \
  --data .tmp/client_metrics.json \
  --weights default \
  --output .tmp/health_scores.json
```

### 3. Health Classifications
| Score | Status | Action |
|-------|--------|--------|
| 80-100 | 🟢 Healthy | Upsell opportunity |
| 60-79 | 🟡 Stable | Monitor, nurture |
| 40-59 | 🟠 At Risk | Proactive outreach |
| 0-39 | 🔴 Critical | Immediate intervention |

### 4. Output Dashboard

```markdown
# Client Health Dashboard
**Generated:** [Date]

## Portfolio Overview
- Total Clients: [X]
- Healthy (80+): [X] ([%])
- Stable (60-79): [X] ([%])
- At Risk (40-59): [X] ([%])
- Critical (<40): [X] ([%])

## At-Risk Clients (Immediate Attention)

| Client | Score | Trend | Top Risk Factor | Action |
|--------|-------|-------|-----------------|--------|
| [Client 1] | 35 | ↓ | No results | Call today |
| [Client 2] | 42 | ↓ | No engagement | Check in |

## Score Breakdown by Client

### [Client Name] - Score: 72 🟡
- Engagement: 18/25
- Results: 22/30
- Relationship: 17/25
- Financial: 15/20

**Risk Factors:**
- Declining engagement (login frequency down)
- Missed last 2 check-in calls

**Recommended Actions:**
1. Schedule urgent call
2. Review deliverables
3. Send value recap

## Trends
- Average health score: [X] (vs [Y] last month)
- Clients improving: [X]
- Clients declining: [X]

## Churn Prediction
Based on historical patterns:
- [X] clients likely to churn in 30 days
- Est. revenue at risk: $[X]
```

### 5. Automation
- Daily score recalculation
- Weekly health report
- Instant alert on score drop >10 points
- Trigger playbooks based on status

## Integrations Required
- CRM (client data)
- Billing (Stripe, payment history)
- Support (Intercom, Zendesk)
- Analytics (usage data)

## Intervention Playbooks

### At Risk (40-59)
1. Personal call from account manager
2. Value recap email
3. Quick win delivery
4. Executive check-in offer

### Critical (<40)
1. Same-day call from leadership
2. Audit current deliverables
3. Present improvement plan
4. Offer concession if needed

## Cost Estimate
- API calls: ~$5/mo
- Automation: Free (n8n)
