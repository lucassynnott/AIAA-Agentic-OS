# Email Flow Writer

## What This Workflow Is
This workflow generates complete e-commerce email flows (Welcome, Cart Abandon, Checkout Abandon, Browse Abandon, Post-Purchase, Site Abandon, Win-Back) using proven $40M methodology.

## What It Does
1. Receives brand info via form
2. Researches brand with Perplexity
3. Generates 7 complete email flows
4. Creates Google Doc for each flow
5. Organizes in client folder, notifies Slack

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

### Via Python Script
```bash
python3 execution/generate_email_flows.py \
  --brand "Brand Name" \
  --website "https://brand.com" \
  --niche "skincare"
```

### Quick One-Liner
```bash
python3 execution/generate_email_flows.py --brand "[BRAND]" --website "[URL]"
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

## Integrations Required
- Slack

## Process
### 1. On form submission
Workflow is triggered via form.

### 2. Brand Research Agent
AI agent processes the input with the following instructions:
```
=Conduct comprehensive brand research for {{ $json.brandName }} to enable the creation of a high-converting Welcome Flow. I need complete intelligence on this e-commerce brand to craft emails that convert at 10%+ rates.

BRAND TO RESEARCH: {{ $json.brandName }}
WEBSITE: {{ $json.brandWebsite }}
INDUSTRY/NICHE: {{ $json.niche }}
EXTRA INFO: {{ $json.notes }}

REQUIRED RESEARCH AREAS:

1. BRAND FOUNDATION INTELLIGENCE
   - Complete company background, founding story, and mission
   - Core values, brand personality, and positioning
   - Unique selling propositions and key differentiators
   - Brand voice, tone, and communication style examples
   - Visual identity and design aesthetic preferences

2. PRODUCT PORTFOLIO ANALYSIS
   - Complete product catalog and main categories
   - Best-selling products and customer favorites
   - Price ranges and average order values
... [truncated]
```

### 3. Message a model in Perplexity
[Describe what this step does]

### 4. OpenRouter Chat Model
[Describe what this step does]

### 5. Set Brand Details
Data is normalized/transformed for the next step.

### 6. Set Research Details
Data is normalized/transformed for the next step.

### 7. Welcome Flow Agent
AI agent processes the input with the following instructions:
```
=Create a master-level 8-email Welcome Flow for {{ $('Set Brand Details').item.json.brandName }} using advanced copywriting principles that maximize conversions and engagement.

BRAND INTELLIGENCE:
- Brand Name: {{ $('Set Brand Details').item.json.brandName }}
- Brand Website: {{ $('Set Brand Details').item.json.brandWebsite }}
- Niche: {{ $('Set Brand Details').item.json.niche }}
- Notes: {{ $('Set Brand Details').item.json.notes }}
- Brand Research: {{ $json.brandResearch }}

COPYWRITING SPECIFICATIONS:
- Apply SCE framework (Skimmable, Clear & Concise, Engaging)
- Maximum 3-5 second reading time per email
- One microtopic focus per email
- Punchy, dopamine-triggering copy
- Educational positioning without being salesy
- Include infographic opportunities where relevant

TECHNICAL REQUIREMENTS:
- Detailed layout markers for complete design control
- Multiple subject line options (2-5 words, curiosity-driven)
... [truncated]
```

### 8. OpenRouter Chat Model1
[Describe what this step does]

### 9. Welcome Flow Google Doc Creator
[Describe what this step does]

### 10. OpenRouter Chat Model2
[Describe what this step does]

### 11. Cart Abandon Flow Agent
AI agent processes the input with the following instructions:
```
=Create a master-level Cart Abandonment Flow using the provided brand intelligence and advanced copywriting principles that maximize cart recovery rates.

BRAND INTELLIGENCE:
- Brand Name: {{ $('Set Brand Details').item.json.brandName }}
- Brand Website: {{ $('Set Brand Details').item.json.brandWebsite }}
- Niche: {{ $('Set Brand Details').item.json.niche }}
- Notes: {{ $('Set Brand Details').item.json.notes }}
- Brand Research: {{ $json.brandResearch }}

