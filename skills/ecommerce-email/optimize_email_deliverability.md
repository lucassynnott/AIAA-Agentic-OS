# Optimize Email Deliverability - Complete Technical & Content Strategy

Expert skill for maximizing email deliverability to ensure your emails land in the primary inbox, not spam or promotions tab.

## What Is Email Deliverability?

**Deliverability = Your Sender Reputation "Credit Score"**

**Good Credit Score**:
✅ Emails land in PRIMARY inbox
✅ High open rates
✅ ISPs trust you

**Bad Credit Score**:
❌ Emails go to SPAM or Promotions tab
❌ Low open rates
❌ ISPs block you

**Goal**: Maintain excellent sender reputation so emails consistently reach the primary inbox.

## Why Deliverability is Only a "0.5" Pillar

It's critically important BUT surprisingly easy if you follow simple rules:

**Simple Formula**:
1. Send to engaged people only
2. Send good content
3. Send consistently
4. Have technical setup correct

That's it. Don't overcomplicate.

## Technical Deliverability Setup (One-Time)

### Required DNS Records

**You MUST have these 3 records** or emails go to spam:

#### 1. SPF (Sender Policy Framework)
**What it is**: Authorizes which mail servers can send from your domain
**Status**: Usually auto-set by Klaviyo, verify it exists

#### 2. DKIM (DomainKeys Identified Mail)
**What it is**: Cryptographic signature proving email legitimacy
**Status**: Auto-set by Klaviyo when you configure sending domain

#### 3. DMARC (Domain-based Message Authentication)
**What it is**: Tells ISPs what to do if SPF/DKIM fail
**Status**: YOU must set this up manually

**Why DMARC is Critical**:
- Required by Gmail and Yahoo (as of Feb 2024)
- Without it: Guaranteed spam folder
- Takes 5 minutes to set up

### How to Check Current Status

**Free Tools**:
- GlockApps.com
- MXToolbox.com
- DMARCAnalyzer.com
- Google: "check SPF record"

**Check Your Domain**:
1. Go to one of these tools
2. Enter your domain
3. See if SPF, DKIM, DMARC exist
4. If missing, follow setup below

### DMARC Setup (Most Commonly Missing)

**Step-by-Step**:

1. Log into your domain DNS provider (GoDaddy, Namecheap, Cloudflare, etc.)

2. Create new DNS record:
   - **Type**: TXT
   - **Name**: `_dmarc`
   - **Value**: `v=DMARC1; p=none; rua=mailto:youremail@yourdomain.com`
   - **TTL**: 3600 (or leave default)

3. Save changes

4. Wait 24-48 hours for DNS propagation

5. Verify with DMARC checker tool

**DMARC Policy Options**:
- `p=none` (recommended to start): Monitor only
- `p=quarantine`: Send failures to spam
- `p=reject`: Block failures completely

Start with `p=none`, graduate to `quarantine` after monitoring

### Dedicated Sending Domain Setup

**Required as of February 2024**

**What This Means**:
Instead of: `yourbrand@klaviyoemail.com`
You send from: `hello@yourbrand.com`

**Why Required**:
- Gmail/Yahoo mandate it
- Improves deliverability
- Builds YOUR domain reputation

**Klaviyo Setup**:
1. Klaviyo → Settings → Email → Sending
2. Click "Add Sending Domain"
3. Enter your domain
4. Klaviyo provides DNS records
5. Add records to your DNS provider
6. Wait for verification (24-48 hours)
7. Set as default sending domain

### Reply-To Domain Alignment

**CRITICAL**: Sending domain and reply-to domain must match

**Wrong** ❌:
- Sending: `hello@send.yourbrand.com`
- Reply-to: `support@yourbrand.com`
- Different subdomains = spam

**Correct** ✅:
- Sending: `hello@yourbrand.com`
- Reply-to: `support@yourbrand.com`
- Same root domain = good

**Set in Klaviyo**:
Settings → Email → Default "From" and "Reply-To" addresses

### Technical Checklist

Complete this ONCE for your domain:
- [ ] SPF record exists and verified
- [ ] DKIM record exists and verified
- [ ] DMARC record created and verified
- [ ] Dedicated sending domain configured
- [ ] Reply-to domain aligned with sending domain
- [ ] All records verified with testing tools

**After Setup**: You're done with technical. Now focus on content and engagement.

