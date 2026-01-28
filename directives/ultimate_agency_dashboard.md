# Ultimate Agency Dashboard Generator

## What This Workflow Is
**Complete agency operations dashboard system** that creates KPI tracking, team performance, client health, and revenue metrics. Produces automated reports, alerts, and visualizations for agency management.

## What It Does
1. Defines key agency KPIs
2. Creates data collection templates
3. Generates dashboard layouts
4. Produces automated reporting
5. Creates alert systems
6. Generates team scorecards
7. Produces client health metrics

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI analysis
GOOGLE_APPLICATION_CREDENTIALS=path   # Sheets integration
```

### Required Skill Bibles
- `SKILL_BIBLE_agency_scaling_systems.md`
- `SKILL_BIBLE_client_reporting_dashboards.md`
- `SKILL_BIBLE_agency_operations.md`
- `SKILL_BIBLE_crm_pipeline_management.md`

## How to Run

```bash
python3 execution/generate_agency_dashboard.py \
  --agency-type "marketing" \
  --team-size 5 \
  --client-count 10 \
  --services "meta_ads,google_ads,seo" \
  --include-financial \
  --include-team-metrics
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| agency-type | string | Yes | Type of agency |
| team-size | int | Yes | Number of employees |
| client-count | int | Yes | Number of clients |
| services | list | Yes | Services offered |
| include-financial | flag | No | Add financial metrics |
| include-team-metrics | flag | No | Add team performance |

## Process

### Phase 1: KPI Definition

**Financial KPIs:**
- Monthly Recurring Revenue (MRR)
- Annual Run Rate
- Revenue per Client
- Profit Margin
- Cash Flow

**Client KPIs:**
- Client Retention Rate
- Client Lifetime Value
- Net Promoter Score
- Client Health Score
- Churn Risk

**Delivery KPIs:**
- On-Time Delivery Rate
- Client Satisfaction
- Campaign Performance
- Response Time
- Issue Resolution Time

**Team KPIs:**
- Utilization Rate
- Revenue per Employee
- Task Completion Rate
- Quality Score
- Client Feedback

### Phase 2: Dashboard Layout

**Executive Dashboard:**
- Revenue snapshot
- Client health overview
- Team utilization
- Key alerts

**Client Dashboard:**
- Individual client metrics
- Campaign performance
- Health score
- Next actions

**Team Dashboard:**
- Workload distribution
- Performance scores
- Capacity planning
- Training needs

**Financial Dashboard:**
- P&L summary
- Cash flow
- Revenue trends
- Forecast

### Phase 3: Alert System

**Critical Alerts:**
- Client churn risk (score < 50)
- Payment overdue (30+ days)
- Team overload (>100% capacity)
- Campaign failure (KPI miss)

**Warning Alerts:**
- Client feedback drop
- Delivery delays
- Budget concerns
- Resource constraints

### Phase 4: Automation

**Daily:**
- Pull campaign metrics
- Update client scores
- Check task completion

**Weekly:**
- Generate team reports
- Update dashboards
- Send summaries

**Monthly:**
- Full financial review
- Client health reports
- Team performance reviews

## Output Structure
```
.tmp/agency_dashboards/{agency_slug}/
├── kpis/
│   ├── kpi_definitions.md
│   └── tracking_templates/
├── dashboards/
│   ├── executive_dashboard.md
│   ├── client_dashboard_template.md
│   ├── team_dashboard.md
│   └── financial_dashboard.md
├── alerts/
│   └── alert_rules.md
├── automation/
│   ├── data_collection.md
│   └── reporting_schedule.md
└── result.json
```

## KPI Templates

### Client Health Score
```
Score = (
  Satisfaction × 0.25 +
  Payment Status × 0.20 +
  Campaign Performance × 0.25 +
  Engagement Level × 0.15 +
  Tenure × 0.15
) / 100

80-100: Healthy (Green)
60-79: At Risk (Yellow)
<60: Critical (Red)
```

### Team Utilization
```
Utilization = (Billable Hours / Available Hours) × 100

Target: 70-80%
>90%: Overloaded
<60%: Underutilized
```

### Revenue Health
```
Monthly Revenue Target: $X
Actual: $Y
% to Target: Y/X × 100

Also track:
- MRR Growth Rate
- Revenue per Client
- Client Acquisition Cost
- Payback Period
```

## Quality Gates

### Dashboard Checklist
- [ ] All KPIs defined with formulas
- [ ] Data sources identified
- [ ] Update frequency set
- [ ] Alert thresholds configured
- [ ] Team trained on usage
- [ ] Automation tested
- [ ] Visualization clear
