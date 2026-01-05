# VSL Funnel Writer

## What This Workflow Is
This workflow generates complete VSL (Video Sales Letter) funnel copy including script, landing page, and email sequence using proven frameworks.

## What It Does
1. Receives product/offer details
2. Generates VSL script with hooks
3. Creates landing page copy
4. Writes email sequence
5. Outputs to Google Docs

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Installation
```bash
pip install openai google-api-python-client
```

## How to Run
```bash
python3 execution/generate_vsl_funnel.py --product "[PRODUCT]" --price "$997" --audience "[AUDIENCE]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: VSL Form Submission

## Inputs
- **Client Name**: text (required)
- **Product/Service Name**: text (required)
- **Price Point**: text (required)
- **Payment Options**: text
- **Target Audience**: textarea (required)
- **Main Pain Points**: textarea (required)
- **Unique Mechanism**: textarea (required)
- **Transformation Promise**: textarea (required)
- **Client Results**: textarea (required)
- **Core Offer Details**: textarea (required)
- **Bonus Stack**: textarea (required)
- **Total Value**: text (required)
- **VSL Style**: dropdown (required)
- **VSL Length**: dropdown (required)
- **Urgency Element**: text (required)
- **Guarantee**: text (required)

## Integrations Required
- Slack

## Process
### 1. Prepare Context
[Describe what this step does]

### 2. Compile Final Script
[Describe what this step does]

### 3. Create VSL Script Doc
[Describe what this step does]

### 4. VSL Hook Creation Agent
AI agent processes the input with the following instructions:
```
=Create 3 powerful VSL opening hooks using different psychological frameworks.

CONTEXT FOR HOOKS:

**RESEARCH DOC**
{{ $json.strategyContext }}

**Product/Service**: {{ $('VSL Form Submission').first().json['Product/Service Name'] }}
Description: 
{{ $('VSL Form Submission').first().json['Core Offer Details'] }}


**Target Audience**: 
- Demographics: {{ $('VSL Form Submission').first().json['Target Audience'] }}

**Primary Pain Points** (in order of intensity):
{{ $('VSL Form Submission').first().json['Main Pain Points'] }}


**Transformation Promise**: 
... [truncated]
```

### 5. OpenRouter Chat Model
[Describe what this step does]

### 6. Simple Memory
[Describe what this step does]

### 7. OpenRouter Chat Model1
[Describe what this step does]

### 8. Simple Memory1
[Describe what this step does]

### 9. VSL Story Architecture Agent
AI agent processes the input with the following instructions:
```
=Create the main story section for this VSL that transforms viewers from skeptics to believers.

STORY CONTEXT:


**RESEARCH DOC**
{{ $('Prepare Context').first().json.strategyContext }}

**Product/Service**: {{ $('VSL Form Submission').first().json['Product/Service Name'] }}
Description: 
{{ $('VSL Form Submission').first().json['Core Offer Details'] }}


**Selected Hook**: {{ $('VSL Hook Creation Agent').first().json.output }}
[The hook you're building from]

**Target Audience**: 
- Demographics: {{ $('VSL Form Submission').first().json['Target Audience'] }}

**Primary Pain Points** (in order of intensity):
... [truncated]
```

### 10. VSL Objection Handling Agent
AI agent processes the input with the following instructions:
```
=Create a masterful objection dissolution section that preemptively eliminates all buying resistance.

**PRODUCT CONTEXT:**

**RESEARCH DOC**
{{ $('Prepare Context').first().json.strategyContext }}

**Product/Service**: {{ $('VSL Form Submission').first().json['Product/Service Name'] }}
Description: 
{{ $('VSL Form Submission').first().json['Core Offer Details'] }}


**Selected Hook**: {{ $('VSL Hook Creation Agent').first().json.output }}
[The hook you're building from]

**Target Audience**: 
- Demographics: {{ $('VSL Form Submission').first().json['Target Audience'] }}

**Primary Pain Points** (in order of intensity):
{{ $('VSL Form Submission').first().json['Main Pain Points'] }}
... [truncated]
```

### 11. OpenRouter Chat Model2
[Describe what this step does]

### 12. Simple Memory2
[Describe what this step does]

### 13. OpenRouter Chat Model3
[Describe what this step does]

### 14. Simple Memory3
[Describe what this step does]

### 15. VSL Form Submission
Workflow is triggered via form.

### 16. Code
[Describe what this step does]

### 17. Find Strategy Document
[Describe what this step does]

### 18. Get Strategy Document
[Describe what this step does]

### 19. Closing CTA Agent
AI agent processes the input with the following instructions:
```
=Create a masterful VSL close and call-to-action that makes purchasing feel inevitable and exciting.

**CLOSING CONTEXT:**

**RESEARCH DOC**
{{ $('Prepare Context').first().json.strategyContext }}

**Product/Service**: {{ $('VSL Form Submission').first().json['Product/Service Name'] }}
Description: 
{{ $('VSL Form Submission').first().json['Core Offer Details'] }}


**Selected Hook**: {{ $('VSL Hook Creation Agent').first().json.output }}
[The hook you're building from]

**Target Audience**: 
- Demographics: {{ $('VSL Form Submission').first().json['Target Audience'] }}

**Primary Pain Points** (in order of intensity):
{{ $('VSL Form Submission').first().json['Main Pain Points'] }}
... [truncated]
```

### 20. Create Summary
Data is normalized/transformed for the next step.

### 21. Search for Existing Folder
[Describe what this step does]

### 22. Slack Notification
[Describe what this step does]

### 23. Create New Client Folder1
[Describe what this step does]

### 24. Move to Existing Folder1
[Describe what this step does]

### 25. Move to New Folder1
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/VSL Funnel Writer.json`
Generated on: 2026-01-02