# Client QBR Generator

## What This Workflow Is
This workflow generates professional quarterly business review slide decks with performance data, AI-generated insights, and strategic recommendations.

## What It Does
1. Pulls quarterly metrics from all platforms
2. Analyzes performance trends
3. Generates AI insights and recommendations
4. Creates slide deck with charts
5. Exports to Google Slides

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
HUBSPOT_API_KEY=your_hubspot_key          # For client data
```

### Required Tools
- Python 3.10+
- Google Slides API
- Analytics APIs

### Installation
```bash
pip install openai google-api-python-client requests
```

## How to Run

### Step 1: Gather Data
```bash
python3 execution/gather_qbr_data.py \
  --client "[CLIENT]" \
  --quarter "Q4 2024" \
  --output .tmp/qbr_data.json
```

### Step 2: Generate QBR Deck
```bash
python3 execution/generate_qbr.py \
  --data .tmp/qbr_data.json \
  --template slides \
  --output .tmp/qbr_deck.pptx
```

### Quick One-Liner
```bash
python3 execution/gather_qbr_data.py --client "[CLIENT]" --quarter "Q4 2024" && \
python3 execution/generate_qbr.py --data .tmp/qbr_data.json
```

## Goal
Generate quarterly business review presentations with performance data, insights, and strategic recommendations.

## Inputs
- **Client**: Company name
- **Quarter**: Q1, Q2, Q3, Q4 + Year
- **Data Sources**: All relevant platforms
- **Format**: Google Slides or PDF

## Process

### 1. Gather Quarterly Data
```bash
python3 execution/gather_qbr_data.py \
  --client "[CLIENT]" \
  --quarter "Q4 2024" \
  --output .tmp/qbr_data.json
```

### 2. Generate QBR Deck
```bash
python3 execution/generate_qbr.py \
  --data .tmp/qbr_data.json \
  --template slides \
  --output .tmp/qbr_deck.pptx
```

### 3. QBR Slide Structure

**Slide 1: Title**
- Client logo
- Quarter
- Date

**Slide 2: Agenda**
- Performance review
- Key wins
- Challenges
- Next quarter priorities

**Slide 3: Executive Summary**
- 3-4 bullet overview
- Overall health indicator

**Slide 4: KPI Dashboard**
- Target vs Actual
- Quarter-over-quarter trend
- Year-over-year comparison

**Slides 5-8: Deep Dives**
- Channel/campaign breakdowns
- What worked, what didn't
- Learnings

**Slide 9: Key Wins**
- Top 3-5 achievements
- ROI highlights

**Slide 10: Challenges & Lessons**
- What went wrong
- How we addressed it
- Prevention going forward

**Slide 11: Next Quarter Priorities**
- Strategic focus areas
- Key initiatives
- Goals

**Slide 12: Recommendations**
- Strategic recommendations
- Investment opportunities
- Risk mitigation

**Slide 13: Questions & Discussion**

### 4. Data Visualizations
- Line charts (trends)
- Bar charts (comparisons)
- Pie charts (distribution)
- Tables (detailed metrics)

### 5. AI-Generated Insights
- Pattern analysis
- Anomaly detection
- Benchmark comparisons
- Predictive recommendations

## Integrations
- Google Analytics
- Ad platforms
- CRM
- Google Slides API

## Cost
- Data gathering: API costs
- Generation: ~$0.30-0.50
