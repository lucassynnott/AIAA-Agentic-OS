#!/usr/bin/env python3
"""
AIAA Agentic OS Dashboard - Complete Management System v2.3

Features:
- Password-protected authentication
- Light/Dark mode toggle with localStorage persistence
- 138 workflows with comprehensive documentation
- Environment variable management (view AND set)
- Webhook endpoint monitoring
- Real-time logs and event tracking
- Mobile-responsive design
"""

import os
import json
import hashlib
import secrets
import re
from datetime import datetime
from functools import wraps
from collections import deque
import threading

from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
from markupsafe import Markup
import requests as http_requests  # Renamed to avoid conflict with flask.request

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))

# =============================================================================
# Configuration
# =============================================================================

DASHBOARD_USERNAME = os.getenv("DASHBOARD_USERNAME", "admin")
DASHBOARD_PASSWORD_HASH = os.getenv("DASHBOARD_PASSWORD_HASH", "")

TRACKED_ENV_VARS = [
    "OPENROUTER_API_KEY",
    "PERPLEXITY_API_KEY",
    "SLACK_WEBHOOK_URL",
    "CALENDLY_API_KEY",
    "GOOGLE_OAUTH_TOKEN_JSON",
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "FAL_KEY",
    "RAILWAY_API_TOKEN",
]

# Railway API configuration
RAILWAY_API_TOKEN = os.getenv("RAILWAY_API_TOKEN", "")
RAILWAY_API_URL = "https://backboard.railway.app/graphql/v2"

events_log = deque(maxlen=500)
events_lock = threading.Lock()
RUNTIME_ENV_VARS = {}

# =============================================================================
# Simple Markdown to HTML Converter
# =============================================================================

