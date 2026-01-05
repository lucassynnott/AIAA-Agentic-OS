# AI Lead Qualification & Scoring

## What This Workflow Is
This workflow uses AI to automatically analyze and score your lead lists, identifying which prospects are most likely to convert based on their fit with your ideal customer profile (ICP) and observable buying signals.

## What It Does
1. Reads your lead list from Google Sheets or CSV
2. Analyzes each lead against your ICP criteria using AI
3. Scores leads on ICP fit, intent signals, and engagement potential
4. Classifies leads as Hot/Warm/Cool/Cold
5. Provides AI reasoning for each score
6. Updates your sheet with scores and recommended actions

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # Or use ANTHROPIC_API_KEY
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Google OAuth credentials (`credentials.json`)
- OpenAI or Anthropic API access

### Installation
```bash
pip install openai anthropic google-api-python-client gspread
```

## How to Run

### Step 1: Define Your ICP Criteria
Create `criteria.json`:
```json
{
  "company_size": {"ideal": "50-200", "weight": 0.25},
  "industry": {"ideal": ["SaaS", "Tech", "Agency"], "weight": 0.20},
  "job_title": {"ideal": ["CEO", "VP", "Director"], "weight": 0.20},
  "location": {"ideal": ["US", "UK", "Canada"], "weight": 0.15},
  "tech_stack": {"ideal": ["HubSpot", "Salesforce"], "weight": 0.10},
  "funding": {"ideal": "Series A+", "weight": 0.10}
}
```

### Step 2: Read Your Lead List
```bash
python3 execution/read_sheet.py "[SHEET_URL]" --output .tmp/leads.json
```

### Step 3: Run AI Scoring
```bash
python3 execution/score_leads_ai.py \
  .tmp/leads.json \
  --icp_criteria criteria.json \
  --output .tmp/scored_leads.json
```

### Step 4: Update Sheet with Scores
```bash
python3 execution/update_sheet.py \
  .tmp/scored_leads.json \
  "[SHEET_URL]" \
  --add_columns "score,classification,reasoning"
```

### Quick One-Liner
```bash
python3 execution/read_sheet.py "[SHEET_URL]" -o .tmp/leads.json && \
python3 execution/score_leads_ai.py .tmp/leads.json --icp_criteria criteria.json && \
python3 execution/update_sheet.py .tmp/scored_leads.json "[SHEET_URL]"
```

## Goal
Use AI to analyze and score leads based on ICP fit, buying signals, and engagement potential.

## Inputs
- **Lead List**: Google Sheet URL or CSV with lead data
- **ICP Criteria**: Ideal customer profile definition
- **Scoring Weights**: Importance of each criterion (optional)

## Tools/Scripts
- `execution/score_leads_ai.py` - AI scoring engine
- `execution/read_sheet.py` - Read leads from Sheets
- `execution/update_sheet.py` - Write scores back

## Process

### 1. Define ICP Criteria
Provide scoring criteria:
```json
{
  "company_size": {"ideal": "50-200", "weight": 0.25},
  "industry": {"ideal": ["SaaS", "Tech"], "weight": 0.20},
  "job_title": {"ideal": ["CEO", "VP", "Director"], "weight": 0.20},
  "location": {"ideal": ["US", "UK", "Canada"], "weight": 0.15},
  "tech_stack": {"ideal": ["HubSpot", "Salesforce"], "weight": 0.10},
  "funding": {"ideal": "Series A+", "weight": 0.10}
}
```

### 2. Read Lead Data
```bash
python3 execution/read_sheet.py "[SHEET_URL]" --output .tmp/leads.json
```

### 3. AI Scoring
```bash
python3 execution/score_leads_ai.py .tmp/leads.json \
  --icp_criteria criteria.json \
  --output .tmp/scored_leads.json
```

AI analyzes each lead for:
- **ICP Fit** (0-100): How well they match ideal customer
- **Intent Signals** (0-100): Hiring, funding, growth indicators
- **Engagement Potential** (0-100): Likelihood to respond
- **Overall Score** (0-100): Weighted composite

### 4. Classify Leads
| Score Range | Classification | Action |
|-------------|----------------|--------|
| 80-100 | Hot | Prioritize immediate outreach |
| 60-79 | Warm | Standard sequence |
| 40-59 | Cool | Nurture campaign |
| 0-39 | Cold | Deprioritize or remove |

### 5. Update Sheet with Scores
```bash
python3 execution/update_sheet.py .tmp/scored_leads.json "[SHEET_URL]" --add_columns "score,classification,reasoning"
```

## Output Schema
| Column | Description |
|--------|-------------|
| lead_score | Overall score (0-100) |
| icp_fit | ICP match score |
| intent_score | Buying intent score |
| classification | Hot/Warm/Cool/Cold |
| reasoning | AI explanation |
| recommended_action | Suggested next step |

## Scoring Factors

### Positive Signals (+points)
- Recent funding round
- Hiring for relevant roles
- Tech stack matches your solution
- Company growth indicators
- Decision-maker title
- Active on LinkedIn

### Negative Signals (-points)
- Too small/large for ICP
- Wrong industry
- Geographic mismatch
- Already using competitor
- No website/minimal presence

## Integrations Required
- OpenAI/Anthropic API
- Google Sheets API

## Cost Estimate
- ~$0.01/lead for AI scoring
- **1000 leads: ~$10**

## Edge Cases
- Missing data: Score based on available fields
- Conflicting signals: Weight toward strongest indicators
- New companies: Flag for manual review
