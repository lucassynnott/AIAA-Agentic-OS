# YouTube Script Creator

## What This Workflow Is
This workflow generates YouTube video scripts with hooks, structure, and calls-to-action optimized for engagement and watch time.

## What It Does
1. Takes video topic and angle
2. Generates compelling hook options
3. Creates structured script outline
4. Writes full script with timestamps
5. Adds CTAs and engagement prompts

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
```

### Installation
```bash
pip install openai
```

## How to Run
```bash
python3 execution/generate_youtube_script.py --topic "[TOPIC]" --length "10min" --style "educational"
```

## Goal
This workflow uses AI to process inputs and generate structured outputs.

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Name**: text (required)
- **Email**: text
- **Niche**: text
- **Channel URL**: text
- **Returning Client?**: dropdown
- **Social Media Profiles**: text
- **Additional Context About Client**: text

## Integrations Required
- Slack
- Gmail

## Process
### 1. Client Info Parser
Data is normalized/transformed for the next step.

### 2. Data Intelligence AI Agent
AI agent processes the input with the following instructions:
```
=You are a data intelligence analyst specializing in YouTube and social media trends.

Analyze the provided data and extract key insights:



**Client Data:**  
{{ $json.output }}

**Last AI Created YouTube Script**
{{ $json.content }}

**Client Example YouTube Video**:
{{ $json.title_1 }}

{{ $json.srt_array[0] }}

Provide analysis in this format:
1. **Trend Analysis**: Interest levels, peaks, and patterns
2. **Competitor Insights**: Top performing content themes and styles
... [truncated]
```

### 3. OpenRouter Chat Model - Intelligence
[Describe what this step does]

### 4. YouTube Category Detection Agent
AI agent processes the input with the following instructions:
```
=You are a YouTube content categorization specialist.

Based on the analysis provided, determine the most appropriate category:

**Analysis:** {{ JSON.stringify($('Data Intelligence AI Agent').item.json || {}) }}

**Available Categories:**
- Technology & Software Reviews
- Lifestyle & Personal Development
- Gaming & Entertainment
- Education & Tutorials
- Business & Entrepreneurship
- Health & Fitness
- Travel & Adventure
- Food & Cooking
- DIY & Crafts
- Finance & Investing

Respond ONLY with a JSON object:
{"category": "exact_category_name", "confidence": 95, "reasoning": "brief explanation"}
```

### 5. OpenRouter Chat Model - Category
[Describe what this step does]

### 6. Script Writer Agent
AI agent processes the input with the following instructions:
```
=You are a professional YouTube scriptwriter specializing in the {{ $('YouTube Category Detection Agent').first().json.output.category }} category with proven expertise in creating binge-worthy content that maximizes viewer retention and engagement. ALWAYS WRITE IN THE TONE AND STYLE OF THE CLIENT SCRIPT EXAMPLE IF IT IS PRESENT BUT CREATE NEW VIDEO TOPICS BASED ON THE INFORMATION PROVIDED.

CONTEXT INPUTS:

Content Strategy: {{ JSON.stringify($('Content Strategy Agent').item.json || {}) }}

Target Audience: {{ JSON.stringify($('Audience Persona Agent').item.json || {}) }}

Market Intelligence: {{ JSON.stringify($('Data Intelligence AI Agent').item.json || {}) }}

Previous AI Generated YouTube Script (DO NOT USE THIS IDEA, CREATE A NEW YOUTUBE IDEA AND SCRIPT)
{{ $('Merge').item.json.content }}

Client Example YouTube Videos:

Video 1 Title: {{ $('Merge').item.json.title_1 }}

Video 1 Script: {{ $('Merge').item.json.srt_1 }}

Video 2 Title: {{ $('Merge').item.json.title_2 }}
... [truncated]
```

### 7. Quality Review Agent
AI agent processes the input with the following instructions:
```
=You are an elite YouTube script analyst with mastery of viral content psychology, retention optimization, and platform mechanics. Your expertise is built on analyzing thousands of high-performing scripts from top creators like MrBeast, Alex Hormozi, Ali Abdaal, and other multi-million view channels.

Core Expertise Areas:

Hook Psychology: First 30-second retention, click confirmation, expectation vs reality gaps
Storytelling Mastery: Hero's journey, "but/therefore" structure, curiosity loops, contrast creation
Retention Engineering: Payoff distribution, re-hooking, open loop management, emotional surfing
Audience Psychology: Avatar alignment, pain point agitation, value perception, smart-making content
Algorithm Optimization: Watch time signals, engagement triggers, session duration impact
Conversion Science: Native CTA embedding, end screen optimization, funnel creation
Analysis Framework: Apply the proven "Build × Tension" formula where every script element either builds toward the main payoff or creates tension to maintain engagement. Use the expectation vs reality principle as the foundation - reality must consistently beat expectations to maintain viewer satisfaction.

