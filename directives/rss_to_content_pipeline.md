# RSS-to-Content Pipeline

## What This Workflow Is
This workflow monitors RSS feeds for industry news, then automatically generates social media content and commentary using AI.

## What It Does
1. Monitors configured RSS feeds
2. Filters for relevant articles
3. Summarizes key points
4. Generates social posts
5. Schedules or outputs drafts

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install feedparser openai
```

## How to Run

### Via N8N Schedule
Configure RSS feeds and run on schedule.

### Quick One-Liner
```bash
python3 execution/rss_to_content.py --feeds "[RSS_URLS]" --platform twitter
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Schedule
- **Node**: Schedule Trigger

## Inputs
- [Define inputs based on trigger type]

## Integrations Required
- Slack

## Process
### 1. TechCrunch
[Describe what this step does]

### 2. Hacker News
[Describe what this step does]

### 3. CrunchBase
[Describe what this step does]

### 4. AI Business
[Describe what this step does]

### 5. Aggregate
[Describe what this step does]

### 6. Aggregate1
[Describe what this step does]

### 7. Aggregate2
[Describe what this step does]

### 8. Aggregate3
[Describe what this step does]

### 9. Aggregate4
[Describe what this step does]

### 10. Wait
[Describe what this step does]

### 11. AI Trends
[Describe what this step does]

### 12. Keyword Filter
[Describe what this step does]

### 13. Merge
[Describe what this step does]

### 14. Aggregate5
[Describe what this step does]

### 15. Keyword Filter1
[Describe what this step does]

### 16. Keyword Filter2
[Describe what this step does]

### 17. Keyword Filter3
[Describe what this step does]

### 18. Keyword Filter4
[Describe what this step does]

### 19. Send message and wait for response
[Describe what this step does]

### 20. AI Agent
AI agent processes the input with the following instructions:
```
=GOAL:
Take the news information and turn it into a 1500 - 2000 character LinkedIn post. Remember that I am Lucas Synnott and I'm writing in the first person.

Use the contents of that articles, combined with your system knowledge, to create a high-performing LinkedIn post.

FORMATTING:
Format the output according to the LinkedIn frameworks provided, including a strong hook, clear structure, and engaging conclusion.

The post should be purely text based.

WARNINGS:
Write the copy in the voice and character that myself, Lucas Synnott, would have when writing content. It sounds real, natural, and like something that I would use in a real human-to-human conversation as the owner of a marketing agency.

In your response, don’t include ANY formatting or odd characters, just text only. Don’t include any of the following in your response, unless it is part of the text of the script: #, *, **

In your response, be sure to ONLY reply with the post copy, don’t include other text or explanations.

Articles:
{{ $json.data[0].data[0].content }}

... [truncated]
```

### 21. OpenRouter Chat Model
[Describe what this step does]

### 22. Think
[Describe what this step does]

### 23. Message a model in Perplexity
[Describe what this step does]

### 24. Create post
[Describe what this step does]

### 25. Workflow Finished
Data is normalized/transformed for the next step.

### 26. If
[Describe what this step does]

### 27. Aggregate6
[Describe what this step does]

### 28. Keyword Filter5
[Describe what this step does]

### 29. RSS.app
[Describe what this step does]

### 30. Schedule Trigger
Workflow is triggered via schedule.

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Content Marketing Agency/RSS-to-Content Pipeline.json`
Generated on: 2026-01-02