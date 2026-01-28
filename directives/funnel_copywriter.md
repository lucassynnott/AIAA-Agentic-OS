# Funnel Copywriter

## What This Workflow Is
This workflow generates complete funnel copy (sales page, email sequences, ads) using AI market research and proven copywriting frameworks.

## What It Does
1. Receives business details via form
2. Conducts AI market research
3. Creates funnel strategy blueprint
4. Generates sales page copy
5. Creates email flow, outputs to Google Doc

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key
SERP_API_KEY=your_serp_key                # For competitor research
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- Google OAuth

### Installation
```bash
pip install openai google-api-python-client requests
```

## How to Run

### Via N8N Form (Recommended)
Submit form with:
- Business/Product Name
- Industry, Target Audience
- Funnel Type, Conversion Goal
- Brand Voice, Benefits, Pain Points
- Value Proposition, Offers

### Via Python Script
```bash
python3 execution/generate_funnel_copy.py \
  --business "Company Name" \
  --industry "SaaS" \
  --funnel_type "VSL" \
  --benefits "benefit1,benefit2,benefit3"
```

### Quick One-Liner
```bash
python3 execution/generate_funnel_copy.py --business "[NAME]" --funnel_type "VSL"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: Copy Request Form

## Inputs
- **Business/Product Name**: textarea (required)
- **Industry/Business Type**: text (required)
- **Target Audience (Be Specific)**: textarea (required)
- **Primary Funnel Type**: textarea (required)
- **Conversion Goal & Current Performance**: textarea (required)
- **Brand Voice & Personality**: textarea (required)
- **Top 3 Product Benefits**: textarea (required)
- **Top 3 Pain Points You Solve**: textarea (required)
- **Unique Value Proposition**: textarea (required)
- **Special Offers/Urgency Elements**: text
- **Existing Copy Sample (Optional)**: textarea
- **Success Metrics to Track**: text
- **Returning Client? **: dropdown

## Integrations Required
- Slack

## Process
### 1. Copy Request Form
Workflow is triggered via form.

### 2. Process Form Data
Data is normalized/transformed for the next step.

### 3. Compile Success Package
Data is normalized/transformed for the next step.

### 4. Final Success Response
Data is normalized/transformed for the next step.

### 5. OpenRouter Chat Model3
[Describe what this step does]

### 6. OpenRouter Chat Model
[Describe what this step does]

### 7. Market Research Agent
AI agent processes the input with the following instructions:
```
=You are an expert audience researcher and market analyst. Using the inputs below, create a copywriter-ready market research dossier and funnel strategy following the System Prompt. Where information is missing, proceed with clearly labeled assumptions; only ask ONE targeted question if a true blocker exists.

Business Profile (from form):
Business/Product Name: {{ $json['Business/Product Name'] }}
Industry/Business Type: {{ $json['Industry/Business Type'] }}
Target Audience (Be Specific): {{ $json['Target Audience (Be Specific)'] }}
Top 3 Product Benefits: {{ $json['Top 3 Product Benefits'] }}

Product Details (from form):
Unique Value Proposition: {{ $json['Unique Value Proposition'] }}
Top 3 Pain Points You Solve: {{ $json['Top 3 Pain Points You Solve'] }}
Existing Copy Sample (Optional): {{ $json['Existing Copy Sample (Optional)'] }}

DELIVERABLES
Produce the following, in order, using the formatting and JSON schema from the System Prompt:

1) Executive Summary (5–7 “Key Moves,” plus top risks & unknowns)
2) Business Snapshot (facts vs. assumptions)
3) Audience Personas (2–4) with JTBD, pains/gains, triggers, decision criteria, objections, and 10+ VOC phrases total
4) Demand & Intent Landscape (awareness spectrum, intent clusters, buying events)
... [truncated]
```

### 8. HTTP Request
[Describe what this step does]

### 9. Move file
[Describe what this step does]

### 10. Send a message
[Describe what this step does]

### 11. If
[Describe what this step does]

### 12. Search files and folders
[Describe what this step does]

### 13. Move file1
[Describe what this step does]

### 14. Create folder
[Describe what this step does]

### 15. SerpAPI
[Describe what this step does]

### 16. Funnel Strategist Agent
AI agent processes the input with the following instructions:
```
=Create a comprehensive funnel strategy and architecture blueprint for this business using proven million-dollar methodologies:

BUSINESS INTELLIGENCE:
Business Name: {{ $('Process Form Data').first().json['Business/Product Name'] }}
Industry: {{ $('Process Form Data').first().json['Industry/Business Type'] }}
Target Audience: {{ $('Process Form Data').first().json['Target Audience (Be Specific)'] }}
Primary Funnel Type: {{ $('Process Form Data').first().json['Primary Funnel Type'] }}
Conversion Goal & Current Performance: {{ $('Process Form Data').first().json['Conversion Goal & Current Performance'] }}
Brand Voice & Personality: {{ $('Process Form Data').first().json['Brand Voice & Personality'] }}
Top 3 Product Benefits: {{ $('Process Form Data').first().json['Top 3 Product Benefits'] }}
Top 3 Pain Points Solved: {{ $('Process Form Data').first().json['Top 3 Pain Points You Solve'] }}
Unique Value Proposition: {{ $('Process Form Data').first().json['Unique Value Proposition'] }}
Special Offers/Urgency Elements: {{ $('Process Form Data').first().json['Special Offers/Urgency Elements'] }}
Success Metrics to Track: {{ $('Process Form Data').first().json['Success Metrics to Track'] }}
Market Research Data: {{ $json.output }}