## Content & Engagement Deliverability

**This is where most people fail or succeed.**

### The 4 Factors That Affect Your "Credit Score"

#### 1. Open Rates

**What ISPs See**: If people open your emails, content must be good

**Benchmarks**:
- **Bad**: Under 15% → Going to spam
- **Acceptable**: 15-25%
- **Good**: 25-40%
- **Excellent**: 40-60%+

**How to Improve**:
- Better subject lines (test variations)
- Send at optimal times
- Only send to engaged segment
- Clean your list regularly
- Provide consistent value

#### 2. Click Rates

**What ISPs See**: People clicking = engaging with content = good

**Benchmarks**:
- **Bad**: Under 1%
- **Acceptable**: 1-3%
- **Good**: 3-8%
- **Excellent**: 8%+

**How to Improve**:
- Clear, prominent CTAs
- Compelling offers
- Better content
- Mobile-optimized buttons
- Reduce friction

#### 3. Spam Complaint Rate

**What ISPs See**: People marking spam = bad sender

**Benchmarks**:
- **Must be**: Under 0.1%
- **Warning**: 0.1-0.5%
- **Critical**: Over 0.5% → You're blocked

**How to Avoid**:
- Only send to people who subscribed
- Honor unsubscribes immediately
- Set correct expectations on signup
- Make unsubscribe easy to find
- Don't buy email lists (ever!)
- Segment to engaged only

#### 4. Sending Volume Over Time

**What ISPs See**: Consistent sending = legitimate business
**What ISPs Suspect**: Sudden spikes = potential spammer

**What This Means**:

**Good Pattern**: ✅
- Week 1: 10,000 emails
- Week 2: 12,000 emails
- Week 3: 11,000 emails
- Week 4: 13,000 emails
(Gradual, consistent growth)

**Bad Pattern**: ❌
- Week 1: 0 emails
- Week 2: 0 emails
- Week 3: 100,000 emails
(Sudden spike = spam alert)

**Best Practice**: Send consistently (3-4x per week)

### The #1 Deliverability Rule

**ONLY SEND TO ENGAGED SUBSCRIBERS**

Create "Engaged 60 Days" or "Engaged 90 Days" segment:

```
Definition:
Someone is in Newsletter list
AND
(Opened email at least once in last 60 days
OR Clicked email at least once in last 60 days
OR Placed order at least once in last 60 days
OR Subscribed in last 30 days)
```

**Use this segment for ALL campaigns.**

**Why This Works**:
- High open rates
- High click rates
- Low spam complaints
- ISPs reward you
- Better deliverability

**What About the Rest?**:
- Send win-back campaign (one last chance)
- If still no engagement: Suppress them
- Don't send to unengaged = protect your reputation

## Domain Warm-Up (New Domains Only)

**If you have a brand new domain**, you need to warm it up:

**Week 1-2**: Send to your most engaged 5,000 subscribers
**Week 3-4**: Send to most engaged 10,000 subscribers
**Week 5-6**: Send to most engaged 25,000 subscribers
**Week 7+**: Send to full engaged list

**Why**: Build reputation gradually with ISPs

**If Established Domain**: No warm-up needed, but maintain consistency

## 6-Week Deliverability Protocol

If your deliverability is suffering, follow this recovery plan:

### Week 1-2: Aggressive List Cleaning
- Create "Engaged 30 Days" segment (strict)
- ONLY send to this group
- Monitor open rates (should increase)
- Goal: Rebuild sender reputation

### Week 3-4: Expand to Engaged
- Expand to "Engaged 60 Days"
- Maintain high-quality content
- Monitor metrics closely
- Goal: Stabilize reputation

### Week 5-6: Back to Normal
- Send to full engaged list
- Resume normal frequency
- Continue monitoring
- Goal: Sustained good deliverability

**After 6 Weeks**: You should see significantly improved inbox placement

## Content That Helps Deliverability

### Send Good Content

**What ISPs Like** (signals of good content):
- People open emails
- People click links
- People spend time reading
- Low unsubscribes
- Low spam complaints

**How to Send Good Content**:
- Provide value (education, entertainment, deals)
- Be consistent with brand voice
- Match expectations set at signup
- 5:1 ratio (value:promotion)
- Mobile-optimized
- Clear, scannable
- Relevant to subscriber

### What to Avoid in Copy