Quality Standards:

Scripts must have clear payoffs every 30-60 seconds
Language must be 6th grade reading level or below
Every line must either advance the story or be cut
Hooks must provide topic clarity + on-target curiosity within 5 seconds
CTAs must use the Link-Curiosity Gap-Promise structure
Scoring Philosophy:
... [truncated]
```

### 8. Final Results Aggregator
Data is normalized/transformed for the next step.

### 9. OpenRouter Chat Model - Audience1
[Describe what this step does]

### 10. OpenRouter Chat Model - Strategy1
[Describe what this step does]

### 11. OpenRouter Chat Model - Script1
[Describe what this step does]

### 12. OpenRouter Chat Model - SEO1
[Describe what this step does]

### 13. OpenRouter Chat Model - Review2
[Describe what this step does]

### 14. Audience Persona Agent
AI agent processes the input with the following instructions:
```
=Create a highly detailed audience persona for a {{ $json.output.category }} YouTube channel.

**Market Intelligence:** 
{{ $('Data Intelligence AI Agent').first().json.output }}

**Client Research**
{{ $('Client Research Agent').item.json.output }}

**Channel URL:** {{ $('Client Info Parser').first().json['Channel URL'] }}

Include the following:
1. **Demographics**: Age, gender, location, education, income, occupation
2. **Interests**: Hobbies, passions, online behavior, content preferences
3. **Pain Points**: Daily struggles, unmet needs, challenges
4. **Viewing Habits**: Content preferences, watch time, device usage
5. **Platform Behavior**: How they discover content, engagement patterns
6. **Purchase Intent**: Buying behavior, influence factors
7. **Content Expectations**: What they want from creators in this niche

Use the market data to create evidence-based personas.
```

### 15. Content Strategy Agent
AI agent processes the input with the following instructions:
```
=You are a content strategist for a YouTube channel in the  niche, specifically in the {{ $('YouTube Category Detection Agent').item.json.output.category }} category.

**Target Audience:** 

{{ JSON.stringify($('Audience Persona Agent').item.json || {}) }}


**Market Intelligence:** 

{{ JSON.stringify($('Data Intelligence AI Agent').item.json || {}) }}

**Channel URL:** 

{{ $('Client Info Parser').first().json['Channel URL'] }}

Create a comprehensive content strategy including:

1. **Content Pillars**: 3-5 main content categories optimized for this audience
2. **Content Types**: Recommended formats (long-form, shorts, tutorials, etc.) for each pillar
3. **Publishing Schedule**: Optimal upload frequency and timing based on audience behavior
... [truncated]
```

### 16. SEO Package Agent
AI agent processes the input with the following instructions:
```
=You are a YouTube SEO specialist. Create a complete SEO package for this video:

**Script Content:** {{ JSON.stringify($('Script Writer Agent').item.json || {}) }}

**Category:** {{ JSON.parse($('YouTube Category Detection Agent').item.json.text || '{}').category || 'general' }}

**Niche:** {{ $('YouTube Category Detection Agent').item.json.output.category }}

**Market Intelligence:** {{ JSON.stringify($('Data Intelligence AI Agent').item.json || {}) }}

Generate a comprehensive SEO package:

1. **Video Title** (60 chars max): Compelling, keyword-optimized title
2. **Description** (5000 chars max): Detailed description with timestamps and keywords
3. **Tags** (30 tags): Mix of broad and specific keywords
4. **Hashtags** (3-5): Strategic hashtags for discoverability
5. **Thumbnail Text**: Text overlay suggestions for thumbnails
6. **End Screen Elements**: Suggested videos and subscribe prompts
7. **Community Post**: Pre-launch community engagement post
8. **SEO Keywords**: Primary and secondary keyword targets
... [truncated]
```

### 17. Data Validator & Parser
Data is normalized/transformed for the next step.

### 18. Compose Client Delivery Email
Data is normalized/transformed for the next step.

### 19. Slack Team Notification
[Describe what this step does]

### 20. On form submission
Workflow is triggered via form.

### 21. Send a message
[Describe what this step does]

### 22. Run an Actor
[Describe what this step does]

### 23. Get dataset items
[Describe what this step does]

### 24. If
[Describe what this step does]

### 25. Code
[Describe what this step does]

### 26. OpenRouter Chat Model
[Describe what this step does]

### 27. Client Research Agent
AI agent processes the input with the following instructions:
```
=You are conducting comprehensive market intelligence research on the client {{ $json.Name }} to inform strategic scriptwriting and content optimization. Your research will directly impact script quality, audience targeting, and content performance. You are only to research {{ $json.Name }} who's channel is {{ $json['Channel URL'] }} and no other people.

