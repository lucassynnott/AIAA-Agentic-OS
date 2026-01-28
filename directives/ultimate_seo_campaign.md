# Ultimate SEO Campaign Generator

## What This Workflow Is
**Complete SEO strategy and content system** that handles keyword research, content planning, on-page optimization, and technical audits. Produces keyword maps, content briefs, meta tag recommendations, and link building strategies. Built for SEO agencies and in-house teams.

## What It Does
1. Conducts comprehensive keyword research
2. Analyzes competitor rankings and content
3. Creates content strategy and calendar
4. Generates SEO-optimized content briefs
5. Produces on-page optimization checklists
6. Performs technical SEO audit
7. Creates link building outreach templates
8. Tracks ranking progress

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
PERPLEXITY_API_KEY=your_key           # Competitive research
AHREFS_API_KEY=your_key               # Keyword/backlink data (optional)
SEMRUSH_API_KEY=your_key              # Alternative SEO data (optional)
```

### Required Skill Bibles
- `SKILL_BIBLE_lead_generation_mastery.md` (SEO section)
- `SKILL_BIBLE_content_marketing.md`
- `SKILL_BIBLE_content_strategy_growth.md`
- `SKILL_BIBLE_blog_post_writing.md`

## How to Run

```bash
# Full SEO campaign
python3 execution/generate_seo_campaign.py \
  --client "Acme Corp" \
  --website "https://acmecorp.com" \
  --industry "B2B SaaS" \
  --target-keywords "project management software, team collaboration tool" \
  --competitors "monday.com, asana.com, clickup.com" \
  --monthly-content 8

# Content-only campaign
python3 execution/generate_seo_campaign.py \
  --client "Acme Corp" \
  --keywords-file keywords.csv \
  --content-briefs-only \
  --monthly-content 12

# Technical audit only
python3 execution/generate_seo_campaign.py \
  --website "https://acmecorp.com" \
  --technical-audit-only
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client | string | Yes | Client name |
| website | string | Yes | Target website URL |
| industry | string | Yes | Industry/niche |
| target-keywords | list | Yes | Primary keywords |
| competitors | list | No | Competitor websites |
| monthly-content | int | No | Content pieces per month |
| keywords-file | path | No | Existing keyword research |
| content-briefs-only | flag | No | Skip audit, just briefs |
| technical-audit-only | flag | No | Only technical audit |

## Process

### Phase 1: Keyword Research

**Seed Keyword Expansion:**
- Related keywords
- Long-tail variations
- Question keywords
- Commercial intent keywords
- Informational keywords

**Keyword Metrics:**
- Search volume
- Keyword difficulty
- CPC (commercial intent)
- Current ranking
- SERP features

**Keyword Categorization:**
- Pillar topics (high volume, high competition)
- Cluster topics (medium volume, medium competition)
- Quick wins (low competition, ranking potential)
- Money keywords (high commercial intent)

### Phase 2: Competitor Analysis

