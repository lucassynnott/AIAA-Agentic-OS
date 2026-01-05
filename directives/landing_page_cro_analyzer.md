# Landing Page CRO Analyzer

## What This Workflow Is
This workflow analyzes landing pages for conversion rate optimization opportunities using AI, providing actionable recommendations.

## What It Does
1. Receives landing page URL via form
2. Fetches and converts page to markdown
3. AI analyzes copy, layout, CRO elements
4. Generates improvement recommendations
5. Outputs report to Slack

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install openai requests
```

## How to Run

### Via N8N Form
Submit form with:
- Client Name, Landing Page URL
- Funnel Type, Industry Niche
- Current Funnel Metrics

### Quick One-Liner
```bash
python3 execution/analyze_landing_page.py --url "[URL]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Client Name**: text
- **Existing Client?**: dropdown
- **Landing Page Url**: text (required)
- **Funnel Type**: text
- **Industry Niche**: text
- **Current Funnel Metrics**: textarea

## Integrations Required
- Slack

## Process
### 1. On form submission
Workflow is triggered via form.

### 2. HTTP Request
[Describe what this step does]

### 3. Markdown
[Describe what this step does]

### 4. OpenRouter Chat Model
[Describe what this step does]

### 5. Landing Page AI Analyzer
AI agent processes the input with the following instructions:
```
=Client Name:
{{ $('On form submission').item.json['Client Name'] }}

Sales Funnel to Analyze:

{{ $json.data }}

Sales Funnel Type:
{{ $('On form submission').item.json['Funnel Type'] }}

Industry Niche:
{{ $('On form submission').item.json['Industry Niche'] }}

Current Funnel Metrics:
{{ $('On form submission').item.json['Current Funnel Metrics'] }}
```

### 6. Check Customer Status
[Describe what this step does]

### 7. Search Existing Client Folder
[Describe what this step does]

### 8. Notify: Returning Customer
[Describe what this step does]

### 9. Create New Client Folder1
[Describe what this step does]

### 10. Move to Existing Folder
[Describe what this step does]

### 11. Move to New Folder
[Describe what this step does]

### 12. HTTP Request1
[Describe what this step does]

### 13. OpenRouter Chat Model2
[Describe what this step does]

### 14. Markdown Converter Agent
AI agent processes the input with the following instructions:
```
=System role:
You are an expert markdown formatter for CRO landing-page teardowns. You take structured CRO analysis JSON and produce a clean, scannable markdown report. You never invent data. If a field is missing, write “Not provided.” You never output template tokens , the words “undefined,” “[invalid syntax],” or any JSON wrapper.

INPUT TEXT:
{{ $json.output }}

Output:
- Return ONLY a complete markdown document. No JSON. No preamble. No commentary.

Global rules:
- Use proper markdown headings: # title, then ## and ###.
- Make it skimmable with short paragraphs and bullet lists.
- Do NOT use tables or grids.
- Use fenced code blocks only for copy snippets, CSS selectors, and event payload examples.
- Preserve exact capitalization/punctuation of example copy.
- No emojis. No decorative characters.
- Add appropriate linebreaks after headings, subheadings, etc.
- Add : colons between headings and body text if needed (e.g. Hero Headline: Activate Your Feminine Energy & Transform Your Life Today)
- Do not include code blocks or ``` sections anywhere, only headings, subheadings, body, and lists
- Never wrap text in ```
... [truncated]
```

### 15. Message a model in Perplexity
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/Landing Page CRO Analyzer.json`
Generated on: 2026-01-02