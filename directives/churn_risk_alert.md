# Churn Risk Alert

## What This Workflow Is
This workflow monitors client engagement, payments, and support data to calculate churn risk scores and trigger retention alerts.

## What It Does
1. Pulls client engagement data from CRM
2. Calculates risk score based on indicators
3. Classifies risk level (critical/high/medium/low)
4. Sends Slack alerts with recommended actions
5. Creates retention tasks in CRM

## Prerequisites

### Required API Keys (add to .env)
```
HUBSPOT_API_KEY=your_hubspot_key          # Or CRM with client data
STRIPE_API_KEY=your_stripe_key            # For payment data
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- CRM API
- Payment platform

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Calculate Risk Scores
```bash
python3 execution/calculate_churn_risk.py \
  --source crm \
  --output .tmp/risk_scores.json
```

### Step 2: Send Alerts
```bash
python3 execution/send_churn_alerts.py \
  --scores .tmp/risk_scores.json \
  --threshold 40
```

### Quick One-Liner (Daily Cron)
```bash
python3 execution/calculate_churn_risk.py && python3 execution/send_churn_alerts.py --threshold 40
```

## Goal
Identify clients at risk of churning and trigger proactive retention actions.

## Inputs
- **Client Data**: Engagement, payments, support tickets
- **Risk Thresholds**: What defines at-risk
- **Alert Recipients**: Who to notify

## Process

### 1. Calculate Risk Score
```bash
python3 execution/calculate_churn_risk.py \
  --source crm \
  --output .tmp/risk_scores.json
```

### 2. Risk Indicators

**High Risk (+20 points each):**
- No login in 30+ days
- Missed payment
- Multiple support complaints
- Negative NPS score
- Requested cancellation info

**Medium Risk (+10 points each):**
- Declining usage trend
- Slow response to emails
- Missed check-in meetings
- No engagement with new features
- Contract renewal approaching

**Low Risk (+5 points each):**
- Reduced communication
- Support tickets increasing
- No referrals given
- Skipped QBR

### 3. Risk Classification
| Score | Level | Action |
|-------|-------|--------|
| 60+ | Critical | Immediate intervention |
| 40-59 | High | Proactive outreach |
| 20-39 | Medium | Monitor closely |
| 0-19 | Low | Standard service |

### 4. Alert Format
```markdown
# 🚨 Churn Risk Alert

## Critical Risk Clients
| Client | Score | Top Risk Factors | MRR at Risk |
|--------|-------|------------------|-------------|
| [Name] | 75 | No login, missed payment | $5,000 |

## Action Required
**[Client Name]** - Score: 75/100

Risk Factors:
- ❌ No platform login in 45 days
- ❌ Missed January payment
- ❌ NPS score dropped to 5

Recommended Actions:
1. Call from account manager today
2. Review recent deliverables
3. Offer value recovery plan

Contact: [Client Contact] - [Email] - [Phone]
```

### 5. Automated Actions
- Slack alert to AM
- Task created in CRM
- Escalation to leadership (if critical)
- Add to retention campaign

### 6. Prevention Playbooks

**Engagement Drop:**
- Send value recap
- Offer training session
- Share new features

**Payment Issues:**
- Payment reminder
- Offer payment plan
- Finance team outreach

**Support Complaints:**
- Executive apology
- Free service credit
- Priority support queue

## Integrations
- CRM
- Billing system
- Analytics
- Slack

## Cost
- Monitoring: Free
- ROI: Prevents churn (high value)