def markdown_to_html(text):
    """Convert markdown to HTML with proper formatting."""
    if not text:
        return ""
    
    # Escape HTML first
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # Code blocks (``` ... ```)
    text = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', text, flags=re.DOTALL)
    
    # Inline code (`code`)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Headers
    text = re.sub(r'^### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Lists - unordered
    lines = text.split('\n')
    in_list = False
    result = []
    for line in lines:
        if re.match(r'^- ', line):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append('<li>' + line[2:] + '</li>')
        elif re.match(r'^\d+\. ', line):
            if not in_list:
                result.append('<ol>')
                in_list = 'ol'
            result.append('<li>' + re.sub(r'^\d+\. ', '', line) + '</li>')
        else:
            if in_list:
                result.append('</ul>' if in_list == True else '</ol>')
                in_list = False
            result.append(line)
    if in_list:
        result.append('</ul>' if in_list == True else '</ol>')
    text = '\n'.join(result)
    
    # Tables
    text = re.sub(r'\|(.+)\|', lambda m: '<tr>' + ''.join(f'<td>{c.strip()}</td>' for c in m.group(1).split('|')) + '</tr>', text)
    text = re.sub(r'(<tr>.*?</tr>\n?)+', r'<table class="md-table">\g<0></table>', text)
    
    # Paragraphs
    text = re.sub(r'\n\n+', '</p><p>', text)
    text = '<p>' + text + '</p>'
    
    # Clean up
    text = text.replace('<p></p>', '').replace('<p><h', '<h').replace('</h2></p>', '</h2>')
    text = text.replace('</h3></p>', '</h3>').replace('</h4></p>', '</h4>')
    text = text.replace('<p><ul>', '<ul>').replace('</ul></p>', '</ul>')
    text = text.replace('<p><ol>', '<ol>').replace('</ol></p>', '</ol>')
    text = text.replace('<p><pre>', '<pre>').replace('</pre></p>', '</pre>')
    text = text.replace('<p><table', '<table').replace('</table></p>', '</table>')
    
    return Markup(text)

# =============================================================================
# Workflow Registry with Comprehensive Descriptions (v2.3 - 138 Workflows)
# =============================================================================

WORKFLOWS = {
    "ab_test_analyzer": {
        "description": "Analyze A/B test results with statistical significance and clear recommendations",
        "has_script": True,
        "category": "Research",
        "full_description": """## Overview
Analyzes A/B test results, calculates statistical significance, and generates clear recommendations on whether to implement the variant.

## Prerequisites
- `OPENAI_API_KEY` (optional for AI insights)
- scipy, numpy installed

## How to Run
```bash
python3 execution/generate_ab_test_analysis.py \\
  --control '{"visitors": 5000, "conversions": 250}' \\
  --variant '{"visitors": 5000, "conversions": 325}' \\
  --test_name "Homepage CTA"
```

## Process
1. Input control vs variant data
2. Calculate conversion rates and lift
3. Perform statistical significance tests (chi-square, t-test)
4. Generate confidence level and p-value
5. Output recommendation with projected impact

## Decision Framework
| Confidence | Lift | Decision |
|------------|------|----------|
| >95% | >10% | Implement |
| >95% | <10% | Consider |
| <95% | Any | Continue testing |

## Cost
~$0.02 per analysis""",
        "inputs": ["control_data", "variant_data", "test_name", "confidence_target"],
        "outputs": ["Statistical analysis", "Recommendation", "Projected impact"]
    },
    
    "ad_creative_generator": {
        "description": "Generate ad creative concepts with copy, headlines, and AI-generated images via fal.ai",
        "has_script": True,
        "category": "Paid Advertising",
        "full_description": """## Overview
Generates ad copy and creative concepts for Meta, Google, and LinkedIn ads with multiple variations for A/B testing. Uses fal.ai Nano Banana Pro for image generation.

## Prerequisites
- `OPENAI_API_KEY` - For ad copy generation
- `FAL_KEY` - For AI image generation

## How to Run
```bash
python3 execution/generate_ad_creative.py \\
  --product "[PRODUCT]" \\
  --audience "[AUDIENCE]" \\
  --platform meta \\
  --type image \\
  --variations 5
```

## Ad Copy Formulas
- **Problem-Solution**: "Tired of [problem]? [Product] helps you [solution]."
- **Social Proof**: "Join [X] companies who [benefit] with [product]."
- **Curiosity**: "The secret to [result] that [audience] are using."

## Platform Formats
- **Meta**: 125 char primary + 40 char headline + 30 char description
- **Google Search**: 3x30 char headlines + 2x90 char descriptions
- **LinkedIn**: 150 char intro + 70 char headline

## Cost
~$0.05-0.10 per ad set (copy) + ~$0.04/image""",
        "inputs": ["product", "audience", "platform", "ad_type", "variations"],
        "outputs": ["Ad copy variations", "Headlines", "Image prompts", "CTA recommendations"]
    },
    
    "ai_cold_email_personalizer": {
        "description": "Personalize cold emails at scale using AI research on each prospect",
        "has_script": True,
        "category": "Sales Outreach",
        "full_description": """## Overview
Uses AI to research each prospect and generate hyper-personalized email openers that significantly increase response rates.

## Prerequisites
- `OPENAI_API_KEY` - For AI generation
- `PERPLEXITY_API_KEY` - For web research
- `GOOGLE_APPLICATION_CREDENTIALS` - For Sheets

## How to Run
```bash
# Step 1: Research prospects
python3 execution/research_prospect.py "[SHEET_URL]" -o .tmp/research.json

# Step 2: Generate personalized lines
python3 execution/personalize_emails_ai.py .tmp/research.json \\
  --service "your service" --value_prop "key benefit"

# Step 3: Update sheet
python3 execution/update_sheet.py .tmp/personalized.json "[SHEET_URL]"
```

## First Line Patterns
- **Recent Achievement**: "Congrats on the Series A..."
- **Content Reference**: "Your LinkedIn post about X hit home..."
- **Company Observation**: "Noticed you're hiring 3 SDRs..."

## Personalization Levels
- Light ($0.01/lead): Company website scan
- Medium ($0.03/lead): Company + LinkedIn profile
- Deep ($0.10/lead): Full prospect research

## Quality Control
- Specific (not generic)
- Accurate (fact-checkable)
- Concise (<25 words)""",
        "inputs": ["lead_list_sheet", "service", "value_proposition"],
        "outputs": ["Personalized first lines", "Pain points", "Research notes"]
    },
    
    "ai_customer_onboarding_agent": {
        "description": "Automated customer onboarding with Slack channels, Google Drive, and CRM tasks",
        "has_script": True,
        "category": "Client Management",
        "full_description": """## Overview
Automates new client onboarding by creating Slack channels, Google Drive folders, CRM contacts, and tasks from form submission.

## Prerequisites
- `OPENROUTER_API_KEY` - For AI processing
- `SLACK_BOT_TOKEN` - For Slack integration
- `GOOGLE_APPLICATION_CREDENTIALS` - For Drive

## How to Run
```bash
python3 execution/onboard_client.py \\
  --name "John Smith" \\
  --email "john@company.com" \\
  --company "Company Inc" \\
  --website "https://company.com" \\
  --proposal "[PATH_TO_FILE]"
```

## Process
1. Receive onboarding form submission
2. Create Slack channel and post welcome
3. Create client folder in Google Drive
4. Extract tasks from proposal document with AI
5. Create tasks in project management
6. Send welcome email

## Integrations
- Slack (channels, messages)
- Google Drive (folders)
- CRM (contact creation)
- Task management""",
        "inputs": ["client_name", "email", "company", "website", "proposal"],
        "outputs": ["Slack channel", "Drive folder", "CRM contact", "Onboarding tasks"]
    },
    
    "ai_image_generator": {
        "description": "Generate images using AI models like DALL-E or fal.ai for content and ads",
        "has_script": True,
        "category": "Creative",
        "full_description": """## Overview
Generates custom images using DALL-E or fal.ai for use in content, ads, and social media.

## Prerequisites
- `OPENAI_API_KEY` - For DALL-E
- `FAL_KEY` - For fal.ai models

## How to Run
```bash
python3 execution/generate_image_prompt.py \\
  --concept "Professional businessman smiling" \\
  --style photorealistic \\
  --platform midjourney \\
  --variations 4
```

## Style Options
- Photorealistic
- Digital illustration
- 3D render
- Watercolor
- Minimalist
- Anime/cartoon

## Prompt Best Practices
`[Subject], [Style], [Lighting], [Composition], [Details]`

## Cost
- DALL-E: ~$0.04/image
- fal.ai Nano Banana Pro: ~$0.02/image""",
        "inputs": ["prompt", "style", "size", "quantity"],
        "outputs": ["Generated images", "Image URLs"]
    },
    
    "ai_landing_page_generator": {
        "description": "Generate complete landing pages with PROPS formula and 5 design styles",
        "has_script": True,
        "category": "Content Generation",
        "full_description": """## Overview
Generate high-converting landing pages using the **PROPS formula** (Problem, Result, Offer, Proof, Scarcity). Creates complete HTML/CSS pages with modern design, responsive layouts, and conversion-optimized copy.

## Prerequisites
- `OPENROUTER_API_KEY` or `ANTHROPIC_API_KEY`
- `PERPLEXITY_API_KEY` (optional for research)

## How to Run
```bash
python3 execution/generate_landing_page.py \\
  --product "AI Course" \\
  --audience "Agency owners" \\
  --benefit "10x productivity" \\
  --price "$997" \\
  --style neo_noir
```

## PROPS Formula
- **P**roblem Amplification (3-layer deep)
- **R**esult Demonstration (Real, Relatable, Reachable)
- **O**bjection Removal (Time, Money, Past failure)
- **P**roof Stacking (Data → Testimonials → Case study)
- **S**imple Next Step (Single CTA)

## 5 Design Styles
1. **Neo Noir** - Dark dramatic, cinematic
2. **Editorial Luxury** - Elegant, high-ticket
3. **Electric Tech** - Futuristic, SaaS
4. **Warm Organic** - Wellness, coaching
5. **Neubrutalism** - Bold, raw, startups

## Quality Gates
- Headlines under 10 words
- Mobile responsive (375px, 768px, 1024px)
- Unique mechanism named and differentiated

## Cost
~$0.06-0.20 per landing page""",
        "inputs": ["product_name", "target_audience", "main_benefit", "price", "design_style"],
        "outputs": ["Complete landing page HTML", "Mobile-responsive CSS", "Live Cloudflare URL"]
    },
    
    "calendly_meeting_prep": {
        "description": "Auto-research prospects when meetings are booked via Calendly webhook",
        "has_script": True,
        "category": "Sales Automation",
        "full_description": """## Overview
Automatically research prospects the moment they book a meeting on Calendly. Get instant Slack alerts, deep company research, personalized talking points, and a formatted Google Doc.

## Step-by-Step Process

### Step 1: Webhook Reception
- Calendly fires webhook on `invitee.created` event
- Extract prospect name, email, company from payload
- Send immediate Slack alert with meeting details

### Step 2: Company Research (Perplexity AI)
Research includes:
- What the company does
- Company size and target market
- Recent news and developments
- Products/services offered
- Key competitors

### Step 3: Prospect Research (Perplexity AI)
Research includes:
- Role and job responsibilities
- Professional background
- LinkedIn activity and content
- Relevant expertise areas

### Step 4: Generate Talking Points (Claude)
AI generates:
- 5 personalized talking points based on research
- 3 thoughtful questions to ask
- Potential pain points to address
- Connection points between your offer and their needs
- Meeting goals and strategy

### Step 5: Create Google Doc
Formatted document includes:
- Executive Summary (3-4 sentences)
- Company Research section
- Prospect Research section
- Talking Points & Questions
- Meeting Details

### Step 6: Send Summary to Slack
Brief summary with:
- Company overview
- Key talking points
- Link to full Google Doc

## Quality Gates
- Slack alert sends within seconds of booking
- Company name extracted correctly
- Research returns relevant, current data
- Google Doc formatted properly

## Integration Requirements
- Calendly API (webhook subscription)
- Perplexity API (research)
- OpenRouter/Claude (talking points)
- Google OAuth (Docs creation)
- Slack Webhook (notifications)""",
        "inputs": ["Calendly webhook (automatic)"],
        "outputs": ["Instant Slack alert", "Company research", "Prospect research", "Talking points", "Google Doc"]
    },
    
    "cold_email_scriptwriter": {
        "description": "Generate personalized cold email sequences with A/B variants using proven frameworks",
        "has_script": True,
        "category": "Sales Outreach",
        "full_description": """## Overview
Generate personalized cold email sequences with A/B variants using AI research and proven copywriting frameworks like AIDA, PAS, and BAB.

## Step-by-Step Process

### Step 1: Process Lead List
- Upload CSV with prospect information
- Normalize and validate data
- Extract key fields (name, title, company, email)

### Step 2: Prospect Research Agent
For each prospect, research via Perplexity:
- Pain points specific to their industry/role
- Business priorities and challenges
- Conversation starters (recent news, content)
- Likely objections
- Best timing context
- Personalization angles

### Step 3: First Line Writer
Generate hyper-personalized first lines:
- Reference specific research insights
- Mention recent company news or achievements
- Connect to their posted content
- Show genuine understanding of their situation

### Step 4: Email Sequence Generator
Create 5-7 email sequence using proven patterns:

**Pattern A: Problem + Social Proof + Soft Ask**
1. Opening: Direct acknowledgment of their situation
2. Social Proof: Concrete result from similar company
3. Bridge: How you achieve this outcome
4. CTA: Low-commitment question

**Pattern B: Observation + Value + Permission**
1. Opening: Specific observation about their business
2. Value Tease: "I found X opportunities"
3. Permission: "Mind if I send over?"

### Step 5: A/B Variant Generator
Create 3 variants for split testing:
- **Variant A**: Before/After/Bridge framework
- **Variant B**: Curiosity hook approach
- **Variant C**: Direct problem/solution

### Step 6: Export to Google Sheet
Organized columns:
- Prospect info
- Research insights
- First line options
- Full email sequence
- A/B variants
- Subject line options

## Email Sequence Structure
- **Email 1**: Value-first introduction
- **Email 2**: Social proof + case study
- **Email 3**: Different angle/hook
- **Email 4**: Break-up / last chance
- **Email 5-7**: Nurture sequence

## Quality Gates
- Personalization verified (no generic openers)
- Each email under 150 words
- Clear CTA in every email
- Subject lines A/B testable""",
        "inputs": ["lead_list_csv", "sender_name", "product", "value_proposition"],
        "outputs": ["5-7 email sequence", "A/B variants", "Subject lines", "Google Sheet"]
    },
    
    "vsl_funnel_orchestrator": {
        "description": "Master orchestrator for complete VSL funnel creation pipeline",
        "has_script": True,
        "category": "Funnel Building",
        "full_description": """## Overview
**Master orchestrator** that coordinates the complete VSL funnel creation pipeline. Single entry point that triggers all sub-workflows in sequence, manages data flow, handles errors, and delivers final outputs.

## Step-by-Step Process

### Step 1: Validate Inputs
- Verify company name provided
- Validate website URL is accessible
- Confirm offer description is clear
- Check all API keys configured

### Step 2: Market Research (Workflow #1)
Trigger `company_market_research` workflow:
- Company background, funding, team
- Products and pricing analysis
- Target audience pain points
- Competitor landscape
- Social proof extraction

**Checkpoint:** Save to `.tmp/vsl_funnel_{company}/01_research.json`

### Step 3: VSL Script Writer (Workflow #2)
Trigger `vsl_script_writer` workflow:

**Script Structure (10 Parts):**
1. Pattern interrupt hook (30 sec)
2. Big promise and credibility (2 min)
3. Problem agitation (5 min)
4. Solution reveal (3 min)
5. Mechanism explanation (5 min)
6. Proof and testimonials (5 min)
7. Offer presentation (5 min)
8. Bonuses and stack (3 min)
9. Guarantee (2 min)
10. Urgency and close (3 min)

**Checkpoint:** Save to `.tmp/vsl_funnel_{company}/02_vsl_script.md`

### Step 4: Sales Page Writer (Workflow #3)
Trigger `vsl_sales_page_writer` workflow:
- Generate headline variations (3)
- Write benefit bullets matching VSL
- Create testimonials section
- Build offer stack
- Add FAQ addressing objections

**Checkpoint:** Save to `.tmp/vsl_funnel_{company}/03_sales_page.md`

### Step 5: Email Sequence Writer (Workflow #4)
Trigger `vsl_email_sequence_writer` workflow:
- 7-email follow-up sequence
- Each email has 2 subject line options
- Progression: value → urgency
- Clear CTAs throughout

**Checkpoint:** Save to `.tmp/vsl_funnel_{company}/04_email_sequence.md`

### Step 6: Google Doc Creation (Workflow #5)
Create 4 Google Docs in parallel:
- Market Research document
- VSL Script document
- Sales Page Copy document
- Email Sequence document

### Step 7: Slack Notification (Workflow #6)
Send completion message with:
- All 4 document links
- Execution time
- VSL estimated length
- Any warnings or notes

## Error Handling Strategy
- Research fails → Retry once → Fail workflow
- VSL generation fails → Retry with adjusted params
- Google Docs fails → Save local files → Continue
- Slack fails → Log error → Workflow still succeeds

## Quality Gates
- All 6 sub-workflows completed
- 4 Google Docs created
- Slack notification sent
- Execution time < 10 minutes""",
        "inputs": ["company", "website", "offer", "price", "target_audience"],
        "outputs": ["Market research doc", "VSL script doc", "Sales page doc", "Email sequence doc"]
    },
    
    "company_market_research": {
        "description": "Deep company and market research via Perplexity AI for VSL funnels",
        "has_script": True,
        "category": "Research",
        "full_description": """## Overview
Conduct comprehensive market research on any company and their offer using Perplexity AI to gather intelligence for VSL funnel creation, positioning strategy, and competitive analysis.

## Step-by-Step Process

### Step 1: Company Overview Research
Perplexity query for:
- Company overview and mission
- Core products/services
- Target market and ideal customers
- Company size and stage
- Recent news or announcements
- Social media presence

### Step 2: Offer Analysis
Research the specific offer:
- How the offer works (mechanism)
- Key features and benefits
- Pricing structure
- Customer results or case studies
- Unique selling propositions
- Common objections

### Step 3: Target Audience Research
Deep dive into audience:
- Demographic profile (titles, company size)
- Primary pain points and challenges
- Current solutions they're using
- Buying triggers and motivations
- Common objections to similar offers
- Language and terminology they use

### Step 4: Competitive Landscape
Analyze competitors:
- Top 3-5 direct competitors
- How they position their offers
- Pricing comparison
- Strengths and weaknesses
- Market gaps and opportunities

### Step 5: Social Proof & Results
Find validation:
- Quantifiable results (revenue, leads, ROI)
- Customer success stories
- Reviews and ratings
- Industry recognition or awards
- Media mentions or features

### Step 6: Synthesis
Combine all research into:
- Executive summary
- Company & offer overview
- Target audience profile
- Unique mechanism identification
- Transformation promise
- Social proof library
- Recommended messaging angles

## Output Structure
```json
{
  "company": { "name", "overview", "size", "industry" },
  "offer": { "name", "mechanism", "price", "features" },
  "targetAudience": { "demographics", "painPoints", "desires" },
  "transformation": { "before", "after", "mechanism" },
  "socialProof": { "results", "testimonials", "caseStudies" },
  "competitors": [ { "name", "positioning", "price" } ],
  "messaging": { "hooks", "angles", "objections" }
}
```

## Quality Gates
- All 5 research sections completed
- Minimum 500 words per section
- At least 3 pain points identified
- At least 1 unique mechanism found
- At least 3 social proof elements""",
        "inputs": ["company", "website", "offer", "industry"],
        "outputs": ["Research dossier JSON", "Markdown report", "Messaging recommendations"]
    },
    
    "ultimate_meta_ads_campaign": {
        "description": "Complete Meta/Facebook/Instagram ads campaign from creative to structure",
        "has_script": True,
        "category": "Paid Advertising",
        "full_description": """## Overview
Complete Meta advertising campaign system from creative generation to campaign structure. Produces ad copy, creative briefs, audience targeting, campaign architecture, and optimization playbook.

## Step-by-Step Process

### Phase 1: Competitive Research
- Scrape Facebook Ad Library for competitor ads
- Analyze ad copy patterns and hooks
- Identify winning creative formats
- Document audience targeting insights

### Phase 2: Audience Strategy
**Cold Audiences:**
- Interest targeting (detailed)
- Lookalike audiences (1%, 2%, 5%)
- Broad targeting with creative filtering

**Warm Audiences:**
- Website visitors (30/60/90 days)
- Video viewers (25%, 50%, 75%)
- Engagement audiences

**Hot Audiences:**
- Cart abandoners
- Past purchasers
- High-intent page visitors

### Phase 3: Ad Copy Generation
**Primary Text (5 variations):**
- Hook-focused (pattern interrupt)
- Problem-focused (pain point)
- Solution-focused (outcome)
- Story-focused (testimonial)
- FOMO-focused (urgency)

**Headlines (5 variations):**
- Benefit-driven
- Curiosity-driven
- Number-driven
- Question-driven
- Command-driven

### Phase 4: Creative Briefs
**Static Images:**
- Hero product shot
- Before/after comparison
- Testimonial quote card
- Feature highlight
- Social proof collage

**Video Concepts:**
- UGC-style testimonial
- Product demo
- Problem/solution narrative
- Founder story

### Phase 5: Campaign Structure
```
Campaign: [Client] - [Objective] - [Stage]
├── Ad Set: Cold - Interest Targeting
│   ├── Ad: Hook v1 - Image A
│   └── Ad: Hook v2 - Video A
├── Ad Set: Cold - Lookalike 1%
│   └── Ad: Problem v1 - Image B
└── Ad Set: Warm - Retargeting
    └── Ad: Testimonial v1
```

### Phase 6: Optimization Playbook
**Day 1-3:** Learning phase, don't touch
**Day 4-7:** Kill <1% CTR ads, scale winners
**Week 2+:** Duplicate winners, increase budgets 20%

## Performance Benchmarks
| Metric | Cold | Warm | Hot |
|--------|------|------|-----|
| CTR | 1%+ | 2%+ | 3%+ |
| CPC | <$2 | <$1.50 | <$1 |
| ROAS | 1.5x+ | 3x+ | 5x+ |""",
        "inputs": ["client", "product", "offer", "target_audience", "monthly_budget", "objective"],
        "outputs": ["Campaign structure", "Ad copy variations", "Creative briefs", "Audience targeting", "Optimization playbook"]
    },
    
    "youtube_knowledge_miner": {
        "description": "Extract knowledge from YouTube videos into structured skill bibles",
        "has_script": True,
        "category": "Research",
        "full_description": """## Overview
Automated system that extracts best practices and how-to knowledge from top YouTube channels in any niche, converts video content into structured manuals, and generates comprehensive skill bibles.

## Step-by-Step Process

### Step 1: Channel Discovery
- Search YouTube Data API for authority channels
- Filter by subscriber count (min 5,000)
- Filter by video count and consistency
- Rank by authority metrics

### Step 2: Video Selection
- Get uploads playlist for each channel
- Filter by view count (min 5,000)
- Filter by duration (min 5 minutes)
- Select top-performing educational content

### Step 3: Transcript Retrieval
Fallback chain:
1. Supadata API (fast, reliable)
2. TranscriptAPI (secondary)
3. youtube-transcript-api (free fallback)

### Step 4: Manual Generation
Send transcript to Claude/Gemini for:
- Executive Summary
- Key Concepts
- Step-by-Step Process
- Best Practices
- Common Mistakes
- Tools/Resources Mentioned
- Actionable Takeaways
- Skill Rating (1-10)

### Step 5: Quality Filtering
- AI rates each manual 1-10
- Filter by minimum rating (default: 7)
- Rank by automation potential

### Step 6: Skill Bible Synthesis
- Combine multiple high-quality manuals
- Generate comprehensive skill bible
- Save to skills/ directory

## Output Structure
```
.tmp/knowledge_mine/
├── channels.json
├── videos.json
├── manuals/
│   ├── video_title_1.md
│   └── video_title_2.md
├── manuals_index.json
└── SKILL_BIBLE_*.md
```

## Cost Estimates
| Component | Cost |
|-----------|------|
| YouTube Data API | Free (10K/day) |
| Supadata transcript | ~$0.01/video |
| Claude processing | ~$0.03/video |
| **50 videos total** | **~$2.00** |""",
        "inputs": ["niche_keywords", "max_channels", "videos_per_channel", "min_skill_rating"],
        "outputs": ["Channel list", "Video metadata", "Individual manuals", "Synthesized skill bible"]
    },
    
    "generate_content_calendar": {
        "description": "Generate complete content calendars with topics, hooks, and schedules",
        "has_script": True,
        "category": "Content Marketing",
        "full_description": """## Overview
Generate complete content calendars with topics, platform-specific hooks, and optimal posting schedules. Output to Google Sheets for team collaboration.

## Step-by-Step Process

### Step 1: Define Content Strategy
Gather from user:
- Unique angle/expertise
- Past high-performing content
- Goals (leads, brand, thought leadership)
- Topics to cover or avoid

### Step 2: Generate Topic Ideas
For each content pillar:
- 10 educational topics (how-to, tips, frameworks)
- 5 story-based topics (case studies, lessons)
- 5 contrarian takes (myths, unpopular opinions)
- 5 engagement topics (questions, polls)

### Step 3: Create Platform-Specific Hooks

**Twitter/X Format:**
- Hook (first line stops scroll)
- Thread outline (5-7 points)
- CTA

**LinkedIn Format:**
- Hook (pattern interrupt)
- Story/insight structure
- Engagement question

**YouTube Format:**
- Title options (3)
- Thumbnail concept
- Video outline

### Step 4: Build Calendar Structure
Google Sheet tabs:
- **Overview**: Monthly view with content mix
- **Twitter**: Daily posts with hooks
- **LinkedIn**: 3-5 posts/week
- **YouTube**: Weekly video topics

### Step 5: Schedule Distribution
Based on:
- Optimal posting times per platform
- Content variety (no same pillar back-to-back)
- Key dates/events in industry

### Step 6: Export to Sheet
Columns include date, pillar, topic, hook, full content, status.

## Content Mix (per week)
- 40% Educational (tips, how-to)
- 25% Story/Case Study
- 20% Engagement (questions, polls)
- 15% Promotional

## Hook Patterns
1. "Stop [common advice]. Here's what actually works:"
2. "I went from [bad] to [good] in [time]. Here's how:"
3. "[Number] [things] that [benefit]:"
4. "Why do most [people] fail at [thing]?"
5. "[Bold claim]. Let me explain:"

## Quality Gates
- All platforms have content assigned
- Hooks pass scroll-stopping test
- No content pillar repeated consecutively""",
        "inputs": ["content_pillars", "platforms", "weeks", "posting_frequency"],
        "outputs": ["Google Sheet calendar", "Topic ideas", "Platform-specific hooks"]
    },
    
    "blog_post_writer": {
        "description": "Generate SEO-optimized long-form blog posts with proper structure",
        "has_script": True,
        "category": "Content Generation",
        "full_description": """## Overview
Generate long-form, SEO-optimized blog posts with proper keyword targeting, structure, and CTAs ready for publication.

## Step-by-Step Process

### Step 1: Keyword Research (Optional)
Research includes:
- Search volume
- Keyword difficulty
- Related keywords
- Questions people ask
- Competitor content analysis

### Step 2: Generate Outline
AI creates structure:
- H1 with primary keyword
- H2s with secondary keywords
- H3s for subsections
- FAQ section topics

### Step 3: Write Article
Using proven structure:
```markdown
# [H1: Primary Keyword in Title]

[Hook paragraph - address reader's problem]

**In this guide, you'll learn:**
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

## [H2: What is X?]
[Definition and context]

## [H2: Why X Matters]
[Pain points and benefits]

## [H2: How to X (Step-by-Step)]
### Step 1: [Action]
### Step 2: [Action]

## [H2: Common Mistakes]
[List with explanations]

## [H2: Expert Tips]
[Advanced insights]

## [H2: FAQ]
### [Question 1]?
[Answer]

## Conclusion
[Summary + CTA]
```

### Step 4: SEO Optimization
Checklist:
- Primary keyword in title, H1, first 100 words
- Secondary keywords in H2s
- Meta description (150-160 chars)
- Internal links (3-5)
- External links (2-3 authoritative)
- Image alt text with keywords

### Step 5: Export
- Full article (Markdown)
- Meta title
- Meta description
- Featured image prompt

## Quality Gates
- Word count meets target (1500/2500/3500)
- All SEO elements present
- Readability score acceptable
- No duplicate content flags

## Cost Estimate
~$0.30-0.50 per 2500-word article""",
        "inputs": ["keyword", "word_count", "tone", "target_audience"],
        "outputs": ["Full article markdown", "Meta title", "Meta description", "Image prompt"]
    },
    
    "case_study_generator": {
        "description": "Generate professional case studies from client results data",
        "has_script": True,
        "category": "Content Generation",
        "full_description": """## Overview
Generate professional case studies from client results data with storytelling, before/after metrics, testimonials, and multiple output formats.

## Step-by-Step Process

### Step 1: Gather Case Study Data
Input structure:
```json
{
  "client": "Acme SaaS",
  "industry": "B2B Software",
  "challenge": "Low reply rates, struggling to book meetings",
  "solution": "AI-personalized cold email sequences",
  "results": {
    "reply_rate": {"before": "2%", "after": "12%"},
    "meetings_booked": {"before": "5/mo", "after": "35/mo"}
  },
  "timeline": "90 days",
  "testimonial": "We 7x'd our meeting rate in 3 months."
}
```

### Step 2: Generate Case Study Structure
```markdown
# How [CLIENT] [ACHIEVED RESULT] in [TIMEFRAME]

## The Challenge
[CLIENT] is a [INDUSTRY] company struggling with [PROBLEM].

**Before working with us:**
- [Pain point 1 with metric]
- [Pain point 2 with metric]

## The Solution
We implemented [SOLUTION]:

### Phase 1: [Step Name]
[Description]

### Phase 2: [Step Name]
[Description]

## The Results
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| [Metric 1] | [X] | [Y] | [+Z%] |

### Key Wins
✅ [Result 1]
✅ [Result 2]

## Client Testimonial
> "[TESTIMONIAL]"
> — [NAME], [TITLE]

## Key Takeaways
1. [Lesson 1]
2. [Lesson 2]
```

### Step 3: Generate Multiple Formats

**Long-Form (Website/PDF):**
Full 800-1500 word case study

**Short-Form (Social):**
3-5 key points with metrics

**One-Liner:**
"We helped [CLIENT] achieve [RESULT] in [TIME]."

**Slide Deck:**
5-7 slides for presentations

### Step 4: Export
- Markdown (blog)
- PDF (downloadable)
- Google Doc (editable)
- Google Slides (presentation)

## Quality Gates
- Specific numbers used (not vague claims)
- Timeline included for credibility
- Client approval obtained
- CTA included at end

## Cost Estimate
~$0.10-0.30 per case study""",
        "inputs": ["client_name", "industry", "challenge", "solution", "results", "testimonial"],
        "outputs": ["Long-form case study", "Social version", "One-liner", "Slide deck"]
    },
    
    "seo_audit_automation": {
        "description": "Automated SEO audits with AI-powered recommendations",
        "has_script": True,
        "category": "SEO",
        "full_description": """## Overview
Crawl a website, analyze technical SEO factors, and generate comprehensive audit report with prioritized fixes and AI-powered recommendations.

## Step-by-Step Process

### Step 1: Crawl Website
Crawl target site up to specified depth:
- Index all pages
- Check response codes
- Map internal links
- Identify resources

### Step 2: Technical SEO Audit

**Site Speed (Core Web Vitals):**
- LCP (Largest Contentful Paint): Target <2.5s
- FID (First Input Delay): Target <100ms
- CLS (Cumulative Layout Shift): Target <0.1

**Crawlability:**
- Pages crawled vs indexable
- Blocked by robots.txt
- Orphan pages
- Crawl depth

**Issues Checked:**
- Broken links (4xx, 5xx)
- Redirect chains
- Missing canonical tags
- Schema markup

### Step 3: On-Page SEO Audit

**Title Tags:**
- Missing titles
- Too long (>60 chars)
- Duplicate titles

**Meta Descriptions:**
- Missing descriptions
- Too short (<120 chars)
- Duplicate descriptions

**Header Structure:**
- Missing H1s
- Multiple H1s
- Improper hierarchy

**Images:**
- Missing alt text
- Oversized images
- Missing lazy loading

### Step 4: Content Analysis
- Thin content pages (<300 words)
- Duplicate content
- Content gaps vs competitors
- Readability scores

### Step 5: Generate Report
```markdown
# SEO Audit Report
**Website:** [URL]
**Overall Score:** [X/100]

## Critical Issues (Fix Immediately)
🔴 [Issue] - [Impact] - [How to Fix]

## Warnings (Address Soon)
🟡 [Issue] - [Impact] - [How to Fix]

## Technical SEO [Score: X/100]
### Core Web Vitals
- LCP: X.Xs ✅/❌
- FID: Xms ✅/❌

### Issues Found
| Issue | Count | Priority |
|-------|-------|----------|
| Broken links | 12 | High |

## Action Plan (Priority Order)
1. [Action] - Impact: High
2. [Action] - Impact: Medium
```

## Quality Gates
- All pages crawled successfully
- Core Web Vitals measured
- Report generated with priorities
- Action plan included

## Cost Estimate
~$0.50-1.00 per audit (APIs + AI)""",
        "inputs": ["website_url", "crawl_depth", "competitors"],
        "outputs": ["Crawl data", "SEO audit report", "Prioritized action plan"]
    },
    
    "deploy_to_modal": {
        "description": "Deploy any workflow directive as a cloud webhook to Modal AI",
        "has_script": True,
        "category": "Deployment",
        "full_description": """## Overview
Deploy any workflow directive as a separate Modal AI app with auto-detected tools and webhook endpoint.

## Step-by-Step Process

### Step 1: Parse Directive
Analyze directive to extract:
- Execution scripts referenced
- Integrations needed (Slack, Google, etc.)
- Input fields required
- Output format expected
- Skill bibles to include

### Step 2: Determine Required Secrets
Based on integrations:
- `anthropic-secret` - Claude API
- `openrouter-secret` - OpenRouter API
- `slack-webhook` - Slack notifications
- `google-token` - Google Docs/Sheets

### Step 3: Generate Modal App
Create Python file with:
- Image definition (packages, files)
- Secrets configuration
- Webhook endpoint
- Health check endpoint
- Info endpoint
- Script execution logic

### Step 4: Deploy to Modal
```bash
modal deploy execution/modal_apps/{directive}_modal.py
```

### Step 5: Return Endpoints
Three endpoints created:
- **Webhook:** POST to trigger workflow
- **Health:** GET for monitoring
- **Info:** GET for workflow metadata

## Example Usage
```bash
# List all deployable workflows
python3 execution/deploy_to_modal.py --list

# Get workflow info
python3 execution/deploy_to_modal.py --info vsl_funnel_writer

# Deploy to Modal
python3 execution/deploy_to_modal.py --directive vsl_funnel_writer

# Test deployed webhook
curl -X POST "https://workspace--app-webhook.modal.run" \\
  -H "Content-Type: application/json" \\
  -d '{"data": {"product": "AI Course"}}'
```

## Quality Gates
- Directive exists and is valid
- Required secrets configured
- Deployment successful
- Webhook responds to requests""",
        "inputs": ["directive_name"],
        "outputs": ["Webhook URL", "Health endpoint", "Info endpoint"]
    },
    
    "deploy_aiaa_dashboard": {
        "description": "Deploy the AIAA Dashboard to Railway with authentication",
        "has_script": True,
        "category": "Deployment",
        "full_description": """## Overview
Deploy the complete AIAA Agentic OS Dashboard to Railway with password authentication, environment variable management, and workflow monitoring.

## Step-by-Step Process

### Step 1: Prerequisites Check
- Verify Railway CLI installed
- Confirm user logged into Railway
- Locate dashboard source files

### Step 2: Project Setup
- Create new Railway project OR link to existing
- Initialize project configuration

### Step 3: Environment Configuration
Set variables:
- `DASHBOARD_USERNAME` - Login username
- `DASHBOARD_PASSWORD_HASH` - SHA-256 hashed password
- `FLASK_SECRET_KEY` - Session encryption key
- API keys from local .env

### Step 4: Deployment
- Upload dashboard app to Railway
- Wait for build completion
- Generate public domain

### Step 5: Verification
- Confirm deployment successful
- Return dashboard URL
- Provide login credentials

## Dashboard Features
- Light/dark mode toggle
- 90+ workflow catalog
- Environment variable management
- Webhook endpoint monitoring
- Real-time event logs
- Claude-style design

## Security
- Passwords hashed with SHA-256
- Secure Flask sessions
- No password recovery (re-deploy required)
- HTTPS only (Railway SSL)

## Quality Gates
- Railway CLI authenticated
- Dashboard deploys successfully
- Public domain generated
- Login works with credentials""",
        "inputs": ["username", "password"],
        "outputs": ["Dashboard URL", "Login credentials"]
    },
}

# Complete workflow documentation for all 138 workflows
# Each workflow has full documentation extracted from directives

# Add comprehensive documentation for remaining workflows
ADDITIONAL_WORKFLOWS = {
    "gmaps_lead_generation": {
        "category": "Lead Generation",
        "description": "Generate B2B leads from Google Maps with deep contact enrichment",
        "has_script": True,
        "full_description": """## Overview
Scrapes Google Maps for local businesses, enriches them with contact info from their websites, and outputs structured leads to Google Sheets.

## Prerequisites
- `APIFY_API_TOKEN` - Google Maps scraping
- `ANTHROPIC_API_KEY` - Contact extraction
- `GOOGLE_APPLICATION_CREDENTIALS` - Sheets export

## How to Run
```bash
# Basic usage - creates new sheet
python3 execution/gmaps_lead_pipeline.py --search "plumbers in Austin TX" --limit 10

# Append to existing sheet
python3 execution/gmaps_lead_pipeline.py --search "dentists in Miami FL" --limit 25 \\
  --sheet-url "[SHEET_URL]"
```

## Process
1. Scrapes Google Maps via Apify
2. Fetches main + contact pages for each business
3. Searches DuckDuckGo for additional contacts
4. Claude extracts structured data (36 fields)
5. Syncs to Google Sheet with deduplication

## Output Fields (36)
Business basics, extracted contacts, social media, owner info, team contacts, metadata

## Cost
~$0.012-0.022 per lead ($1.50-2.50 per 100 leads)""",
        "inputs": ["search_query", "limit", "sheet_url"],
        "outputs": ["Google Sheet with leads", "Contact info", "Social profiles"]
    },
    
    "linkedin_lead_scraper": {
        "category": "Lead Generation", 
        "description": "Scrape LinkedIn profiles and enrich with verified emails for cold outreach",
        "has_script": True,
        "full_description": """## Overview
Automates finding B2B leads on LinkedIn by scraping public profile data based on targeting criteria, then enriching with verified email addresses.

## Prerequisites
- `APIFY_API_TOKEN` - LinkedIn scraping
- `HUNTER_API_KEY` or `APOLLO_API_KEY` - Email enrichment
- `GOOGLE_APPLICATION_CREDENTIALS` - Sheets export

## How to Run
```bash
# Step 1: Scrape LinkedIn
python3 execution/scrape_linkedin_apify.py \\
  --titles "CEO,Founder" \\
  --industries "SaaS" \\
  --locations "United States" \\
  --company_size "11-50" \\
  --max_items 500

# Step 2: Enrich with emails
python3 execution/enrich_emails.py .tmp/linkedin_leads.json --provider hunter

# Step 3: Export to Sheets
python3 execution/update_sheet.py .tmp/enriched_leads.json --title "LinkedIn Leads"
```

## Process
1. Search LinkedIn by job title, industry, location
2. Extract profile data (name, title, company, URL)
3. Enrich with verified emails via Hunter/Apollo
4. Export to Google Sheets

## Cost
~$0.02/profile + ~$0.03/email = ~$25 for 500 leads""",
        "inputs": ["job_titles", "industries", "locations", "company_size", "max_items"],
        "outputs": ["Lead list JSON", "Enriched emails", "Google Sheet"]
    },
    
    "cold_email_mass_personalizer": {
        "category": "Sales Outreach",
        "description": "Personalize thousands of cold emails with AI-researched icebreakers",
        "has_script": True,
        "full_description": """## Overview
Takes a cold email script and lead list CSV, then generates personalized icebreakers for each prospect using AI research.

## Prerequisites
- `OPENROUTER_API_KEY` - AI generation
- `PERPLEXITY_API_KEY` - Prospect research
- `GOOGLE_APPLICATION_CREDENTIALS` - Sheets

## How to Run
```bash
python3 execution/personalize_cold_emails.py \\
  --leads leads.csv \\
  --email_body "Your base email script here..." \\
  --output_sheet "[SHEET_URL]"
```

## Process
1. Process CSV with prospect data
2. Research each prospect (LinkedIn, news)
3. Generate custom icebreaker (8-22 words)
4. Append to email body
5. Output to Google Sheet

## Icebreaker Requirements
- Length: 8-22 words max
- Focus: 100% about them, 0% about you
- Tone: Observational and conversational

## Related Skill Bibles
- SKILL_BIBLE_cold_email_mastery.md
- SKILL_BIBLE_hormozi_email_marketing_complete.md""",
        "inputs": ["lead_csv", "email_body", "sender_name"],
        "outputs": ["Personalized emails", "Google Sheet"]
    },
    
    "newsletter_writer": {
        "category": "Content Marketing",
        "description": "Generate email newsletters with curated content and original commentary",
        "has_script": True,
        "full_description": """## Overview
Generates email newsletters by curating content from RSS feeds, social media, and news sources, formatting with original commentary and CTAs.

## Prerequisites
- `OPENAI_API_KEY` - Content generation
- `CONVERTKIT_API_KEY` or email platform API

## How to Run
```bash
# Step 1: Gather content
python3 execution/gather_newsletter_content.py --topic "cold email" --sources "twitter,linkedin,rss"

# Step 2: Generate newsletter
python3 execution/generate_newsletter.py --content .tmp/content.json --template weekly --tone casual

# Step 3: Send
python3 execution/send_newsletter.py --html .tmp/newsletter.html --list "subscribers"
```

## Newsletter Structure
- Intro with theme
- News section (2-3 items)
- Tip of the week
- Tool spotlight
- Stat that matters
- Action item
- Quick links

## Subject Line Patterns
- "[Topic] Weekly: [Hook]"
- "The [X] thing about [topic] this week"
- "[Number] things you missed in [topic]"
""",
        "inputs": ["topic", "sources", "template", "tone"],
        "outputs": ["Newsletter HTML", "Subject lines", "Send confirmation"]
    },
    
    "vsl_email_sequence_writer": {
        "category": "Funnel Building",
        "description": "Generate 5-7 email nurture sequence for VSL funnel follow-up",
        "has_script": True,
        "full_description": """## Overview
Generates email sequences for VSL funnel viewers who didn't convert. Includes indoctrination, value delivery, objection handling, and urgency.

## Prerequisites
- `OPENROUTER_API_KEY` - AI generation

## Email Sequence Structure
- **Email 1**: "Did you watch?" (immediate follow-up)
- **Email 2**: Indoctrination (your story/credentials)
- **Email 3**: Case study deep dive
- **Email 4**: Mechanism explanation
- **Email 5**: Objection crusher
- **Email 6**: Urgency reminder (spots filling)
- **Email 7**: Last chance (deadline)

## Process
1. Load research, VSL script, sales page copy
2. Extract key elements (mechanism, objections, proof)
3. Generate each email with subject line options
4. Add PS sections with secondary CTAs

## Integration
Position 4/7 in VSL funnel pipeline.

## Related Skill Bibles
- SKILL_BIBLE_sturtevant_email_master_system.md
- SKILL_BIBLE_sturtevant_copywriting.md""",
        "inputs": ["vsl_script", "sales_page_copy", "research_data"],
        "outputs": ["7 email sequence", "Subject line variations", "Send timing"]
    },
    
    "ultimate_webinar_funnel": {
        "category": "Funnel Building",
        "description": "Complete webinar funnel from registration to replay with all assets",
        "has_script": True,
        "full_description": """## Overview
Complete webinar funnel system that generates registration pages, email sequences, webinar scripts, and follow-up campaigns.

## Prerequisites
- `OPENROUTER_API_KEY` - Content generation
- `GOOGLE_APPLICATION_CREDENTIALS` - Docs/Slides

## How to Run
```bash
python3 execution/generate_webinar_funnel.py \\
  --topic "How to Scale Your Agency to $100K/Month" \\
  --presenter "John Smith" \\
  --offer "Agency Accelerator Program" \\
  --price 2997 \\
  --webinar-date "2026-02-15" \\
  --target-audience "Agency owners at $10-30K/month"
```

## Deliverables
1. **Registration Page** - Headline, bullets, about presenter
2. **Pre-Webinar Emails** - Confirmation, reminders
3. **Webinar Script** - 90-min Perfect Webinar format
4. **Slides Outline** - Speaker notes included
5. **Post-Webinar Sequence** - Replay + urgency emails
6. **Replay Page** - Video embed + offer

## Perfect Webinar Structure (90 min)
- Intro (5 min)
- The One Thing (5 min)
- Secret 1-3 (45 min)
- The Stack (10 min)
- The Close (15 min)
- Bonus/Q&A (10 min)""",
        "inputs": ["topic", "presenter", "offer", "price", "webinar_date"],
        "outputs": ["Registration page", "Email sequences", "Webinar script", "Slides", "Replay page"]
    },
    
    "churn_risk_alert": {
        "category": "Client Management",
        "description": "Monitor client engagement and alert on churn risk signals",
        "has_script": True,
        "full_description": """## Overview
Monitors client engagement, payments, and support data to calculate churn risk scores and trigger retention alerts.

## Prerequisites
- `HUBSPOT_API_KEY` or CRM API
- `STRIPE_API_KEY` - Payment data
- `SLACK_WEBHOOK_URL` - Alerts

## How to Run
```bash
# Calculate risk scores
python3 execution/calculate_churn_risk.py --source crm --output .tmp/risk_scores.json

# Send alerts
python3 execution/send_churn_alerts.py --scores .tmp/risk_scores.json --threshold 40
```

## Risk Indicators
**High Risk (+20 pts):** No login 30+ days, missed payment, complaints, negative NPS
**Medium Risk (+10 pts):** Declining usage, slow responses, missed meetings
**Low Risk (+5 pts):** Reduced communication, support tickets increasing

## Risk Classification
| Score | Level | Action |
|-------|-------|--------|
| 60+ | Critical | Immediate intervention |
| 40-59 | High | Proactive outreach |
| 20-39 | Medium | Monitor closely |
| 0-19 | Low | Standard service |

## Automated Actions
- Slack alert to account manager
- Task created in CRM
- Escalation to leadership (if critical)""",
        "inputs": ["client_data", "risk_thresholds"],
        "outputs": ["Risk scores", "Slack alerts", "CRM tasks"]
    },
    
    "client_qbr_generator": {
        "category": "Client Management",
        "description": "Generate quarterly business review slide decks with AI insights",
        "has_script": True,
        "full_description": """## Overview
Generates professional quarterly business review presentations with performance data, AI-generated insights, and strategic recommendations.

## Prerequisites
- `OPENAI_API_KEY` - AI insights
- `GOOGLE_APPLICATION_CREDENTIALS` - Slides
- CRM/Analytics APIs

## How to Run
```bash
# Gather data
python3 execution/gather_qbr_data.py --client "[CLIENT]" --quarter "Q4 2024"

# Generate deck
python3 execution/generate_qbr.py --data .tmp/qbr_data.json --template slides
```

## QBR Slide Structure
1. Title slide
2. Agenda
3. Executive Summary
4. KPI Dashboard (target vs actual)
5-8. Deep Dives (channel breakdowns)
9. Key Wins
10. Challenges & Lessons
11. Next Quarter Priorities
12. Recommendations
13. Q&A

## AI-Generated Insights
- Pattern analysis
- Anomaly detection
- Benchmark comparisons
- Predictive recommendations""",
        "inputs": ["client", "quarter", "data_sources"],
        "outputs": ["QBR slide deck", "Performance data", "Recommendations"]
    },
    
    "carousel_post_creator": {
        "category": "Content Marketing",
        "description": "Generate LinkedIn/Instagram carousel posts with slide content and captions",
        "has_script": True,
        "full_description": """## Overview
Generates complete carousel posts including slide content, design specs, and captions optimized for engagement.

## Prerequisites
- `OPENAI_API_KEY` - Content generation
- `CANVA_API_KEY` (optional) - Design

## How to Run
```bash
python3 execution/generate_carousel.py \\
  --topic "5 Cold Email Mistakes" \\
  --slides 8 \\
  --platform linkedin
```

## Carousel Structure
- **Slide 1**: Hook (bold statement, curiosity)
- **Slides 2-7**: Value (one point per slide, 10-20 words)
- **Slide 8**: Summary (recap key points)
- **Slide 9**: CTA (follow, save, share)

## Design Specs
- Size: 1080x1080 (square) or 1080x1350 (portrait)
- Font: Bold, readable
- Whitespace: Generous margins

## Caption Template
```
[Hook - expand on slide 1]
[Key takeaways in bullets]
Which tip will you try first?
Save this for later
#hashtags
```""",
        "inputs": ["topic", "slides", "platform", "style"],
        "outputs": ["Slide content", "Captions", "Hashtags", "Design specs"]
    },
    
    "ultimate_content_calendar": {
        "category": "Content Marketing",
        "description": "Generate 30-90 days of content across all platforms with hooks and schedules",
        "has_script": True,
        "full_description": """## Overview
Complete content planning system that generates 30-90 days of content ideas, topics, and hooks across all platforms with optimal posting schedules.

## Prerequisites
- `OPENROUTER_API_KEY` - AI generation
- `PERPLEXITY_API_KEY` - Trend research

## How to Run
```bash
python3 execution/generate_content_calendar.py \\
  --client "Acme Corp" \\
  --industry "B2B SaaS" \\
  --platforms "linkedin,twitter,instagram" \\
  --content-pillars "product tips,industry insights,behind the scenes" \\
  --posts-per-week 5 \\
  --days 30
```

## Content Pillar Framework
- Educational (40%): How-to, tips, tutorials
- Social Proof (25%): Case studies, testimonials
- Behind the Scenes (20%): Team, process, culture
- Engagement (15%): Questions, polls, trends

## Platform-Specific Content
- **LinkedIn**: Long-form posts, carousels
- **Twitter/X**: Threads, zingers
- **Instagram**: Carousels, Reels, Stories
- **YouTube**: Scripts, Shorts

## Related Skill Bibles
- SKILL_BIBLE_content_calendar_creation.md
- SKILL_BIBLE_content_strategy_growth.md""",
        "inputs": ["client", "industry", "platforms", "content_pillars", "days"],
        "outputs": ["Content calendar", "Topic ideas", "Platform hooks", "Posting schedule"]
    },
    
    "ai_lead_scorer": {
        "category": "Sales Automation",
        "description": "Score leads using AI based on ICP fit, engagement, and behavior signals",
        "has_script": True,
        "full_description": """## Overview
Uses AI to score and prioritize leads based on Ideal Customer Profile (ICP) fit, engagement signals, and behavior patterns.

## Prerequisites
- `OPENROUTER_API_KEY` - AI scoring
- CRM API access

## Scoring Categories
**Fit Score (0-40):**
- Company size match
- Industry alignment
- Job title seniority
- Technology stack

**Engagement Score (0-30):**
- Email opens/clicks
- Website visits
- Content downloads
- Meeting attendance

**Behavior Score (0-30):**
- Pricing page visits
- Demo requests
- Return visits
- Time on site

## Lead Classification
| Score | Priority | Action |
|-------|----------|--------|
| 80+ | Hot | Immediate outreach |
| 60-79 | Warm | Nurture sequence |
| 40-59 | Cool | Long-term nurture |
| <40 | Cold | Re-evaluate fit |""",
        "inputs": ["lead_data", "icp_criteria", "engagement_data"],
        "outputs": ["Lead scores", "Priority rankings", "Recommended actions"]
    },
    
    "static_ad_generator": {
        "category": "Paid Advertising",
        "description": "Generate static ad creatives with AI images for Meta, Google, LinkedIn",
        "has_script": True,
        "full_description": """## Overview
Generates static ad creatives with AI-generated images and optimized copy for Meta, Google, and LinkedIn ads.

## Prerequisites
- `FAL_KEY` - AI image generation (Nano Banana Pro)
- `OPENAI_API_KEY` - Ad copy

## How to Run
```bash
python3 execution/generate_static_ads.py \\
  --product "[PRODUCT]" \\
  --audience "[AUDIENCE]" \\
  --platform meta \\
  --variations 5
```

## Ad Formats by Platform
**Meta**: 1080x1080, 1200x628, 1080x1920
**Google Display**: 300x250, 728x90, 160x600
**LinkedIn**: 1200x627, 1080x1080

## Creative Styles
- Product hero shot
- Lifestyle imagery
- Before/after
- Text overlay
- Testimonial card

## Cost
~$0.04/image (fal.ai Nano Banana Pro)""",
        "inputs": ["product", "audience", "platform", "variations"],
        "outputs": ["Ad images", "Ad copy", "Headlines", "CTAs"]
    },
    
    "twitter_thread_writer": {
        "category": "Content Marketing",
        "description": "Write viral Twitter/X threads with hooks and engagement structure",
        "has_script": True,
        "full_description": """## Overview
Generates engaging Twitter/X threads optimized for viral reach with proven hook patterns and engagement structures.

## Prerequisites
- `OPENAI_API_KEY` - Content generation

## Thread Structure
1. **Hook Tweet**: Pattern interrupt, curiosity gap
2. **Promise**: What they'll learn
3. **Tweets 3-8**: Value points (one idea each)
4. **Summary**: Recap key points
5. **CTA**: Follow, RT, bookmark

## Hook Patterns
- "I spent [time] doing [thing]. Here's what I learned:"
- "[Number] [things] that [result]:"
- "Stop [common advice]. Here's what actually works:"
- "The [topic] playbook that [result]:"

## Formatting Rules
- 280 chars max per tweet
- Use line breaks for readability
- Number tweets for threads
- End with engagement CTA""",
        "inputs": ["topic", "thread_length", "hook_style"],
        "outputs": ["Thread tweets", "Hooks", "CTAs"]
    },
    
    "youtube_script_creator": {
        "category": "Content Marketing",
        "description": "Create YouTube video scripts with MrBeast-style retention engineering",
        "has_script": True,
        "full_description": """## Overview
Creates YouTube video scripts optimized for retention with proven hook formulas, pattern interrupts, and engagement techniques.

## Prerequisites
- `OPENROUTER_API_KEY` - Script generation

## Script Structure
1. **Hook (0-30 sec)**: Pattern interrupt, promise payoff
2. **Intro (30-60 sec)**: Set expectations, build curiosity
3. **Content Sections**: 3-5 main points with transitions
4. **Pattern Interrupts**: Every 2-3 minutes
5. **Climax**: Deliver on promise
6. **CTA**: Subscribe, watch next

## Retention Techniques
- Open loops throughout
- Preview future content
- "But wait, there's more"
- Unexpected transitions
- Payoff promises made

## Related Skill Bibles
- SKILL_BIBLE_youtube_script_writing.md
- SKILL_BIBLE_youtube_retention_mastery.md""",
        "inputs": ["topic", "video_length", "target_audience"],
        "outputs": ["Full script", "Hook options", "Thumbnail concepts", "Title options"]
    },
    
    "vsl_script_writer": {
        "category": "Funnel Building",
        "description": "Write video sales letter scripts using proven 10-part structure",
        "has_script": True,
        "full_description": """## Overview
Generates VSL scripts using the proven 10-part structure optimized for high-ticket conversions.

## Prerequisites
- `OPENROUTER_API_KEY` - Script generation
- Research data from company_market_research

## 10-Part VSL Structure
1. **Pattern Interrupt Hook** (30 sec)
2. **Big Promise + Credibility** (2 min)
3. **Problem Agitation** (5 min)
4. **Solution Reveal** (3 min)
5. **Mechanism Explanation** (5 min)
6. **Proof & Testimonials** (5 min)
7. **Offer Presentation** (5 min)
8. **Bonuses & Stack** (3 min)
9. **Guarantee** (2 min)
10. **Urgency & Close** (3 min)

## Related Skill Bibles
- SKILL_BIBLE_vsl_writing_production.md
- SKILL_BIBLE_vsl_script_mastery_fazio.md""",
        "inputs": ["company", "offer", "price", "target_audience", "research_data"],
        "outputs": ["VSL script", "B-roll suggestions", "Estimated length"]
    },
    
    "vsl_sales_page_writer": {
        "category": "Funnel Building",
        "description": "Write VSL sales pages with headline variations and offer stacks",
        "has_script": True,
        "full_description": """## Overview
Generates sales page copy to accompany VSL videos with headlines, bullets, offer stacks, and objection handlers.

## Prerequisites
- `OPENROUTER_API_KEY` - Copy generation

## Page Elements
- **Headlines** (3 variations)
- **Subheadline** with specific result
- **Benefit bullets** matching VSL
- **Video embed area**
- **Offer stack** with value
- **Testimonials section**
- **FAQ section**
- **Guarantee badge**
- **CTA buttons**

## Headline Formulas
- "How to [Result] Without [Obstacle]"
- "The [Mechanism] That [Result]"
- "[Number] [Audience] Are Using This to [Result]"

## Related Skill Bibles
- SKILL_BIBLE_funnel_copywriting_mastery.md""",
        "inputs": ["vsl_script", "offer", "price", "testimonials"],
        "outputs": ["Sales page copy", "Headline variations", "Offer stack", "FAQ"]
    },
    
    "ultimate_hiring_system": {
        "category": "Operations",
        "description": "Complete hiring workflow from job post to offer with scorecards",
        "has_script": False,
        "full_description": """## Overview
Complete hiring automation from job description creation through offer letter generation with AI-assisted candidate scoring.

## Process
1. **Job Description Generator**: Create compelling JDs
2. **Candidate Screening**: AI scores applications
3. **Interview Scheduler**: Automated scheduling
4. **Interview Scorecards**: Structured evaluation
5. **Reference Check Templates**: Questions to ask
6. **Offer Letter Generator**: Custom offers

## Scorecard Criteria
- Technical skills (40%)
- Culture fit (25%)
- Communication (20%)
- Growth potential (15%)

## Integrations
- ATS (Lever, Greenhouse)
- Calendly
- Google Docs
- Slack notifications""",
        "inputs": ["role", "requirements", "salary_range", "team"],
        "outputs": ["Job description", "Scorecards", "Interview questions", "Offer letter"]
    },
    
    "ultimate_lead_magnet_creator": {
        "category": "Content Generation",
        "description": "Create lead magnets: ebooks, checklists, templates, calculators",
        "has_script": False,
        "full_description": """## Overview
Creates compelling lead magnets including ebooks, checklists, templates, and calculators optimized for conversion.

## Lead Magnet Types
1. **Ebook/Guide**: 10-30 pages of value
2. **Checklist**: Step-by-step action items
3. **Template**: Fill-in-the-blank documents
4. **Swipe File**: Examples and copy
5. **Calculator**: Interactive tool
6. **Cheat Sheet**: Quick reference

## Best Practices
- Solve one specific problem
- Deliver quick wins
- Professional design
- Clear next step CTA

## Naming Patterns
- "The [Audience] Guide to [Result]"
- "[Number] [Things] to [Result]"
- "The Ultimate [Topic] Checklist"
- "[Topic] Template: [Benefit]"

## Related Skill Bibles
- SKILL_BIBLE_lead_magnet_creation.md""",
        "inputs": ["topic", "audience", "magnet_type", "desired_result"],
        "outputs": ["Lead magnet content", "Landing page copy", "Thank you page"]
    },
    
    "ultimate_niche_research": {
        "category": "Research",
        "description": "Deep niche research and market analysis for business entry",
        "has_script": False,
        "full_description": """## Overview
Comprehensive niche research and validation system for market entry decisions.

## Research Areas
1. **Market Size**: TAM, SAM, SOM
2. **Competition**: Direct and indirect
3. **Audience**: Demographics, psychographics
4. **Pain Points**: Problems and desires
5. **Pricing**: What market will bear
6. **Channels**: Where to find customers
7. **Trends**: Growth trajectory

## Validation Criteria
| Factor | Weight |
|--------|--------|
| Market size | 25% |
| Competition level | 20% |
| Profit margins | 20% |
| Accessibility | 20% |
| Personal fit | 15% |

## Related Skill Bibles
- SKILL_BIBLE_niche_research_validation.md
- SKILL_BIBLE_market_research.md""",
        "inputs": ["niche_idea", "budget", "timeline"],
        "outputs": ["Market analysis", "Competition report", "Recommendation"]
    },
    
    "ultimate_pricing_strategy": {
        "category": "Strategy",
        "description": "Pricing strategy optimization with competitive analysis",
        "has_script": False,
        "full_description": """## Overview
Develops optimal pricing strategy based on market research, competitor analysis, and value perception.

## Pricing Models
- **Cost-Plus**: Cost + margin
- **Value-Based**: Perceived value
- **Competitor-Based**: Market rates
- **Tiered**: Good/Better/Best
- **Usage-Based**: Pay per use

## Analysis Components
1. Cost structure analysis
2. Competitor pricing audit
3. Customer willingness to pay
4. Value stack development
5. Pricing psychology

## Pricing Psychology
- Anchor pricing (show high first)
- Charm pricing ($997 vs $1000)
- Price bundling
- Decoy effect

## Related Skill Bibles
- SKILL_BIBLE_pricing_strategy.md
- SKILL_BIBLE_offer_positioning.md""",
        "inputs": ["product", "costs", "competitors", "target_margin"],
        "outputs": ["Pricing recommendation", "Tier structure", "Value stack"]
    },
    
    "ultimate_linkedin_outreach": {
        "category": "Sales Outreach",
        "description": "LinkedIn outreach system with connection requests and messaging",
        "has_script": False,
        "full_description": """## Overview
Complete LinkedIn outreach system including connection request templates, messaging sequences, and follow-up automation.

## Outreach Sequence
1. **Day 0**: Connection request (personalized)
2. **Day 1**: Thank you message (after accept)
3. **Day 3**: Value message (no pitch)
4. **Day 7**: Soft pitch
5. **Day 14**: Follow-up

## Connection Request Templates
- Mention shared connection
- Reference their content
- Compliment achievement
- Ask relevant question

## Message Best Practices
- Under 300 characters
- One clear question
- No sales pitch in first message
- Personalize each message""",
        "inputs": ["target_audience", "value_proposition", "offer"],
        "outputs": ["Connection templates", "Message sequences", "Follow-up cadence"]
    },
    
    "ultimate_sales_call_system": {
        "category": "Sales",
        "description": "Sales call preparation, execution scripts, and follow-up system",
        "has_script": False,
        "full_description": """## Overview
Complete sales call system with pre-call research, call scripts, objection handling, and follow-up sequences.

## Call Structure
1. **Rapport** (2 min): Build connection
2. **Discovery** (15 min): Ask questions
3. **Present** (10 min): Show solution
4. **Handle Objections** (5 min): Address concerns
5. **Close** (5 min): Ask for business

## Key Questions
- "What's your biggest challenge with [topic]?"
- "What have you tried so far?"
- "What would success look like?"
- "What's holding you back?"

## Common Objections
- "Too expensive" → Value comparison
- "Need to think" → Identify concern
- "Bad timing" → Future commitment
- "Need approval" → Bring decision maker

## Related Skill Bibles
- SKILL_BIBLE_sales_call_mastery.md
- SKILL_BIBLE_hormozi_sales_training.md""",
        "inputs": ["prospect_info", "offer", "pricing"],
        "outputs": ["Pre-call research", "Call script", "Objection handlers", "Follow-up emails"]
    },
    
    "ultimate_seo_campaign": {
        "category": "SEO",
        "description": "Complete SEO campaign management with keyword research and tracking",
        "has_script": False,
        "full_description": """## Overview
Full SEO campaign system from keyword research through content creation and rank tracking.

## Campaign Components
1. **Keyword Research**: Find opportunities
2. **Competitor Analysis**: Gap analysis
3. **Content Strategy**: Topic clusters
4. **On-Page SEO**: Optimization checklist
5. **Link Building**: Outreach plan
6. **Rank Tracking**: Monitor progress

## Keyword Selection Criteria
- Search volume (min 100/mo)
- Keyword difficulty (<40 for new sites)
- Business relevance (high intent)
- Content opportunity

## Content Cluster Model
- Pillar page (2000+ words)
- Cluster pages (1000+ words)
- Internal linking strategy

## Related Skill Bibles
- SKILL_BIBLE_seo_mastery.md
- SKILL_BIBLE_content_seo.md""",
        "inputs": ["website", "target_keywords", "competitors"],
        "outputs": ["Keyword list", "Content plan", "Technical audit", "Link building plan"]
    },
    
    "ultimate_video_ad_script": {
        "category": "Paid Advertising",
        "description": "Video ad script writing with hooks and direct response CTAs",
        "has_script": False,
        "full_description": """## Overview
Creates video ad scripts optimized for paid media with proven hook formulas and direct response CTAs.

## Video Ad Structures
**UGC Style (15-30 sec):**
- Hook (3 sec)
- Problem (5 sec)
- Solution (10 sec)
- CTA (5 sec)

**Story Style (30-60 sec):**
- Hook (5 sec)
- Story setup (15 sec)
- Transformation (15 sec)
- Offer + CTA (10 sec)

## Hook Formulas
- "Stop scrolling if you [pain point]"
- "I made [mistake] and here's what happened"
- "This [product] changed everything"
- "POV: You finally [desired result]"

## Platform Specs
- Meta: 4:5 or 9:16, <15 sec best
- YouTube: 16:9, skip after 5 sec
- TikTok: 9:16, <30 sec best

## Related Skill Bibles
- SKILL_BIBLE_video_ad_scripts.md""",
        "inputs": ["product", "audience", "platform", "ad_length"],
        "outputs": ["Video script", "Hook options", "B-roll suggestions", "CTA options"]
    },
    
    "facebook_ad_library_analysis_automation": {
        "category": "Paid Advertising",
        "description": "Analyze competitor ads from Facebook Ad Library for insights",
        "has_script": True,
        "full_description": """## Overview
Scrapes and analyzes competitor ads from Facebook Ad Library to identify winning creative patterns and copy formulas.

## Prerequisites
- `APIFY_API_TOKEN` - Scraping
- `OPENAI_API_KEY` - Analysis

## Analysis Components
1. **Ad Creative Types**: Images, videos, carousels
2. **Copy Patterns**: Headlines, primary text, CTAs
3. **Offers**: Discounts, trials, demos
4. **Run Time**: How long ads have been active
5. **Platforms**: FB, IG, Messenger, Audience Network

## Insights Extracted
- Top-performing ad formats
- Common hook patterns
- Offer structures
- Landing page strategies
- Creative refresh frequency

## Output
- Competitor ad database
- Pattern analysis report
- Creative recommendations""",
        "inputs": ["competitor_pages", "date_range"],
        "outputs": ["Ad database", "Analysis report", "Creative recommendations"]
    },
    
    "ecom_email_campaign_generator_agent": {
        "category": "Sales Outreach",
        "description": "E-commerce email campaigns using Max Sturtevant's $40M methodology",
        "has_script": True,
        "full_description": """## Overview
Generates e-commerce email campaigns using Max Sturtevant's proven methodology that generated $40M+ in email revenue.

## Prerequisites
- `OPENROUTER_API_KEY` - AI generation

## Campaign Types
- Product launch
- Flash sale
- Abandoned cart
- Win-back
- VIP exclusive
- Holiday/seasonal

## SCE Framework
- **S**kimmable: Scannable layout
- **C**lear: One message, one CTA
- **E**ngaging: Hooks and curiosity

## Email Structure Rules
- 75 words max body copy
- Single column layout
- One CTA per email
- Mobile-first design

## Related Skill Bibles
- SKILL_BIBLE_sturtevant_email_master_system.md
- SKILL_BIBLE_ecommerce_email_marketing.md""",
        "inputs": ["product", "campaign_type", "discount", "urgency"],
        "outputs": ["Email sequence", "Subject lines", "Preview text"]
    },

    "x_keyword_youtube_content": {
        "category": "Content Marketing",
        "description": "Search X for trending posts and generate YouTube video ideas with full outlines",
        "has_script": True,
        "full_description": """## Overview
Automated content research workflow that searches X (Twitter) for high-performing posts matching specified keywords, analyzes engagement patterns, and generates YouTube video ideas with full outlines.

## Prerequisites
- `OPENROUTER_API_KEY` - For Grok-4-fast access (X search) and Claude (analysis)
- `SLACK_WEBHOOK_URL` - For notifications
- Google OAuth configured (`client_secrets.json` + `token.pickle`)

## How to Run
```bash
# Basic usage with defaults
python3 execution/x_keyword_youtube_content.py

# With custom keywords
python3 execution/x_keyword_youtube_content.py \\
    --keywords "AI agents" "Claude Code" "automation workflows" \\
    --num_videos 5 \\
    --time_range 24h
```

## Process
1. **X Search via Grok-4-fast**: Searches X for trending/high-performing posts
2. **Theme Analysis**: Extracts common themes and viral angles via Claude
3. **Video Idea Generation**: Creates 5 YouTube video concepts
4. **Full Outlines**: Hook script, body structure, retention tactics, CTAs
5. **Delivery**: Google Doc + Slack notification

## Default Keywords
- AI agents
- AI automation
- Claude Code
- agentic workflows
- AI coding assistants

## Output Structure
Each video idea includes:
- **Title**: Under 60 chars, optimized for CTR
- **Thumbnail Concept**: Visual direction
- **Hook**: Full 30-second script using 5-part framework
- **Body Outline**: Points with retention tactics
- **CTA**: Specific call to action

## Quality Gates
- Minimum 10 high-performing posts found
- All 5 video ideas have complete outlines
- Each outline includes hook, body, and CTA
- Google Doc created successfully
- Slack notification sent

## Scheduling
Designed to run every 3 hours via cron:
```
0 */3 * * * cd /path/to/AIAA-Agentic-OS && python3 execution/x_keyword_youtube_content.py
```

## Related Skill Bibles
- SKILL_BIBLE_youtube_script_writing.md
- SKILL_BIBLE_youtube_growth.md""",
        "inputs": ["keywords", "num_videos", "time_range", "channel"],
        "outputs": ["Video ideas markdown", "Google Doc", "Slack notification"]
    },
}

# Merge additional workflows into main WORKFLOWS dict
for name, data in ADDITIONAL_WORKFLOWS.items():
    if name not in WORKFLOWS:
        WORKFLOWS[name] = data

# Add remaining workflows with basic descriptions
remaining_workflows = {
    "automated_prospecting_ghl_crm": ("Lead Generation", "Automated prospecting pipeline syncing to GoHighLevel CRM", True),
    "booked_meeting_alert_prospect_research": ("Sales Automation", "Instant alerts and research when meetings are booked", True),
    "brand_mention_monitor": ("Research", "Monitor brand mentions across web and social media", True),
    "build_lead_list": ("Lead Generation", "Build targeted lead lists from multiple sources", True),
    "bulk_email_validator": ("Utilities", "Validate email lists for deliverability before sending", True),
    "contract_renewal_reminder": ("Client Management", "Automated contract renewal reminders and follow-ups", True),
    "convert_n8n_workflow": ("Utilities", "Convert N8N workflow JSON to AIAA directive format", True),
    "crm_deal_automator": ("Sales Automation", "Automate CRM deal stage updates and tasks", True),
    "crunchbase_lead_finder": ("Lead Generation", "Find funded startups from Crunchbase for outreach", True),
    "daily_campaign_reports_health_metrics_bounce_rate_alerts": ("Reporting", "Daily email campaign health reports with bounce alerts", True),
    "demo_scheduler": ("Sales Automation", "Automated demo scheduling with calendar integration", True),
    "dream_100_instagram_personalized_dm_automation": ("Sales Outreach", "Dream 100 Instagram DM outreach with personalization", True),
    "email_deliverability_reputation_manager": ("Utilities", "Monitor and manage email deliverability reputation", True),
    "email_reply_classifier": ("Sales Automation", "AI classifier for email replies (interested, not interested, OOO)", True),
    "faq_chatbot": ("Client Management", "AI-powered FAQ chatbot for customer support", True),
    "follow_up_sequence": ("Sales Outreach", "Automated follow-up email sequences", True),
    "formatted_google_doc_creator": ("Utilities", "Create beautifully formatted Google Docs from markdown", True),
    "full_campaign_pipeline": ("Sales Outreach", "End-to-end cold email campaign pipeline", True),
    "funnel_outline_strategy_agent": ("Funnel Building", "AI agent for funnel strategy and outline creation", True),
    "funding_round_tracker": ("Research", "Track funding rounds for prospecting opportunities", True),
    "google_serp_lead_scraper": ("Lead Generation", "Scrape Google search results for lead generation", True),
    "hubspot_enrichment": ("Lead Generation", "Enrich HubSpot contacts with additional data", True),
    "instantly_autoreply": ("Sales Automation", "Automated replies for Instantly.ai email campaigns", True),
    "job_board_lead_finder": ("Lead Generation", "Find leads from job board postings", True),
    "jump_cut_vad": ("Content Marketing", "AI-powered jump cut detection for video editing", True),
    "launch_cold_email_campaign": ("Sales Outreach", "Launch and manage cold email campaigns", True),
    "lead_deduplication": ("Utilities", "Deduplicate lead lists across sources", True),
    "lead_magnet_delivery": ("Content Marketing", "Automated lead magnet delivery system", True),
    "lead_notification": ("Sales Automation", "Instant notifications when new leads arrive", True),
    "linkedin_group_scraper": ("Lead Generation", "Scrape members from LinkedIn groups", True),
    "linkedin_profile_tracker": ("Research", "Track LinkedIn profile changes and updates", True),
    "payment_reminder": ("Client Management", "Automated payment reminder sequences", True),
    "project_milestone_tracker": ("Operations", "Track project milestones and send updates", True),
    "review_collection": ("Client Management", "Automated review and testimonial collection", True),
    "rss_to_content_pipeline": ("Content Marketing", "Convert RSS feeds into social content", True),
    "scrape_leads": ("Lead Generation", "Generic lead scraping from various sources", True),
    "social_media_scheduler": ("Content Marketing", "Schedule posts across social platforms", True),
    "stripe_client_onboarding": ("Client Management", "Trigger onboarding when Stripe payment received", True),
    "team_task_assignment": ("Operations", "Automated task assignment to team members", True),
    "ticket_auto_responder": ("Client Management", "Auto-respond to support tickets with AI", True),
    "ticket_triage": ("Client Management", "AI triage for support tickets by priority", True),
    "ultimate_ai_automation_builder": ("Automation", "Build custom AI automations from natural language", False),
    "ultimate_client_onboarding": ("Client Management", "Complete client onboarding from contract to kickoff", True),
    "ultimate_client_reporting": ("Reporting", "Comprehensive automated client reporting", True),
    "ultimate_cold_email_campaign": ("Sales Outreach", "End-to-end cold email campaign management", True),
    "ultimate_ecommerce_email": ("Sales Outreach", "E-commerce email marketing with flows and campaigns", True),
    "ultimate_google_ads_campaign": ("Paid Advertising", "Complete Google Ads campaign setup and management", False),
    "ultimate_local_newsletter": ("Content Marketing", "Local business newsletter with news and promotions", True),
    "ultimate_proposal_generator": ("Sales", "Generate winning client proposals", False),
    "upwork_scrape_apply": ("Lead Generation", "Scrape Upwork jobs and auto-apply", True),
    "utm_generator": ("Utilities", "Generate UTM parameters for campaign tracking", True),
    "video_shorts_extractor": ("Content Marketing", "Extract short clips from long videos", True),
    "video_transcription_summary": ("Content Marketing", "Transcribe and summarize video content", True),
    "vsl_funnel_writer": ("Funnel Building", "Write complete VSL funnel copy", True),
    "webinar_followup": ("Funnel Building", "Webinar follow-up sequences for attendees", True),
    "webinar_funnel_generator": ("Funnel Building", "Generate complete webinar funnels", True),
    "website_contact_scraper": ("Lead Generation", "Scrape contact info from websites", True),
    "whatsapp_support_bot": ("Client Management", "WhatsApp support bot with AI responses", True),
    "win_loss_analysis": ("Sales", "Analyze sales wins and losses for insights", True),
    "yelp_review_scraper": ("Lead Generation", "Scrape Yelp for business data and reviews", True),
    "youtube_channel_finder": ("Research", "Find relevant YouTube channels in any niche", True),
    "youtube_script_generator": ("Content Marketing", "Generate YouTube video scripts", True),
    "youtube_scriptwriter_workflow": ("Content Marketing", "Complete YouTube scriptwriting workflow", True),
    "youtube_to_campaign_pipeline": ("Content Marketing", "Convert YouTube content to marketing campaigns", True),
    "zoom_call_multi_content_copywriter_scheduler": ("Content Marketing", "Repurpose Zoom calls into multiple content pieces", True),
    "ai_prospect_researcher": ("Research", "Deep prospect research for sales personalization", True),
    "ai_thumbnail_generator": ("Content Marketing", "Generate YouTube thumbnail concepts and images", True),
    "client_feedback_collector": ("Client Management", "Collect and analyze client feedback", True),
    "client_health_score": ("Client Management", "Calculate client health scores", True),
    "competitor_monitor": ("Research", "Monitor competitor changes and updates", True),
    "content_translator": ("Content Marketing", "Translate content preserving tone", True),
    "create_proposal": ("Sales", "Generate client proposals", True),
    "email_campaign_report": ("Reporting", "Email campaign performance reports", True),
    "email_flow_writer": ("Sales Outreach", "Write automated email flows", True),
    "funnel_copywriter": ("Funnel Building", "Write funnel copy with proven frameworks", True),
    "google_doc_creator": ("Utilities", "Create Google Docs from content", True),
    "google_maps_scraper": ("Lead Generation", "Scrape Google Maps business data", True),
    "instagram_reel_script": ("Content Marketing", "Write Instagram Reel scripts", True),
    "invoice_generator": ("Client Management", "Generate professional invoices", True),
    "landing_page_cro_analyzer": ("SEO", "Analyze landing pages for CRO", True),
    "linkedin_dm_automation": ("Sales Outreach", "Automate LinkedIn DM outreach", True),
    "linkedin_post_generator": ("Content Marketing", "Generate LinkedIn posts", True),
    "monthly_reporting": ("Reporting", "Generate monthly reports", True),
    "objection_handler": ("Sales", "Generate objection handling scripts", True),
    "podcast_repurposer": ("Content Marketing", "Repurpose podcasts to content", True),
    "press_release_generator": ("Content Marketing", "Generate press releases", True),
    "product_description_writer": ("Content Generation", "Write product descriptions", True),
    "product_photoshoot_generator": ("Creative", "Generate product photoshoot concepts", True),
    "reddit_to_ad_scripts": ("Paid Advertising", "Convert Reddit to ad scripts", True),
    "sales_call_summarizer": ("Sales", "Summarize sales call recordings", True),
    "sales_pipeline_dashboard": ("Reporting", "Sales pipeline dashboards", True),
    "slack_notifier": ("Utilities", "Send Slack notifications", True),
    "testimonial_request": ("Client Management", "Request testimonials from clients", True),
    "ultimate_agency_dashboard": ("Reporting", "Agency management dashboard", False),
    "ultimate_case_study_generator": ("Content Generation", "Generate case studies", True),
}

for name, (cat, desc, has_script) in remaining_workflows.items():
    if name not in WORKFLOWS:
        WORKFLOWS[name] = {
            "description": desc,
            "has_script": has_script,
            "category": cat,
            "full_description": f"""## Overview
{desc}

## Prerequisites
Check the directive file at `directives/{name}.md` for required API keys and setup instructions.

## How to Run
```bash
python3 execution/{name}.py --help
```

See `directives/{name}.md` for detailed step-by-step instructions and examples.""",
            "inputs": [],
            "outputs": []
        }

for name, wf in WORKFLOWS.items():
    wf["name"] = name
    if "category" not in wf:
        wf["category"] = "General"

# =============================================================================
# Authentication
# =============================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password):
    if not DASHBOARD_PASSWORD_HASH:
        return False
    return hash_password(password) == DASHBOARD_PASSWORD_HASH

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def log_event(event_type, status, data, source="system"):
    with events_lock:
        events_log.appendleft({
            "id": len(events_log) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "status": status,
            "data": data,
            "source": source
        })

# =============================================================================
# CSS with Theme Support and Markdown Styling
# =============================================================================

BASE_CSS = '''
<style>
    :root {
        --bg-base: #1a1a1a;
        --bg-surface: #232323;
        --bg-elevated: #2a2a2a;
        --bg-hover: #333333;
        --text-primary: #f5f5f5;
        --text-secondary: #a3a3a3;
        --text-muted: #737373;
        --border: #333333;
        --border-subtle: #2a2a2a;
        --accent: #e07a3a;
        --accent-hover: #f08a4a;
        --accent-muted: rgba(224, 122, 58, 0.15);
        --success: #4ade80;
        --success-muted: rgba(74, 222, 128, 0.15);
        --error: #f87171;
        --error-muted: rgba(248, 113, 113, 0.15);
        --warning: #fbbf24;
        --warning-muted: rgba(251, 191, 36, 0.15);
    }
    [data-theme="light"] {
        --bg-base: #f8f8f8;
        --bg-surface: #ffffff;
        --bg-elevated: #f0f0f0;
        --bg-hover: #e8e8e8;
        --text-primary: #1a1a1a;
        --text-secondary: #525252;
        --text-muted: #737373;
        --border: #e0e0e0;
        --border-subtle: #ebebeb;
        --accent: #d96c2c;
        --accent-hover: #c45e20;
        --accent-muted: rgba(217, 108, 44, 0.12);
        --success: #16a34a;
        --success-muted: rgba(22, 163, 74, 0.12);
        --error: #dc2626;
        --error-muted: rgba(220, 38, 38, 0.12);
        --warning: #ca8a04;
        --warning-muted: rgba(202, 138, 4, 0.12);
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'DM Sans', -apple-system, sans-serif;
        background: var(--bg-base);
        color: var(--text-primary);
        min-height: 100vh;
        line-height: 1.6;
        transition: background 0.2s, color 0.2s;
    }
    
    /* Markdown Content Styling */
    .md-content { line-height: 1.8; }
    .md-content h2 { font-size: 1.25rem; font-weight: 600; margin: 1.5rem 0 0.75rem; color: var(--accent); border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.5rem; }
    .md-content h3 { font-size: 1.1rem; font-weight: 600; margin: 1.25rem 0 0.5rem; color: var(--text-primary); }
    .md-content h4 { font-size: 1rem; font-weight: 500; margin: 1rem 0 0.5rem; color: var(--text-secondary); }
    .md-content p { margin: 0.75rem 0; }
    .md-content strong { color: var(--accent); font-weight: 600; }
    .md-content em { font-style: italic; color: var(--text-secondary); }
    .md-content ul, .md-content ol { margin: 0.75rem 0; padding-left: 1.5rem; }
    .md-content li { margin: 0.375rem 0; }
    .md-content code { font-family: 'DM Mono', monospace; font-size: 0.875em; background: var(--bg-elevated); padding: 0.125rem 0.375rem; border-radius: 4px; color: var(--accent); }
    .md-content pre { background: var(--bg-elevated); padding: 1rem; border-radius: 8px; overflow-x: auto; margin: 1rem 0; border: 1px solid var(--border-subtle); }
    .md-content pre code { background: none; padding: 0; color: var(--text-primary); }
    .md-content .md-table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.875rem; }
    .md-content .md-table td { padding: 0.5rem 0.75rem; border: 1px solid var(--border-subtle); }
    .md-content .md-table tr:first-child { background: var(--bg-elevated); font-weight: 500; }
    
    .theme-toggle { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 8px; cursor: pointer; font-size: 0.8125rem; color: var(--text-secondary); transition: all 0.15s; }
    .theme-toggle:hover { background: var(--bg-hover); color: var(--text-primary); }
    .theme-toggle svg { width: 16px; height: 16px; stroke: currentColor; fill: none; }
    
    .sidebar { position: fixed; left: 0; top: 0; bottom: 0; width: 240px; background: var(--bg-surface); border-right: 1px solid var(--border-subtle); padding: 1.5rem 0; display: flex; flex-direction: column; }
    .sidebar-brand { display: flex; align-items: center; gap: 0.75rem; padding: 0 1.25rem; margin-bottom: 1.5rem; }
    .brand-icon { width: 32px; height: 32px; background: var(--accent); border-radius: 8px; display: flex; align-items: center; justify-content: center; }
    .brand-icon svg { width: 18px; height: 18px; stroke: white; fill: none; }
    .sidebar-brand h1 { font-size: 1rem; font-weight: 600; }
    .theme-row { padding: 0 1.25rem; margin-bottom: 1.5rem; }
    .nav-section { margin-bottom: 1.5rem; }
    .nav-label { padding: 0 1.25rem; font-size: 0.6875rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.5rem; }
    .nav-item { display: flex; align-items: center; gap: 0.75rem; padding: 0.625rem 1.25rem; color: var(--text-secondary); text-decoration: none; font-size: 0.875rem; transition: all 0.15s; }
    .nav-item:hover { background: var(--bg-elevated); color: var(--text-primary); }
    .nav-item.active { background: var(--accent-muted); color: var(--accent); }
    .nav-item svg { width: 18px; height: 18px; stroke: currentColor; fill: none; }
    .sidebar-footer { margin-top: auto; padding: 1rem 1.25rem; border-top: 1px solid var(--border-subtle); }
    .user-info { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; }
    .user-avatar { width: 32px; height: 32px; background: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 500; font-size: 0.8125rem; color: white; }
    .user-name { font-size: 0.875rem; font-weight: 500; }
    .logout-btn { display: block; width: 100%; padding: 0.5rem; background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 6px; color: var(--text-secondary); font-family: inherit; font-size: 0.8125rem; cursor: pointer; text-align: center; text-decoration: none; }
    .logout-btn:hover { background: var(--bg-hover); color: var(--text-primary); }
    
    .main { margin-left: 240px; padding: 2rem; }
    .page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; gap: 1rem; flex-wrap: wrap; }
    .page-title { font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
    .page-subtitle { color: var(--text-muted); font-size: 0.875rem; margin-top: 0.25rem; }
    .status-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.875rem; background: var(--success-muted); border-radius: 9999px; font-size: 0.8125rem; color: var(--success); }
    .status-badge::before { content: ''; width: 8px; height: 8px; background: currentColor; border-radius: 50%; box-shadow: 0 0 8px currentColor; }
    
    .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
    .stat-card { background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.25rem; }
    .stat-icon { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 0.75rem; }
    .stat-icon svg { width: 18px; height: 18px; stroke: currentColor; fill: none; }
    .stat-icon.orange { background: var(--accent-muted); color: var(--accent); }
    .stat-icon.green { background: var(--success-muted); color: var(--success); }
    .stat-icon.red { background: var(--error-muted); color: var(--error); }
    .stat-icon.yellow { background: var(--warning-muted); color: var(--warning); }
    .stat-value { font-size: 1.75rem; font-weight: 600; }
    .stat-label { font-size: 0.8125rem; color: var(--text-muted); }
    
    .card { background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; margin-bottom: 1.5rem; }
    .card-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-subtle); }
    .card-title { font-size: 0.9375rem; font-weight: 500; }
    .card-action { font-size: 0.8125rem; color: var(--accent); text-decoration: none; padding: 0.25rem 0.5rem; border-radius: 4px; }
    .card-action:hover { background: var(--accent-muted); }
    .card-body { padding: 1.25rem; }
    
    .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 500; }
    .badge-success { background: var(--success-muted); color: var(--success); }
    .badge-error { background: var(--error-muted); color: var(--error); }
    .badge-warning { background: var(--warning-muted); color: var(--warning); }
    .badge-info { background: var(--accent-muted); color: var(--accent); }
    .badge-muted { background: var(--bg-elevated); color: var(--text-muted); }
    .badge-category { background: var(--bg-elevated); color: var(--text-secondary); font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.03em; }
    
    .form-group { margin-bottom: 1.25rem; }
    .form-label { display: block; font-size: 0.875rem; font-weight: 500; color: var(--text-secondary); margin-bottom: 0.5rem; }
    .form-input { width: 100%; padding: 0.75rem 1rem; background: var(--bg-elevated); border: 1px solid var(--border); border-radius: 8px; color: var(--text-primary); font-family: inherit; font-size: 0.9375rem; }
    .form-input:focus { outline: none; border-color: var(--accent); }
    .btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.25rem; background: var(--accent); color: white; border: none; border-radius: 8px; font-family: inherit; font-size: 0.875rem; font-weight: 500; cursor: pointer; }
    .btn:hover { background: var(--accent-hover); }
    
    .workflows-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
    .workflow-card { background: var(--bg-elevated); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1rem; text-decoration: none; color: inherit; display: block; transition: all 0.15s; }
    .workflow-card:hover { border-color: var(--accent); transform: translateY(-2px); }
    .workflow-name { font-weight: 500; font-size: 0.875rem; margin-bottom: 0.25rem; }
    .workflow-desc { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.75rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .workflow-meta { display: flex; gap: 0.5rem; flex-wrap: wrap; }
    
    .env-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }
    .env-item { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1rem; background: var(--bg-elevated); border-radius: 8px; }
    .env-name { font-family: 'DM Mono', monospace; font-size: 0.8125rem; }
    .env-status { display: flex; align-items: center; gap: 0.375rem; font-size: 0.75rem; }
    .env-status.set { color: var(--success); }
    .env-status.unset { color: var(--error); }
    .env-status::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
    
    .event-row { display: grid; grid-template-columns: 80px 120px 1fr 100px; gap: 1rem; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-subtle); font-size: 0.8125rem; }
    .event-row:last-child { border-bottom: none; }
    .event-row:hover { background: var(--bg-hover); }
    .event-time { font-family: 'DM Mono', monospace; color: var(--text-muted); }
    .event-type { font-weight: 500; }
    .event-data { color: var(--text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    
    .table { width: 100%; border-collapse: collapse; }
    .table th { text-align: left; padding: 0.75rem 1rem; font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); background: var(--bg-elevated); }
    .table td { padding: 0.875rem 1rem; font-size: 0.875rem; border-bottom: 1px solid var(--border-subtle); }
    .table tr:last-child td { border-bottom: none; }
    .table tbody tr:hover { background: var(--bg-hover); }
    .mono { font-family: 'DM Mono', monospace; font-size: 0.8125rem; }
    
    .empty { text-align: center; padding: 3rem 1rem; color: var(--text-muted); }
    .alert { padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.875rem; }
    .alert-success { background: var(--success-muted); color: var(--success); border: 1px solid var(--success); }
    .alert-error { background: var(--error-muted); color: var(--error); border: 1px solid var(--error); }
    
    .search-box { margin-bottom: 1.5rem; }
    .search-box input { width: 100%; max-width: 400px; padding: 0.75rem 1rem; background: var(--bg-surface); border: 1px solid var(--border); border-radius: 8px; color: var(--text-primary); font-family: inherit; font-size: 0.9375rem; }
    .search-box input:focus { outline: none; border-color: var(--accent); }
    
    .back-btn { display: inline-flex; align-items: center; gap: 0.5rem; color: var(--accent); text-decoration: none; margin-bottom: 1.5rem; font-size: 0.875rem; }
    .back-btn:hover { text-decoration: underline; }
    
    @media (max-width: 1024px) { 
        .stats-grid { grid-template-columns: repeat(2, 1fr); } 
        .workflows-grid { grid-template-columns: repeat(2, 1fr); } 
        .env-grid { grid-template-columns: 1fr; } 
    }
    @media (max-width: 768px) { 
        .sidebar { display: none; } 
        .main { margin-left: 0; padding: 1rem; } 
        .workflows-grid { grid-template-columns: 1fr; } 
        .event-row { grid-template-columns: 1fr; gap: 0.5rem; } 
        .page-header { flex-direction: column; }
        .page-title { font-size: 1.25rem; }
        .stats-grid { grid-template-columns: 1fr 1fr; gap: 0.75rem; }
        .stat-card { padding: 1rem; }
        .stat-value { font-size: 1.5rem; }
        .card-body { padding: 1rem; }
        .md-content pre { font-size: 0.75rem; padding: 0.75rem; }
        .md-content .md-table { font-size: 0.75rem; }
        .md-content .md-table td { padding: 0.375rem 0.5rem; }
        .table { font-size: 0.8rem; }
        .table th, .table td { padding: 0.5rem; }
        .form-input { font-size: 16px; } /* Prevent zoom on iOS */
    }
    @media (max-width: 480px) {
        .stats-grid { grid-template-columns: 1fr; }
        .main { padding: 0.75rem; }
        .page-title { font-size: 1.1rem; }
        .workflow-card { padding: 0.75rem; }
        .workflow-name { font-size: 0.8125rem; }
        .workflow-desc { font-size: 0.6875rem; }
        .badge { font-size: 0.625rem; padding: 0.125rem 0.375rem; }
        .card-header { padding: 0.75rem 1rem; }
        .md-content h2 { font-size: 1.1rem; }
        .md-content h3 { font-size: 1rem; }
        .md-content { font-size: 0.875rem; }
    }
</style>
'''

THEME_SCRIPT = '''
<script>
    function getTheme() { return localStorage.getItem('theme') || 'dark'; }
    function setTheme(theme) { localStorage.setItem('theme', theme); document.documentElement.setAttribute('data-theme', theme); updateToggleIcon(theme); }
    function toggleTheme() { setTheme(getTheme() === 'dark' ? 'light' : 'dark'); }
    function updateToggleIcon(theme) {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.innerHTML = theme === 'light' 
                ? '<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                : '<circle cx="12" cy="12" r="5" stroke-width="2"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke-width="2" stroke-linecap="round"/>';
        }
    }
    document.documentElement.setAttribute('data-theme', getTheme());
    document.addEventListener('DOMContentLoaded', function() { updateToggleIcon(getTheme()); });
</script>
'''

def render_sidebar(active="overview", username="admin"):
    return f'''
    <aside class="sidebar">
        <div class="sidebar-brand">
            <div class="brand-icon"><svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
            <h1>AIAA</h1>
        </div>
        <div class="theme-row">
            <button class="theme-toggle" onclick="toggleTheme()">
                <svg id="theme-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5" stroke-width="2"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke-width="2" stroke-linecap="round"/></svg>
                <span>Toggle theme</span>
            </button>
        </div>
        <nav>
            <div class="nav-section">
                <div class="nav-label">Dashboard</div>
                <a href="/" class="nav-item {'active' if active == 'overview' else ''}"><svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke-width="2"/></svg>Overview</a>
            </div>
            <div class="nav-section">
                <div class="nav-label">Management</div>
                <a href="/workflows" class="nav-item {'active' if active == 'workflows' else ''}"><svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" stroke-width="2"/></svg>Active Workflows</a>
                <a href="/workflow-catalog" class="nav-item {'active' if active == 'workflow-catalog' else ''}"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71" stroke-width="2"/></svg>Workflow Catalog</a>
                <a href="/env" class="nav-item {'active' if active == 'env' else ''}"><svg viewBox="0 0 24 24"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" stroke-width="2"/></svg>Environment</a>
                <a href="/logs" class="nav-item {'active' if active == 'logs' else ''}"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z M14 2v6h6 M16 13H8 M16 17H8 M10 9H8" stroke-width="2"/></svg>Logs</a>
            </div>
        </nav>
        <div class="sidebar-footer">
            <div class="user-info"><div class="user-avatar">{username[0].upper()}</div><span class="user-name">{username}</span></div>
            <a href="/logout" class="logout-btn">Sign Out</a>
        </div>
    </aside>
    '''

# =============================================================================
# Routes
# =============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == DASHBOARD_USERNAME and check_password(password):
            session['logged_in'] = True
            session['username'] = username
            log_event("auth", "success", {"user": username}, source="login")
            return redirect(url_for('dashboard'))
        log_event("auth", "failed", {"user": username}, source="login")
        return render_template_string(LOGIN_TEMPLATE, error="Invalid username or password")
    return render_template_string(LOGIN_TEMPLATE, error=None)

LOGIN_TEMPLATE = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login — AIAA Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono&display=swap" rel="stylesheet">
    {BASE_CSS}{THEME_SCRIPT}
</head>
<body style="display:flex;align-items:center;justify-content:center;">
    <div style="width:100%;max-width:380px;padding:2rem;">
        <div class="card" style="padding:2.5rem;">
            <div style="display:flex;align-items:center;gap:0.75rem;justify-content:center;margin-bottom:2rem;">
                <div class="brand-icon"><svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
                <h1 style="font-size:1.25rem;font-weight:600;">AIAA Dashboard</h1>
            </div>
            {{% if error %}}<div class="alert alert-error">{{{{ error }}}}</div>{{% endif %}}
            <form method="POST">
                <div class="form-group"><label class="form-label">Username</label><input type="text" name="username" class="form-input" required autofocus></div>
                <div class="form-group"><label class="form-label">Password</label><input type="password" name="password" class="form-input" required></div>
                <button type="submit" class="btn" style="width:100%;">Sign In</button>
            </form>
            <div style="text-align:center;margin-top:1.5rem;font-size:0.8125rem;color:var(--text-muted);">AIAA Agentic OS v2.3</div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    with events_lock:
        recent = list(events_log)[:10]
    env_vars = [{"name": var, "set": bool(os.getenv(var, "") or RUNTIME_ENV_VARS.get(var, ""))} for var in TRACKED_ENV_VARS]
    stats = {"workflows": len(WORKFLOWS), "events_success": sum(1 for e in events_log if e["status"] == "success"), "events_error": sum(1 for e in events_log if e["status"] == "error"), "webhooks": 4}
    workflows_list = list(WORKFLOWS.items())[:6]
    username = session.get('username', 'admin')
    return render_template_string(DASHBOARD_TEMPLATE, username=username, env_vars=env_vars, recent_events=recent, stats=stats, workflows=workflows_list, sidebar=render_sidebar("overview", username))

DASHBOARD_TEMPLATE = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard — AIAA</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    {BASE_CSS}{THEME_SCRIPT}
</head>
<body>
    {{{{ sidebar | safe }}}}
    <main class="main">
        <div class="page-header"><div><h1 class="page-title">Dashboard</h1><p class="page-subtitle">AIAA Agentic Operating System</p></div><div class="status-badge">All Systems Operational</div></div>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-icon orange"><svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" stroke-width="2"/></svg></div><div class="stat-value">{{{{ stats.workflows }}}}</div><div class="stat-label">Workflows</div></div>
            <div class="stat-card"><div class="stat-icon green"><svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 11-5.93-9.14" stroke-width="2"/><path d="M22 4L12 14.01l-3-3" stroke-width="2"/></svg></div><div class="stat-value">{{{{ stats.events_success }}}}</div><div class="stat-label">Successful Events</div></div>
            <div class="stat-card"><div class="stat-icon yellow"><svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71" stroke-width="2"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71" stroke-width="2"/></svg></div><div class="stat-value">{{{{ stats.webhooks }}}}</div><div class="stat-label">Webhook Endpoints</div></div>
            <div class="stat-card"><div class="stat-icon red"><svg viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke-width="2"/><path d="M12 9v4M12 17h.01" stroke-width="2"/></svg></div><div class="stat-value">{{{{ stats.events_error }}}}</div><div class="stat-label">Errors (24h)</div></div>
        </div>
        <div class="card"><div class="card-header"><span class="card-title">Environment Variables</span><a href="/env" class="card-action">Manage</a></div><div class="card-body"><div class="env-grid">{{% for var in env_vars %}}<div class="env-item"><span class="env-name">{{{{ var.name }}}}</span><span class="env-status {{{{ 'set' if var.set else 'unset' }}}}">{{{{ 'Set' if var.set else 'Not set' }}}}</span></div>{{% endfor %}}</div></div></div>
        <div class="card"><div class="card-header"><span class="card-title">Recent Events</span><a href="/logs" class="card-action">View All</a></div>{{% if recent_events %}}<div>{{% for event in recent_events %}}<div class="event-row"><span class="event-time">{{{{ event.timestamp[11:19] }}}}</span><span class="event-type">{{{{ event.type }}}}</span><span class="event-data">{{{{ event.data | tojson | truncate(60) }}}}</span><span class="badge badge-{{{{ 'success' if event.status == 'success' else 'error' if event.status == 'error' else 'muted' }}}}">{{{{ event.status }}}}</span></div>{{% endfor %}}</div>{{% else %}}<div class="empty">No events yet.</div>{{% endif %}}</div>
        <div class="card"><div class="card-header"><span class="card-title">Available Workflows</span><a href="/workflows" class="card-action">View All ({{{{ stats.workflows }}}})</a></div><div class="card-body"><div class="workflows-grid">{{% for name, wf in workflows %}}<a href="/workflow/{{{{ name }}}}" class="workflow-card"><div class="workflow-name">{{{{ name.replace('_', ' ').title() }}}}</div><div class="workflow-desc">{{{{ wf.description }}}}</div><div class="workflow-meta"><span class="badge badge-category">{{{{ wf.category }}}}</span><span class="badge {{{{ 'badge-success' if wf.has_script else 'badge-muted' }}}}">{{{{ 'Script' if wf.has_script else 'Directive' }}}}</span></div></a>{{% endfor %}}</div></div></div>
    </main>
    <script>setTimeout(() => location.reload(), 60000);</script>
</body>
</html>
'''

@app.route('/workflow-catalog')
@login_required
def workflows_page():
    username = session.get('username', 'admin')
    workflows_list = sorted(WORKFLOWS.items(), key=lambda x: x[0])
    return render_template_string(WORKFLOWS_TEMPLATE, workflows=workflows_list, sidebar=render_sidebar("workflow-catalog", username))

WORKFLOWS_TEMPLATE = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workflows — AIAA</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    {BASE_CSS}{THEME_SCRIPT}
</head>
<body>
    {{{{ sidebar | safe }}}}
    <main class="main">
        <div class="page-header"><div><h1 class="page-title">Workflow Catalog</h1><p class="page-subtitle">{{{{ workflows | length }}}} available workflows</p></div></div>
        <div class="search-box"><input type="text" id="search" placeholder="Search workflows..." oninput="filterWorkflows()"></div>
        <div class="workflows-grid" id="grid">{{% for name, wf in workflows %}}<a href="/workflow/{{{{ name }}}}" class="workflow-card" data-name="{{{{ name }}}} {{{{ wf.category }}}} {{{{ wf.description }}}}"><div class="workflow-name">{{{{ name.replace('_', ' ').title() }}}}</div><div class="workflow-desc">{{{{ wf.description }}}}</div><div class="workflow-meta"><span class="badge badge-category">{{{{ wf.category }}}}</span><span class="badge {{{{ 'badge-success' if wf.has_script else 'badge-muted' }}}}">{{{{ 'Script' if wf.has_script else 'Directive' }}}}</span></div></a>{{% endfor %}}</div>
    </main>
    <script>function filterWorkflows() {{ const s = document.getElementById('search').value.toLowerCase(); document.querySelectorAll('.workflow-card').forEach(c => {{ c.style.display = c.dataset.name.toLowerCase().includes(s) ? 'block' : 'none'; }}); }}</script>
</body>
</html>
'''

@app.route('/workflow/<name>')
@login_required
def workflow_detail(name):
    if name not in WORKFLOWS:
        return redirect(url_for('workflows_page'))
    wf = WORKFLOWS[name]
    username = session.get('username', 'admin')
    html_content = markdown_to_html(wf.get('full_description', ''))
    return render_template_string(WORKFLOW_DETAIL_TEMPLATE, name=name, wf=wf, html_content=html_content, sidebar=render_sidebar("workflows", username))

WORKFLOW_DETAIL_TEMPLATE = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ name.replace('_', ' ').title() }}}} — AIAA</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    {BASE_CSS}{THEME_SCRIPT}
</head>
<body>
    {{{{ sidebar | safe }}}}
    <main class="main">
        <a href="/workflows" class="back-btn">← Back to Workflows</a>
        <div class="page-header">
            <div><span class="badge badge-category" style="margin-bottom:0.5rem;">{{{{ wf.category }}}}</span><h1 class="page-title">{{{{ name.replace('_', ' ').title() }}}}</h1><p class="page-subtitle">{{{{ wf.description }}}}</p></div>
            <span class="badge {{{{ 'badge-success' if wf.has_script else 'badge-muted' }}}}" style="font-size:0.875rem;padding:0.5rem 1rem;">{{{{ 'Execution Script Available' if wf.has_script else 'Directive Only' }}}}</span>
        </div>
        <div class="card"><div class="card-body md-content">{{{{ html_content }}}}</div></div>
        {{% if wf.inputs %}}<div class="card"><div class="card-header"><span class="card-title">Inputs</span></div><div class="card-body"><div style="display:flex;flex-wrap:wrap;gap:0.5rem;">{{% for inp in wf.inputs %}}<span class="badge badge-info">{{{{ inp }}}}</span>{{% endfor %}}</div></div></div>{{% endif %}}
        {{% if wf.outputs %}}<div class="card"><div class="card-header"><span class="card-title">Outputs</span></div><div class="card-body"><div style="display:flex;flex-wrap:wrap;gap:0.5rem;">{{% for out in wf.outputs %}}<span class="badge badge-success">{{{{ out }}}}</span>{{% endfor %}}</div></div></div>{{% endif %}}
        <div class="card"><div class="card-header"><span class="card-title">How to Run</span></div><div class="card-body"><pre><code>python3 execution/{{{{ name }}}}.py --help</code></pre></div></div>
    </main>