**Content Gap Analysis:**
- Keywords competitors rank for (we don't)
- Content topics they cover
- Content formats that perform
- Backlink profile comparison

**SERP Analysis:**
- Top 10 results for target keywords
- Content length analysis
- Header structure patterns
- Featured snippet opportunities
- People Also Ask questions

### Phase 3: Content Strategy

**Pillar-Cluster Model:**
```
Pillar Page: [Main Topic]
├── Cluster 1: [Subtopic]
│   ├── Blog Post 1
│   ├── Blog Post 2
│   └── Blog Post 3
├── Cluster 2: [Subtopic]
│   ├── Blog Post 1
│   └── Blog Post 2
└── Cluster 3: [Subtopic]
    └── Blog Post 1
```

**Content Calendar:**
- 12-month content plan
- Publishing cadence
- Topic prioritization
- Seasonal opportunities
- Evergreen vs. timely content

### Phase 4: Content Brief Generation

For each content piece:

**Brief Sections:**
- Target keyword + secondary keywords
- Search intent analysis
- Recommended word count
- Header structure (H1, H2, H3)
- Topics to cover
- Questions to answer (PAA)
- Internal linking targets
- External linking suggestions
- Competitor content analysis
- Unique angle/value add

**Meta Tag Recommendations:**
- Title tag (60 chars)
- Meta description (155 chars)
- URL slug
- Featured image alt text

### Phase 5: On-Page Optimization Audit

**Page-by-Page Checklist:**
- [ ] Title tag optimized
- [ ] Meta description compelling
- [ ] H1 contains primary keyword
- [ ] Headers follow logical hierarchy
- [ ] Keyword in first 100 words
- [ ] Internal links added
- [ ] External links to authority sites
- [ ] Images optimized (alt text, compression)
- [ ] Schema markup added
- [ ] URL structure clean

**Site-Wide Optimization:**
- Navigation structure
- Category/tag organization
- Orphan page identification
- Duplicate content issues
- Cannibalization analysis

### Phase 6: Technical SEO Audit

**Crawlability:**
- Robots.txt configuration
- XML sitemap status
- Crawl errors
- Index coverage
- Canonical tags

**Performance:**
- Core Web Vitals (LCP, FID, CLS)
- Page speed scores
- Mobile usability
- HTTPS security
- Structured data

**Issues Identified:**
- Broken links (4xx errors)
- Server errors (5xx)
- Redirect chains
- Missing meta tags
- Thin content pages

### Phase 7: Link Building Strategy

**Outreach Templates:**
- Guest post pitches
- Resource page outreach
- Broken link building
- HARO responses
- Competitor backlink replication

**Link Building Tactics:**
- Create linkable assets
- Digital PR opportunities
- Podcast guest appearances
- Industry directories
- Partnership opportunities

## Output Structure
```
.tmp/seo_campaigns/{client_slug}/
├── research/
│   ├── keyword_research.csv
│   ├── competitor_analysis.md
│   └── serp_analysis.json
├── strategy/
│   ├── content_strategy.md
│   ├── pillar_cluster_map.md
│   └── content_calendar.csv
├── briefs/
│   ├── brief_001_[keyword].md
│   ├── brief_002_[keyword].md
│   └── ...
├── optimization/
│   ├── on_page_audit.md
│   └── page_recommendations/
├── technical/
│   ├── technical_audit.md
│   └── issues_prioritized.csv
├── link_building/
│   ├── strategy.md
│   └── outreach_templates.md
└── result.json
```

## Content Brief Template

```markdown
# Content Brief: {Primary Keyword}

## Overview
- **Primary Keyword:** {keyword}
- **Secondary Keywords:** {list}
- **Search Intent:** {informational/commercial/transactional}
- **Target Word Count:** {X-Y words}
- **Difficulty:** {easy/medium/hard}

## SERP Analysis
- **Current Top 3:**
  1. {URL} - {word count} words
  2. {URL} - {word count} words
  3. {URL} - {word count} words

## Recommended Structure

### H1: {Headline with keyword}

### H2: {Section 1}
- Cover: {topics}
- Include: {data points}

### H2: {Section 2}
- Cover: {topics}
- Answer: {PAA questions}

### H2: {Section 3}
- Cover: {topics}
- Add: {examples/case studies}

## Questions to Answer (PAA)
1. {Question 1}
2. {Question 2}
3. {Question 3}

## Internal Links
- Link to: {page 1}
- Link to: {page 2}
- Link from: {existing page}

## Unique Angle
{What makes this piece different from competitors}

## Meta Tags
- **Title:** {60 chars max}
- **Description:** {155 chars max}
- **URL:** /{slug}
```

## Quality Gates

### Pre-Publish Checklist
- [ ] Primary keyword in title
- [ ] Keyword in first 100 words
- [ ] All H2s address subtopics
- [ ] Images have alt text
- [ ] Internal links added (3-5)
- [ ] External links to authority sources
- [ ] Meta tags optimized
- [ ] Schema markup added
- [ ] Mobile formatting checked
- [ ] Readability score 60+

### Performance Benchmarks
| Metric | Target |
|--------|--------|
| Time to Index | <7 days |
| First Page Ranking | <90 days |
| Organic Traffic Growth | 20%+ MoM |
| Backlinks Acquired | 5+ per month |

## Error Handling

| Error | Solution |
|-------|----------|
| No keyword data | Use Perplexity research |
| Competitor site blocked | Manual analysis |
| Thin content warning | Expand brief scope |
| Cannibalization detected | Consolidate or differentiate |

## Integration with Other Workflows

- `blog_post_writer.md` - Content generation
- `content_calendar_generator.md` - Planning
- `client_reporting.md` - Performance tracking
- `landing_page_generator.md` - Conversion pages

## Self-Annealing Notes

### What Works
- Pillar-cluster model for authority
- Long-form (2000+ words) for competitive keywords
- Regular content publishing (weekly minimum)
- Strategic internal linking

### What Doesn't Work
- Keyword stuffing
- Thin content pages
- Ignoring search intent
- Publishing without promotion

### Continuous Improvement
- Track keyword movement weekly
- Refresh top performers quarterly
- Prune underperformers annually
- Monitor algorithm updates
