# Ecom Email Campaign Generator Agent

## What This Workflow Is
This workflow generates 5 high-converting email campaigns for e-commerce brands using AI research and proven $40M email marketing methodology.

## What It Does
1. Receives brand info via form
2. Researches brand with Perplexity
3. Generates 5 campaign ideas
4. Writes full email copy for each
5. Creates Google Doc and notifies Slack

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key
PERPLEXITY_API_KEY=your_perplexity_key
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
- Brand Name, Website, Industry/Niche
- Existing Client (yes/no)
- Personalization Notes
- Campaign Types (checkbox)

### Via Python Script
```bash
python3 execution/generate_ecom_campaigns.py \
  --brand "Brand Name" \
  --website "https://brand.com" \
  --niche "skincare" \
  --campaigns "welcome,abandoned_cart,win_back"
```

### Quick One-Liner
```bash
python3 execution/generate_ecom_campaigns.py --brand "[BRAND]" --website "[URL]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Brand Name**: text (required)
- **Brand Website**: text (required)
- **Industry / Niche**: text (required)
- **Existing Client?**: dropdown (required)
- **Personalization Notes**: textarea
- **Campaign Type**: checkbox

## Integrations Required
- Slack
- OpenAI

## Process
### 1. On form submission
Workflow is triggered via form.

### 2. Brand Research Agent
AI agent processes the input with the following instructions:
```
=You are researching {{ $json.brandName }} to create 5 high-converting email campaigns: {{ $json.campaignTypes }}
BRAND: {{ $json.brandName }}
WEBSITE: {{ $json.brandWebsite }}
INDUSTRY: {{ $json.niche }}
NOTES: {{ $json.notes }}
CAMPAIGNS TO CREATE: {{ $json.campaignTypes }}
RESEARCH STRATEGY (Maximum 3 searches):
1. BRAND & PRODUCT ESSENTIALS (Single perplexity call)
   Search: "{{ $json.brandName }} brand voice customer reviews best selling products unique value proposition"
   Extract: brand personality, top products, customer language, key benefits, price positioning
2. CUSTOMER & COMPETITIVE INTEL (Single perplexity call)
   Search: "{{ $json.brandName }} target audience pain points {{ $json.niche }} competitors differentiation"
   Extract: customer demographics, main problems solved, competitor landscape, unique angles
3. SOCIAL PROOF & MARKETING (Single perplexity call - only if needed for campaigns)
   Search: "{{ $json.brandName }} testimonials media coverage email marketing social media"
   Extract: credibility markers, existing messaging patterns, engagement themes
CAMPAIGN-SPECIFIC FOCUS:
For each campaign type requested, identify:
- Primary goal and conversion trigger
- Ideal customer segment to target
... [truncated]
```

### 3. OpenRouter Chat Model
[Describe what this step does]

### 4. Set Brand Details
Data is normalized/transformed for the next step.

### 5. Set Research Details
Data is normalized/transformed for the next step.

### 6. Campaign Idea Agent
AI agent processes the input with the following instructions:
```
=Create 5 high-converting email campaign ideas using Max's proven $40M methodology. Use Perplexity to research current trends, opportunities, and insights that will make these campaigns uniquely powerful and timely.

BRAND INTELLIGENCE:

Brand Name: {{ $('Set Brand Details').first().json.brandName }}
Brand Website: {{ $('Set Brand Details').first().json.brandWebsite }}
Niche: {{ $('Set Brand Details').first().json.niche }}
Notes: {{ $('Set Brand Details').first().json.notes }}
Campaign Types: {{ $('Set Brand Details').item.json.campaignTypes }}
Brand Research: {{ $json.brandResearch }}

RESEARCH REQUIREMENTS: Before creating campaigns, use Perplexity to research:

Industry Trends (2024-2025): Latest developments, studies, controversies in the brand's niche
Competitor Content Gaps: What are competitors NOT talking about that this brand could own?
Customer Pain Points: Recent discussions on Reddit, forums, reviews about problems in this niche
Scientific/Research Backing: Recent studies that could support the brand's positioning
Seasonal Opportunities: Current trending topics, upcoming holidays, cultural moments relevant to the niche
Emerging Concerns: New customer interests, concerns, or questions in the industry

