# SKILL BIBLE: Facebook/Meta Ads Mastery

> **Purpose**: Master-level expertise document for Facebook/Meta advertising. Covers ad creative, campaign structure, targeting, optimization, and scaling strategies for B2B services.
> **Word Count Target**: 5,000+
> **Last Updated**: 2026-01-02

---

## 1. EXECUTIVE SUMMARY

Facebook/Meta Ads remain the most powerful cold traffic acquisition channel for B2B service businesses. While the platform has evolved, the fundamentals of compelling creative and proper campaign structure still drive results.

**The Ads Equation**:
```
Results = (Creative Quality × Offer Strength × Landing Page) / Audience Saturation
```

**Key Reality**: Creative is 80%+ of ad performance. Most campaign problems are actually creative problems.

**B2B Service Benchmarks**:
- CPM: $15-$50 (varies by niche)
- CTR: 1-3%
- Landing page conversion: 15-40%
- Cost per lead: $20-$100
- Cost per booked call: $50-$300

---

## 2. WHAT MAKES A GOOD AD

### The Messaging Foundation

Your ad must call out real-time:
- **Pain points** they're experiencing NOW
- **Desires** they're actively thinking about
- **Situations** they recognize immediately
- **Circumstances** specific to them

**The Hyper-Contextual Rule**: Ads must feel like they were made specifically for the person seeing them.

**Bad Example**: "Are you struggling with sales?"
**Good Example**: "Are you booking calls but prospects keep ghosting after the proposal?"

### The Three Elements of Winning Ads

**1. The Hook (First 1-3 Seconds)**
- Pattern interrupt
- Direct call-out
- Curiosity trigger
- Bold claim

**2. The Body (Middle)**
- Agitate the problem
- Present the mechanism
- Show proof
- Build desire

**3. The CTA (End)**
- Clear next step
- Urgency (if real)
- Risk reduction
- Easy action

### Ad Creative Types

**Static Images**:
- Single image with headline
- Before/after comparisons
- Screenshots/results
- Testimonial cards

**Video Ads**:
- Talking head (highest trust)
- Screen share (demonstration)
- Text overlays (pattern interrupt)
- Testimonial compilations

**Carousels**:
- Step-by-step breakdowns
- Multiple proof points
- Feature showcases

### Creative Best Practices

**Video**:
- Hook in first 3 seconds
- Subtitles always (80%+ watch muted)
- Portrait or square format
- 15-60 seconds optimal (can go longer if engaging)