</body>
</html>
'''

@app.route('/env', methods=['GET', 'POST'])
@login_required
def env_page():
    username = session.get('username', 'admin')
    message = message_type = None
    if request.method == 'POST':
        var_name = request.form.get('var_name', '').strip()
        var_value = request.form.get('var_value', '').strip()
        if var_name and var_value:
            RUNTIME_ENV_VARS[var_name] = var_value
            os.environ[var_name] = var_value
            log_event("env_var", "set", {"variable": var_name}, source="dashboard")
            message, message_type = f"Successfully set {var_name}", "success"
        else:
            message, message_type = "Please provide both name and value", "error"
    env_vars = [{"name": var, "set": bool(os.getenv(var, "") or RUNTIME_ENV_VARS.get(var, "")), "preview": f"{(os.getenv(var, '') or RUNTIME_ENV_VARS.get(var, ''))[:4]}...{(os.getenv(var, '') or RUNTIME_ENV_VARS.get(var, ''))[-4:]}" if len(os.getenv(var, "") or RUNTIME_ENV_VARS.get(var, "")) > 10 else "***" if os.getenv(var, "") or RUNTIME_ENV_VARS.get(var, "") else ""} for var in TRACKED_ENV_VARS]
    return render_template_string(ENV_TEMPLATE, env_vars=env_vars, sidebar=render_sidebar("env", username), message=message, message_type=message_type, tracked_vars=TRACKED_ENV_VARS)

ENV_TEMPLATE = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Environment — AIAA</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    {BASE_CSS}{THEME_SCRIPT}
</head>
<body>
    {{{{ sidebar | safe }}}}
    <main class="main">
        <div class="page-header"><div><h1 class="page-title">Environment Variables</h1><p class="page-subtitle">Manage API keys and configuration</p></div></div>
        {{% if message %}}<div class="alert alert-{{{{ message_type }}}}">{{{{ message }}}}</div>{{% endif %}}
        <div class="card"><div class="card-header"><span class="card-title">Set Environment Variable</span></div><div class="card-body"><form method="POST"><div style="display:grid;grid-template-columns:1fr 2fr auto;gap:1rem;align-items:end;"><div class="form-group" style="margin-bottom:0;"><label class="form-label">Variable Name</label><select name="var_name" class="form-input">{{% for var in tracked_vars %}}<option value="{{{{ var }}}}">{{{{ var }}}}</option>{{% endfor %}}</select></div><div class="form-group" style="margin-bottom:0;"><label class="form-label">Value</label><input type="password" name="var_value" class="form-input" placeholder="Enter API key..."></div><button type="submit" class="btn">Set Variable</button></div></form></div></div>
        <div class="card"><div class="card-header"><span class="card-title">Current Configuration</span></div><ul style="list-style:none;">{{% for var in env_vars %}}<li style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.25rem;border-bottom:1px solid var(--border-subtle);"><span class="mono">{{{{ var.name }}}}</span><div style="display:flex;align-items:center;gap:0.75rem;">{{% if var.set %}}<span class="mono" style="color:var(--text-muted);background:var(--bg-elevated);padding:0.25rem 0.5rem;border-radius:4px;">{{{{ var.preview }}}}</span>{{% else %}}<span style="font-size:0.8125rem;color:var(--text-muted);">Not configured</span>{{% endif %}}<span style="width:8px;height:8px;border-radius:50%;background:{{{{ 'var(--success)' if var.set else 'var(--error)' }}}};"></span></div></li>{{% endfor %}}</ul></div>
        <div style="padding:1rem 1.25rem;background:var(--bg-elevated);border-radius:8px;font-size:0.8125rem;color:var(--text-secondary);"><strong>Note:</strong> Variables set here are stored in memory for this session. For persistent storage, set them in Railway's dashboard.</div>
    </main>
</body>
</html>
'''

