# SEO Blog Post Writer

## What This Workflow Is
This workflow generates long-form, SEO-optimized blog posts with proper keyword targeting, structure, and CTAs ready for publication.

## What It Does
1. Researches keyword and competitor content
2. Generates SEO-optimized outline
3. Writes full article with proper H1/H2 structure
4. Includes meta title, description, and schema markup
5. Outputs ready-to-publish content

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For content generation
SEMRUSH_API_KEY=your_semrush_key          # For keyword research (optional)
```

### Required Tools
- Python 3.10+
- OpenAI API access

### Installation
```bash
pip install openai requests
```

## How to Run

### Step 1: Research Keyword (Optional)
```bash
python3 execution/research_keyword.py --keyword "cold email tips"
```

### Step 2: Generate Outline
```bash
python3 execution/generate_blog_outline.py \
  --keyword "cold email tips" \
  --competitors 5 \
  --output .tmp/outline.md
```

### Step 3: Write Full Article
```bash
python3 execution/write_blog_post.py \
  --outline .tmp/outline.md \
  --word_count 2500 \
  --tone conversational \
  --output .tmp/article.md
```

### Quick One-Liner
```bash
python3 execution/write_blog_post.py --keyword "cold email tips" --word_count 2500 --tone conversational
```

### Batch Generate
```bash
python3 execution/write_blog_post.py --keywords keywords.txt --batch --output_dir .tmp/articles/
```

## Goal
Generate long-form, SEO-optimized blog posts with proper structure, keywords, and CTAs.

## Inputs
- **Topic/Keyword**: Primary keyword to target
- **Word Count**: 1500, 2500, or 3500+
- **Tone**: Professional, Conversational, Technical
- **Target Audience**: Who's reading
- **CTA**: What action you want readers to take

## Process

### 1. Keyword Research
```bash
python3 execution/research_keyword.py --keyword "[KEYWORD]"
```
- Search volume
- Difficulty
- Related keywords
- Questions people ask
- Competitor content analysis

### 2. Generate Outline
```bash
python3 execution/generate_blog_outline.py \
  --keyword "[KEYWORD]" \
  --competitors 5 \
  --output .tmp/outline.md
```

### 3. Write Article
```bash
python3 execution/write_blog_post.py \
  --outline .tmp/outline.md \
  --word_count 2500 \
  --tone conversational \
  --output .tmp/article.md
```

### 4. Article Structure
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
[Details]

### Step 2: [Action]
[Details]

## [H2: Common Mistakes]
[List with explanations]

## [H2: Expert Tips]
[Advanced insights]

## [H2: FAQ]
### [Question 1]?
[Answer]

### [Question 2]?
[Answer]

## Conclusion
[Summary + CTA]
```

### 5. SEO Checklist
- [ ] Primary keyword in title, H1, first 100 words
- [ ] Secondary keywords in H2s
- [ ] Meta description (150-160 chars)
- [ ] Internal links (3-5)
- [ ] External links (2-3 authoritative)
- [ ] Image alt text with keywords
- [ ] URL slug optimized

## Output
- Full article (Markdown)
- Meta title
- Meta description
- Featured image prompt
- Schema markup (optional)

## Integrations
- OpenAI/Anthropic
- SEO tools (optional)
- WordPress API (auto-publish)

## Cost
- ~$0.30-0.50 per 2500-word article

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_content_strategy.md](../skills/SKILL_BIBLE_hormozi_content_strategy.md)**
- 30-day content strategy framework
- Content that drives business results
- Engagement and value optimization

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- 14 years of marketing advice
- Content marketing principles
- Audience building strategies

**[SKILL_BIBLE_hormozi_lead_generation.md](../skills/SKILL_BIBLE_hormozi_lead_generation.md)**
- Content as lead generation tool
- Blog-to-lead conversion
- Value-first content approach

**[SKILL_BIBLE_hormozi_persuasion_speaking.md](../skills/SKILL_BIBLE_hormozi_persuasion_speaking.md)**
- Compelling writing techniques
- Hook and engagement formulas
- Persuasive content structure
