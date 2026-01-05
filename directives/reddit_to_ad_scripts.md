# Reddit to Ad Scripts

## What This Workflow Is
This workflow scrapes Reddit threads for customer pain points and language, then generates ad scripts using real voice-of-customer insights.

## What It Does
1. Scrapes relevant Reddit threads
2. Extracts pain points and language
3. Analyzes sentiment and themes
4. Generates ad scripts using VOC
5. Outputs ready-to-use copy

## Prerequisites

### Required API Keys (add to .env)
```
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret
OPENAI_API_KEY=your_openai_key
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install praw openai
```

## How to Run

### Via N8N Form
Submit form with subreddits and keywords to scrape.

### Quick One-Liner
```bash
python3 execution/reddit_to_ads.py --subreddits "[SUBREDDITS]" --keywords "[KEYWORDS]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Research Topic/Product Name**: text
- **Business/Product Description**: text
- **Target Audience**: text
- **Content Source Type**: dropdown
- **Drop the URL here**: text
- **Returning Customer?**: dropdown (required)
- **Client Name**: text
- **Returning Client?**: dropdown

## Integrations Required
- Slack

## Process
### 1. 🔗 Enter Forum URL
Data is normalized/transformed for the next step.

### 2. OpenRouter Chat Model
[Describe what this step does]

### 3. SerpAPI
[Describe what this step does]

### 4. Analysis Content  By AI1
AI agent processes the input with the following instructions:
```
=MISSION: Evaluate the business opportunity potential of this extracted Reddit content.

INPUT DATA:
{{ JSON.stringify($json, null, 2) }}

MULTI-STAGE ANALYSIS PROTOCOL:

STAGE 1: PROBLEM VALIDATION
Assess the following indicators:
1. FREQUENCY SIGNALS
   - How often is this problem mentioned? (raw count)
   - Is it a recurring theme or isolated incident?
   - Temporal patterns (getting worse/better over time?)

2. SEVERITY MARKERS
   - Emotional intensity (frustration level 1-10)
   - Impact on daily life/business operations
   - Failed solution attempts mentioned
   - Time/money already wasted on problem

... [truncated]
```

### 5. Ad scripting agent that writes 3 ad scripts
AI agent processes the input with the following instructions:
```
=Create 3 high-converting ad scripts using the Villain-Hero framework that's generated $300M+ in proven ad spend results. Transform the business problem into a compelling narrative that stops scrolls and drives conversions.

**BUSINESS CONTEXT:**
Problem Summary: [Auto-extracted]
Key Pain Points: [Auto-extracted]
Target Demographics: [Auto-extracted]
Product/Service: [Auto-extracted]
Context: {{ JSON.stringify($json) }}

**PROVEN FRAMEWORK REQUIREMENTS:**

1. **VILLAIN-HERO NARRATIVE (Primary Framework)**
   - Hook: Pattern interrupt that captures RIGHT attention (3 seconds)
   - Villain Setup: Position competitor/old way as the enemy (10-15 seconds)
   - Twist the Knife: Amplify pain points and consequences (10-15 seconds)
   - Hero Reveal: Present solution as the savior (5-10 seconds)
   - Payoff: Show transformation and benefits (5-10 seconds)
   - CTA: Direct action with urgency (3-5 seconds)

2. **PROBLEM-AGITATE-SOLUTION (PAS)**
... [truncated]
```

### 6. Search files and folders
[Describe what this step does]

### 7. Create folder
[Describe what this step does]

### 8. Wait
[Describe what this step does]

### 9. Set Success Response
Data is normalized/transformed for the next step.

### 10. On form submission
Workflow is triggered via form.

### 11. OpenRouter Chat Model1
[Describe what this step does]

### 12. OpenRouter Chat Model2
[Describe what this step does]

### 13. Reddit Search
[Describe what this step does]

### 14. Perplexity
[Describe what this step does]

### 15. OpenRouter Chat Model3
[Describe what this step does]

### 16. HTTP Request
[Describe what this step does]

### 17. Send a message
[Describe what this step does]

### 18. Move file
[Describe what this step does]

### 19. OpenRouter Chat Model4
[Describe what this step does]

### 20. Simple Memory
[Describe what this step does]

### 21. Code
[Describe what this step does]

### 22. Research Agent
AI agent processes the input with the following instructions:
```
=MISSION: Extract consumer insights from Reddit for ad copy creation using SMART SAMPLING methodology.

INPUTS:
- Topic: {{ $('🔗 Enter Forum URL').item.json.researchTopic }}
- Product: {{ $('🔗 Enter Forum URL').item.json.productDescription }}
- Audience: {{ $('🔗 Enter Forum URL').item.json.targetAudience }}
- Batch Size Limit: {{ $json.batchSize || '5 posts' }}
- Client Name: {{ $('🔗 Enter Forum URL').item.json.clientName }}

EXECUTION STRATEGY:

PHASE 1: DISCOVERY (Use Reddit Search Tool)
- Search for: "{{ $('🔗 Enter Forum URL').item.json.researchTopic }}" + problem/help/advice
- Target subreddits: Identify top 2-3 relevant communities
- Time filter: Past 3 months
- Sort by: Relevance + High engagement
- RETRIEVE: Post titles and metadata ONLY (no full content yet)

PHASE 2: STRATEGIC SAMPLING
Select the 5 MOST VALUABLE posts based on:
... [truncated]
```

### 23. If
[Describe what this step does]

### 24. Move file1
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

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/Social Media Pain Point Scraper & Ad Script Generator.json`
Generated on: 2026-01-02