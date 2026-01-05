# Win/Loss Analysis Report

## What This Workflow Is
This workflow analyzes won and lost deals from CRM to identify patterns, common objections, and opportunities to improve close rates.

## What It Does
1. Pulls deal data from CRM
2. Segments wins vs losses
3. Analyzes patterns (size, industry, timing)
4. Identifies common loss reasons
5. Generates actionable report

## Prerequisites

### Required API Keys (add to .env)
```
HUBSPOT_API_KEY=your_hubspot_key
OPENAI_API_KEY=your_openai_key
```

### Installation
```bash
pip install requests openai
```

## How to Run
```bash
python3 execution/win_loss_analysis.py --period "last_quarter" --output .tmp/report.md
```

## Goal
Analyze won and lost deals to identify patterns and improve close rates.

## Inputs
- **CRM Data**: Closed deals (won and lost)
- **Time Period**: Last quarter, 6 months, year
- **Analysis Depth**: Basic or detailed

## Process

### 1. Generate Analysis
```bash
python3 execution/win_loss_analysis.py \
  --crm hubspot \
  --period last_quarter \
  --output .tmp/win_loss_report.md
```

### 2. Report Structure
```markdown
# Win/Loss Analysis Report
**Period:** [Date Range]

## Executive Summary
- Total deals analyzed: X
- Win rate: X%
- Key finding: [Main insight]

## Overall Performance
| Metric | Won | Lost | Total |
|--------|-----|------|-------|
| Deals | 45 | 55 | 100 |
| Value | $500K | $600K | $1.1M |
| Win Rate | 45% | 55% | - |

## Win Patterns

### What Won Deals Have in Common
1. **[Pattern 1]**: X% of wins had this
2. **[Pattern 2]**: X% correlation
3. **[Pattern 3]**: Strong indicator

### Top Reasons for Winning
1. Price/Value (32%)
2. Product fit (28%)
3. Relationship (22%)
4. Speed (18%)

## Loss Patterns

### Common Loss Reasons
1. Budget/Price (35%)
2. Competitor (25%)
3. No decision (20%)
4. Product gap (12%)
5. Timing (8%)

### Lost to Which Competitors
| Competitor | Lost Deals | % of Losses |
|------------|------------|-------------|
| Competitor A | 12 | 22% |
| Competitor B | 8 | 15% |

## Segment Analysis

### By Deal Size
| Size | Win Rate | Trend |
|------|----------|-------|
| <$10K | 55% | ↑ |
| $10-50K | 42% | → |
| >$50K | 28% | ↓ |

### By Industry
| Industry | Win Rate |
|----------|----------|
| Tech | 48% |
| Healthcare | 35% |
| Finance | 42% |

### By Lead Source
| Source | Win Rate |
|--------|----------|
| Referral | 62% |
| Inbound | 45% |
| Outbound | 32% |

## Recommendations
1. [Actionable recommendation based on data]
2. [Process improvement suggestion]
3. [Training focus area]
```

### 3. AI Insights
- Pattern recognition across deals
- Anomaly detection
- Predictive indicators

## Integrations
- CRM API
- Google Sheets
- AI analysis

## Cost
- ~$0.10-0.20 per analysis
