# Product Photoshoot Generator

## What This Workflow Is
This workflow generates AI product photoshoot images using DALL-E or similar, creating professional-looking product shots without photography.

## What It Does
1. Takes product image or description
2. Generates scene/background concepts
3. Creates AI product images
4. Outputs multiple variations
5. Optimizes for e-commerce use

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For DALL-E
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install openai requests
```

## How to Run

### Via N8N Form
Submit form with product details and style preferences.

### Quick One-Liner
```bash
python3 execution/generate_product_photos.py --product "[DESCRIPTION]" --style "lifestyle"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Brand Name**: text (required)
- **Brand Website**: text (required)
- **Brand Niche**: text (required)
- **Photoshoot Goals**: text
- **Additional Context**: text
- **Existing Client?**: dropdown
- **Product Photo (PNG Preferable)**: file

## Integrations Required
- Slack

## Process
### 1. Create Image
[Describe what this step does]

### 2. Set data
Data is normalized/transformed for the next step.

### 3. Completed?
[Describe what this step does]

### 4. Wait 60 sec.
[Describe what this step does]

### 5. Get status
[Describe what this step does]

### 6. Get Url image
[Describe what this step does]

### 7. Get File image
[Describe what this step does]

### 8. On form submission
Workflow is triggered via form.

### 9. Analyze image
[Describe what this step does]

### 10. OpenRouter Chat Model
[Describe what this step does]

### 11. Message a model in Perplexity
[Describe what this step does]

### 12. Photoshoot Research Agent
AI agent processes the input with the following instructions:
```
=Conduct comprehensive brand research for {{ $json.brandName }} and generate 5 detailed Nano Banana prompts for visually distinct product photoshoot scenes that align with brand identity and drive visual engagement.
BRAND TO RESEARCH: {{ $json.brandName }}
WEBSITE: {{ $json.brandWebsite }}
PRODUCT DESCRIPTION: {{ $('Analyze image').first().json.content}}
PHOTOSHOOT GOALS: {{ $json.photoshootGoals }}
ADDITIONAL CONTEXT: {{ $json.context }}


REQUIRED RESEARCH AREAS:

1. VISUAL BRAND IDENTITY ANALYSIS
   - Brand aesthetic, color palettes, and visual style guidelines
   - Existing product photography style and presentation
   - Visual storytelling themes and motifs
   - Typography, textures, and design elements
   - Mood and emotional tone in visual content

2. PRODUCT PRESENTATION INTELLIGENCE
   - How products are currently showcased (angles, lighting, staging)
   - Hero product features to highlight visually
... [truncated]
```

### 13. Code
[Describe what this step does]

### 14. Loop Over Items
[Describe what this step does]

### 15. Upload Original Image to imgbb
[Describe what this step does]

### 16. Check If Returning Client
[Describe what this step does]

### 17. Search for Existing Folder
[Describe what this step does]

### 18. Create New Client Folder
[Describe what this step does]

### 19. Move to Existing Folder
[Describe what this step does]

### 20. Move to New Folder
[Describe what this step does]

### 21. Slack Notification
[Describe what this step does]

### 22. Upload file
[Describe what this step does]

### 23. Aggregate
[Describe what this step does]

### 24. Code1
[Describe what this step does]

### 25. Loop Over Items1
[Describe what this step does]

### 26. Prepare Notification Data (New Client)
Data is normalized/transformed for the next step.

### 27. Prepare Notification Data (Existing Client)
Data is normalized/transformed for the next step.

### 28. Slack Notification1
[Describe what this step does]

### 29. Code2
[Describe what this step does]

### 30. Loop Over Items2
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Ecom Email Marketing Agency/Product Photoshoot Generator.json`
Generated on: 2026-01-02