**Spam Trigger Words** (use sparingly):
- All caps: "FREE MONEY NOW"
- Excessive punctuation: "Amazing!!!!!!"
- Spam phrases: "Act now", "Limited time", "Click here"
- Currency symbols: "$$$"
- Financial terms: "Earn money fast"

**Note**: These aren't banned, but excessive use triggers filters

**Better Approach**:
- Normal capitalization
- One exclamation point per email (max)
- Natural, conversational language
- Specific, not salesy

### Subject Line Best Practices for Deliverability

**Do**:
- Keep under 50 characters
- Be specific and honest
- Test with/without emojis
- Personalize appropriately
- Match email content

**Don't**:
- Deceive or mislead
- Use all caps
- Overuse punctuation
- Make false promises
- Use spam trigger words excessively

## Email Authentication & Technical Monitoring

### Monitor Your Sender Reputation

**Tools to Check Reputation**:

1. **Sender Score** (by Validity):
   - Score: 0-100
   - 90+: Excellent
   - 70-90: Good
   - Below 70: Problems

2. **Google Postmaster Tools**:
   - Gmail-specific insights
   - Reputation rating
   - Spam rate
   - Encryption status
   - IP reputation

3. **Microsoft SNDS** (Smart Network Data Services):
   - Outlook/Hotmail specific
   - Spam complaint rates
   - Trap hits

**Set Up Monitoring**:
- Add your domain to these tools
- Check weekly
- Address issues immediately

### Inbox Placement Testing

**Tools**:
- GlockApps
- Mail-Tester.com
- Email on Acid

**How to Use**:
1. Send test email to tool
2. Tool shows where it lands (inbox, spam, promotions)
3. Provides feedback on what to fix
4. Make adjustments
5. Re-test

**Do this monthly** to catch issues early

## Deliverability by Email Provider

### Gmail

**Primary vs Promotions vs Spam**:
- **Primary**: Best, most engaged users
- **Promotions**: Still okay, opened less often
- **Spam**: Bad, not opened

**How to Reach Primary**:
- High engagement (opens/clicks)
- Personal content (not template-heavy)
- Text-to-image ratio balanced
- Consistent sending
- Good authentication

**Promotions Tab**: Mostly unavoidable for e-commerce, but...
- Some emails still make Primary
- Users still check Promotions
- Better than spam

### Yahoo/AOL

**Similar to Gmail**:
- Focus on engagement
- Good authentication
- Consistent sending

**Yahoo Specifics**:
- More strict on spam complaints
- Less forgiving of poor engagement
- Monitor SNDS closely

### Outlook/Hotmail

**Microsoft is Strictest**:
- Very low tolerance for spam
- Monitor SNDS religiously
- Keep spam complaints under 0.1%
- Any issues = immediate blocking

### Apple Mail (iCloud, me.com)

**Apple Specifics**:
- Built-in tracking protection
- Open rates may be inflated (MPP)
- Focus on clicks and conversions instead
- Authentication critical

## Deliverability Footer Trick

**Add to Email Footer**:

"Not interested? No problem. Click here to [Unsubscribe] or [Update Preferences]"

**Also Include**:
"Didn't want this email? Make sure we're in your address book to ensure delivery."

**Why This Works**:
- Easy unsubscribe = fewer spam complaints
- Preference center = keeps engaged subscribers
- Address book request = improves deliverability

## Common Deliverability Mistakes

1. **Sending to entire list**: Send to engaged only
2. **Buying email lists**: NEVER do this (instant spam folder)
3. **No DMARC record**: Gmail/Yahoo requirement
4. **Mismatched reply-to**: Must match sending domain
5. **Inconsistent sending**: Send regularly (3-4x/week)
6. **Poor content**: Provide value, not just sales
7. **Hiding unsubscribe**: Make it easy to opt out
8. **Not cleaning list**: Remove unengaged regularly
9. **Sudden volume spikes**: Gradual growth only
10. **Ignoring metrics**: Monitor and respond to data

## Deliverability Checklist

### One-Time Technical Setup:
- [ ] SPF record verified
- [ ] DKIM record verified
- [ ] DMARC record created
- [ ] Dedicated sending domain configured
- [ ] Reply-to domain aligned
- [ ] Sender Score account created
- [ ] Google Postmaster Tools set up
- [ ] Microsoft SNDS monitoring enabled

