# Analyze Cold Email Performance

## Skill Overview
This skill guides you through analyzing cold email campaign performance using key metrics, identifying issues, and optimizing campaigns for better results.

## Table of Contents
1. [Understanding Cold Email KPIs](#understanding-cold-email-kpis)
2. [The Golden KPI](#the-golden-kpi)
3. [Key Metrics Breakdown](#key-metrics-breakdown)
4. [Campaign Economics](#campaign-economics)
5. [Troubleshooting Framework](#troubleshooting-framework)
6. [Optimization Strategies](#optimization-strategies)

## Understanding Cold Email KPIs

Cold email success is measured through a funnel of metrics that indicate campaign health and ROI.

### The Cold Email Funnel

```
1,000 Prospects Contacted
    ↓
500-600 Emails Opened (50-60% open rate)
    ↓
20-40 Total Replies (2-4% reply rate)
    ↓
2.5-5 Positive Replies (0.25-0.5% positive rate)
    ↓
2-4 Calls Booked (0.2-0.4% booking rate)
    ↓
1 Deal Closed (0.1% close rate)
```

### What "Good" Looks Like

**Standard benchmarks:**
- Open Rate: 50-60%
- Total Reply Rate: 2-4%
- Positive Reply Rate: 0.25-0.5%
- Calls Booked: 2-4 per 1,000
- Deals Closed: 1 per 1,000

**Important:** These are averages. Your results will vary based on offer, industry, and ICP.

## The Golden KPI

### 1 Deal Per 1,000 Prospects

This is the north star metric for cold email campaigns.

**Why it's the golden KPI:**
- Simple to track
- Directly ties to revenue
- Accounts for entire funnel
- Easy to scale linearly

**Linear scalability:**
- 1,000 prospects = 1 deal
- 10,000 prospects = 10 deals
- 100,000 prospects = 100 deals

**What if you're not hitting it?**
- 1 deal per 2,000 = Acceptable
- 1 deal per 4,000 = Still profitable (but optimize)
- 1 deal per 10,000 = Major issues (pause and fix)

### Cost Per Acquisition

At 1 deal per 1,000 prospects:

**Cost breakdown:**
- **Smartlead:** $100/month (for 10 email accounts)
- **Domains:** $20/month (for secondary domains)
- **Tools (validation, etc.):** $0-50/month
- **Total:** ~$120/month per 1,000 prospects contacted

**CAC at scale:**
- 1,000 prospects = $120 CAC
- 2,000 prospects = $240 CAC
- 4,000 prospects = $480 CAC

**Acceptable range:** $120-480 CAC depending on customer LTV.

## Key Metrics Breakdown

### 1. Open Rate: 50-60%

**What it measures:**
Percentage of recipients who opened your email.

**Benchmark:**
- Good: 50-60%
- Average: 40-50%
- Poor: Under 40%

**Important note:** DO NOT track open rates.

**Why?**
- Open tracking uses invisible pixels
- Spam filters detect tracking pixels
- Tanks deliverability
- Not worth the data

**What to do instead:**
- Disable open tracking in Smartlead
- Focus on reply rate instead
- Assume 50-60% if you need to estimate

### 2. Total Reply Rate: 2-4%

**What it measures:**
Percentage of prospects who replied (any type of reply).

**Calculation:**
```
Total replies ÷ Total prospects contacted = Reply rate

Example: 30 replies ÷ 1,000 prospects = 3% reply rate
```

**Benchmark:**
- Good: 2-4%
- Average: 1-2%
- Poor: Under 1%

**What counts as a reply:**
- "Interested, tell me more"
- "Not interested"
- "Remove me"
- "Out of office"
- Any response = reply

**Expected volume:**
- 1,000 prospects = 20-40 total replies
- 10,000 prospects = 200-400 total replies

**If reply rate is low:**
- Deliverability issue (see troubleshooting)
- Poor targeting (wrong ICP)
- Bad subject lines

### 3. Positive Reply Rate: 0.25-0.5%

**What it measures:**
Percentage of prospects who replied with positive interest.

**Calculation:**
```
Positive replies ÷ Total prospects contacted = Positive reply rate

Example: 4 positive ÷ 1,000 prospects = 0.4% positive rate
```

**Benchmark:**
- Good: 0.25-0.5% (standard)
- Excellent: 3-10% (no-brainer offer)
- Poor: 0.1-0.2% (hard sell like cybersecurity)

**What counts as positive:**
- "Interested"
- "Tell me more"
- "What are your prices?"
- "Let's schedule a call"
- "Send me information"

**What does NOT count:**
- "Not interested"
- "Remove me"
- "Not right now"
- "Out of office"

**Expected volume:**
- 1,000 prospects = 2.5-5 positive replies
- 10,000 prospects = 25-50 positive replies

**If positive reply rate is low:**
- Copy issue (not compelling)
- Product-market fit issue
- Offer not clear/attractive
- Wrong ICP

### 4. Meeting Booked Rate: 0.2-0.4%

**What it measures:**
Percentage of prospects who booked a call.

**Calculation:**
```
Calls booked ÷ Total prospects contacted = Booking rate

Example: 3 calls booked ÷ 1,000 prospects = 0.3% booking rate
```

**Benchmark:**
- Good: 2-4 calls per 1,000 prospects
- Average: 1-2 calls per 1,000 prospects
- Poor: Under 1 call per 1,000 prospects

**Expected volume:**
- 1,000 prospects = 2-4 calls
- 10,000 prospects = 20-40 calls

**Conversion from positive replies:**
- 2.5-5 positive replies → 2-4 calls booked
- Roughly 80% of positive replies should book calls

**If booking rate is low:**
- Sales/inbox management issue
- Slow response time
- Poor qualification
- Unclear booking process

### 5. Deal Closed Rate: 0.1%

**What it measures:**
Percentage of prospects who became paying customers.

**Calculation:**
```
Deals closed ÷ Total prospects contacted = Close rate

Example: 1 deal ÷ 1,000 prospects = 0.1% close rate
```

**Benchmark:**
- Good: 1 deal per 1,000 prospects (0.1%)
- Acceptable: 1 deal per 2,000-4,000 prospects
- Poor: 1 deal per 10,000+ prospects

**Expected volume:**
- 1,000 prospects = 1 deal
- 10,000 prospects = 10 deals
- 100,000 prospects = 100 deals

**Conversion from calls:**
- 2-4 calls booked → 1 deal closed
- Roughly 25-50% close rate on calls

**If close rate is low:**
- Sales issue
- Poor call performance
- Weak offer
- Pricing misalignment
- Unqualified leads making it to calls

## Campaign Economics

### Cost Structure

**Per 1,000 prospects contacted:**

| Item | Cost |
|------|------|
| Smartlead (10 accounts) | $100 |
| Secondary domains | $20 |
| Email validation | $10-20 |
| Lead data (List Kit, etc.) | $30-50 |
| **Total per 1,000** | **~$120** |

**Scaling costs:**
- 10,000 prospects = $1,200/month
- 100,000 prospects = $12,000/month

### ROI Calculation

**Example scenario:**
- Customer LTV: $5,000
- CAC: $120 (1 deal per 1,000)
- ROI: 4,167% (or 41.67x return)

**Acceptable CAC ranges:**
- $120 CAC (1/1,000) - Excellent
- $240 CAC (1/2,000) - Good
- $480 CAC (1/4,000) - Acceptable
- $1,200 CAC (1/10,000) - Poor (fix campaign)

**Break-even analysis:**
If your LTV is $2,000:
- Max acceptable CAC: $600 (3:1 LTV:CAC ratio)
- Max prospects: 5,000 per deal
- Below 1/5,000 = Profitable
- Above 1/5,000 = Unprofitable

## Troubleshooting Framework

Use this framework to diagnose and fix campaign issues.

### Issue 1: Low Total Reply Rate (Under 2%)

**Diagnosis:** Deliverability issue

**Possible causes:**
1. Emails landing in spam
2. Sending volume too high
3. Poor email infrastructure
4. Spam trigger words in copy
5. Links/images/HTML in emails

**How to check:**
- Send test emails to multiple inboxes
- Check spam folders
- Use mail-tester.com
- Review bounce rate (should be under 3%)

**How to fix:**

**Fix 1: Audit your copy**
- Remove ALL links
- Remove ALL images
- Remove ALL HTML
- Use plain text only
- Check for spam words (free, guarantee, click here)

**Fix 2: Check sending volume**
- Max 20 emails per day per inbox (during warmup)
- Max 40-50 emails per day per inbox (post-warmup)
- Reduce volume if exceeding limits

**Fix 3: Review infrastructure**
- Verify DNS records (SPF, DKIM, DMARC)
- Ensure warmup completed (14 days minimum)
- Check domain reputation
- Validate email list (under 3% bounce rate)

**Fix 4: Improve targeting**
- Wrong ICP = no replies
- Ensure leads match your ideal customer profile
- Check job titles are accurate
- Verify company size matches

### Issue 2: Low Positive Reply Rate (Under 0.2%)

**Diagnosis:** Copy or product-market fit issue

**Possible causes:**
1. Weak value proposition
2. Poor email copy
3. Wrong ICP targeting
4. Offer not compelling
5. Unclear messaging

**How to check:**
- Read your replies - what are people saying?
- "Not interested" = Copy/offer issue
- "Not relevant" = Targeting issue
- No replies at all = Deliverability issue

**How to fix:**

**Fix 1: Improve your copy**
- Rewrite value proposition
- Make offer clearer
- Add social proof
- Simplify language
- Test new angles (see Personalization skill)

**Fix 2: Refine targeting**
- Narrow ICP criteria
- Exclude poor-fit prospects
- Test different industries
- Adjust company size filters

**Fix 3: Test different offers**
- Add guarantee
- Lower barrier to entry
- Performance-based pricing
- Free trial/audit
- Risk reversal

**Fix 4: Improve personalization**
- Use better opening lines
- Reference specific pain points
- Show you understand their business
- Make it feel 1:1, not mass email

### Issue 3: Low Meeting Booked Rate (Under 0.2%)

**Diagnosis:** Sales or inbox management issue

**Possible causes:**
1. Slow response time to replies
2. Poor inbox management
3. Weak qualification
4. Unclear booking process
5. Sales team not following up

**How to check:**
- Track time from reply to response
- Review response quality
- Check booking link functionality
- Audit call-to-action clarity

**How to fix:**

**Fix 1: Speed up response time**
- Set up email notifications
- Check inbox 3x per day minimum
- Use AI inbox manager (RevReply)
- Target under 1-hour response time

**Fix 2: Improve inbox responses**
- Create response templates
- Always include calendar link
- Ask qualifying questions early
- Make booking process obvious

**Fix 3: Qualify better**
- Ask budget, timeline, authority upfront
- Don't book unqualified calls
- Pre-qualify via email
- Save call slots for good fits

**Fix 4: Simplify booking**
- Use Calendly or similar
- Offer 2-3 specific time slots
- Send calendar link in every response
- Reduce friction (one-click booking)

### Issue 4: Low Close Rate (Under 0.1%)

**Diagnosis:** Sales issue

**Possible causes:**
1. Poor sales performance on calls
2. Weak close strategy
3. Pricing too high
4. Offer not compelling
5. Wrong prospects making it to calls

**How to check:**
- Track show rate (should be 70%+)
- Review sales call recordings
- Ask for feedback from no-shows
- Analyze objections

**How to fix:**

**Fix 1: Improve sales calls**
- Better discovery questions
- Stronger value presentation
- Handle objections better
- Clearer next steps
- Follow-up process

**Fix 2: Adjust pricing**
- Test lower price point
- Add payment plans
- Offer trial period
- Performance-based component

**Fix 3: Better qualification**
- Filter harder before booking
- Ask budget questions earlier
- Confirm decision-maker
- Verify timeline

**Fix 4: Improve show rate**
- Send confirmation email
- Send reminder 24hrs before
- Send reminder 1hr before
- Call no-shows to reschedule

## Optimization Strategies

### A/B Testing Framework

**What to test:**
1. Subject lines
2. Opening lines
3. Value propositions
4. CTAs
5. Email length
6. Follow-up sequences

**How to test:**
- Use Smartlead A/B split test feature
- Test one variable at a time
- Need 200+ sends per variant for statistical significance
- Run for at least 1 week

**Example test:**
```
Variant A: "Hi {{first_name}}, I noticed..."
Variant B: "Hi {{first_name}}, I was shopping..."

Measure: Positive reply rate
Winner: Variant with higher positive replies
```

### Scaling Strategies

**When results are good (1/1,000 or better):**

**Step 1: Increase volume**
- Add more email accounts (20 → 50)
- Add more sending domains
- Build larger lead lists
- Expected result: Linear scaling

**Step 2: Expand targeting**
- Add similar industries
- Add adjacent job titles
- Expand geographic regions
- Test new ICPs

**Step 3: Add channels**
- Layer in LinkedIn outreach
- Add phone prospecting
- Test direct mail
- Multi-channel approach

**When results are poor (1/5,000 or worse):**

**Step 1: STOP**
- Pause campaign immediately
- Don't throw good money after bad
- Analyze what's broken

**Step 2: Fix root cause**
- Use troubleshooting framework above
- Fix deliverability OR copy OR sales
- Don't scale broken campaigns

**Step 3: Retest small**
- Test fix with 500 prospects
- Validate improvement
- Scale only when fixed

### Segmentation Strategy

**Don't send same email to everyone.**

**Segment by:**
1. Industry
2. Company size
3. Job title
4. Geography
5. Tech stack (if relevant)

**Customize per segment:**
- Opening line
- Pain points referenced
- Social proof (case studies)
- Offer positioning

**Example:**
- Segment A: E-commerce brands → Reference shopping/consumer angle
- Segment B: SaaS companies → Reference demo booking angle
- Segment C: Agencies → Reference fellow agency owner angle

### Follow-Up Optimization

**Standard sequence:**
- Email 1: Initial outreach
- Wait 3-5 days
- Email 2: Value-add follow-up
- Wait 3-5 days
- Email 3: Final breakup email

**Optimization tips:**

**Email 2 should:**
- Add new value (case study, resource)
- Different angle from Email 1
- NOT: "Just following up"
- YES: "Thought you might find this helpful"

**Email 3 should:**
- Breakup angle ("Is this a priority?")
- Permission to close loop
- Final offer to connect

**Open loop rates:**
- After Email 1: 1-2% reply rate
- After Email 2: +0.5-1% additional
- After Email 3: +0.25-0.5% additional
- Total: 2-4% across sequence

## Advanced Metrics

### Time-Based Analysis

**Best sending times:**
- Tuesday-Thursday: Best days
- 7am-11am: Best time window (recipient timezone)
- Avoid Mondays (inbox overload)
- Avoid Fridays (checked out for weekend)

**Response time analysis:**
- Track: Time from send to reply
- Insight: When prospects are most engaged
- Optimize: Send during high-response windows

### Cohort Analysis

**Track by send date:**
- Week 1 performance
- Week 2 performance
- Week 3 performance
- Identify trends over time

**Track by list source:**
- List Kit vs Apollo vs LinkedIn
- Which source performs best?
- Double down on winners

### Revenue Attribution

**Track full funnel:**
```
1,000 prospects → $120 spent
    ↓
30 replies (3% reply rate)
    ↓
4 positive (0.4% positive rate)
    ↓
3 calls (0.3% booking rate)
    ↓
1 deal ($5,000 revenue)
    ↓
ROI: 41.67x ($5,000 / $120)
```

**Calculate:**
- Cost per reply: $120 / 30 = $4 per reply
- Cost per positive: $120 / 4 = $30 per positive
- Cost per call: $120 / 3 = $40 per call
- Cost per deal: $120 / 1 = $120 CAC

## Dashboard Template

### Weekly Metrics Dashboard

| Metric | This Week | Last Week | Goal | Status |
|--------|-----------|-----------|------|--------|
| Prospects contacted | 5,000 | 4,500 | 5,000 | On track |
| Total replies | 150 | 135 | 100-200 | Good |
| Reply rate | 3% | 3% | 2-4% | Good |
| Positive replies | 20 | 18 | 12-25 | Good |
| Positive rate | 0.4% | 0.4% | 0.25-0.5% | Good |
| Calls booked | 15 | 12 | 10-20 | Good |
| Booking rate | 0.3% | 0.27% | 0.2-0.4% | Good |
| Deals closed | 5 | 4 | 5 | On track |
| Close rate | 0.1% | 0.09% | 0.1% | On track |
| CAC | $120 | $135 | <$200 | Excellent |

### Monthly Performance Tracking

```
Month: January 2025
Prospects contacted: 20,000
Total cost: $2,400
Deals closed: 20
Revenue: $100,000
ROI: 41.67x
CAC: $120
```

## Key Takeaways

1. **Golden KPI:** 1 deal per 1,000 prospects is the north star
2. **Don't track opens:** Hurts deliverability, focus on replies instead
3. **Troubleshooting order:** Deliverability → Copy → Sales
4. **Cost efficiency:** $120-480 CAC is acceptable range
5. **Linear scaling:** Good campaigns scale predictably
6. **Fix before scaling:** Never scale broken campaigns
7. **Speed matters:** Reply within 1 hour for best conversion
8. **Test systematically:** A/B test one variable at a time
9. **Segment smartly:** Customize messaging per segment
10. **Track everything:** Use dashboard to monitor weekly progress

## Related Skills
- [Setup Smartlead](./setup_smartlead.md)
- [Write Cold Email Script](./write_cold_email_script.md)
- [Manage Cold Email Inbox](./manage_cold_email_inbox.md)
- [Setup Cold Email Infrastructure](./setup_cold_email_infrastructure.md)

## Analysis Checklist

Weekly review:

- [ ] Pull metrics from Smartlead dashboard
- [ ] Calculate reply rate, positive rate, booking rate
- [ ] Review any significant changes from last week
- [ ] Identify bottleneck in funnel (if any)
- [ ] Apply troubleshooting framework if needed
- [ ] Update dashboard with current week's data
- [ ] Set goals for next week
- [ ] Share report with team/client
- [ ] Schedule optimization tasks if needed
- [ ] Document wins and lessons learned