... [truncated]
```

### 7. OpenRouter Chat Model1
[Describe what this step does]

### 8. Message a model in Perplexity1
[Describe what this step does]

### 9. OpenRouter Chat Model2
[Describe what this step does]

### 10. Message a model in Perplexity2
[Describe what this step does]

### 11. OpenRouter Chat Model3
[Describe what this step does]

### 12. Message a model in Perplexity3
[Describe what this step does]

### 13. OpenRouter Chat Model4
[Describe what this step does]

### 14. Message a model in Perplexity4
[Describe what this step does]

### 15. OpenRouter Chat Model5
[Describe what this step does]

### 16. OpenRouter Chat Model6
[Describe what this step does]

### 17. Message a model in Perplexity6
[Describe what this step does]

### 18. Campaign 3 Writer
AI agent processes the input with the following instructions:
```
=Write a complete, high-converting email campaign using the following structured campaign idea:

CAMPAIGN IDEA: {{ $json.output.campaigns[2] }}

Research Foundation: {{ $json.output.researchSummary }} 


Instructions:

Use all research, positioning, and engagement strategies from the campaign idea JSON.
Rigorously follow Max’s “one email, one topic, one takeaway” rule.
Make the email skimmable, punchy, and educational.
Subtly position the brand/product as the superior choice.
Match the brand’s tone, personality, and audience as described.
If this is a Black Friday/Q4 campaign, emphasize urgency, exclusivity, and value, and ensure the offer and CTA are immediately clear.
Required Output Structure:

Subject Line:
Compelling, curiosity-driven, or benefit-focused
Must pass the “would I open this?” test
... [truncated]
```

### 19. Campaign 1 Writer
AI agent processes the input with the following instructions:
```
=Write a complete, high-converting email campaign using the following structured campaign idea:

CAMPAIGN IDEA: {{ $json.output.campaigns[0] }}

Research Foundation: {{ $json.output.researchSummary }} 


Instructions:

Use all research, positioning, and engagement strategies from the campaign idea JSON.
Rigorously follow Max’s “one email, one topic, one takeaway” rule.
Make the email skimmable, punchy, and educational.
Subtly position the brand/product as the superior choice.
Match the brand’s tone, personality, and audience as described.
If this is a Black Friday/Q4 campaign, emphasize urgency, exclusivity, and value, and ensure the offer and CTA are immediately clear.
Required Output Structure:

Subject Line:
Compelling, curiosity-driven, or benefit-focused
Must pass the “would I open this?” test
... [truncated]
```

### 20. Campaign 2 Writer
AI agent processes the input with the following instructions:
```
=Write a complete, high-converting email campaign using the following structured campaign idea:

CAMPAIGN IDEA: {{ $json.output.campaigns[1] }}

Research Foundation: {{ $json.output.researchSummary }} 


Instructions:

Use all research, positioning, and engagement strategies from the campaign idea JSON.
Rigorously follow Max’s “one email, one topic, one takeaway” rule.
Make the email skimmable, punchy, and educational.
Subtly position the brand/product as the superior choice.
Match the brand’s tone, personality, and audience as described.
If this is a Black Friday/Q4 campaign, emphasize urgency, exclusivity, and value, and ensure the offer and CTA are immediately clear.
Required Output Structure:

Subject Line:
Compelling, curiosity-driven, or benefit-focused
Must pass the “would I open this?” test
... [truncated]
```

### 21. Campaign 4 Writer
AI agent processes the input with the following instructions:
```
=Write a complete, high-converting email campaign using the following structured campaign idea:

CAMPAIGN IDEA: {{ $json.output.campaigns[3] }}

Research Foundation: {{ $json.output.researchSummary }} 


Instructions:

Use all research, positioning, and engagement strategies from the campaign idea JSON.
Rigorously follow Max’s “one email, one topic, one takeaway” rule.
Make the email skimmable, punchy, and educational.
Subtly position the brand/product as the superior choice.
Match the brand’s tone, personality, and audience as described.
If this is a Black Friday/Q4 campaign, emphasize urgency, exclusivity, and value, and ensure the offer and CTA are immediately clear.
Required Output Structure:

Subject Line:
Compelling, curiosity-driven, or benefit-focused
Must pass the “would I open this?” test
... [truncated]
```

### 22. Campaign 5 Writer
AI agent processes the input with the following instructions:
```
=Write a complete, high-converting email campaign using the following structured campaign idea:

CAMPAIGN IDEA: {{ $json.output.campaigns[4] }}

Research Foundation: {{ $json.output.researchSummary }} 


Instructions:

Use all research, positioning, and engagement strategies from the campaign idea JSON.
Rigorously follow Max’s “one email, one topic, one takeaway” rule.
Make the email skimmable, punchy, and educational.
Subtly position the brand/product as the superior choice.
Match the brand’s tone, personality, and audience as described.
If this is a Black Friday/Q4 campaign, emphasize urgency, exclusivity, and value, and ensure the offer and CTA are immediately clear.
Required Output Structure:

Subject Line:
Compelling, curiosity-driven, or benefit-focused
Must pass the “would I open this?” test
... [truncated]
```

### 23. Perplexity Tool 1
[Describe what this step does]

### 24. Edit Fields
Data is normalized/transformed for the next step.

### 25. Aggregate
[Describe what this step does]

### 26. Campaign Google Doc Creator
[Describe what this step does]

### 27. Check If Returning Client
[Describe what this step does]

### 28. Search for Existing Folder
[Describe what this step does]

### 29. Create New Client Folder
[Describe what this step does]

### 30. Move to Existing Folder
[Describe what this step does]

### 31. Move to New Folder
[Describe what this step does]

### 32. Prepare Notification Data
Data is normalized/transformed for the next step.

### 33. Slack Notification
[Describe what this step does]

### 34. Prepare Document Data
Data is normalized/transformed for the next step.

### 35. Auto-fixing Output Parser
[Describe what this step does]

### 36. Message a model in Perplexity
[Describe what this step does]

### 37. Merge
[Describe what this step does]

## Output Schema
### Structured Output Parser
```json
{}
```

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Related Skill Bibles

### PRIMARY: Max Sturtevant's $40M+ Ecommerce Email Methodology

**[SKILL_BIBLE_sturtevant_email_master_system.md](../skills/SKILL_BIBLE_sturtevant_email_master_system.md)** ⭐ ESSENTIAL
- Complete ecommerce email system (6,968 words)
- Campaign architecture and revenue optimization
- SCE Framework (Skimmable, Clear, Engaging)

**[SKILL_BIBLE_sturtevant_copywriting.md](../skills/SKILL_BIBLE_sturtevant_copywriting.md)** ⭐ FOR CAMPAIGNS
- Email copywriting formulas (5,395 words)
- Subject line swipe files (25+ examples)
- CTA optimization patterns

**[SKILL_BIBLE_sturtevant_black_friday.md](../skills/SKILL_BIBLE_sturtevant_black_friday.md)** ⭐ FOR PROMOS
- BFCM & Q4 campaign strategies (7,101 words)
- Sale campaign sequencing
- Urgency and scarcity tactics

**[SKILL_BIBLE_sturtevant_email_design.md](../skills/SKILL_BIBLE_sturtevant_email_design.md)**
- High-converting email design (6,686 words)
- Mobile-first layouts
- Visual hierarchy for campaigns

**[SKILL_BIBLE_sturtevant_revenue_systems.md](../skills/SKILL_BIBLE_sturtevant_revenue_systems.md)**
- Revenue optimization tactics (5,812 words)
- Campaign ROI maximization

### SUPPLEMENTARY: Hormozi Sales Psychology

**[SKILL_BIBLE_hormozi_email_marketing_complete.md](../skills/SKILL_BIBLE_hormozi_email_marketing_complete.md)**
- Sales psychology for email campaigns
- Urgency and scarcity frameworks

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Promotional strategies
- Conversion optimization

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Ecom Email Marketing Agency/Ecom Email Campaign Generator Agent.json`
Generated on: 2026-01-02