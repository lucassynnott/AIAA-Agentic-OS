# Newsletter Writer

## What This Workflow Is
This workflow generates email newsletters by curating relevant content from RSS feeds, social media, and news sources, then formatting it with original commentary and clear CTAs.

## What It Does
1. Gathers content from specified RSS feeds and social accounts
2. Filters and selects most relevant items
3. Generates commentary and insights for each section
4. Formats into email-ready HTML
5. Optionally sends via your email platform

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For content generation
CONVERTKIT_API_KEY=your_convertkit_key    # Or MAILCHIMP, SENDGRID
```

### Required Tools
- Python 3.10+
- OpenAI API access
- Email platform account

### Installation
```bash
pip install openai requests feedparser
```

## How to Run

### Step 1: Gather Content
```bash
python3 execution/gather_newsletter_content.py \
  --topic "cold email" \
  --sources "twitter,linkedin,rss" \
  --output .tmp/content.json
```

### Step 2: Generate Newsletter
```bash
python3 execution/generate_newsletter.py \
  --content .tmp/content.json \
  --template weekly \
  --tone casual \
  --output .tmp/newsletter.html
```

### Step 3: Send Newsletter
```bash
python3 execution/send_newsletter.py \
  --html .tmp/newsletter.html \
  --list "newsletter_subscribers" \
  --subject "Cold Email Weekly: 5 New Tactics" \
  --from "you@domain.com"
```

### Quick One-Liner
```bash
python3 execution/gather_newsletter_content.py --topic "cold email" && \
python3 execution/generate_newsletter.py --content .tmp/content.json --template weekly && \
python3 execution/send_newsletter.py --html .tmp/newsletter.html --list "subscribers"
```

### Weekly Automation (Cron)
```bash
0 8 * * 2 cd /path/to/project && python3 execution/run_weekly_newsletter.py
```

## Goal
Generate engaging email newsletters with curated content, original insights, and clear CTAs.

## Inputs
- **Newsletter Topic**: Main theme
- **Audience**: Who's receiving
- **Frequency**: Daily, Weekly, Monthly
- **Sections**: News, Tips, Tools, etc.
- **Tone**: Professional, Casual, Witty

## Tools/Scripts
- `execution/generate_newsletter.py` - Content generation
- `execution/send_newsletter.py` - Email delivery

## Process

### 1. Content Gathering
```bash
python3 execution/gather_newsletter_content.py \
  --topic "cold email" \
  --sources "twitter,linkedin,rss" \
  --output .tmp/content.json
```

Sources:
- RSS feeds (industry blogs)
- Twitter/X (thought leaders)
- LinkedIn posts
- News sites
- Product Hunt (tools)

### 2. Generate Newsletter
```bash
python3 execution/generate_newsletter.py \
  --content .tmp/content.json \
  --template weekly \
  --tone casual \
  --output .tmp/newsletter.html
```

### 3. Newsletter Structure

```markdown
# [NEWSLETTER NAME]
**Edition #[X] | [Date]**

---

## 👋 Hey [NAME],

[Personal intro - 2-3 sentences on theme]

Here's what's inside:
• [Section 1]
• [Section 2]
• [Section 3]

---

## 📰 This Week's News

**[Headline 1]**
[2-3 sentence summary]
[Link]

**[Headline 2]**
[2-3 sentence summary]
[Link]

---

## 💡 Tip of the Week

**[Tip Title]**

[Actionable tip in 3-5 sentences]

Example: [Concrete example]

---

## 🛠️ Tool Spotlight

**[Tool Name]** - [One-line description]

What it does: [Explanation]
Best for: [Use case]
Pricing: [Cost]
[Link]

---

## 📊 Stat That Matters

> "[Interesting statistic]"

What this means: [Brief analysis]

---

## 🎯 Action Item

This week, try: [Specific action reader can take]

---

## 🔗 Quick Links
- [Resource 1]
- [Resource 2]
- [Resource 3]

---

That's all for this week!

Hit reply and let me know [question/feedback request].

[Sign-off],
[Your Name]

---

[Unsubscribe] | [Preferences] | [Forward to a friend]
```

### 4. Subject Line Options
Generate 3-5 options:
- "[Topic] Weekly: [Hook]"
- "The [X] thing about [topic] this week"
- "[Number] things you missed in [topic]"

### 5. Send Newsletter
```bash
python3 execution/send_newsletter.py \
  --html .tmp/newsletter.html \
  --list "newsletter_subscribers" \
  --subject "[SUBJECT]" \
  --from "name@domain.com"
```

## Newsletter Types

### Curated
Collect and comment on best content from others.

### Original
Your own insights, frameworks, stories.

### Hybrid
Mix of curated + original (most common).

### News Digest
Industry news with brief commentary.

## Integrations Required
- OpenAI/Anthropic (content generation)
- RSS reader (content gathering)
- Email service (ConvertKit, Mailchimp, SendGrid)

## Cost Estimate
- AI generation: ~$0.10-0.20/newsletter
- Email delivery: Based on list size

## Best Practices
- Consistent send time/day
- Mobile-optimized design
- Clear unsubscribe option
- Segment by engagement
- A/B test subject lines

## Related Skill Bibles

### PRIMARY: Max Sturtevant's $40M+ Email Methodology

**[SKILL_BIBLE_sturtevant_email_master_system.md](../skills/SKILL_BIBLE_sturtevant_email_master_system.md)** ⭐ ESSENTIAL
- SCE Framework (Skimmable, Clear, Engaging)
- Email structure principles
- 75-word body copy guideline

**[SKILL_BIBLE_sturtevant_copywriting.md](../skills/SKILL_BIBLE_sturtevant_copywriting.md)**
- Subject line formulas (5,395 words)
- Email copywriting tactics
- CTA optimization

**[SKILL_BIBLE_sturtevant_deliverability.md](../skills/SKILL_BIBLE_sturtevant_deliverability.md)**
- List health for newsletters (5,464 words)
- Inbox placement optimization
- Engagement metrics

### SUPPLEMENTARY

**[SKILL_BIBLE_hormozi_content_strategy.md](../skills/SKILL_BIBLE_hormozi_content_strategy.md)**
- Value-driven content creation
- Audience engagement

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Newsletter positioning
- List building strategies