@app.route('/workflows')
@app.route('/workflow')  # Keep old route for backward compatibility
@app.route('/webhooks')  # Keep old route for backward compatibility
@login_required
def workflow_page():
    username = session.get('username', 'admin')
    base_url = request.host_url.rstrip('/')
    endpoints = [
        {"method": "GET", "path": "/", "description": "Dashboard"},
        {"method": "GET", "path": "/health", "description": "Health check"},
        {"method": "GET", "path": "/api/events", "description": "Events JSON"},
        {"method": "POST", "path": "/webhook/calendly", "description": "Calendly meeting prep"},
        {"method": "POST", "path": "/webhook/<workflow>", "description": "Generic workflow webhook"}
    ]
    active_workflows = [
        {
            "name": "X Keyword Search → YouTube Content",
            "description": "Searches X for trending posts and generates YouTube video ideas with full outlines",
            "schedule": "Every 3 hours",
            "cron": "0 */3 * * *",
            "status": "active",
            "platform": "Railway Cron",
            "last_run": "Scheduled",
            "project_id": "3b96c81f-9518-4131-b2bc-bcd7a524a5ef",
            "project_url": "https://railway.com/project/3b96c81f-9518-4131-b2bc-bcd7a524a5ef",
            "service_id": "5fbf1961-5c49-41ec-a776-fb4c7723bf69"
        }
    ]
    return render_template_string(WORKFLOW_TEMPLATE, base_url=base_url, endpoints=endpoints, active_workflows=active_workflows, sidebar=render_sidebar("workflow", username))

