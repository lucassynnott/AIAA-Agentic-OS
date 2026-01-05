# Brand Mention Monitor

## What This Workflow Is
This workflow monitors brand mentions across social media, news, forums, and the web to manage reputation and identify engagement opportunities.

## What It Does
1. Configures monitoring for brand names and keywords
2. Scans Twitter, Reddit, news, and web daily
3. Categorizes mentions (positive/negative/neutral)
4. Sends daily digest with action items
5. Alerts immediately on negative mentions

## Prerequisites

### Required API Keys (add to .env)
```
TWITTER_API_KEY=your_twitter_key          # For Twitter monitoring
REDDIT_CLIENT_ID=your_reddit_id           # For Reddit monitoring
OPENAI_API_KEY=your_openai_key            # For sentiment analysis
```

### Required Tools
- Python 3.10+
- Social media API access
- OR Brand24/Mention subscription

### Installation
```bash
pip install tweepy praw requests openai
```

## How to Run

### Step 1: Configure Monitoring
```bash
python3 execution/setup_brand_monitor.py \
  --brands "YourCompany,Product1" \
  --keywords "industry term" \
  --platforms "twitter,reddit,news"
```

### Step 2: Run Daily Scan
```bash
python3 execution/scan_brand_mentions.py --output .tmp/mentions.json
```

### Step 3: Generate Digest
```bash
python3 execution/generate_mention_digest.py --mentions .tmp/mentions.json
```

### Quick One-Liner
```bash
python3 execution/scan_brand_mentions.py && python3 execution/generate_mention_digest.py
```

## Goal
Track brand mentions across web and social to manage reputation and find opportunities.

## Inputs
- **Brand Names**: Your company, products, key people
- **Keywords**: Related terms to track
- **Competitors**: Their brand names
- **Platforms**: Web, Twitter, Reddit, LinkedIn, News

## Process

### 1. Configure Monitoring
```bash
python3 execution/setup_brand_monitor.py \
  --brands "YourCompany,Product1" \
  --keywords "industry term,competitor name" \
  --platforms "twitter,reddit,news,web"
```

### 2. Sources to Monitor
- Twitter/X mentions and hashtags
- Reddit discussions
- News articles
- Blog posts
- LinkedIn mentions
- YouTube comments
- Forum discussions
- Review sites

### 3. Alert Categories

**Positive Mentions:**
- Thank/engage
- Request testimonial
- Amplify content

**Negative Mentions:**
- Respond promptly
- Address concerns
- Escalate if serious

**Competitor Mentions:**
- Join conversation
- Note sentiment
- Identify opportunities

**Questions About You:**
- Answer directly
- Provide resources
- Build relationship

### 4. Daily Digest
```markdown
# Brand Mentions Report
**Date:** [DATE]

## Summary
- Total mentions: X
- Positive: X
- Negative: X
- Neutral: X

## Action Required
🔴 [Negative mention needing response]
- Source: [Platform]
- [Quote/summary]
- [Link]

## Opportunities
🟢 [Positive mention to engage]

## Competitor Activity
[Competitor] mentioned X times
- Key themes: [themes]
```

### 5. Response Templates

**Positive:**
```
Thanks for the kind words, [NAME]! We're glad 
[specific thing] is working well for you. 🙌
```

**Negative:**
```
Hey [NAME], sorry to hear this. DM us and we'll 
make it right. We take this seriously.
```

## Integrations
- Brand24 or Mention
- Twitter API
- Google Alerts
- Reddit API

## Cost
- Mention tools: $50-200/mo
- Custom setup: Free
