# Ultimate Client Reporting System

## What This Workflow Is
**Automated client reporting pipeline** that generates beautiful, insightful reports from raw data. Pulls metrics from ad platforms, analytics, and CRMs to create executive summaries, detailed breakdowns, and actionable recommendations. Saves agencies 10+ hours per client per month.

## What It Does
1. Pulls data from connected platforms (Meta, Google, Analytics)
2. Calculates key performance metrics
3. Generates AI-powered insights and recommendations
4. Creates beautiful formatted reports
5. Builds client-facing dashboards
6. Sends automated report delivery
7. Tracks historical performance trends

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI insights generation
GOOGLE_APPLICATION_CREDENTIALS=path   # Google Sheets/Docs
```

### Data Sources (provide API keys or manual data)
```
META_ACCESS_TOKEN=your_token          # Facebook/Instagram ads
GOOGLE_ADS_API_KEY=your_key           # Google Ads
GOOGLE_ANALYTICS_KEY=your_key         # GA4 data
```

### Required Skill Bibles
- `SKILL_BIBLE_client_reporting_dashboards.md`
- `SKILL_BIBLE_ad_performance_analysis.md`
- `SKILL_BIBLE_roi_calculator_creation.md`
- `SKILL_BIBLE_client_communication_setup.md`

## How to Run

```bash
# Generate monthly report
python3 execution/generate_client_report.py \
  --client "Acme Corp" \
  --period "monthly" \
  --start-date "2026-01-01" \
  --end-date "2026-01-31" \
  --service "meta_ads" \
  --format "pdf"

# Weekly performance update
python3 execution/generate_client_report.py \
  --client "Acme Corp" \
  --period "weekly" \
  --service "all" \
  --format "google_doc" \
  --send-email

# From manual data
python3 execution/generate_client_report.py \
  --client "Acme Corp" \
  --data-file performance_data.json \
  --format "both"
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client | string | Yes | Client name |
| period | enum | Yes | "weekly", "monthly", "quarterly" |
| start-date | date | Yes | Reporting period start |
| end-date | date | Yes | Reporting period end |
| service | enum | No | "meta_ads", "google_ads", "seo", "all" |
| format | enum | No | "pdf", "google_doc", "html", "both" |
| data-file | path | No | Manual data import |
| send-email | flag | No | Auto-send to client |
| include-recommendations | flag | No | Add AI recommendations |

## Process

### Phase 1: Data Collection

**Meta Ads Metrics:**
- Spend
- Impressions
- Reach
- Clicks (Link, All)
- CTR
- CPC
- CPM
- Conversions
- Cost per Conversion
- ROAS
- Frequency

**Google Ads Metrics:**
- Spend
- Impressions
- Clicks
- CTR
- CPC
- Conversions
- Cost per Conversion
- Search Impression Share
- Quality Score

**Google Analytics:**
- Sessions
- Users
- Page Views
- Bounce Rate
- Avg Session Duration
- Goal Completions
- E-commerce Revenue

### Phase 2: Data Processing

**Calculations:**
- Period-over-period changes (%)
- Running averages
- Trend analysis
- Anomaly detection
- Benchmark comparisons

**Segmentation:**
- By campaign
- By ad set/ad group
- By creative
- By audience
- By device
- By placement

### Phase 3: AI Insights Generation

Generate for each metric category:

**What Happened:**
- Key changes from previous period
- Notable trends
- Anomalies or outliers

**Why It Happened:**
- Analysis of contributing factors
- External factors (seasonality, competition)
- Internal factors (creative fatigue, audience saturation)

**What To Do Next:**
- Specific optimization recommendations
- Testing suggestions
- Budget reallocation advice
- Creative refresh priorities

### Phase 4: Report Generation

**Executive Summary (Page 1):**
- Overall performance score
- Key wins
- Areas of concern
- Top 3 recommendations

**Performance Dashboard (Page 2-3):**
- Visual charts and graphs
- Key metrics at a glance
- Trend lines