WORKFLOW_TEMPLATE = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workflow — AIAA</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    {BASE_CSS}{THEME_SCRIPT}
    <style>
        .workflow-card {{
            background: var(--bg-elevated);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            transition: border-color 0.15s;
        }}
        .workflow-card:hover {{
            border-color: var(--accent);
        }}
        .workflow-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }}
        .workflow-name {{
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.25rem;
        }}
        .workflow-desc {{
            color: var(--text-muted);
            font-size: 0.8125rem;
            margin-bottom: 1rem;
        }}
        .workflow-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            font-size: 0.8125rem;
        }}
        .workflow-meta-item {{
            display: flex;
            align-items: center;
            gap: 0.375rem;
        }}
        .workflow-meta-label {{
            color: var(--text-muted);
        }}
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.25rem 0.625rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        .status-active {{
            background: rgba(34, 197, 94, 0.1);
            color: #22c55e;
        }}
        .status-paused {{
            background: rgba(234, 179, 8, 0.1);
            color: #eab308;
        }}
        .status-dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: currentColor;
        }}
        .section-title {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-subtle);
        }}
        .btn-control {{
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            padding: 0.5rem 0.875rem;
            border: none;
            border-radius: 6px;
            font-family: inherit;
            font-size: 0.75rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .btn-start {{
            background: rgba(34, 197, 94, 0.1);
            color: #22c55e;
        }}
        .btn-start:hover {{
            background: rgba(34, 197, 94, 0.2);
        }}
        .schedule-editor {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.375rem 0.5rem;
            background: var(--bg-muted);
            border-radius: 6px;
            font-size: 0.7rem;
        }}
        .schedule-editor select, .schedule-editor input {{
            background: var(--bg-subtle);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
            padding: 0.2rem 0.35rem;
            border-radius: 4px;
            font-size: 0.7rem;
            cursor: pointer;
        }}
        .schedule-editor input[type="number"] {{
            width: 40px;
            text-align: center;
        }}
        .schedule-editor select:focus, .schedule-editor input:focus {{
            outline: none;
            border-color: var(--accent);
        }}
        .schedule-editor .schedule-label {{
            color: var(--text-muted);
            font-size: 0.65rem;
        }}
        .schedule-editor .btn-save {{
            background: var(--accent);
            color: white;
            border: none;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.65rem;
            font-weight: 500;
        }}
        .schedule-editor .btn-save:hover {{
            opacity: 0.9;
        }}
        .schedule-editor .btn-save:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .schedule-editor .current-cron {{
            color: var(--text-muted);
            font-family: monospace;
            font-size: 0.6rem;
            padding: 0.15rem 0.3rem;
            background: var(--bg-subtle);
            border-radius: 3px;
        }}
        .btn-control:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .btn-control.loading {{
            position: relative;
            color: transparent;
        }}
        .btn-control.loading::after {{
            content: "";
            position: absolute;
            width: 14px;
            height: 14px;
            border: 2px solid currentColor;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        .cron-toggle {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.375rem 0.75rem;
            background: var(--bg-muted);
            border-radius: 6px;
            font-size: 0.75rem;
        }}
        .cron-toggle-label {{
            color: var(--text-muted);
        }}
        .toggle-switch {{
            position: relative;
            width: 36px;
            height: 20px;
            background: rgba(239, 68, 68, 0.3);
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .toggle-switch.active {{
            background: rgba(34, 197, 94, 0.3);
        }}
        .toggle-switch::after {{
            content: "";
            position: absolute;
            top: 2px;
            left: 2px;
            width: 16px;
            height: 16px;
            background: #ef4444;
            border-radius: 50%;
            transition: all 0.2s;
        }}
        .toggle-switch.active::after {{
            left: 18px;
            background: #22c55e;
        }}
        .toggle-switch.loading {{
            opacity: 0.5;
            pointer-events: none;
        }}
        .cron-status {{
            font-size: 0.6875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}
        .cron-status.active {{
            color: #22c55e;
        }}
        .cron-status.inactive {{
            color: #ef4444;
        }}
    </style>
</head>
<body>
    {{{{ sidebar | safe }}}}
    <main class="main">
        <div class="page-header">
            <div>
                <h1 class="page-title">Active Workflows</h1>
                <p class="page-subtitle">Running workflow deployments</p>
            </div>
        </div>

        <!-- Webhooks Section -->
        <div class="section-title">Webhooks</div>
        <div style="padding:1rem 1.25rem;background:var(--bg-elevated);border-radius:8px;margin-bottom:1rem;">
            <div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">Base URL</div>
            <code class="mono" style="font-size:0.9375rem;color:var(--accent);">{{{{ base_url }}}}</code>
        </div>
        <div class="card" style="margin-bottom:2rem;">
            <div class="card-header"><span class="card-title">Available Endpoints</span></div>
            {{% for endpoint in endpoints %}}
            <div style="display:flex;align-items:center;gap:1rem;padding:1rem 1.25rem;border-bottom:1px solid var(--border-subtle);">
                <span class="mono badge {{{{ 'badge-success' if endpoint.method == 'GET' else 'badge-info' }}}}" style="min-width:50px;text-align:center;">{{{{ endpoint.method }}}}</span>
                <span class="mono" style="flex:1;">{{{{ endpoint.path }}}}</span>
                <span style="color:var(--text-muted);font-size:0.8125rem;">{{{{ endpoint.description }}}}</span>
            </div>
            {{% endfor %}}
        </div>

        <!-- Active Workflows Section -->
        <div class="section-title">Active Workflows</div>
        {{% if active_workflows %}}
        {{% for wf in active_workflows %}}
        <div class="workflow-card">
            <div class="workflow-header">
                <div>
                    <div class="workflow-name">{{{{ wf.name }}}}</div>
                </div>
                <span class="status-badge status-{{{{ wf.status }}}}">
                    <span class="status-dot"></span>
                    {{{{ wf.status | capitalize }}}}
                </span>
            </div>
            <div class="workflow-desc">{{{{ wf.description }}}}</div>
            <div class="workflow-meta">
                <div class="workflow-meta-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                    <span class="workflow-meta-label">Schedule:</span>
                    <span class="schedule-text" data-service-id="{{{{ wf.service_id }}}}">{{{{ wf.schedule }}}}</span>
                </div>
                <div class="workflow-meta-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
                    <span class="workflow-meta-label">Platform:</span>
                    <span>{{{{ wf.platform }}}}</span>
                </div>
                <div class="workflow-meta-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/></svg>
                    <span class="workflow-meta-label">Cron:</span>
                    <code class="mono" style="font-size:0.75rem;">{{{{ wf.cron }}}}</code>
                </div>
            </div>
            <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border-subtle);display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap;">
                {{% if wf.service_id %}}
                <button onclick="startWorkflow('{{{{ wf.service_id }}}}', '{{{{ wf.name }}}}')" class="btn-control btn-start" title="Run workflow now">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                    Run Now
                </button>
                <div class="cron-toggle" data-service-id="{{{{ wf.service_id }}}}" data-project-id="{{{{ wf.project_id }}}}" data-cron="{{{{ wf.cron }}}}" data-name="{{{{ wf.name }}}}">
                    <span class="cron-toggle-label">Cron:</span>
                    <div class="toggle-switch active" onclick="toggleCron(this)" title="Click to deactivate cron schedule"></div>
                    <span class="cron-status active">Active</span>
                </div>
                <div class="schedule-editor" data-service-id="{{{{ wf.service_id }}}}" data-name="{{{{ wf.name }}}}" data-current="{{{{ wf.cron }}}}">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    <span class="schedule-label">Every</span>
                    <input type="number" class="sched-interval" min="1" max="24" value="3" title="Interval (hours)">
                    <select class="sched-unit">
                        <option value="hours">hours</option>
                        <option value="days">days</option>
                    </select>
                    <span class="schedule-label">at min</span>
                    <input type="number" class="sched-minute" min="0" max="59" value="0" title="Minute (0-59)">
                    <button class="btn-save" onclick="saveSchedule(this)">Save</button>
                    <span class="current-cron" title="Current cron expression">{{{{ wf.cron }}}}</span>
                </div>
                <a href="https://railway.com/project/{{{{ wf.project_id }}}}/service/{{{{ wf.service_id }}}}/settings" target="_blank" class="btn-control" style="background:var(--bg-muted);color:var(--text-muted);" title="Manage cron schedule on Railway">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 00-2 2v.18a2 2 0 01-1 1.73l-.43.25a2 2 0 01-2 0l-.15-.08a2 2 0 00-2.73.73l-.22.38a2 2 0 00.73 2.73l.15.1a2 2 0 011 1.72v.51a2 2 0 01-1 1.74l-.15.09a2 2 0 00-.73 2.73l.22.38a2 2 0 002.73.73l.15-.08a2 2 0 012 0l.43.25a2 2 0 011 1.73V20a2 2 0 002 2h.44a2 2 0 002-2v-.18a2 2 0 011-1.73l.43-.25a2 2 0 012 0l.15.08a2 2 0 002.73-.73l.22-.39a2 2 0 00-.73-2.73l-.15-.08a2 2 0 01-1-1.74v-.5a2 2 0 011-1.74l.15-.09a2 2 0 00.73-2.73l-.22-.38a2 2 0 00-2.73-.73l-.15.08a2 2 0 01-2 0l-.43-.25a2 2 0 01-1-1.73V4a2 2 0 00-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
                    Settings
                </a>
                <button onclick="deleteWorkflow('{{{{ wf.service_id }}}}', '{{{{ wf.name }}}}')" class="btn-control btn-delete" style="background:#fee2e2;color:#dc2626;border:1px solid #fecaca;" title="Delete this workflow from Railway">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                    Delete
                </button>
                {{% endif %}}
                {{% if wf.project_url %}}
                <a href="{{{{ wf.project_url }}}}" target="_blank" style="font-size:0.8125rem;color:var(--accent);text-decoration:none;display:inline-flex;align-items:center;gap:0.375rem;margin-left:auto;">
                    View on Railway
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>
                </a>
                {{% endif %}}
            </div>
        </div>
        {{% endfor %}}
        {{% else %}}
        <div class="card" style="padding:2rem;text-align:center;color:var(--text-muted);">
            No active workflows configured yet.
        </div>
        {{% endif %}}
    </main>
    <script>
        async function startWorkflow(serviceId, name) {{
            const btn = event.target.closest('.btn-control');
            if (btn.classList.contains('loading')) return;

            btn.classList.add('loading');
            try {{
                const response = await fetch('/api/workflow/start', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ service_id: serviceId, name: name }})
                }});
                const data = await response.json();

                if (response.ok) {{
                    showToast(`${{name}} triggered successfully`, 'success');
                }} else {{
                    showToast(data.error || 'Failed to start workflow', 'error');
                }}
            }} catch (err) {{
                showToast('Network error: ' + err.message, 'error');
            }} finally {{
                btn.classList.remove('loading');
            }}
        }}

        async function deleteWorkflow(serviceId, name) {{
            // Confirm deletion
            if (!confirm(`Are you sure you want to delete "${{name}}"?\n\nThis will permanently delete the service from Railway and cannot be undone.`)) {{
                return;
            }}

            const btn = event.target.closest('.btn-control');
            if (btn.classList.contains('loading')) return;

            btn.classList.add('loading');
            btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Deleting...';

            try {{
                const response = await fetch('/api/workflow/delete', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ service_id: serviceId, name: name }})
                }});
                const data = await response.json();

                if (response.ok) {{
                    showToast(`${{name}} deleted successfully`, 'success');
                    // Remove the workflow card from the page
                    const card = btn.closest('.workflow-card');
                    if (card) {{
                        card.style.opacity = '0';
                        card.style.transform = 'translateX(-20px)';
                        card.style.transition = 'all 0.3s ease';
                        setTimeout(() => card.remove(), 300);
                    }}
                }} else {{
                    showToast(data.error || 'Failed to delete workflow', 'error');
                    // Restore button
                    btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg> Delete';
                }}
            }} catch (err) {{
                showToast('Network error: ' + err.message, 'error');
                btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg> Delete';
            }} finally {{
                btn.classList.remove('loading');
            }}
        }}

        // Convert cron expression to human-readable text
        function cronToText(cron) {{
            if (!cron) return 'Not set';
            const parts = cron.split(' ');
            if (parts.length < 5) return cron;

            const [minute, hour, day, month, weekday] = parts;

            // Every N hours
            if (hour.startsWith('*/')) {{
                const interval = hour.substring(2);
                return `Every ${{interval}} hour${{interval === '1' ? '' : 's'}}`;
            }}

            // Every hour
            if (hour === '*') {{
                return minute === '0' ? 'Every hour' : `Every hour at :${{minute.padStart(2, '0')}}`;
            }}

            // Every N days
            if (day.startsWith('*/')) {{
                const interval = day.substring(2);
                return `Every ${{interval}} day${{interval === '1' ? '' : 's'}}`;
            }}

            // Daily at specific hour
            if (day === '*' && month === '*' && weekday === '*') {{
                return `Daily at ${{hour.padStart(2, '0')}}:${{minute.padStart(2, '0')}}`;
            }}

            // Weekly
            if (weekday !== '*') {{
                const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                return `Weekly (${{days[parseInt(weekday)] || weekday}})`;
            }}

            return cron;
        }}

        // Update schedule text display for a service
        function updateScheduleText(serviceId, cron) {{
            const textEl = document.querySelector(`.schedule-text[data-service-id="${{serviceId}}"]`);
            if (textEl) {{
                textEl.textContent = cronToText(cron);
            }}
        }}

        // Initialize schedule editors with current cron values
        function initScheduleEditors() {{
            document.querySelectorAll('.schedule-editor').forEach(editor => {{
                const cron = editor.dataset.current;
                if (!cron) return;

                // Parse cron: minute hour day month weekday
                const parts = cron.split(' ');
                if (parts.length < 5) return;

                const minute = parts[0];
                const hour = parts[1];

                // Set minute
                const minuteInput = editor.querySelector('.sched-minute');
                if (minuteInput && minute !== '*') {{
                    minuteInput.value = parseInt(minute) || 0;
                }}

                // Parse hour pattern
                const intervalInput = editor.querySelector('.sched-interval');
                const unitSelect = editor.querySelector('.sched-unit');

                if (hour.startsWith('*/')) {{
                    // Every N hours pattern
                    intervalInput.value = parseInt(hour.substring(2)) || 1;
                    unitSelect.value = 'hours';
                }} else if (hour === '*') {{
                    // Every hour
                    intervalInput.value = 1;
                    unitSelect.value = 'hours';
                }} else {{
                    // Specific hour - treat as daily at that hour
                    intervalInput.value = 1;
                    unitSelect.value = 'days';
                    // Store the hour for reference
                    editor.dataset.specificHour = hour;
                }}
            }});
        }}

        // Build cron expression from editor values
        function buildCronExpression(editor) {{
            const interval = parseInt(editor.querySelector('.sched-interval').value) || 1;
            const unit = editor.querySelector('.sched-unit').value;
            const minute = parseInt(editor.querySelector('.sched-minute').value) || 0;

            // Validate minute
            const validMinute = Math.max(0, Math.min(59, minute));

            if (unit === 'hours') {{
                if (interval === 1) {{
                    return `${{validMinute}} * * * *`;  // Every hour at minute X
                }} else {{
                    return `${{validMinute}} */${{interval}} * * *`;  // Every N hours at minute X
                }}
            }} else {{
                // Days - run once per day at midnight (or first hour)
                if (interval === 1) {{
                    return `${{validMinute}} 0 * * *`;  // Daily at 00:XX
                }} else {{
                    return `${{validMinute}} 0 */${{interval}} * *`;  // Every N days at 00:XX
                }}
            }}
        }}

        async function saveSchedule(btn) {{
            const editor = btn.closest('.schedule-editor');
            const serviceId = editor.dataset.serviceId;
            const name = editor.dataset.name;
            const newSchedule = buildCronExpression(editor);

            // Add loading state
            btn.disabled = true;
            btn.textContent = '...';
            editor.style.opacity = '0.6';

            try {{
                const response = await fetch('/api/workflow/schedule', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ service_id: serviceId, name: name, cron: newSchedule }})
                }});
                const data = await response.json();

                if (response.ok) {{
                    showToast(`Schedule updated to ${{newSchedule}}`, 'success');
                    // Update the current cron display
                    editor.dataset.current = newSchedule;
                    editor.querySelector('.current-cron').textContent = newSchedule;
                    // Update the schedule text in the workflow card
                    updateScheduleText(serviceId, newSchedule);
                }} else {{
                    showToast(data.error || 'Failed to update schedule', 'error');
                }}
            }} catch (err) {{
                showToast('Network error: ' + err.message, 'error');
            }} finally {{
                btn.disabled = false;
                btn.textContent = 'Save';
                editor.style.opacity = '1';
            }}
        }}

        // Initialize schedule text displays from editor cron values
        function initScheduleTexts() {{
            document.querySelectorAll('.schedule-editor').forEach(editor => {{
                const serviceId = editor.dataset.serviceId;
                const cron = editor.dataset.current;
                if (serviceId && cron) {{
                    updateScheduleText(serviceId, cron);
                }}
            }});
        }}

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {{
            initScheduleEditors();
            initScheduleTexts();
        }});

        async function toggleCron(toggle) {{
            if (toggle.classList.contains('loading')) return;

            const container = toggle.closest('.cron-toggle');
            const serviceId = container.dataset.serviceId;
            const projectId = container.dataset.projectId;
            const cronSchedule = container.dataset.cron;
            const name = container.dataset.name;
            const statusEl = container.querySelector('.cron-status');
            const isActive = toggle.classList.contains('active');

            const action = isActive ? 'deactivate' : 'activate';
            const confirmMsg = isActive
                ? `Deactivate cron for "${{name}}"?\\n\\nThis marks the workflow as inactive in the dashboard.\\nTo fully disable, use the Settings button to manage on Railway.`
                : `Reactivate cron for "${{name}}"?\\n\\nThis marks the workflow as active (${{cronSchedule}}).`;

            if (!confirm(confirmMsg)) return;

            toggle.classList.add('loading');
            try {{
                const response = await fetch(`/api/workflow/cron/${{action}}`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ service_id: serviceId, project_id: projectId, name: name, cron: cronSchedule }})
                }});
                const data = await response.json();

                if (response.ok) {{
                    // Toggle the visual state
                    if (isActive) {{
                        toggle.classList.remove('active');
                        statusEl.classList.remove('active');
                        statusEl.classList.add('inactive');
                        statusEl.textContent = 'Inactive';
                        toggle.title = 'Click to activate cron schedule';
                    }} else {{
                        toggle.classList.add('active');
                        statusEl.classList.remove('inactive');
                        statusEl.classList.add('active');
                        statusEl.textContent = 'Active';
                        toggle.title = 'Click to deactivate cron schedule';
                    }}
                    showToast(data.message || `Cron ${{action}}d successfully`, 'success');
                }} else {{
                    showToast(data.error || `Failed to ${{action}} cron`, 'error');
                }}
            }} catch (err) {{
                showToast('Network error: ' + err.message, 'error');
            }} finally {{
                toggle.classList.remove('loading');
            }}
        }}

        // Check cron status on page load
        document.addEventListener('DOMContentLoaded', async () => {{
            const toggles = document.querySelectorAll('.cron-toggle');
            for (const container of toggles) {{
                const serviceId = container.dataset.serviceId;
                if (!serviceId) continue;

                try {{
                    const response = await fetch(`/api/workflow/cron/status?service_id=${{serviceId}}`);
                    if (response.ok) {{
                        const data = await response.json();
                        const toggle = container.querySelector('.toggle-switch');
                        const statusEl = container.querySelector('.cron-status');

                        if (!data.active) {{
                            toggle.classList.remove('active');
                            statusEl.classList.remove('active');
                            statusEl.classList.add('inactive');
                            statusEl.textContent = 'Inactive';
                            toggle.title = 'Click to activate cron schedule';
                        }}
                    }}
                }} catch (e) {{
                    console.error('Failed to check cron status:', e);
                }}
            }}
        }});

        function showToast(message, type) {{
            const toast = document.createElement('div');
            toast.style.cssText = `
                position: fixed; bottom: 24px; right: 24px; padding: 12px 20px;
                background: ${{type === 'error' ? '#ef4444' : '#22c55e'}}; color: white;
                border-radius: 8px; font-size: 0.875rem; font-weight: 500;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 9999;
                animation: slideIn 0.3s ease;
            `;
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(() => {{
                toast.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }}, 3000);
        }}
    </script>
    <style>
        @keyframes slideIn {{ from {{ transform: translateX(100%); opacity: 0; }} to {{ transform: translateX(0); opacity: 1; }} }}
        @keyframes fadeOut {{ to {{ opacity: 0; transform: translateY(10px); }} }}
        @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
        .spin {{ animation: spin 1s linear infinite; }}
        .btn-delete:hover {{ background: #fecaca !important; border-color: #f87171 !important; }}
        .btn-delete.loading {{ pointer-events: none; opacity: 0.7; }}
    </style>
</body>
</html>
'''

@app.route('/logs')
@login_required
def logs_page():
    username = session.get('username', 'admin')
    with events_lock:
        events = list(events_log)
    return render_template_string(LOGS_TEMPLATE, events=events, sidebar=render_sidebar("logs", username))

LOGS_TEMPLATE = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logs — AIAA</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    {BASE_CSS}{THEME_SCRIPT}
</head>
<body>
    {{{{ sidebar | safe }}}}
    <main class="main">
        <div class="page-header"><div><h1 class="page-title">Event Logs</h1><p class="page-subtitle">System activity and webhook events</p></div></div>
        <div class="card"><table class="table"><thead><tr><th>Timestamp</th><th>Type</th><th>Source</th><th>Data</th><th>Status</th></tr></thead><tbody>{{% if events %}}{{% for event in events %}}<tr><td class="mono">{{{{ event.timestamp[:19] }}}}</td><td>{{{{ event.type }}}}</td><td>{{{{ event.source }}}}</td><td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{{{ event.data | tojson }}}}</td><td><span class="badge badge-{{{{ 'success' if event.status == 'success' else 'error' if event.status == 'error' else 'muted' }}}}">{{{{ event.status }}}}</span></td></tr>{{% endfor %}}{{% else %}}<tr><td colspan="5" class="empty">No events recorded yet.</td></tr>{{% endif %}}</tbody></table></div>
    </main>
    <script>setTimeout(() => location.reload(), 30000);</script>
</body>
</html>
'''

# =============================================================================
# API Endpoints
# =============================================================================

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "aiaa-dashboard", "version": "2.3.0", "workflows": len(WORKFLOWS), "timestamp": datetime.now().isoformat()})