### Ongoing Best Practices:
- [ ] Only send to engaged segments
- [ ] Send 3-4 campaigns per week consistently
- [ ] Monitor open rates (target 25-40%+)
- [ ] Monitor spam complaint rate (under 0.1%)
- [ ] Clean list monthly (suppress unengaged 90+ days)
- [ ] Test inbox placement monthly
- [ ] Provide value in 80% of emails
- [ ] Make unsubscribe easy to find
- [ ] Match subject line to email content
- [ ] Mobile-optimize all emails

### Monthly Monitoring:
- [ ] Check Sender Score
- [ ] Review Google Postmaster
- [ ] Check Microsoft SNDS
- [ ] Test inbox placement
- [ ] Review campaign metrics
- [ ] Update engaged segment criteria if needed
- [ ] Suppress unengaged subscribers
- [ ] Test subject lines for spam triggers

## Troubleshooting Deliverability Issues

### Symptom: Open Rates Dropping

**Possible Causes**:
- Sending to unengaged list
- Poor subject lines
- Inconsistent sending
- Landing in spam/promotions

**Solutions**:
- Segment to engaged only
- Test subject line variations
- Resume consistent sending schedule
- Check inbox placement testing
- Review sender reputation

### Symptom: Emails Going to Spam

**Possible Causes**:
- Missing DMARC
- High spam complaint rate
- Low engagement
- Sudden volume spike
- Poor sender reputation

**Solutions**:
- Add DMARC record immediately
- Segment to highly engaged only
- Follow 6-week recovery protocol
- Check spam complaint rate
- Verify authentication records

### Symptom: High Unsubscribe Rate

**Possible Causes**:
- Sending too frequently
- Content not matching expectations
- Too promotional
- Not providing value
- Targeting wrong segment

**Solutions**:
- Reduce frequency temporarily
- Survey unsubscribers (why leaving?)
- Increase value content (5:1 ratio)
- Better segment targeting
- Set clearer expectations at signup

### Symptom: Deliverability Good at First, Then Declines

**Possible Causes**:
- List degradation (natural)
- Inconsistent sending
- Content quality declined
- Engagement dropped

**Solutions**:
- Clean list regularly
- Resume consistent sending
- Audit content quality
- Re-engage with value content
- Suppress unengaged subscribers

## Deliverability Metrics to Track

**In Klaviyo Analytics → Dashboards**:

1. **Open Rate Trend** (target: 25-40%+)
2. **Click Rate Trend** (target: 2-8%+)
3. **Spam Complaint Rate** (target: <0.1%)
4. **Unsubscribe Rate** (target: <0.5%)
5. **Bounce Rate** (target: <2%)
6. **List Growth vs. Churn**
7. **Engaged vs. Unengaged Ratio**

**Create Custom Dashboard**:
- Track these metrics weekly
- Set up alerts for concerning trends
- Review and adjust strategy

## Advanced Deliverability Strategies

### IP Warming (Agency/High-Volume Only)

If sending 100K+ emails/day, consider dedicated IP:
- Gradual IP warm-up required
- Builds IP-specific reputation
- More control
- Higher cost

For most: Shared IP (Klaviyo default) is fine

### List Hygiene Automation

**Automated Sunset Flow**:
```
Trigger: Profile has not engaged in 90 days
Wait: 7 days
Email: "We miss you! Final reminder"
Wait: 14 days
If still no engagement:
Action: Suppress from all future sends
```

### Preference Center

Give subscribers control:
- Email frequency preferences
- Content type preferences
- Product category interests
- Update profile information

**Benefits**:
- Reduces unsubscribes
- Improves relevance
- Increases engagement
- Better deliverability

### Double Opt-In (Optional)

**What it is**: Subscriber must confirm via email

**Pros**:
- Higher quality list
- Better engagement
- Fewer spam complaints

**Cons**:
- Lose 20-40% of signups
- Friction in signup process

**Recommendation**: Single opt-in for e-commerce (immediate welcome email), double opt-in for B2B/content

---

**Pro Tip**: Deliverability is 80% about sending to engaged people and 20% technical setup. Get the technical right once, then focus on engagement forever.

**Remember**: ISPs want to deliver emails that recipients want. Make your emails wanted (valuable content, to engaged people) and deliverability takes care of itself.

**Bottom Line**: Send good content to people who want it, consistently, with proper authentication. That's the entire deliverability playbook.