DELIVER A COMPREHENSIVE FUNNEL STRATEGY INCLUDING:

## 1. STRATEGIC FOUNDATION
- Power of One Analysis (One problem, one desire, one method, one promise)
... [truncated]
```

### 17. OpenRouter Chat Model1
[Describe what this step does]

### 18. OpenRouter Chat Model2
[Describe what this step does]

### 19. Sales Page Agent
AI agent processes the input with the following instructions:
```
=Create a high-converting sales page that seamlessly integrates with the overall funnel strategy for this business:

BUSINESS INTELLIGENCE:
Business Name: {{ $('Process Form Data').first().json['Business/Product Name'] }}
Industry: {{ $('Process Form Data').first().json['Industry/Business Type'] }}
Target Audience: {{ $('Process Form Data').first().json['Target Audience (Be Specific)'] }}
Primary Funnel Type: {{ $('Process Form Data').first().json['Primary Funnel Type'] }}
Conversion Goal & Current Performance: {{ $('Process Form Data').first().json['Conversion Goal & Current Performance'] }}
Brand Voice & Personality: {{ $('Process Form Data').first().json['Brand Voice & Personality'] }}
Top 3 Product Benefits: {{ $('Process Form Data').first().json['Top 3 Product Benefits'] }}
Top 3 Pain Points Solved: {{ $('Process Form Data').first().json['Top 3 Pain Points You Solve'] }}
Unique Value Proposition: {{ $('Process Form Data').first().json['Unique Value Proposition'] }}
Special Offers/Urgency Elements: {{ $('Process Form Data').first().json['Special Offers/Urgency Elements'] }}
Success Metrics to Track: {{ $('Process Form Data').first().json['Success Metrics to Track'] }}
Market Research Data: {{ $json.output }}

FUNNEL STRATEGY CONTEXT:
{{ $json.output }}

DELIVER A COMPLETE HIGH-CONVERTING SALES PAGE INCLUDING:
... [truncated]
```

### 20. Email Flow Agent
AI agent processes the input with the following instructions:
```
=Create a comprehensive value-dense email sequence that seamlessly integrates with the overall funnel strategy for this business:

BUSINESS INTELLIGENCE:
Business Name: {{ $('Process Form Data').first().json['Business/Product Name'] }}
Industry: {{ $('Process Form Data').first().json['Industry/Business Type'] }}
Target Audience: {{ $('Process Form Data').first().json['Target Audience (Be Specific)'] }}
Primary Funnel Type: {{ $('Process Form Data').first().json['Primary Funnel Type'] }}
Conversion Goal & Current Performance: {{ $('Process Form Data').first().json['Conversion Goal & Current Performance'] }}
Brand Voice & Personality: {{ $('Process Form Data').first().json['Brand Voice & Personality'] }}
Top 3 Product Benefits: {{ $('Process Form Data').first().json['Top 3 Product Benefits'] }}
Top 3 Pain Points Solved: {{ $('Process Form Data').first().json['Top 3 Pain Points You Solve'] }}
Unique Value Proposition: {{ $('Process Form Data').first().json['Unique Value Proposition'] }}
Special Offers/Urgency Elements: {{ $('Process Form Data').first().json['Special Offers/Urgency Elements'] }}
Success Metrics to Track: {{ $('Process Form Data').first().json['Success Metrics to Track'] }}
Market Research Data: {{ $json.output }}

FUNNEL STRATEGY CONTEXT:
{{ $('Funnel Strategist Agent').item.json.output }}

SALES PAGE CONTEXT:
... [truncated]
```

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Related Skill Bibles

Load these skill bibles for high-converting funnel copy:

**[SKILL_BIBLE_landing_page_ai_mastery.md](../skills/SKILL_BIBLE_landing_page_ai_mastery.md)** (PRIMARY)
- Complete landing page optimization framework
- AI-powered content creation and design automation
- Conversion-first design philosophy
- A/B testing and optimization methodologies

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- 14 years of marketing advice condensed
- Funnel strategy and optimization
- Conversion psychology principles

**[SKILL_BIBLE_hormozi_email_marketing_complete.md](../skills/SKILL_BIBLE_hormozi_email_marketing_complete.md)**
- Complete email marketing framework
- Email sequence optimization
- Revenue-driving email tactics

**[SKILL_BIBLE_hormozi_sales_training.md](../skills/SKILL_BIBLE_hormozi_sales_training.md)**
- Sales copy psychology
- Objection handling in copy
- Urgency and scarcity frameworks

**[SKILL_BIBLE_funnel_copywriting_mastery.md](../skills/SKILL_BIBLE_funnel_copywriting_mastery.md)**
- Funnel copy best practices
- Sales page structure
- Conversion optimization

**[SKILL_BIBLE_hormozi_10x_pricing.md](../skills/SKILL_BIBLE_hormozi_10x_pricing.md)**
- Pricing psychology for offers
- Value stack creation
- Premium positioning

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/Funnel Copywriter.json`
Generated on: 2026-01-02