@app.route('/api/events')
def api_events():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    with events_lock:
        return jsonify(list(events_log))

@app.route('/api/workflows')
def api_workflows():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({k: {"description": v["description"], "has_script": v["has_script"], "category": v.get("category", "General")} for k, v in WORKFLOWS.items()})

@app.route('/api/env', methods=['POST'])
def api_set_env():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    if not data or 'name' not in data or 'value' not in data:
        return jsonify({"error": "Missing name or value"}), 400
    RUNTIME_ENV_VARS[data['name']] = data['value']
    os.environ[data['name']] = data['value']
    log_event("env_var", "set", {"variable": data['name']}, source="api")
    return jsonify({"status": "ok", "variable": data['name']})

# =============================================================================
# Workflow Control API (Start/Stop)
# =============================================================================

def railway_api_call(query: str, variables: dict = None) -> dict:
    """Make a GraphQL call to Railway API."""
    if not RAILWAY_API_TOKEN:
        return {"error": "RAILWAY_API_TOKEN not configured"}

    headers = {
        "Authorization": f"Bearer {RAILWAY_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    try:
        response = http_requests.post(RAILWAY_API_URL, json=payload, headers=headers, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@app.route('/api/workflow/start', methods=['POST'])
def api_workflow_start():
    """Trigger an immediate execution of a Railway cron service (bypasses schedule)."""
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or 'service_id' not in data:
        return jsonify({"error": "Missing service_id"}), 400

    service_id = data['service_id']
    workflow_name = data.get('name', 'Unknown')

    # Get the service instance ID (different from service_id)
    instance_query = """
    query service($id: String!) {
        service(id: $id) {
            serviceInstances {
                edges {
                    node {
                        id
                    }
                }
            }
        }
    }
    """

    instance_result = railway_api_call(instance_query, {"id": service_id})
    if "error" in instance_result:
        log_event("workflow", "start_failed", {"service_id": service_id, "error": instance_result.get("error")}, source="api")
        return jsonify(instance_result), 500

    service_instance_id = None
    try:
        edges = instance_result.get("data", {}).get("service", {}).get("serviceInstances", {}).get("edges", [])
        if edges:
            service_instance_id = edges[0]["node"]["id"]
    except (KeyError, IndexError, TypeError):
        pass

    if not service_instance_id:
        log_event("workflow", "start_failed", {"service_id": service_id, "error": "No service instance found"}, source="api")
        return jsonify({"error": "No service instance found - service may not be deployed"}), 500

    # Trigger immediate execution (works for cron jobs - bypasses schedule)
    execute_mutation = """
    mutation deploymentInstanceExecutionCreate($input: DeploymentInstanceExecutionCreateInput!) {
        deploymentInstanceExecutionCreate(input: $input)
    }
    """

    result = railway_api_call(execute_mutation, {"input": {"serviceInstanceId": service_instance_id}})

    if "error" in result or result.get("errors"):
        error_msg = result.get("error") or result.get("errors", [{}])[0].get("message", "Unknown error")
        log_event("workflow", "start_failed", {"service_id": service_id, "error": error_msg}, source="api")
        return jsonify({"error": error_msg}), 500

    log_event("workflow", "executed", {"service_id": service_id, "name": workflow_name, "service_instance_id": service_instance_id}, source="api")
    return jsonify({
        "status": "executed",
        "service_id": service_id,
        "name": workflow_name,
        "message": f"{workflow_name} triggered for immediate execution"
    })


@app.route('/api/workflow/delete', methods=['POST'])
def api_workflow_delete():
    """Delete a Railway service (workflow deployment)."""
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or 'service_id' not in data:
        return jsonify({"error": "Missing service_id"}), 400

    service_id = data['service_id']
    workflow_name = data.get('name', 'Unknown')

    # First verify the service exists
    verify_query = """
    query service($id: String!) {
        service(id: $id) {
            id
            name
        }
    }
    """

    verify_result = railway_api_call(verify_query, {"id": service_id})
    if verify_result.get("errors") or not verify_result.get("data", {}).get("service"):
        error_msg = "Service not found or already deleted"
        if verify_result.get("errors"):
            error_msg = verify_result["errors"][0].get("message", error_msg)
        log_event("workflow", "delete_failed", {"service_id": service_id, "error": error_msg}, source="api")
        return jsonify({"error": error_msg}), 404

    # Delete the service using Railway API
    delete_mutation = """
    mutation serviceDelete($id: String!) {
        serviceDelete(id: $id)
    }
    """

    result = railway_api_call(delete_mutation, {"id": service_id})

    if "error" in result or result.get("errors"):
        error_msg = result.get("error") or result.get("errors", [{}])[0].get("message", "Unknown error")
        log_event("workflow", "delete_failed", {"service_id": service_id, "error": error_msg}, source="api")
        return jsonify({"error": error_msg}), 500

    log_event("workflow", "deleted", {"service_id": service_id, "name": workflow_name}, source="api")
    return jsonify({
        "status": "deleted",
        "service_id": service_id,
        "name": workflow_name,
        "message": f"{workflow_name} has been deleted from Railway"
    })


@app.route('/api/workflow/schedule', methods=['POST'])
def api_workflow_schedule():
    """Update the cron schedule for a workflow."""
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or 'service_id' not in data or 'cron' not in data:
        return jsonify({"error": "Missing service_id or cron"}), 400

    service_id = data['service_id']
    workflow_name = data.get('name', 'Unknown')
    new_cron = data['cron']

    # Get environment ID for the service
    service_query = """
    query service($id: String!) {
        service(id: $id) {
            id
            projectId
            serviceInstances {
                edges {
                    node {
                        environmentId
                    }
                }
            }
        }
    }
    """

    service_result = railway_api_call(service_query, {"id": service_id})

    environment_id = None
    try:
        edges = service_result.get("data", {}).get("service", {}).get("serviceInstances", {}).get("edges", [])
        if edges:
            environment_id = edges[0]["node"]["environmentId"]
    except (KeyError, TypeError, IndexError):
        pass

    if not environment_id:
        log_event("workflow", "schedule_update_failed", {"service_id": service_id, "error": "No environment found"}, source="api")
        return jsonify({"error": "Could not find environment for service"}), 500

    # Update cron schedule via serviceInstanceUpdate
    update_mutation = """
    mutation serviceInstanceUpdate($serviceId: String!, $environmentId: String, $input: ServiceInstanceUpdateInput!) {
        serviceInstanceUpdate(serviceId: $serviceId, environmentId: $environmentId, input: $input)
    }
    """

    update_result = railway_api_call(update_mutation, {
        "serviceId": service_id,
        "environmentId": environment_id,
        "input": {"cronSchedule": new_cron}
    })

    if update_result.get("errors"):
        error_msg = update_result["errors"][0].get("message", "Unknown error")
        log_event("workflow", "schedule_update_failed", {"service_id": service_id, "error": error_msg}, source="api")
        return jsonify({"error": error_msg}), 500

    # Update local cron state
    state = get_cron_state(service_id, new_cron)
    state["active"] = True
    state["original_cron"] = new_cron

    log_event("workflow", "schedule_updated", {"service_id": service_id, "name": workflow_name, "cron": new_cron}, source="api")
    return jsonify({
        "status": "updated",
        "service_id": service_id,
        "name": workflow_name,
        "cron": new_cron,
        "message": f"Schedule updated to {new_cron}"
    })


@app.route('/api/workflow/status', methods=['GET'])
def api_workflow_status():
    """Get status of a Railway service."""
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    service_id = request.args.get('service_id')
    if not service_id:
        return jsonify({"error": "Missing service_id parameter"}), 400

    query = """
    query service($id: String!) {
        service(id: $id) {
            id
            name
            deployments(first: 1) {
                edges {
                    node {
                        id
                        status
                        createdAt
                    }
                }
            }
        }
    }
    """

    result = railway_api_call(query, {"id": service_id})

    if "error" in result:
        return jsonify(result), 500

    try:
        service = result["data"]["service"]
        deployment = service["deployments"]["edges"][0]["node"] if service["deployments"]["edges"] else None
        return jsonify({
            "service_id": service["id"],
            "name": service["name"],
            "status": deployment["status"] if deployment else "no_deployments",
            "last_deploy": deployment["createdAt"] if deployment else None
        })
    except (KeyError, TypeError) as e:
        return jsonify({"error": f"Failed to parse response: {str(e)}"}), 500


# Store cron states locally for tracking
CRON_STATES = {}  # service_id -> {"active": bool, "original_cron": str}

def get_cron_state(service_id: str, original_cron: str) -> dict:
    """Get or initialize cron state for a service."""
    if service_id not in CRON_STATES:
        CRON_STATES[service_id] = {"active": True, "original_cron": original_cron}
    return CRON_STATES[service_id]


@app.route('/api/workflow/cron/deactivate', methods=['POST'])
def api_workflow_cron_deactivate():
    """Deactivate a cron job by removing the cron schedule (keeps service deployed)."""
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or 'service_id' not in data:
        return jsonify({"error": "Missing service_id"}), 400

    service_id = data['service_id']
    workflow_name = data.get('name', 'Unknown')
    original_cron = data.get('cron', '0 */3 * * *')

    # Get environment ID for the service
    service_query = """
    query service($id: String!) {
        service(id: $id) {
            id
            projectId
            serviceInstances {
                edges {
                    node {
                        environmentId
                    }
                }
            }
        }
    }
    """

    service_result = railway_api_call(service_query, {"id": service_id})

    environment_id = None
    project_id = None
    try:
        service_data = service_result.get("data", {}).get("service", {})
        project_id = service_data.get("projectId")
        edges = service_data.get("serviceInstances", {}).get("edges", [])
        if edges:
            environment_id = edges[0]["node"]["environmentId"]
    except (KeyError, TypeError, IndexError):
        pass

    # If no environment from service instances, try getting from project
    if not environment_id and project_id:
        project_query = """
        query project($id: String!) {
            project(id: $id) {
                environments {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
        project_result = railway_api_call(project_query, {"id": project_id})
        try:
            env_edges = project_result.get("data", {}).get("project", {}).get("environments", {}).get("edges", [])
            for edge in env_edges:
                if edge["node"]["name"].lower() == "production":
                    environment_id = edge["node"]["id"]
                    break
            if not environment_id and env_edges:
                environment_id = env_edges[0]["node"]["id"]
        except (KeyError, TypeError, IndexError):
            pass

    if not environment_id:
        log_event("workflow", "cron_deactivate_failed", {"service_id": service_id, "error": "No environment found"}, source="api")
        return jsonify({"error": "Could not find environment for service"}), 500

    # Remove cron schedule via serviceInstanceUpdate (set to null to disable)
    update_mutation = """
    mutation serviceInstanceUpdate($serviceId: String!, $environmentId: String, $input: ServiceInstanceUpdateInput!) {
        serviceInstanceUpdate(serviceId: $serviceId, environmentId: $environmentId, input: $input)
    }
    """

    update_result = railway_api_call(update_mutation, {
        "serviceId": service_id,
        "environmentId": environment_id,
        "input": {"cronSchedule": None}
    })

    if update_result.get("errors"):
        error_msg = update_result["errors"][0].get("message", "Unknown error")
        log_event("workflow", "cron_deactivate_failed", {"service_id": service_id, "error": error_msg}, source="api")
        return jsonify({"error": error_msg}), 500

    # Store state with original cron for re-activation
    state = get_cron_state(service_id, original_cron)
    state["active"] = False
    state["original_cron"] = original_cron

    log_event("workflow", "cron_deactivated", {"service_id": service_id, "name": workflow_name, "original_cron": original_cron}, source="api")
    return jsonify({
        "status": "deactivated",
        "service_id": service_id,
        "name": workflow_name,
        "message": "Cron schedule removed - service still deployed but cron disabled"
    })


@app.route('/api/workflow/cron/activate', methods=['POST'])
def api_workflow_cron_activate():
    """Reactivate a cron job by restoring the cron schedule."""
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or 'service_id' not in data:
        return jsonify({"error": "Missing service_id"}), 400

    service_id = data['service_id']
    workflow_name = data.get('name', 'Unknown')
    original_cron = data.get('cron', '0 */3 * * *')

    # Check if we have a stored original cron schedule
    state = CRON_STATES.get(service_id, {})
    if state.get("original_cron"):
        original_cron = state["original_cron"]

    # Get the service's project and environment info
    service_query = """
    query service($id: String!) {
        service(id: $id) {
            id
            projectId
            serviceInstances {
                edges {
                    node {
                        environmentId
                    }
                }
            }
        }
    }
    """

    service_result = railway_api_call(service_query, {"id": service_id})

    environment_id = None
    project_id = None
    try:
        service_data = service_result.get("data", {}).get("service", {})
        project_id = service_data.get("projectId")
        edges = service_data.get("serviceInstances", {}).get("edges", [])
        if edges:
            environment_id = edges[0]["node"]["environmentId"]
    except (KeyError, TypeError, IndexError):
        pass

    # If no environment from service instances, try getting from project
    if not environment_id and project_id:
        project_query = """
        query project($id: String!) {
            project(id: $id) {
                environments {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
            }
        }
        """
        project_result = railway_api_call(project_query, {"id": project_id})
        try:
            env_edges = project_result.get("data", {}).get("project", {}).get("environments", {}).get("edges", [])
            for edge in env_edges:
                if edge["node"]["name"].lower() == "production":
                    environment_id = edge["node"]["id"]
                    break
            if not environment_id and env_edges:
                environment_id = env_edges[0]["node"]["id"]
        except (KeyError, TypeError, IndexError):
            pass

    if not environment_id:
        log_event("workflow", "cron_activate_failed", {"service_id": service_id, "error": "No environment found"}, source="api")
        return jsonify({"error": "Could not find environment for service"}), 500

    # Restore cron schedule via serviceInstanceUpdate
    update_mutation = """
    mutation serviceInstanceUpdate($serviceId: String!, $environmentId: String, $input: ServiceInstanceUpdateInput!) {
        serviceInstanceUpdate(serviceId: $serviceId, environmentId: $environmentId, input: $input)
    }
    """

    update_result = railway_api_call(update_mutation, {
        "serviceId": service_id,
        "environmentId": environment_id,
        "input": {"cronSchedule": original_cron}
    })

    if update_result.get("errors"):
        error_msg = update_result["errors"][0].get("message", "Unknown error")
        log_event("workflow", "cron_activate_failed", {"service_id": service_id, "error": error_msg}, source="api")
        return jsonify({"error": error_msg}), 500

    # Update state
    state = get_cron_state(service_id, original_cron)
    state["active"] = True

    log_event("workflow", "cron_activated", {"service_id": service_id, "name": workflow_name, "cron": original_cron}, source="api")
    return jsonify({
        "status": "activated",
        "service_id": service_id,
        "name": workflow_name,
        "cron": original_cron,
        "message": f"Cron schedule restored ({original_cron})"
    })


@app.route('/api/workflow/cron/status', methods=['GET'])
def api_workflow_cron_status():
    """Get current cron status by checking if service has an active cron schedule."""
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401

    service_id = request.args.get('service_id')
    if not service_id:
        return jsonify({"error": "Missing service_id parameter"}), 400

    # Check Railway for cron schedule in service instance
    query = """
    query service($id: String!) {
        service(id: $id) {
            serviceInstances {
                edges {
                    node {
                        cronSchedule
                    }
                }
            }
            deployments(first: 1) {
                edges {
                    node {
                        id
                        status
                    }
                }
            }
        }
    }
    """

    result = railway_api_call(query, {"id": service_id})

    try:
        service_data = result.get("data", {}).get("service", {})

        # Check cron schedule
        instance_edges = service_data.get("serviceInstances", {}).get("edges", [])
        cron_schedule = None
        if instance_edges:
            cron_schedule = instance_edges[0]["node"].get("cronSchedule")

        # Check deployment status
        deployment_edges = service_data.get("deployments", {}).get("edges", [])
        deployment_status = "NO_DEPLOYMENT"
        if deployment_edges:
            deployment_status = deployment_edges[0]["node"]["status"]

        # Cron is active if schedule is set (not empty/null)
        is_active = bool(cron_schedule and cron_schedule.strip())

        return jsonify({
            "service_id": service_id,
            "active": is_active,
            "cron_schedule": cron_schedule or "",
            "deployment_status": deployment_status
        })
    except (KeyError, TypeError) as e:
        # Fallback to local state
        state = CRON_STATES.get(service_id, {"active": True})
        return jsonify({
            "service_id": service_id,
            "active": state.get("active", True),
            "deployment_status": "UNKNOWN"
        })


@app.route('/webhook/<workflow_name>', methods=['POST'])
def generic_webhook(workflow_name):
    payload = request.get_json() or {}
    log_event(f"webhook:{workflow_name}", "received", {"workflow": workflow_name}, source="webhook")
    if workflow_name not in WORKFLOWS:
        log_event(f"webhook:{workflow_name}", "error", {"error": "Not found"}, source="webhook")
        return jsonify({"error": f"Workflow '{workflow_name}' not found"}), 404
    log_event(f"webhook:{workflow_name}", "success", {"workflow": workflow_name}, source="webhook")
    return jsonify({"status": "received", "workflow": workflow_name, "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    log_event("system", "started", {"port": port, "workflows": len(WORKFLOWS)})
    print(f"Starting AIAA Dashboard v2.3 on port {port} with {len(WORKFLOWS)} workflows")
    app.run(host="0.0.0.0", port=port, debug=False)