CART ABANDON FLOW SPECIFICATIONS:
Create a complete 6-8 email Cart Abandonment sequence that:
- Recovers 25-50% more abandoned cart sales
- Uses Max Sturtavant's proven $40M+ methodology
- Applies advanced copywriting psychology
- Focuses specifically on cart abandoners (not checkout abandoners)

COPYWRITING REQUIREMENTS:
- Apply SCE framework (Skimmable, Clear & Concise, Engaging)
- Maximum 3-5 second reading time per email
- Under 75 words of body copy per email
... [truncated]
```

### 12. Cart Abandon Google Doc Creator
[Describe what this step does]

### 13. OpenRouter Chat Model3
[Describe what this step does]

### 14. Checkout Abandon Flow Agent
AI agent processes the input with the following instructions:
```
=Create a master-level Checkout Abandonment Flow using the provided brand intelligence and advanced copywriting principles that maximize checkout completion rates for the highest-intent customers.

BRAND INTELLIGENCE:
- Brand Name: {{ $('Set Brand Details').item.json.brandName }}
- Brand Website: {{ $('Set Brand Details').item.json.brandWebsite }}
- Niche: {{ $('Set Brand Details').item.json.niche }}
- Notes: {{ $('Set Brand Details').item.json.notes }}
- Brand Research: {{ $json.brandResearch }}

CHECKOUT ABANDON FLOW SPECIFICATIONS:
Create a complete 6-8 email Checkout Abandonment sequence that:
- Recovers 40-60% of checkout abandoners (highest conversion flow)
- Uses Max Sturtavant's proven $40M+ methodology
- Applies advanced copywriting psychology for high-intent customers
- Focuses specifically on checkout abandoners (furthest down funnel)

COPYWRITING REQUIREMENTS:
- Apply SCE framework (Skimmable, Clear & Concise, Engaging)
- Maximum 3-5 second reading time per email
- Under 60 words of body copy per email (shortest of all flows)
... [truncated]
```

### 15. OpenRouter Chat Model4
[Describe what this step does]

### 16. Browse Abandon Flow Agent
AI agent processes the input with the following instructions:
```
=Create a master-level Browse Abandonment Flow using the provided brand intelligence and advanced copywriting principles that maximize conversion of product browsers into purchasers.

BRAND INTELLIGENCE:
- Brand Name: {{ $('Set Brand Details').item.json.brandName }}
- Brand Website: {{ $('Set Brand Details').item.json.brandWebsite }}
- Niche: {{ $('Set Brand Details').item.json.niche }}
- Notes: {{ $('Set Brand Details').item.json.notes }}
- Brand Research: {{ $json.brandResearch }}

