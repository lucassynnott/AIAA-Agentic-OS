# Case Study Generator

## What This Workflow Is
This workflow generates professional case studies from client results data, complete with storytelling, before/after metrics, testimonials, and multiple output formats.

## What It Does
1. Takes client challenge, solution, and results as inputs
2. Structures into compelling narrative format
3. Highlights key metrics with before/after comparison
4. Generates multiple formats (web, PDF, slides, social)
5. Creates ready-to-publish assets

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For AI writing
GOOGLE_APPLICATION_CREDENTIALS=credentials.json  # For Google Docs/Slides
```

### Required Tools
- Python 3.10+
- OpenAI API access
- Google OAuth credentials (optional, for Docs/Slides export)

### Installation
```bash
pip install openai google-api-python-client
```

## How to Run

### Step 1: Prepare Input Data
Create `case_study_input.json`:
```json
{
  "client": "Acme SaaS",
  "industry": "B2B Software",
  "challenge": "Low reply rates on cold email, struggling to book meetings",
  "solution": "Implemented AI-personalized cold email sequences",
  "results": {
    "reply_rate": {"before": "2%", "after": "12%"},
    "meetings_booked": {"before": "5/month", "after": "35/month"}
  },
  "timeline": "90 days",
  "testimonial": "We 7x'd our meeting rate in 3 months."
}
```

### Step 2: Generate Case Study
```bash
python3 execution/generate_case_study.py \
  --data case_study_input.json \
  --format long \
  --output .tmp/case_study.md
```

### Step 3: Export to Different Formats
```bash
# PDF
python3 execution/export_case_study.py --input .tmp/case_study.md --format pdf

# Google Doc
python3 execution/export_case_study.py --input .tmp/case_study.md --format gdoc

# Social Media Version
python3 execution/generate_case_study.py --data case_study_input.json --format social
```

### Quick One-Liner
```bash
python3 execution/generate_case_study.py --data case_study_input.json --format long --output .tmp/case_study.md
```

## Goal
Generate compelling case studies from client results data with storytelling, metrics, and social proof.

## Inputs
- **Client Name**: Company name (or anonymized)
- **Industry**: Client's business category
- **Challenge**: Problem they faced
- **Solution**: What you implemented
- **Results**: Metrics and outcomes
- **Timeline**: Duration of engagement
- **Testimonial**: Client quote (optional)

## Process

### 1. Gather Case Study Data
```json
{
  "client": "Acme SaaS",
  "industry": "B2B Software",
  "company_size": "50-100 employees",
  "challenge": "Low reply rates on cold email campaigns, struggling to book meetings",
  "solution": "Implemented personalized cold email sequences with AI research",
  "results": {
    "reply_rate": {"before": "2%", "after": "12%"},
    "meetings_booked": {"before": "5/month", "after": "35/month"},
    "pipeline_generated": "$450,000 in 90 days"
  },
  "timeline": "90 days",
  "testimonial": "We 7x'd our meeting rate in 3 months. The personalization made all the difference.",
  "testimonial_author": "John Smith, VP Sales"
}
```

### 2. Generate Case Study
```bash
python3 execution/generate_case_study.py \
  --data case_study_input.json \
  --format long \
  --output .tmp/case_study.md
```

### 3. Case Study Structure

```markdown
# How [CLIENT] [ACHIEVED RESULT] in [TIMEFRAME]

## The Challenge

[CLIENT] is a [INDUSTRY] company that was struggling with [PROBLEM].

**Before working with us:**
- [Pain point 1 with metric]
- [Pain point 2 with metric]
- [Pain point 3 with metric]

[Quote from client about the problem]

## The Solution

We implemented [SOLUTION] to address their challenges:

### Phase 1: [Step Name]
[Description of what was done]

### Phase 2: [Step Name]
[Description of what was done]

### Phase 3: [Step Name]
[Description of what was done]

## The Results

After [TIMEFRAME], [CLIENT] achieved:

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| [Metric 1] | [X] | [Y] | [+Z%] |
| [Metric 2] | [X] | [Y] | [+Z%] |
| [Metric 3] | [X] | [Y] | [+Z%] |

### Key Wins
✅ [Result 1]
✅ [Result 2]
✅ [Result 3]

## Client Testimonial

> "[TESTIMONIAL]"
> 
> — [NAME], [TITLE] at [COMPANY]

## Key Takeaways

1. [Lesson 1]
2. [Lesson 2]
3. [Lesson 3]

---

**Want similar results?** [CTA]
```

### 4. Output Formats

**Long-Form (Website/PDF)**
Full 800-1500 word case study.

**Short-Form (Social)**
3-5 key points with metrics.

**One-Liner**
"We helped [CLIENT] achieve [RESULT] in [TIME]."

**Slide Deck**
5-7 slides for presentations.

### 5. Export Options
- Markdown (blog)
- PDF (downloadable)
- Google Doc (editable)
- Google Slides (presentation)

## Case Study Angles

### Results-Focused
Lead with the numbers and outcomes.

### Story-Driven
Narrative arc: challenge → journey → transformation.

### Process-Focused
Deep dive into methodology.

### Problem-Solution
Heavy on the pain point, quick to solution.

## Integrations Required
- OpenAI/Anthropic (writing)
- Google Docs API (export)
- PDF generation

## Cost Estimate
- ~$0.10-0.30 per case study

## Best Practices
- Always get client approval
- Use specific numbers, not vague claims
- Include timeline for credibility
- Add visuals (charts, screenshots)
- End with clear CTA