**Detailed Breakdown (Page 4-6):**
- Campaign-level analysis
- Creative performance
- Audience insights
- Device/placement breakdown

**Recommendations (Page 7):**
- Prioritized action items
- Testing roadmap
- Budget optimization

**Appendix:**
- Raw data tables
- Glossary of terms
- Methodology notes

### Phase 5: Delivery

**Google Doc:**
- Create from template
- Apply client branding
- Share with client

**PDF Export:**
- Generate from HTML/Markdown
- Professional formatting
- Charts as images

**Email Delivery:**
- Summary in email body
- Full report attached
- Key metrics highlighted

## Output Structure
```
.tmp/client_reports/{client_slug}/{period}/
├── data/
│   ├── raw_metrics.json
│   ├── processed_metrics.json
│   └── historical_comparison.json
├── insights/
│   ├── ai_analysis.md
│   └── recommendations.md
├── reports/
│   ├── executive_summary.md
│   ├── full_report.md
│   ├── report.pdf
│   └── charts/
├── delivery/
│   ├── email_body.md
│   └── sent_confirmation.json
└── result.json
```

## Report Templates

### Executive Summary Template
```markdown
# {Client Name} - {Period} Report

## Performance Score: {Score}/100

### Key Wins 🎉
- {Win 1}
- {Win 2}
- {Win 3}

### Areas of Focus 📊
- {Focus 1}
- {Focus 2}

### Top Recommendations
1. {Recommendation 1}
2. {Recommendation 2}
3. {Recommendation 3}

---

## Key Metrics at a Glance

| Metric | This Period | Last Period | Change |
|--------|-------------|-------------|--------|
| Spend | ${spend} | ${prev_spend} | {change}% |
| Conversions | {conv} | {prev_conv} | {change}% |
| ROAS | {roas}x | {prev_roas}x | {change}% |
| CPA | ${cpa} | ${prev_cpa} | {change}% |
```

### Insight Generation Prompts

**For Performance Analysis:**
```
Analyze this performance data and provide:
1. What happened (2-3 key observations)
2. Why it happened (root cause analysis)
3. What to do next (specific, actionable recommendations)

Data: {metrics_json}
Previous Period: {prev_metrics_json}
Industry Benchmarks: {benchmarks}
```

## Quality Gates

### Pre-Delivery Checklist
- [ ] All data sources connected
- [ ] Metrics calculated correctly
- [ ] Period-over-period accurate
- [ ] Charts rendering properly
- [ ] AI insights reviewed
- [ ] Recommendations relevant
- [ ] Formatting clean
- [ ] Client branding applied

### Report Quality Metrics
- Data accuracy: 100%
- Insight relevance: 90%+
- Actionability score: 8/10+
- Client satisfaction: 4.5/5+

## Error Handling

| Error | Solution |
|-------|----------|
| API connection fails | Use cached data, flag incomplete |
| Missing data points | Interpolate or exclude with note |
| AI insights irrelevant | Regenerate with more context |
| Formatting breaks | Fall back to simple template |

## Integration with Other Workflows

- `client_qbr_generator.md` - Quarterly reviews
- `meta_ads_campaign.md` - Campaign context
- `google_ads_campaign.md` - Campaign context
- `churn_risk_alert.md` - Early warning

## Automation Schedule

| Report Type | Frequency | Send Day | Send Time |
|-------------|-----------|----------|-----------|
| Weekly Update | Weekly | Monday | 9:00 AM |
| Monthly Report | Monthly | 1st | 10:00 AM |
| Quarterly Review | Quarterly | 1st of Q | 10:00 AM |

## Self-Annealing Notes

### What Works
- Visual charts > raw data tables
- Executive summary first
- Specific recommendations > generic advice
- Comparisons make data meaningful

### What Doesn't Work
- Data dumps without context
- Too many metrics (stick to 5-7 key ones)
- Vague recommendations
- No historical context

### Continuous Improvement
- Track which insights clients act on
- Survey clients on report usefulness
- Monitor report open/read rates
- A/B test report formats