BROWSE ABANDON FLOW SPECIFICATIONS:
Create a complete 3-5 email Browse Abandonment sequence that:
- Converts 15-25% of browse abandoners into purchasers
- Uses Max Sturtavant's proven $40M+ methodology
- Applies advanced copywriting psychology for mid-funnel customers
- Focuses specifically on browse abandoners (viewed products, didn't add to cart)

COPYWRITING REQUIREMENTS:
- Apply SCE framework (Skimmable, Clear & Concise, Engaging)
- Maximum 3-5 second reading time per email
- Under 80 words of body copy per email
... [truncated]
```

### 17. Checkout Abandon Google Doc Creator
[Describe what this step does]

### 18. Browse Abandon Google Doc Creator
[Describe what this step does]

### 19. OpenRouter Chat Model5
[Describe what this step does]

### 20. Post Purchase Flow Agent
AI agent processes the input with the following instructions:
```
=Create a master-level Post-Purchase Flow using the provided brand intelligence and advanced copywriting principles that maximizes customer lifetime value and creates exceptional post-purchase experiences.

BRAND INTELLIGENCE:
- Brand Name: {{ $('Set Brand Details').item.json.brandName }}
- Brand Website: {{ $('Set Brand Details').item.json.brandWebsite }}
- Niche: {{ $('Set Brand Details').item.json.niche }}
- Notes: {{ $('Set Brand Details').item.json.notes }}
- Brand Research: {{ $json.brandResearch }}

POST-PURCHASE FLOW SPECIFICATIONS:
Create a complete 3-4 email Post-Purchase sequence that:
- Maximizes the 27% higher purchase propensity window
- Uses Max Sturtavant's proven $40M+ methodology
- Applies advanced copywriting psychology for post-purchase customers
- Focuses on customer experience, loyalty, and lifetime value

COPYWRITING REQUIREMENTS:
- Apply SCE framework (Skimmable, Clear & Concise, Engaging)
- Maximum 3-5 second reading time per email
- Under 100 words of body copy per email (welcome flow length)
... [truncated]
```

### 21. Post Purchase Google Doc Creator
[Describe what this step does]

### 22. OpenRouter Chat Model6
[Describe what this step does]

### 23. Site Abandon Flow Agent
AI agent processes the input with the following instructions:
```
=Create a master-level Site Abandonment Flow using the provided brand intelligence and advanced copywriting principles that converts site visitors into product browsers.

BRAND INTELLIGENCE:
- Brand Name: {{ $('Set Brand Details').item.json.brandName }}
- Brand Website: {{ $('Set Brand Details').item.json.brandWebsite }}
- Niche: {{ $('Set Brand Details').item.json.niche }}
- Notes: {{ $('Set Brand Details').item.json.notes }}
- Brand Research: {{ $json.brandResearch }}

SITE ABANDON FLOW SPECIFICATIONS:
Create a single high-impact Site Abandonment email that:
- Converts 2%+ of site abandoners into product browsers
- Uses Max Sturtavant's proven $40M+ methodology
- Applies advanced copywriting psychology for earliest-stage visitors
- Focuses specifically on site abandoners (visited site, didn't view products)

COPYWRITING REQUIREMENTS:
- Apply SCE framework (Skimmable, Clear & Concise, Engaging)
- Maximum 3-5 second reading time
- Under 50 words of body copy (shortest of all flows)
... [truncated]
```

### 24. Site Abandon Google Doc Creator
[Describe what this step does]

### 25. OpenRouter Chat Model7
[Describe what this step does]

### 26. Win-Back Flow Agent
AI agent processes the input with the following instructions:
```
=Create a master-level Win-Back Flow using the provided brand intelligence and advanced copywriting principles that re-engages dormant customers and rebuilds purchasing relationships.

BRAND INTELLIGENCE:
- Brand Name: {{ $('Set Brand Details').item.json.brandName }}
- Brand Website: {{ $('Set Brand Details').item.json.brandWebsite }}
- Niche: {{ $('Set Brand Details').item.json.niche }}
- Notes: {{ $('Set Brand Details').item.json.notes }}
- Brand Research: {{ $json.brandResearch }}

WIN-BACK FLOW SPECIFICATIONS:
Create a complete 3-email Win-Back sequence that:
- Re-engages 5-15% of dormant customers into repeat purchasers
- Uses Max Sturtavant's proven $40M+ methodology
- Applies advanced copywriting psychology for past customers
- Focuses specifically on customers who haven't purchased in 60-120+ days

COPYWRITING REQUIREMENTS:
- Apply SCE framework (Skimmable, Clear & Concise, Engaging)
- Maximum 3-5 second reading time per email
- Under 75 words of body copy per email
... [truncated]
```

### 27. Win-Back Google Doc Creator
[Describe what this step does]

### 28. Set Google Drive Links
Data is normalized/transformed for the next step.

### 29. If
[Describe what this step does]

### 30. Create folder
[Describe what this step does]

### 31. Move file
[Describe what this step does]

### 32. Move file1
[Describe what this step does]

### 33. Search files and folders
[Describe what this step does]

### 34. Code
[Describe what this step does]

### 35. Code1
[Describe what this step does]

### 36. Aggregate
[Describe what this step does]

### 37. Code2
[Describe what this step does]

### 38. Aggregate1
[Describe what this step does]

### 39. Send a message
[Describe what this step does]

### 40. Aggregate2
[Describe what this step does]

### 41. Send a message1
[Describe what this step does]

### 42. Merge
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Ecom Email Marketing Agency/Email Flow Writer.json`
Generated on: 2026-01-02