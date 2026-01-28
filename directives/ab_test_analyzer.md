# A/B Test Result Analyzer

## What This Workflow Is
This workflow analyzes A/B test results, calculates statistical significance, and generates clear recommendations on whether to implement the variant.

## What It Does
1. Takes control vs variant data as input
2. Calculates conversion rates and lift
3. Performs statistical significance tests
4. Generates confidence level and p-value
5. Outputs clear recommendation with projected impact

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For insights (optional)
```

### Required Tools
- Python 3.10+
- scipy (for statistical calculations)

### Installation
```bash
pip install scipy numpy
```

## How to Run

### Step 1: Prepare Test Data
Create `test_data.json`:
```json
{
  "test_name": "Homepage CTA",
  "control": {"visitors": 5000, "conversions": 250},
  "variant": {"visitors": 5000, "conversions": 325}
}
```

### Step 2: Analyze Results
```bash
python3 execution/generate_ab_test_analysis.py \
  --control '{"visitors": 5000, "conversions": 250}' \
  --variant '{"visitors": 5000, "conversions": 325}' \
  --test_name "Homepage CTA" \
  --output .tmp/analysis.md
```

### Quick One-Liner
```bash
python3 execution/generate_ab_test_analysis.py --control '{"visitors": 1000, "conversions": 50}' --variant '{"visitors": 1000, "conversions": 65}' --test_name "Test Name"
```

## Goal
Analyze A/B test results and generate statistically valid recommendations.

## Inputs
- **Test Data**: Control vs Variant metrics
- **Sample Size**: Number of visitors/recipients
- **Primary Metric**: What you're optimizing for
- **Test Duration**: How long test ran

## Process

### 1. Input Test Data
```json
{
  "test_name": "Homepage CTA Button",
  "metric": "click_through_rate",
  "control": {
    "visitors": 5000,
    "conversions": 250
  },
  "variant": {
    "visitors": 5000,
    "conversions": 325
  },
  "confidence_target": 95
}
```

### 2. Analyze Results
```bash
python3 execution/analyze_ab_test.py \
  --data test_data.json \
  --output .tmp/analysis.md
```

### 3. Analysis Output
```markdown
# A/B Test Analysis: [Test Name]

## Results Summary
| Metric | Control | Variant | Difference |
|--------|---------|---------|------------|
| Sample Size | 5,000 | 5,000 | - |
| Conversions | 250 | 325 | +75 |
| Conv. Rate | 5.0% | 6.5% | +30% |

## Statistical Analysis
- **Lift:** +30%
- **Confidence Level:** 98.2%
- **P-Value:** 0.018
- **Statistical Significance:** ✅ Yes

## Recommendation
🟢 **IMPLEMENT VARIANT**

The variant shows a statistically significant improvement 
of +30% in click-through rate with 98.2% confidence.

## Projected Impact
- Additional conversions/month: ~150
- Estimated revenue impact: $X

## Caveats
- Test ran for X days (recommend minimum 2 weeks)
- Consider seasonal factors
- Monitor post-implementation
```

### 4. Statistical Methods
- Chi-square test (conversion rates)
- T-test (continuous metrics)
- Bayesian probability (optional)

### 5. Decision Framework
| Confidence | Lift | Decision |
|------------|------|----------|
| >95% | >10% | Implement |
| >95% | <10% | Consider |
| <95% | Any | Continue testing |
| Any | Negative | Stop test |

## Integrations
- Google Analytics
- Optimizely/VWO
- Custom data input

## Cost
- ~$0.02 per analysis

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Testing methodology
- Conversion optimization
- Data-driven decisions

**[SKILL_BIBLE_hormozi_10x_sales_process.md](../skills/SKILL_BIBLE_hormozi_10x_sales_process.md)**
- Funnel optimization
- Conversion improvement
- Revenue impact analysis
