# Press Release Generator

## What This Workflow Is
This workflow generates professional press releases for product launches, funding, partnerships, awards, and executive hires.

## What It Does
1. Takes announcement type and details
2. Structures using AP style format
3. Generates headline and body
4. Incorporates provided quotes
5. Adds company boilerplate

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install openai
```

## How to Run

### Step 1: Generate Press Release
```bash
python3 execution/generate_press_release.py \
  --type product_launch \
  --details details.json \
  --output .tmp/press_release.md
```

### Quick One-Liner
```bash
python3 execution/generate_press_release.py --type "[TYPE]" --details "[JSON]"
```

## Goal
Generate professional press releases for company announcements.

## Inputs
- **Announcement Type**: Product launch, funding, partnership, award, hire
- **Key Details**: Who, what, when, where, why
- **Quotes**: From executives/stakeholders
- **Company Boilerplate**: About section

## Process

### 1. Generate Press Release
```bash
python3 execution/generate_press_release.py \
  --type product_launch \
  --details details.json \
  --output .tmp/press_release.md
```

### 2. Press Release Structure
```markdown
FOR IMMEDIATE RELEASE

# [HEADLINE: Action-Oriented, Newsworthy]

**[SUBHEADLINE: Key Benefit or Detail]**

[CITY, STATE] — [DATE] — [COMPANY] today announced 
[NEWS]. [Expand on significance in 2-3 sentences].

[PARAGRAPH 2: Details and context]
[Explain the what, why, and how. Include specifics 
like features, benefits, availability.]

[PARAGRAPH 3: Quote from executive]
"[Quote that adds perspective and vision]," said 
[NAME], [TITLE] at [COMPANY]. "[Additional context]."

[PARAGRAPH 4: Additional details]
[Supporting information, partnerships, pricing, 
availability dates.]

[PARAGRAPH 5: Optional second quote]
[From partner, customer, or industry expert]

[PARAGRAPH 6: Call to action]
[How to learn more, where to sign up, etc.]

## About [COMPANY]
[Boilerplate: 2-3 sentences about company, mission, 
and key facts]

## Media Contact
[Name]
[Email]
[Phone]

###
```

### 3. Headline Formulas
- [Company] Launches [Product] to [Benefit]
- [Company] Raises $[X] to [Mission]
- [Company] Partners with [Partner] to [Outcome]
- [Company] Named [Award] by [Organization]

### 4. Output Formats
- Plain text (for distribution)
- HTML (for website)
- PDF (for press kit)
- Social media snippets

## Integrations
- OpenAI (writing)
- PR distribution (optional)

## Cost
- ~$0.10-0.20 per release
