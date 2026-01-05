# SEO Audit Automation

## What This Workflow Is
This workflow crawls a website, analyzes technical SEO factors, and generates a comprehensive audit report with prioritized fixes and AI-powered recommendations.

## What It Does
1. Crawls the target website (up to specified depth)
2. Checks Core Web Vitals and page speed
3. Analyzes on-page SEO elements (titles, metas, headers)
4. Identifies broken links, redirect chains, and crawl issues
5. Generates prioritized report with fix instructions

## Prerequisites

### Required API Keys (add to .env)
```
PAGESPEED_API_KEY=your_google_key         # Get from Google Cloud Console
OPENAI_API_KEY=your_openai_key            # For AI recommendations
AHREFS_API_KEY=your_ahrefs_key            # Optional for backlinks
```

### Required Tools
- Python 3.10+
- Google PageSpeed Insights API access
- Optional: Ahrefs/Moz for backlink analysis

### Installation
```bash
pip install beautifulsoup4 requests openai lxml
```

## How to Run

### Step 1: Crawl Website
```bash
python3 execution/run_seo_audit.py \
  --url "https://example.com" \
  --depth 3 \
  --output .tmp/audit_data.json
```

### Step 2: Generate Report
```bash
python3 execution/generate_seo_report.py \
  --data .tmp/audit_data.json \
  --format pdf \
  --output .tmp/seo_report.pdf
```

### Step 3: Compare to Competitors (Optional)
```bash
python3 execution/run_seo_audit.py \
  --url "https://example.com" \
  --competitors "competitor1.com,competitor2.com" \
  --output .tmp/audit_data.json
```

### Quick One-Liner
```bash
python3 execution/run_seo_audit.py --url "https://example.com" --depth 2 && \
python3 execution/generate_seo_report.py --data .tmp/audit_data.json --format pdf
```

### Weekly Automated Audit (Cron)
```bash
0 9 * * 1 cd /path/to/project && python3 execution/run_seo_audit.py --url "https://yoursite.com" --email "you@company.com"
```

## Goal
Run comprehensive technical SEO audits and generate actionable reports with AI-powered recommendations.

## Inputs
- **Website URL**: Site to audit
- **Competitor URLs**: 2-3 competitor sites (optional)
- **Focus Areas**: Technical, Content, Backlinks, or All
- **Report Format**: PDF, Google Doc, or Sheet

## Tools/Scripts
- `execution/run_seo_audit.py` - Crawl and analyze
- `execution/generate_seo_report.py` - Create report

## Process

### 1. Crawl Website
```bash
python3 execution/run_seo_audit.py \
  --url "https://example.com" \
  --depth 3 \
  --output .tmp/audit_data.json
```

### 2. Audit Areas

**Technical SEO**
- Site speed (Core Web Vitals)
- Mobile-friendliness
- HTTPS status
- XML sitemap
- Robots.txt
- Crawl errors
- Broken links (4xx, 5xx)
- Redirect chains
- Canonical tags
- Schema markup

**On-Page SEO**
- Title tags (length, uniqueness)
- Meta descriptions
- H1-H6 structure
- Image alt text
- Internal linking
- Content length
- Keyword density

**Content Analysis**
- Thin content pages
- Duplicate content
- Content gaps vs competitors
- Readability score

**Backlink Profile**
- Domain authority
- Referring domains
- Toxic links
- Anchor text distribution

### 3. Generate Report
```bash
python3 execution/generate_seo_report.py \
  --data .tmp/audit_data.json \
  --output .tmp/seo_report.pdf
```

### 4. Report Structure

```markdown
# SEO Audit Report
**Website:** [URL]
**Date:** [Date]
**Overall Score:** [X/100]

## Executive Summary
[AI-generated summary of findings]

## Critical Issues (Fix Immediately)
🔴 [Issue 1] - [Impact] - [How to Fix]
🔴 [Issue 2] - [Impact] - [How to Fix]

## Warnings (Address Soon)
🟡 [Issue 1] - [Impact] - [How to Fix]
🟡 [Issue 2] - [Impact] - [How to Fix]

## Technical SEO [Score: X/100]
### Core Web Vitals
- LCP: X.Xs (Target: <2.5s) ✅/❌
- FID: Xms (Target: <100ms) ✅/❌
- CLS: X.XX (Target: <0.1) ✅/❌

### Crawlability
- Pages crawled: X
- Indexable pages: X
- Blocked by robots.txt: X

### Issues Found
| Issue | Count | Priority |
|-------|-------|----------|
| Broken links | 12 | High |
| Missing alt text | 45 | Medium |
| Redirect chains | 8 | Medium |

## On-Page SEO [Score: X/100]
### Title Tags
- Missing: X pages
- Too long: X pages
- Duplicate: X pages

### Meta Descriptions
- Missing: X pages
- Too short: X pages

## Content Analysis [Score: X/100]
- Thin content pages: X
- Average word count: X
- Content gaps: [List]

## Competitor Comparison
| Metric | You | Competitor 1 | Competitor 2 |
|--------|-----|--------------|--------------|
| Domain Authority | X | X | X |
| Indexed Pages | X | X | X |
| Backlinks | X | X | X |

## Action Plan (Priority Order)
1. [Action 1] - Est. impact: High
2. [Action 2] - Est. impact: High
3. [Action 3] - Est. impact: Medium
```

## Integrations Required
- Screaming Frog or custom crawler
- PageSpeed Insights API
- Ahrefs/Moz API (backlinks)
- OpenAI (recommendations)

## Cost Estimate
- Crawling: Free (self-hosted)
- APIs: ~$0.50-1.00/audit
- AI analysis: ~$0.20/report

## Automation Options
- Weekly automated audits
- Alert on critical issues
- Track improvements over time
