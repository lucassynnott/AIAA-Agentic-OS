# Cold Email Scriptwriter

## What This Workflow Is
This workflow generates personalized cold email sequences with A/B variants using AI research and proven copywriting frameworks.

## What It Does
1. Receives lead list CSV via form
2. Researches each prospect with Perplexity
3. Generates personalized first lines
4. Creates multi-email sequences
5. Outputs to Google Sheet with A/B variants

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key    # For AI generation
PERPLEXITY_API_KEY=your_perplexity_key    # For prospect research
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
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
- Sender Name, Sender Title
- Product/Service, Value Proposition
- Company Website
- Lead List CSV

### Via Python Script
```bash
python3 execution/write_cold_emails.py \
  --leads "[CSV_PATH]" \
  --sender_name "[NAME]" \
  --product "[PRODUCT]" \
  --value_prop "[VALUE_PROP]"
```

### Quick One-Liner
```bash
python3 execution/write_cold_emails.py --leads leads.csv --product "[PRODUCT]"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: Campaign Request Form

## Inputs
- **Sender Name**: text (required)
- **Sender Title**: text (required)
- **Your Product/Service**: textarea (required)
- **Value Proposition**: textarea (required)
- **Company Website**: text (required)
- **Upload Lead List CSV (for multiple campaigns)**: file (required)

## Integrations Required
- Slack
- Google Sheets

## Process
### 1. Process CSV Upload
[Describe what this step does]

### 2. Normalize CSV Data
Data is normalized/transformed for the next step.

### 3. Merge Normalized Data
[Describe what this step does]

### 4. Prospect Research Agent
AI agent processes the input with the following instructions:
```
=You are an expert B2B sales researcher and fact checker. Your goal is to generate high-signal insights and a single personalized first line for a cold email based on verifiable facts. You must use the Perplexity tool for all prospect research. Never invent facts. Return ONLY valid JSON per the schema at the end. No markdown, no preamble, no explanations.

Context
Trigger Type: {{ $('Merge Normalized Data').first().json.trigger_type }}

Prospect Details:
- Name: {{ $('Merge Normalized Data').first().json.prospect_name }}
- Title: {{ $('Merge Normalized Data').first().json.prospect_title }}
- Company: {{ $('Merge Normalized Data').first().json.company_name }}
- Industry: {{ $('Merge Normalized Data').first().json.industry }}
- Company Size: {{ $('Merge Normalized Data').first().json.company_size }}
- Personalization Notes: {{ $('Merge Normalized Data').first().json.personalization_notes }}
- Optional: Domain: {{ $('Merge Normalized Data').first().json.company_domain }}
- Optional: Prospect LinkedIn: {{ $('Merge Normalized Data').first().json.prospect_linkedin_url }}

Product/Service Context:
- Offering: {{ $('Campaign Request Form').first().json['Your Product/Service'] }}
- Value Proposition: {{ $('Campaign Request Form').first().json['Value Proposition'] }}


... [truncated]
```

### 5. Email Sequence Generator
AI agent processes the input with the following instructions:
```
=# Cold Email Writer Agent Prompt

You are an expert cold email copywriter trained on Christian Bonnier's "30 Scripts That Won" methodology. You craft hyper-focused, conversational emails that achieve >10% response rates by following proven patterns from successful campaigns. You create just the email body, prospect personalization data will be added as a first line before the email body

### Your Offering
- **Service/Product:** {{ $('Process Form Data').first().json.product_service }}
- **Value Proposition:** {{ $('Process Form Data').first().json.value_proposition }}


## PROVEN EMAIL PATTERNS

### Pattern A: Problem + Social Proof + Soft Ask
1. **Opening:** Direct acknowledgment of their specific situation/pain
2. **Social Proof:** Concrete result from similar company (numbers preferred)
3. **Bridge:** How you achieve this outcome
4. **CTA:** Low-commitment question ("Open to..." / "Mind if I...")

### Pattern B: Observation + Value + Permission
1. **Opening:** Specific observation about their business
2. **Value Tease:** "I noticed/found/spotted X issues/opportunities"
... [truncated]
```

### 6. A/B Variant Generator
AI agent processes the input with the following instructions:
```
=You are an expert A/B testing specialist for cold email campaigns. Create alternative versions of the first email for split testing.

Original Campaign Data:
{{ JSON.stringify($('Merge Normalized Data').first().json) }}

Research Context:
{{ JSON.stringify($('Prospect Research Agent').first().json) }}

