# Static Ad Generator

## What This Workflow Is
This workflow generates static ad images for Meta, Google, and LinkedIn using AI-generated visuals and copy.

## What It Does
1. Takes product/offer details via form
2. Generates ad copy variations
3. Creates static ad images with AI
4. Outputs multiple size formats
5. Ready for upload to ad platforms

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
```

### Installation
```bash
pip install openai requests pillow
```

## How to Run
```bash
python3 execution/generate_static_ads.py --product "[PRODUCT]" --platform meta
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: Static Ad Form Trigger

## Inputs
- **Business Name**: text (required)
- **Service Description**: textarea (required)
- **Target Audience**: text (required)
- **Key Benefits**: textarea (required)
- **Brand Style**: text (required)
- **Primary Brand Colors**: text
- **Returning Client?**: dropdown (required)

## Integrations Required
- Slack

## Process
### 1. Static Ad Form Trigger
Workflow is triggered via form.

### 2. AI Agent - Ad Prompt Generator
AI agent processes the input with the following instructions:
```
=Create 3 high-converting static ad concepts with the following specifications:
BRAND DETAILS:

Business: {{$json['Business Name'] || 'Specify business name'}}
Service/Product: {{$json['Service Description'] || 'Describe offering'}}
Industry/Category: {{$json['Industry'] || 'Specify industry'}}
Unique Value Proposition: {{$json['UVP'] || 'What makes this unique?'}}

Website:
{{ $json.Website }}

TARGET AUDIENCE:

Primary Demographic: {{$json['Target Audience'] || 'Define target audience'}}
Pain Points: {{$json['Pain Points'] || 'List main challenges/problems'}}
Desired Outcomes: {{$json['Desired Outcomes'] || 'What do they want to achieve?'}}
Platform Behavior: {{$json['Platform Preference'] || 'Where do they spend time online?'}}

BRAND GUIDELINES:

... [truncated]
```

### 3. Split Prompts for Processing
[Describe what this step does]

### 4. Generate Image - Concept 1
[Describe what this step does]

### 5. Generate Image - Concept 2
[Describe what this step does]

### 6. Generate Image - Concept 3
[Describe what this step does]

### 7. Check Returning Client
[Describe what this step does]

### 8. Search Client Folder
[Describe what this step does]

### 9. Create Client Folder
[Describe what this step does]

### 10. Upload to Google Drive
[Describe what this step does]

### 11. Success Response
Data is normalized/transformed for the next step.

### 12. OpenRouter Chat Model
[Describe what this step does]

### 13. SerpAPI
[Describe what this step does]

### 14. Aggregate
[Describe what this step does]

### 15. Send a message
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/Static Ad Generator.json`
Generated on: 2026-01-02