RESEARCH TARGET:

Creator Name/Business: {{ $json.Name }}
YouTube Channel URL: {{ $json['Channel URL'] }}
Industry/Niche: {{ $json.Niche }}
Additional Context: {{ $json['Additional Context About Client'] }}

COMPREHENSIVE RESEARCH OBJECTIVES:

1. CREATOR/BUSINESS PROFILE ANALYSIS:

Business Model & Revenue Streams: How do they monetize? (courses, coaching, products, services, affiliate marketing, sponsorships)
Brand Positioning: What unique value proposition do they claim? How do they differentiate from competitors?
Authority Markers: What credentials, achievements, or social proof do they leverage?
Content Philosophy: What's their stated approach to helping their audience?
Business Scale: Team size, revenue indicators, client testimonials, case studies mentioned

2. YOUTUBE CHANNEL DEEP DIVE:
... [truncated]
```

### 28. Merge
[Describe what this step does]

### 29. Simple Memory
[Describe what this step does]

### 30. Move file
[Describe what this step does]

### 31. Create folder
[Describe what this step does]

### 32. If2
[Describe what this step does]

### 33. Script Improver Agent
AI agent processes the input with the following instructions:
```
=You are an elite YouTube Script Optimization Specialist with mastery of viral content psychology, retention engineering, and audience engagement. Your expertise is built on analyzing and implementing improvements from thousands of high-performing scripts across all major YouTube categories. You specialize in taking quality review feedback and transforming it into compelling, binge-worthy content that maximizes viewer satisfaction and platform performance.

CORE EXPERTISE & SPECIALIZATIONS
Script Transformation Mastery
Quality Review Integration: Expert at interpreting feedback and implementing specific improvements without losing original voice
Retention Engineering: Advanced knowledge of the 30-second rule, payoff distribution, and re-hooking techniques
Psychological Optimization: Deep understanding of expectation vs reality management and curiosity gap creation
Voice Preservation: Ability to maintain creator's authentic tone while optimizing for performance
Advanced Scriptwriting Principles
The Build × Tension Formula Implementation:

Every line must either build toward the main payoff or create tension to maintain engagement
Strategic open loop placement and resolution timing
Conflict-driven narrative progression using "but/therefore" instead of "and then"
Emotional surfing across the full spectrum of human emotions
Hook Optimization Mastery:

Eliminate the four fatal hook mistakes: Delay, Confusion, Irrelevance, Disinterest
Achieve topic clarity + on-target curiosity within 5 seconds
Perfect click confirmation that exceeds title/thumbnail expectations
... [truncated]
```

### 34. OpenRouter Chat Model1
[Describe what this step does]

### 35. Markdown Converter
AI agent processes the input with the following instructions:
```
=Convert this text to formatted markdown text and structure it with appropriate headings, subheadings, bold text, line breaks, and overall professional formatting for a Google Doc. ONLY OUTPUT THE MARKDOWN, NOTHING ELSE:

CLIENT NAME: {{ $json.client_name }}
CLIENT EMAIL: {{ $json.client_email }}
TIMESTAMP: {{ $json.processing_timestamp }}

YOUTUBE SCRIPT:
{{ $json.script_content }}

SEO PACKAGE:
{{ $json.seo_package }}

```

### 36. OpenRouter Chat Model2
[Describe what this step does]

### 37. If1
[Describe what this step does]

### 38. Get a document
[Describe what this step does]

### 39. Search For Client Folder
[Describe what this step does]

### 40. Find Last Created YouTube Script
[Describe what this step does]

### 41. Create Formatted Google Doc
[Describe what this step does]

### 42. Search For Client
[Describe what this step does]

### 43. Move Script to Existing Client Folder
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

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_content_strategy.md](../skills/SKILL_BIBLE_hormozi_content_strategy.md)**
- 30-day content strategy framework
- YouTube content optimization
- Audience retention tactics

**[SKILL_BIBLE_hormozi_persuasion_speaking.md](../skills/SKILL_BIBLE_hormozi_persuasion_speaking.md)**
- Speak so well people give you money
- Hook and attention formulas
- Script delivery optimization

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- 14 years of marketing advice
- Content marketing principles
- Audience building strategies

**[SKILL_BIBLE_youtube_lead_generation.md](../skills/SKILL_BIBLE_youtube_lead_generation.md)**
- YouTube as lead generation tool
- Content-to-conversion frameworks
- Channel growth tactics

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Content Marketing Agency/YouTube Script Creator.json`
Generated on: 2026-01-02