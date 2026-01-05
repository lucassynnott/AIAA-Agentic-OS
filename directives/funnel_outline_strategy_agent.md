# Funnel Outline & Strategy Agent

## What This Workflow Is
This workflow analyzes business inputs and generates a comprehensive funnel strategy blueprint with architecture recommendations, page outlines, and implementation roadmap.

## What It Does
1. Receives detailed business intake form
2. AI researches optimal funnel type
3. Creates funnel architecture recommendation
4. Generates page-by-page outline
5. Outputs Google Doc with strategy

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key
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
- Business/Product Name, Type, Industry
- Ideal Customer Description
- Funnel Objective, Offer Price
- Pain Points, Differentiator
- Traffic Sources, Existing Assets
- Budget, Timeline

### Via Python Script
```bash
python3 execution/generate_funnel_strategy.py \
  --business "Company Name" \
  --business_type "info_product" \
  --objective "lead_gen" \
  --price "$997"
```

### Quick One-Liner
```bash
python3 execution/generate_funnel_strategy.py --business "[NAME]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Business / Product Name**: text (required)
- **What type of business are you?**: dropdown (required)
- **Industry / Niche**: text (required)
- **Describe Your Ideal Customer**: textarea (required)
- **What's your primary funnel objective?**: dropdown (required)
- **Core Offer Price**: text (required)
- **What stage is your business at?**: dropdown (required)
- **Top 3-5 Customer Pain Points**: textarea (required)
- **What Makes You Different?**: textarea (required)
- **Primary Traffic Sources (Select all that apply)**: checkbox (required)
- **What do you already have? (Select all that apply)**: checkbox (required)
- **Successful Competitors**: text (required)
- **Preferred Funnel Type (if known)**: dropdown (required)
- **When do you need this funnel live?**: dropdown (required)
- **Implementation Budget**: dropdown (required)
- **Have we built a funnel for you before?**: dropdown
- **Anything else we should know?**: textarea

## Integrations Required
- Slack

## Process
### 1. Process Form Data
Data is normalized/transformed for the next step.

### 2. Prepare Document Data
Data is normalized/transformed for the next step.

### 3. Create Google Doc
[Describe what this step does]

### 4. Check If Returning Client
[Describe what this step does]

### 5. Search for Existing Folder
[Describe what this step does]

### 6. Create New Client Folder
[Describe what this step does]

### 7. Move to Existing Folder
[Describe what this step does]

### 8. Move to New Folder
[Describe what this step does]

### 9. Prepare Notification Data
Data is normalized/transformed for the next step.

### 10. Slack Notification
[Describe what this step does]

### 11. On form submission
Workflow is triggered via form.

### 12. OpenRouter Chat Model
[Describe what this step does]

### 13. Research Agent
AI agent processes the input with the following instructions:
```
=Research and analyze the optimal funnel strategy for:

Business: {{ $json['Business / Product Name'] }}
Type: {{ $json['What type of business are you?'] }}
Industry: {{ $json['Industry / Niche'] }} 
Target Audience: {{ $json['Describe Your Ideal Customer'] }}
Objective: {{ $json['What\'s your primary funnel objective?'] }}
Pain Points: {{ $json['Top 3-5 Customer Pain Points'] }}
Offer Price: {{ $json['Core Offer Price'] }}
Differentiator: {{ $json['What Makes You Different?'] }}
Traffic Sources: {{ $json['Primary Traffic Sources (Select all that apply)'] }}
Existing Funnel Elements: {{ $json['What do you already have? (Select all that apply)'] }}
Competitors: {{ $json['Successful Competitors'] }}
Preferred Funnel Type: {{ $json['Preferred Funnel Type (if known)'] }}
Additional Context: {{ $json['Anything else we should know?'] }}

Provide a comprehensive funnel strategy analysis including:

1. **FUNNEL ARCHITECTURE RECOMMENDATION**
   - Primary funnel type (VSL, Webinar, Challenge, Application, Book, SLO, Product Launch, etc.)
... [truncated]
```

### 14. OpenRouter Chat Model2
[Describe what this step does]

### 15. Markdown Agent
AI agent processes the input with the following instructions:
```
=Format the following content into clean, professional markdown with proper hierarchy and formatting:

{{ $json.output }}

Requirements:

Add appropriate headers (use # for main title, ## for sections, ### for subsections)
Format any lists with proper markdown bullets or numbers
Bold all important terms, names, or key concepts using text
Use italics for emphasis or quotes
Put any code, commands, or technical terms in backticks
Use code blocks with language specification for any multi-line code
Add blockquotes (>) for important notes or callouts
Format any data as tables if appropriate
Add horizontal rules (---) between major sections if needed
Ensure proper spacing between elements

Example of expected formatting:
Main Document Title
Introduction Section
... [truncated]
```

### 16. Funnel Outline Builder Agent1
AI agent processes the input with the following instructions:
```
=Based on this comprehensive research:

{{ $json.output }}

Create a strategic funnel architecture and implementation roadmap for:

Business: {{ $('Process Form Data').item.json['Business / Product Name'] }}
Type: {{ $('Process Form Data').item.json['What type of business are you?'] }}
Industry: {{ $('Process Form Data').item.json['Industry / Niche'] }}
Target Audience: {{ $('Process Form Data').item.json['Describe Your Ideal Customer'] }}
Objective: {{ $('Process Form Data').item.json['What\'s your primary funnel objective?'] }}
Pain Points: {{ $('Process Form Data').item.json['Top 3-5 Customer Pain Points'] }}
Offer Price: {{ $('Process Form Data').item.json['Core Offer Price'] }}
Differentiator: {{ $('Process Form Data').item.json['What Makes You Different?'] }}
Traffic Sources: {{ $('Process Form Data').item.json['Primary Traffic Sources (Select all that apply)'] }}
Existing Funnel Elements: {{ $('Process Form Data').item.json['What do you already have? (Select all that apply)'] }}
Competitors: {{ $('Process Form Data').item.json['Successful Competitors'] }}
Preferred Funnel Type: {{ $('Process Form Data').item.json['Preferred Funnel Type (if known)'] }}
Additional Context: {{ $('Process Form Data').item.json['Anything else we should know?'] }}

... [truncated]
```

### 17. OpenRouter Chat Model3
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/Funnel Outline & Strategy Agent.json`
Generated on: 2026-01-02