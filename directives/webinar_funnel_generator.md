# Webinar Funnel Generator

## What This Workflow Is
This workflow generates complete webinar funnel assets including registration page, webinar slides outline, and email sequences.

## What It Does
1. Takes webinar topic and offer
2. Generates registration page copy
3. Creates webinar slide outline
4. Writes email sequences
5. Outputs to Google Docs/Slides

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
python3 execution/generate_webinar_funnel.py --topic "[TOPIC]" --offer "[OFFER]" --price "$997"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Client Name**: text (required)
- **Google Doc URL**: text
- **Webinar Type**: dropdown (required)
- **Webinar Date/Time**: text (required)
- **Webinar Platform**: dropdown (required)
- **Webinar Duration**: dropdown (required)
- **Fast Action Bonus**: text
- **Replay Availability**: dropdown (required)
- **Teaching Style**: dropdown (required)
- **Pitch Intensity**: dropdown (required)
- **Special Guest or Interview**: text

## Integrations Required
- Slack

## Process
### 1. Get Strategy Document
[Describe what this step does]

### 2. Store Generated Content
Data is normalized/transformed for the next step.

### 3. Create Summary
Data is normalized/transformed for the next step.

### 4. On form submission
Workflow is triggered via form.

### 5. Search for Existing Folder
[Describe what this step does]

### 6. Create New Client Folder
[Describe what this step does]

### 7. Move to Existing Folder
[Describe what this step does]

### 8. Move to New Folder
[Describe what this step does]

### 9. Slack Notification
[Describe what this step does]

### 10. Get a document
[Describe what this step does]

### 11. Registration Page Copywriter
AI agent processes the input with the following instructions:
```
=Objective
Create a high-converting webinar registration page from the inputs below. Enforce the system rules and adaptive logic.

Strategic Blueprint
{{ $('Get a document').first().json.content }}

Webinar Configuration
Client: {{ $('On form submission').first().json['Client Name'] }}
Type: {{ $('On form submission').first().json['Webinar Type'] }}
Date/Time: {{ $('On form submission').first().json['Webinar Date/Time'] }}
Platform: {{ $('On form submission').first().json['Webinar Platform'] }}
Duration: {{ $('On form submission').first().json['Webinar Duration'] }}
Fast Action Bonus: {{ $('On form submission').first().json['Fast Action Bonus'] }}
Replay Availability: {{ $('On form submission').first().json['Replay Availability'] }}
Special Guest: {{ $('On form submission').first().json['Special Guest or Interview'] }}

Webinar Script:
{{ $json.output }}

Deliverables
... [truncated]
```

### 12. OpenRouter Chat Model
[Describe what this step does]

### 13. Webinar Copywriter Agent
AI agent processes the input with the following instructions:
```
=Objective
Produce a complete, conversion-ready webinar package tailored to the inputs below. Respect all system rules and decision logic.

Inputs
Strategic Blueprint
{{ $('Get a document').first().json.content }}

Webinar Configuration
Client: {{ $('On form submission').first().json['Client Name'] }}
Type: {{ $('On form submission').first().json['Webinar Type'] }}
Date/Time: {{ $('On form submission').first().json['Webinar Date/Time'] }}
Platform: {{ $('On form submission').first().json['Webinar Platform'] }}
Duration: {{ $('On form submission').first().json['Webinar Duration'] }}
Fast Action Bonus: {{ $('On form submission').first().json['Fast Action Bonus'] }}
Replay Availability: {{ $('On form submission').first().json['Replay Availability'] }}
Special Guest: {{ $('On form submission').first().json['Special Guest or Interview'] }}

Constraints and requirements

Select the correct webinar spine based on the inputs and state which spine you chose in one sentence at the top.
... [truncated]
```

### 14. OpenRouter Chat Model1
[Describe what this step does]

### 15. Simple Memory1
[Describe what this step does]

### 16. Code
[Describe what this step does]

### 17. OpenRouter Chat Model2
[Describe what this step does]

### 18. Email Sequence Copywriter
AI agent processes the input with the following instructions:
```
=Objective
Create complete pre and post-webinar email sequences from the inputs below. Enforce the system rules, adaptive logic, segmentation lanes, and quality gates.

Strategic Blueprint
{{ $('Get a document').first().json.content }}

Webinar Configuration
Client: {{ $('On form submission').first().json['Client Name'] }}
Type: {{ $('On form submission').first().json['Webinar Type'] }}
Date/Time: {{ $('On form submission').first().json['Webinar Date/Time'] }}
Platform: {{ $('On form submission').first().json['Webinar Platform'] }}
Duration: {{ $('On form submission').first().json['Webinar Duration'] }}
Fast Action Bonus: {{ $('On form submission').first().json['Fast Action Bonus'] }}
Replay Availability: {{ $('On form submission').first().json['Replay Availability'] }}
Special Guest: {{ $('On form submission').first().json['Special Guest or Interview'] }}

Webinar Script:
{{ $json.output }}

Deliverables
... [truncated]
```

### 19. OpenRouter Chat Model3
[Describe what this step does]

### 20. Slide Deck Copywriter
AI agent processes the input with the following instructions:
```
=Create a complete slide deck outline based on the webinar script and strategy.

Strategic Blueprint
{{ $('Get a document').first().json.content }}

Webinar Configuration
Client: {{ $('On form submission').first().json['Client Name'] }}
Type: {{ $('On form submission').first().json['Webinar Type'] }}
Date/Time: {{ $('On form submission').first().json['Webinar Date/Time'] }}
Platform: {{ $('On form submission').first().json['Webinar Platform'] }}
Duration: {{ $('On form submission').first().json['Webinar Duration'] }}
Fast Action Bonus: {{ $('On form submission').first().json['Fast Action Bonus'] }}
Replay Availability: {{ $('On form submission').first().json['Replay Availability'] }}
Special Guest: {{ $('On form submission').first().json['Special Guest or Interview'] }}

Webinar Script:
{{ $json.output }}

Create the following slide-by-slide outline:

... [truncated]
```

### 21. Thank You Page Copywriter
AI agent processes the input with the following instructions:
```
=Objective
Create a high-converting webinar thank you page that maximizes live attendance and primed intent. Enforce the system rules and adaptive logic.

Strategic Blueprint
{{ $('Get a document').first().json.content }}

Webinar Configuration
Client: {{ $('On form submission').first().json['Client Name'] }}
Type: {{ $('On form submission').first().json['Webinar Type'] }}
Date/Time: {{ $('On form submission').first().json['Webinar Date/Time'] }}
Platform: {{ $('On form submission').first().json['Webinar Platform'] }}
Duration: {{ $('On form submission').first().json['Webinar Duration'] }}
Fast Action Bonus: {{ $('On form submission').first().json['Fast Action Bonus'] }}
Replay Availability: {{ $('On form submission').first().json['Replay Availability'] }}
Special Guest: {{ $('On form submission').first().json['Special Guest or Interview'] }}

Webinar Script:
{{ $json.output }}

Deliverables
... [truncated]
```

### 22. OpenRouter Chat Model4
[Describe what this step does]

### 23. Create Webinar Script Doc
[Describe what this step does]

### 24. Create Thank You Page Doc
[Describe what this step does]

### 25. Create Slide Deck Doc
[Describe what this step does]

### 26. Create Email Sequence Doc
[Describe what this step does]

### 27. Create Registration Page Doc
[Describe what this step does]

### 28. Edit Fields
Data is normalized/transformed for the next step.

### 29. Code1
[Describe what this step does]

### 30. Aggregate
[Describe what this step does]

### 31. If
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/Webinar Funnel Generator.json`
Generated on: 2026-01-02