Original Email Sequence:
{{ JSON.stringify($('Email Sequence Generator').first().json) }}

Personalized First Line:
{{ $json.output }}

My Service: {{ $('Campaign Request Form').first().json['Your Product/Service'] }}
Value Proposition: {{ $('Campaign Request Form').first().json['Value Proposition'] }}

Generate 3 A/B/C variants of Email #1 using different approaches:

**VARIANT A**: Before/After/Bridge framework
... [truncated]
```

### 7. OpenRouter Chat Model
[Describe what this step does]

### 8. OpenRouter Chat Model2
[Describe what this step does]

### 9. OpenRouter Chat Model3
[Describe what this step does]

### 10. Notify: Returning Customer
[Describe what this step does]

### 11. Loop Over Items
[Describe what this step does]

### 12. If CSV uploaded
[Describe what this step does]

### 13. Create spreadsheet
[Describe what this step does]

### 14. Process Form Data
Data is normalized/transformed for the next step.

### 15. Format Final Email
Data is normalized/transformed for the next step.

### 16. Update Google Sheet
[Describe what this step does]

### 17. Campaign Request Form
Workflow is triggered via form.

### 18. Autofix
[Describe what this step does]

### 19. Perplexity
[Describe what this step does]

### 20. First Line Writer
AI agent processes the input with the following instructions:
```
=Write a personalized first line for a cold email to this prospect:
Recipient Details:

Name: {{ $('Process CSV Upload').first().json['First Name'] }} {{ $('Process CSV Upload').first().json['Last Name'] }}
Company: {{ $('Process CSV Upload').first().json.Company }}

Research Insights:

Pain Points: {{ $json.pain_points }}
Business Priorities: {{ $json.business_priorities }}
Conversation Starters: {{ $json.conversation_starters }}
Likely Objections: {{ $json.likely_objections }}
Best Timing Context: {{ $json.best_timing }}
Personalization Angle: {{ $json.personalization_angle }}
Industry Insights: {{ $json.industry_insights }}

My Services:
Product/service: {{ $('Campaign Request Form').first().json['Your Product/Service'] }}
Value Proposition: {{ $('Campaign Request Form').first().json['Value Proposition'] }}

... [truncated]
```

### 21. OpenRouter Chat Model5
[Describe what this step does]

## Output Schema
### Research Output Parser
```json
{
  "type": "object",
  "properties": {
    "pain_points": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "business_priorities": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "conversation_starters": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "personalized_first_line": {
      "type": "string",
      "items": {
        "type": "string"
      }
    },
    "likely_objections": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "best_timing": {
      "type": "string"
    },
    "personalization_angle": {
      "type": "string"
    },
    "industry_insights": {
      "type": "string"
    }
  },
  "required": [
    "pain_points",
    "business_priorities",
    "conversation_starters",
    "likely_objections",
    "best_timing",
    "personalization_angle",
    "industry_insights"
  ]
}
```
### Sequence Output Parser
```json
{
  "type": "object",
  "properties": {
    "email_sequence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "email_number": {
            "type": "number"
          },
          "timing": {
            "type": "string"
          },
          "subject_suggestion": {
            "type": "string"
          },
          "body": {
            "type": "string"
          },
          "cta": {
            "type": "string"
          },
          "framework": {
            "type": "string"
          },
          "key_elements": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "personalization_used": {
            "type": "string"
          }
        },
        "required": [
          "email_number",
          "timing",
          "subject_suggestion",
          "body",
          "cta",
          "framework",
          "key_elements",
          "personalization_used"
        ]
      }
    }
  },
  "required": [
    "email_sequence"
  ]
}
```
### Variant Output Parser
```json
{
  "type": "object",
  "properties": {
    "ab_variants": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "variant": {
            "type": "string"
          },
          "framework": {
            "type": "string"
          },
          "subject_line": {
            "type": "string"
          },
          "body": {
            "type": "string"
          },
          "first_line": {
            "type": "string"
          },
          "cta": {
            "type": "string"
          },
          "test_hypothesis": {
            "type": "string"
          },
          "research_angle": {
            "type": "string"
          }
        },
        "required": [
          "variant",
          "framework",
          "subject_line",
          "body",
          "cta",
          "test_hypothesis",
          "research_angle"
        ]
      }
    }
  },
  "required": [
    "ab_variants"
  ]
}
```

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Cold Email Lead Generation Agency/Cold Email Scriptwriter.json`
Generated on: 2026-01-02