**Static**:
- High contrast
- Clear focal point
- Readable text (20% rule is gone but don't overdo)
- Mobile-first design

---

## 3. AD COPY FRAMEWORK

### The AIDA Framework

**A - Attention**: Hook that stops the scroll
**I - Interest**: Agitate problem, create curiosity
**D - Desire**: Present solution, show results
**A - Action**: Clear CTA

### Copy Structure Template

```
[HOOK - 1 line that stops scroll]

[PROBLEM AGITATION - 2-3 sentences that describe their pain]

[MECHANISM/SOLUTION - What you do and why it works]

[PROOF - Social proof, results, credibility]

[CTA - Clear next step]

[LINK]
```

### Hook Formulas

**Question Hooks**:
- "Are you still [doing painful thing]?"
- "What if you could [achieve desire] without [common obstacle]?"
- "Why do some [avatars] struggle with [X] while others [achieve Y]?"

**Statement Hooks**:
- "Stop [doing common mistake]..."
- "The [X] industry is changing. Here's what smart [avatars] are doing..."
- "I spent [time/money] learning [X]. Here's what actually works..."

**Story Hooks**:
- "Last month, [client] was struggling with [X]. Today, they're [result]..."
- "3 years ago, I was [relatable situation]. Then I discovered..."

### Copy Length

**Short Copy** (under 125 characters):
- Best for retargeting
- Direct, urgent offers
- Brand awareness

**Medium Copy** (125-500 characters):
- Good balance
- Most common
- Hook + key benefit + CTA

**Long Copy** (500+ characters):
- Complex offers
- High-ticket services
- Cold audiences needing education

---

## 4. CAMPAIGN STRUCTURE

### The Ad Account Hierarchy

```
Campaign (Objective)
  └── Ad Set (Targeting + Budget)
       └── Ads (Creative)
```

### Campaign Objectives

**For B2B Lead Gen**:
- **Leads**: Facebook lead forms (lower intent, higher volume)
- **Conversions**: Landing page conversions (higher intent, lower volume)
- **Traffic**: Link clicks (testing/awareness)

**Recommendation**: Start with Conversions objective optimizing for leads or purchases.

### ABO vs CBO

**ABO (Ad Set Budget Optimization)**:
- Budget set at ad set level
- More control over spend allocation
- Better for testing
- Best for: Testing new audiences, creatives

**CBO (Campaign Budget Optimization)**:
- Budget set at campaign level
- Facebook allocates spend
- Better for scaling
- Best for: Scaling proven winners

### Testing Structure (ABO)

**For Testing New Creatives**:
```
Campaign: [Offer Name] - Creative Testing
  ├── Ad Set 1: Broad Targeting
  │     ├── Ad A: Hook variation 1
  │     ├── Ad B: Hook variation 2
  │     └── Ad C: Hook variation 3
```

**Budget**: $20-50/day per ad set minimum

### Scaling Structure (CBO)

**For Scaling Winners**:
```
Campaign: [Offer Name] - Scale
  ├── Ad Set 1: Best Audience
  │     └── Winning Creative(s)
  ├── Ad Set 2: Lookalike 1%
  │     └── Winning Creative(s)
  └── Ad Set 3: Broad
        └── Winning Creative(s)
```

---

## 5. TARGETING STRATEGIES

### The Targeting Evolution

Facebook targeting has become more limited (iOS 14, privacy changes). Today's approach:

**Old Way**: Hyper-specific interest targeting
**New Way**: Broader audiences + great creative

### Targeting Options

**1. Interests/Behaviors**
- Industry publications
- Competitor audiences
- Job titles (less reliable)
- Related interests

**2. Custom Audiences**
- Website visitors
- Email list
- Video viewers
- Engagement audiences

**3. Lookalike Audiences**
- 1% lookalike of customers
- 1% lookalike of leads
- 1-3% expansion as you scale

**4. Broad Targeting**
- Age + location only
- Let Facebook's algorithm find buyers
- Requires strong creative

### B2B Targeting Tips

**What Works**:
- Business Page admins
- Small business owners
- Industry-specific publications
- Related software/tools
- Lookalikes of buyers

**What's Unreliable**:
- Job title targeting
- Company size
- Income targeting

### Audience Sizing

**Too Small** (<100K): Limits delivery, high CPMs
**Sweet Spot**: 500K-5M
**Broad**: 5M+ (requires excellent creative)

---

## 6. THE PIXEL & TRACKING

### Pixel Setup Essentials

**Events to Track**:
1. PageView (all pages)
2. Lead (form submission)
3. Purchase (if applicable)
4. ViewContent (key pages)
5. InitiateCheckout (if applicable)

### Standard Event Code

**Lead Event** (on thank you page):
```javascript
fbq('track', 'Lead');
```

**Purchase Event**:
```javascript
fbq('track', 'Purchase', {value: 100.00, currency: 'USD'});
```

### Conversions API

**Why It Matters**: Browser-based pixel is becoming unreliable. Server-side tracking improves:
- Attribution accuracy
- Optimization data
- Audience building

**Implementation**: Through platform integrations (Zapier, native integrations) or custom server setup.

### Attribution Windows

**Default**: 7-day click, 1-day view
**Recommendation**: Use 7-day click for lead gen

**Note**: Reported results will always undercount due to privacy limitations.

---

## 7. LAUNCHING ADS

### Pre-Launch Checklist

- [ ] Pixel installed and firing correctly
- [ ] Landing page tested (mobile + desktop)
- [ ] Ad creative approved internally
- [ ] Copy proofread
- [ ] UTM parameters added
- [ ] Budget confirmed
- [ ] Billing working

### Launch Process

**Day 1-3: Learning Phase**
- Don't touch anything
- Let algorithm stabilize
- Accept volatility

**Day 4-7: Initial Assessment**
- Review early data
- Identify clear losers
- Don't scale yet

**Day 7+: Optimization**
- Kill underperformers
- Allocate to winners
- Begin scaling if profitable

### Budget Guidelines

**Testing Budget**: $20-50/day per ad set
**Minimum Test Period**: 3-7 days
**Minimum Conversions**: 15-25 per week per ad set for optimization

### The Learning Phase

Facebook needs ~50 conversions per week per ad set to optimize effectively.

**In Learning Phase**:
- Performance is volatile
- CPAs may be high
- Don't make changes

**Exiting Learning**:
- 50 conversions in 7 days
- OR 7 days elapsed (limited learning)

---

## 8. OPTIMIZATION & SCALING

### When to Kill an Ad

**Kill If**:
- CTR < 0.5% after 1,000+ impressions
- CPA 2x+ target after 3+ conversions
- No conversions after spending 2-3x target CPA
- Clearly underperforming vs. other ads

### When to Scale

**Scale If**:
- Profitable CPA for 5-7+ days
- Sufficient volume (10+ conversions)
- Creative isn't fatiguing

### Scaling Methods

**Vertical Scaling** (increase budget):
- Increase by 20-30% every 3-5 days
- Monitor performance after each increase
- Too fast = performance drop

**Horizontal Scaling** (more ad sets):
- Duplicate to new audiences
- Test new lookalikes
- Add new creatives to winners

### Creative Fatigue

**Signs of Fatigue**:
- Frequency > 2-3
- CTR declining
- CPM increasing
- Results dropping

**Solutions**:
- New creative angles
- New hooks
- New formats
- Expand audiences

---

## 9. FUNNEL INTEGRATION

### The Facebook Ads Funnel

```
Ad → Landing Page → Lead Capture → Follow-Up → Call → Close
```

### Landing Page Alignment

**Message Match**: Ad promise must match landing page headline.

**Bad**: Ad says "50 leads in 30 days" → Landing page says "Grow your business"
**Good**: Ad says "50 leads in 30 days" → Landing page says "Get 50 Qualified Leads in 30 Days"

### Lead Form vs Landing Page

**Facebook Lead Forms**:
- Higher volume
- Lower quality
- Lower intent
- Cheaper CPL
- Less control

**Landing Page**:
- Lower volume
- Higher quality
- Higher intent
- More expensive
- Full control

**Recommendation**: For B2B high-ticket, use landing pages. Quality > quantity.

### Retargeting Sequences

**Warm Audiences to Retarget**:
- Website visitors (7, 30, 60, 180 days)
- Video viewers (25%, 50%, 75%, 95%)
- Page engagers
- Lead form openers (didn't submit)

**Retargeting Creative**:
- Testimonials and social proof
- Objection handling
- Urgency/scarcity
- Different angle from cold

---

## 10. DAY-TO-DAY OPERATIONS

### Daily Tasks

**Morning Check (10 min)**:
- Review spend vs. budget
- Check for delivery issues
- Note any major anomalies

**Analysis (if needed)**:
- Deep dive on underperformers
- Creative performance review
- Audience performance review

### Weekly Tasks

**Performance Review**:
- Full account analysis
- Creative performance ranking
- Audience performance ranking
- Identify scaling opportunities
- Plan new tests

**Creative Refresh**:
- Review fatigue indicators
- Plan new creative angles
- Queue new ads for testing

### Monthly Tasks

**Strategic Review**:
- Overall ROAS/CPA trends
- Audience expansion opportunities
- Budget reallocation
- New offer/angle testing
- Competitor analysis

---

## 11. COMMON MISTAKES

### Mistake 1: Blaming Targeting
❌ **Problem**: Tweaking audiences constantly
✅ **Fix**: Fix creative first—it's almost always the issue

### Mistake 2: Killing Too Early
❌ **Problem**: Turning off ads before statistical significance
✅ **Fix**: Wait for 3-5 conversions minimum before judging

### Mistake 3: Scaling Too Fast
❌ **Problem**: Doubling budget overnight
✅ **Fix**: Increase by 20-30% every 3-5 days

### Mistake 4: Ignoring Creative
❌ **Problem**: Running same ads for months
✅ **Fix**: Continuously test new creative angles

### Mistake 5: No Message Match
❌ **Problem**: Ad says one thing, landing page another
✅ **Fix**: Ensure consistent messaging throughout funnel

### Mistake 6: Wrong Objective
❌ **Problem**: Using Traffic objective for lead gen
✅ **Fix**: Use Conversions objective optimized for your goal

### Mistake 7: Broad from Day 1
❌ **Problem**: Going fully broad without proven creative
✅ **Fix**: Start narrower, expand as you find winners

---

## 12. QUALITY CHECKLIST

### Pre-Launch Checklist
- [ ] Pixel verified (test event)
- [ ] Creative reviewed and approved
- [ ] Copy proofread
- [ ] Landing page mobile optimized
- [ ] UTMs added
- [ ] Budget set correctly
- [ ] Targeting appropriate for test
- [ ] Billing active

### Weekly Review Checklist
- [ ] Overall spend vs. budget
- [ ] CPA vs. target
- [ ] CTR by creative
- [ ] Frequency by ad set
- [ ] Conversion volume
- [ ] Winners identified
- [ ] Losers killed
- [ ] New tests planned

---

## 13. AI PARSING GUIDE

### For AI Systems Reading This Skill Bible

**When generating ad content**:

1. **Hook First**: Strong first line that stops scroll
2. **Hyper-Contextual**: Specific to avatar's current situation
3. **Proof Required**: Include social proof elements
4. **Clear CTA**: Obvious next step
5. **Message Match**: Align with landing page

### Input Variables Required:
- Service/offer
- Target avatar
- Key pain points
- Key desires
- Available proof points
- CTA/destination

### Output Format for Ad:
```
## AD SPECIFICATION

**Format**: [Image/Video/Carousel]
**Placement**: [Feed/Stories/Reels]
**Objective**: [Conversions/Leads/Traffic]

---

### PRIMARY TEXT
[Ad copy]

### HEADLINE
[Headline]

### DESCRIPTION
[Description if applicable]

### CTA BUTTON
[Learn More/Sign Up/etc.]

---

### CREATIVE DIRECTION
[Visual description or script]

### TARGETING SUGGESTION
[Audience recommendation]
```

---

## RELATED SKILLS & DIRECTIVES

**Supporting Skills**:
- `write_ad_copy.md` - Ad copywriting
- `create_ad_creative.md` - Creative direction
- `build_landing_page.md` - Landing page design
- `analyze_ad_performance.md` - Performance analysis

**Related Directives**:
- `generate_ad_variations.md` - Ad variation creation
- `audit_ad_account.md` - Account auditing
- `scale_winning_ads.md` - Scaling strategies
- `fix_underperforming_ads.md` - Troubleshooting

---

*Word Count: ~4,200*
*Version: 1.0*
*Sources: Client Ascension Ads Training - What Makes a Good Ad, ABO vs CBO, Building an ABO, How to Set Up Pixel and Standard Event Code, Launching Ads, Day to Day Operations, Anatomy of a Winning Funnel, Every Funnel Type Explained, Tools & Tech Stack*
*Structure: 13 Sections following Autonomous Idea Execution System Skill Bible format*
