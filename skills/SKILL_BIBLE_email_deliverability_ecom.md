# SKILL BIBLE: Email Deliverability Optimization - Complete Technical & Content Strategy

## Executive Summary

Email deliverability is the foundation of successful email marketing, determining whether your carefully crafted campaigns reach the primary inbox or get buried in spam folders. This skill bible provides a comprehensive framework for maximizing email deliverability through both technical authentication and content optimization strategies. Unlike many deliverability guides that focus solely on technical setup, this approach emphasizes the critical balance between proper DNS configuration and engagement-driven content strategy.

The methodology treats deliverability as a "sender reputation credit score" that ISPs use to determine email placement. By following the systematic approach outlined here—including one-time technical setup, ongoing engagement optimization, and continuous monitoring—you can achieve consistently high inbox placement rates. This skill is particularly valuable because while deliverability is critically important, it's surprisingly manageable when you follow proven protocols rather than overcomplicating the process.

The framework has been battle-tested across various email volumes and industries, with particular emphasis on e-commerce applications using Klaviyo as the primary email service provider. The strategies scale from small businesses sending thousands of emails per week to larger operations managing hundreds of thousands of subscribers.

## Source
- **Type:** Internal SOP/Skill Document
- **Category:** ecommerce-email
- **Original File:** optimize_email_deliverability.md

## Core Principles

### 1. Deliverability as Credit Score Management
Email deliverability functions exactly like a financial credit score—ISPs continuously evaluate your sender reputation based on subscriber behavior. Good credit scores (high engagement, low complaints) result in primary inbox placement, while poor scores lead to spam folder relegation or complete blocking. This principle guides all strategic decisions.

### 2. Technical Setup is One-Time, Engagement is Forever
The technical foundation (SPF, DKIM, DMARC records) requires proper setup once, but engagement optimization is an ongoing process. Most deliverability failures stem from poor engagement management rather than technical issues. Focus 80% of effort on engagement, 20% on technical maintenance.

### 3. Engaged Subscribers Only Strategy
The cardinal rule of deliverability: only send emails to subscribers who have demonstrated recent engagement. This means creating and consistently using engaged segments (typically 60-90 day engagement windows) for all campaigns. Sending to unengaged subscribers destroys sender reputation faster than any other factor.

### 4. Consistency Builds Trust with ISPs
ISPs favor predictable sending patterns over sporadic bursts. Consistent sending volume and frequency (3-4 campaigns per week) signals legitimate business operations, while sudden spikes trigger spam detection algorithms. Gradual growth is always preferred over rapid scaling.

### 5. Content Quality Drives Engagement Metrics
High-quality, valuable content naturally generates the engagement metrics (opens, clicks, low complaints) that ISPs use to evaluate sender reputation. The 5:1 value-to-promotion ratio ensures subscribers remain engaged and responsive to your emails.

### 6. Authentication Must Be Complete and Aligned
Partial authentication setup is worse than no setup—ISPs expect complete SPF, DKIM, and DMARC implementation. Additionally, sending domains and reply-to domains must be properly aligned to avoid triggering security filters.

### 7. Proactive Monitoring Prevents Problems
Regular monitoring of sender reputation, inbox placement, and engagement metrics allows for early intervention before deliverability issues become critical. Monthly testing and weekly metric reviews are essential maintenance activities.

### 8. Recovery Requires Systematic Approach
When deliverability problems occur, recovery must follow a structured protocol rather than random fixes. The 6-week recovery framework provides a proven path back to good standing with ISPs.

## Step-by-Step Process

### Phase 1: Technical Foundation Setup (One-Time)

#### Step 1: Audit Current Authentication Status
1. Use free tools (GlockApps.com, MXToolbox.com, DMARCAnalyzer.com) to check current SPF, DKIM, and DMARC records
2. Document which records exist and which are missing
3. Verify that existing records are properly configured
4. Note any authentication failures or warnings

#### Step 2: Configure Missing DNS Records
1. **SPF Record**: Usually auto-configured by Klaviyo, verify existence
2. **DKIM Record**: Auto-configured when setting up dedicated sending domain
3. **DMARC Record** (most commonly missing):
   - Log into DNS provider (GoDaddy, Namecheap, Cloudflare, etc.)
   - Create new TXT record
   - Name: `_dmarc`
   - Value: `v=DMARC1; p=none; rua=mailto:youremail@yourdomain.com`
   - TTL: 3600
   - Save and wait 24-48 hours for propagation

#### Step 3: Set Up Dedicated Sending Domain
1. In Klaviyo: Settings → Email → Sending
2. Click "Add Sending Domain"
3. Enter your primary domain
4. Copy provided DNS records to your DNS provider
5. Wait for verification (24-48 hours)
6. Set as default sending domain

#### Step 4: Align Reply-To Domain
1. Ensure reply-to domain matches sending domain root
2. Configure in Klaviyo: Settings → Email → Default "From" and "Reply-To" addresses
3. Test alignment with authentication tools

#### Step 5: Verify Complete Setup
1. Re-test all authentication records
2. Confirm dedicated sending domain is active
3. Send test email and verify proper authentication
4. Document completion date for future reference

### Phase 2: Engagement Optimization Setup

#### Step 6: Create Engaged Subscriber Segments
1. **Primary Engaged Segment (60-90 days)**:
   ```
   Someone is in Newsletter list
   AND
   (Opened email at least once in last 60 days
   OR Clicked email at least once in last 60 days
   OR Placed order at least once in last 60 days
   OR Subscribed in last 30 days)
   ```
2. **Highly Engaged Segment (30 days)** for recovery situations
3. **Unengaged Segment** for sunset campaigns

#### Step 7: Implement List Hygiene Automation
1. Create automated sunset flow:
   - Trigger: No engagement in 90 days
   - Wait 7 days
   - Send "We miss you" email
   - Wait 14 days
   - If no engagement: Suppress from future sends
2. Set up monthly list cleaning reminders
3. Configure unsubscribe and preference center

#### Step 8: Establish Baseline Metrics
1. Record current open rates, click rates, spam complaint rates
2. Set up monitoring dashboard in Klaviyo
3. Configure alerts for concerning metric trends
4. Document baseline for future comparison

### Phase 3: Content Strategy Implementation

#### Step 9: Audit Current Content Strategy
1. Review last 30 days of email content
2. Calculate value-to-promotion ratio
3. Identify spam trigger words or phrases
4. Assess mobile optimization
5. Review subject line patterns

#### Step 10: Implement Content Best Practices
1. Establish 5:1 value-to-promotion ratio
2. Create content calendar ensuring consistent value delivery
3. Optimize subject lines (under 50 characters, honest, specific)
4. Ensure mobile-responsive design
5. Add proper unsubscribe and preference links

#### Step 11: Set Up Testing Protocols
1. Implement A/B testing for subject lines
2. Schedule monthly inbox placement testing
3. Create feedback loops for content performance
4. Document what works for future campaigns

### Phase 4: Monitoring and Maintenance

#### Step 12: Establish Monitoring Routine
1. **Weekly**: Review engagement metrics dashboard
2. **Monthly**: 
   - Check sender reputation scores
   - Test inbox placement
   - Review and clean subscriber list
   - Audit authentication records
3. **Quarterly**: Comprehensive deliverability audit

#### Step 13: Implement Continuous Improvement
1. Analyze top-performing content for patterns
2. Refine engaged segment criteria based on performance
3. Adjust sending frequency based on engagement trends
4. Update content strategy based on subscriber feedback

### Phase 5: Troubleshooting and Recovery (As Needed)

#### Step 14: Identify Deliverability Issues
1. Monitor for declining open rates (below 25%)
2. Watch for increased spam complaints (above 0.1%)
3. Check for inbox placement problems
4. Review sender reputation scores

#### Step 15: Execute Recovery Protocol
1. **Week 1-2**: Send only to highly engaged 30-day segment
2. **Week 3-4**: Expand to engaged 60-day segment
3. **Week 5-6**: Resume normal engaged segment
4. Monitor metrics closely throughout recovery
5. Document lessons learned for prevention

## Frameworks & Templates

### The Deliverability Credit Score Framework

**Excellent Credit (90-100 Score)**:
- Open rates: 40-60%+
- Click rates: 8%+
- Spam complaints: <0.05%
- Result: Primary inbox placement

**Good Credit (70-89 Score)**:
- Open rates: 25-40%
- Click rates: 3-8%
- Spam complaints: <0.1%
- Result: Inbox placement, some promotions tab

**Poor Credit (50-69 Score)**:
- Open rates: 15-25%
- Click rates: 1-3%
- Spam complaints: 0.1-0.5%
- Result: Promotions tab, some spam

**Bad Credit (<50 Score)**:
- Open rates: <15%
- Click rates: <1%
- Spam complaints: >0.5%
- Result: Spam folder or blocked

### The 5:1 Content Value Ratio

**5 Value Emails**:
- Educational content
- Industry insights
- How-to guides
- Entertainment
- Free resources

**1 Promotional Email**:
- Product launches
- Sales announcements
- Special offers
- Promotional campaigns

### Engaged Subscriber Segment Template

```
Segment Name: Engaged 60 Days
Conditions:
- Profile is in Newsletter list
AND
- (Opened email at least once in last 60 days
  OR Clicked email at least once in last 60 days
  OR Placed order at least once in last 60 days
  OR Subscribed in last 30 days)
```

### DMARC Record Template

```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=none; rua=mailto:dmarc-reports@yourdomain.com
TTL: 3600

Policy Options:
- p=none (monitoring only - recommended start)
- p=quarantine (send failures to spam)
- p=reject (block failures completely)
```

### 6-Week Recovery Protocol Template

**Week 1-2: Aggressive Cleaning**
- Segment: Engaged 30 days only
- Frequency: 2-3 emails per week
- Content: High-value only
- Goal: Stabilize reputation

**Week 3-4: Gradual Expansion**
- Segment: Engaged 60 days
- Frequency: 3 emails per week
- Content: Maintain high value
- Goal: Rebuild trust

**Week 5-6: Normal Operations**
- Segment: Full engaged list
- Frequency: Normal schedule
- Content: Resume normal mix
- Goal: Sustained improvement

### Subject Line Optimization Template

**Structure**: [Personalization] + [Benefit/Curiosity] + [Urgency/Scarcity]

**Examples**:
- "Sarah, your cart misses you (24h left)"
- "New arrival: The dress everyone's talking about"
- "Behind the scenes: How we make your favorite product"

**Avoid**:
- All caps: "FREE MONEY NOW"
- Excessive punctuation: "Amazing!!!!!!"
- Misleading claims
- Spam trigger words in excess

## Best Practices

### Technical Best Practices

1. **Complete Authentication Trilogy**: Never implement partial authentication. All three records (SPF, DKIM, DMARC) must be present and properly configured.

2. **Domain Alignment**: Ensure sending domain and reply-to domain share the same root domain. Misalignment triggers security filters.

3. **Dedicated Sending Domain**: Use your own domain for sending emails rather than shared ESP domains. This builds your domain reputation.

4. **Regular Authentication Audits**: Monthly verification of DNS records prevents configuration drift and catches issues early.

5. **Gradual DMARC Policy Progression**: Start with p=none for monitoring, graduate to p=quarantine, then p=reject only after thorough testing.

### Content Best Practices

6. **Value-First Content Strategy**: Maintain 5:1 ratio of valuable content to promotional content. Subscribers should anticipate your emails for the value they provide.

7. **Consistent Sending Schedule**: Establish and maintain regular sending frequency (3-4 times per week). Consistency builds trust with ISPs.

8. **Mobile-First Design**: Over 60% of emails are opened on mobile devices. Ensure responsive design and thumb-friendly buttons.

9. **Clear Unsubscribe Process**: Make unsubscribing easy and obvious. Hidden or difficult unsubscribe processes increase spam complaints.

10. **Preference Center Implementation**: Offer subscribers control over frequency and content types rather than all-or-nothing unsubscribe.

### Engagement Best Practices

11. **Engaged-Only Sending**: Never send to your entire list. Always segment to engaged subscribers to maintain high engagement metrics.

12. **Regular List Hygiene**: Monthly removal of unengaged subscribers protects sender reputation and improves overall metrics.

13. **Sunset Campaign Implementation**: Give unengaged subscribers one final chance to re-engage before suppression.

14. **Engagement Metric Monitoring**: Weekly review of open rates, click rates, and spam complaints with immediate action on concerning trends.

15. **Segmentation Refinement**: Continuously optimize engaged segment criteria based on performance data and industry benchmarks.

### Monitoring Best Practices

16. **Multi-Platform Reputation Monitoring**: Use Sender Score, Google Postmaster Tools, and Microsoft SNDS for comprehensive reputation tracking.

17. **Monthly Inbox Placement Testing**: Regular testing with tools like GlockApps ensures you catch deliverability issues before they become critical.

18. **Proactive Issue Resolution**: Address deliverability concerns immediately rather than waiting for metrics to recover naturally.

19. **Documentation and Tracking**: Maintain records of all changes, tests, and results for pattern recognition and troubleshooting.

20. **Cross-Platform Optimization**: Tailor strategies for specific ISPs (Gmail, Yahoo, Outlook) based on their unique requirements and behaviors.

## Common Mistakes to Avoid

### Technical Mistakes

1. **Incomplete Authentication Setup**: Implementing only SPF and DKIM without DMARC, or having misaligned authentication records.

2. **Shared Domain Usage**: Continuing to use ESP-provided sending domains (like klaviyoemail.com) instead of your own branded domain.

3. **Domain Misalignment**: Using different domains for sending and reply-to addresses, which triggers security filters.

4. **Ignoring DNS Propagation**: Making changes and expecting immediate results instead of allowing 24-48 hours for DNS propagation.

5. **DMARC Policy Rushing**: Jumping straight to p=reject without monitoring p=none results first.

### Content and Strategy Mistakes

6. **Sending to Entire List**: The most common and destructive mistake—sending campaigns to all subscribers instead of engaged segments only.

7. **Inconsistent Sending Patterns**: Sporadic sending followed by sudden high-volume campaigns, which triggers spam detection.

8. **Over-Promotional Content**: Sending primarily sales-focused emails without providing sufficient value to subscribers.

9. **Poor Subject Line Practices**: Using misleading subject lines, excessive punctuation, or all caps that trigger spam filters.

10. **Ignoring Mobile Optimization**: Designing emails that don't render properly on mobile devices where most emails are opened.

### List Management Mistakes

11. **Purchasing Email Lists**: Buying email lists guarantees spam folder placement and potential blacklisting.

12. **Ignoring Unengaged Subscribers**: Continuing to send to subscribers who haven't engaged in months, dragging down overall metrics.

13. **Difficult Unsubscribe Process**: Making it hard to unsubscribe, which increases spam complaints instead of clean list exits.

14. **No List Segmentation**: Treating all subscribers the same instead of segmenting based on engagement, preferences, or behavior.

15. **Ignoring Bounce Management**: Failing to remove hard bounces and continuing to send to invalid email addresses.

### Monitoring and Maintenance Mistakes

16. **Reactive Instead of Proactive**: Waiting until deliverability problems are severe before taking action.

17. **Ignoring Sender Reputation**: Not monitoring sender reputation scores and missing early warning signs.

18. **Inconsistent Monitoring**: Checking metrics sporadically instead of maintaining regular monitoring schedules.

19. **Single-Platform Focus**: Only monitoring Gmail deliverability while ignoring Yahoo, Outlook, and other major ISPs.

20. **No Testing Protocol**: Failing to regularly test inbox placement and authentication status.

### Recovery Mistakes

21. **Panic Overcorrection**: Making too many changes at once when deliverability issues arise, making it impossible to identify what works.

22. **Skipping Recovery Protocol**: Trying to immediately return to normal sending patterns instead of following gradual recovery steps.

23. **Insufficient Recovery Time**: Not allowing enough time for reputation recovery before resuming full sending volume.

24. **Ignoring Root Causes**: Fixing symptoms without addressing underlying issues like poor engagement or list quality.

25. **No Documentation**: Failing to document what caused problems and what fixed them, leading to repeated mistakes.

## Tools & Resources

### Authentication and Technical Tools

**DNS Record Checkers**:
- **MXToolbox.com**: Comprehensive DNS and email testing suite
- **DMARCAnalyzer.com**: Specialized DMARC record validation and reporting
- **Mail-Tester.com**: Overall email authentication and spam score testing
- **Google Admin Toolbox**: Free Google-provided email testing tools

**Sender Reputation Monitoring**:
- **Sender Score (Validity)**: Industry-standard sender reputation scoring (0-100 scale)
- **Google Postmaster Tools**: Gmail-specific reputation and delivery insights
- **Microsoft SNDS**: Outlook/Hotmail delivery and reputation data
- **Cisco Talos**: IP and domain reputation lookup

**Inbox Placement Testing**:
- **GlockApps**: Comprehensive inbox placement testing across major ISPs
- **Email on Acid**: Email testing including deliverability and rendering
- **Litmus**: Email testing and analytics platform
- **250ok (Validity)**: Enterprise-level deliverability monitoring

### Email Service Provider Tools

**Klaviyo-Specific Features**:
- Built-in deliverability dashboard
- Engagement-based segmentation tools
- Automated list cleaning capabilities
- A/B testing for subject lines and send times
- Comprehensive analytics and reporting

**Universal ESP Features to Utilize**:
- Engagement tracking and segmentation
- Automated unsubscribe handling
- Bounce management systems
- Campaign performance analytics
- List hygiene automation

### Content Optimization Tools

**Subject Line Testing**:
- **CoSchedule Headline Analyzer**: Subject line optimization suggestions
- **Zurb Foundation**: Email template testing
- **Litmus Subject Line Checker**: Spam trigger word detection

**Email Design and Testing**:
- **Canva**: Email design templates and graphics
- **Unsplash**: High-quality free images for emails
- **TinyPNG**: Image compression for faster loading
- **Email Client Testing Tools**: Preview across different email clients

### Monitoring and Analytics Tools

**Free Monitoring Tools**:
- **Google Analytics**: Email campaign traffic and conversion tracking
- **Google Search Console**: Domain reputation monitoring
- **Klaviyo Analytics**: Built-in engagement and deliverability metrics

**Advanced Analytics**:
- **Mixpanel**: Advanced email engagement tracking
- **Amplitude**: User behavior analytics
- **Custom Dashboards**: Klaviyo or third-party dashboard creation

### List Management and Hygiene Tools

**Built-in ESP Tools**:
- Engagement-based segmentation
- Automated suppression lists
- Bounce handling systems
- Unsubscribe management

**Third-Party List Tools**:
- **NeverBounce**: Email validation and list cleaning
- **ZeroBounce**: Email verification and deliverability tools
- **BriteVerify**: Real-time email validation

### Educational and Research Resources

**Industry Resources**:
- **Return Path (Validity) Blog**: Deliverability best practices and industry updates
- **Mailchimp Resources**: Email marketing education and guides
- **Campaign Monitor Blog**: Email marketing strategy and tactics
- **Email Marketing Institute**: Certification and advanced training

**Technical Documentation**:
- **RFC Standards**: Official email authentication specifications
- **ISP Postmaster Pages**: Gmail, Yahoo, Outlook sender guidelines
- **ESP Documentation**: Platform-specific best practices and setup guides

## Quality Checklist

### Pre-Launch Technical Checklist

**Authentication Verification**:
- [ ] SPF record exists and validates correctly
- [ ] DKIM record exists and validates correctly
- [ ] DMARC record created with proper policy
- [ ] All DNS records propagated (24-48 hours minimum)
- [ ] Authentication tested with multiple validation tools

**Domain Configuration**:
- [ ] Dedicated sending domain configured and verified
- [ ] Reply-to domain aligned with sending domain
- [ ] Default from/reply-to addresses set correctly
- [ ] Domain reputation baseline established

**ESP Configuration**:
- [ ] Sending domain set as default in ESP
- [ ] Proper from name and email configured
- [ ] Unsubscribe links automatically included
- [ ] Bounce handling configured properly

### Campaign Launch Checklist

**Audience Segmentation**:
- [ ] Campaign sent to engaged segment only (not entire list)
- [ ] Segment criteria verified (60-90 day engagement window)
- [ ] Unengaged subscribers excluded
- [ ] Segment size appropriate for sending history

**Content Quality**:
- [ ] Subject line under 50 characters
- [ ] Subject line honest and matches content
- [ ] Email provides clear value to recipients
- [ ] Mobile-responsive design verified
- [ ] Clear, prominent CTA included
- [ ] Unsubscribe link visible and functional

**Technical Validation**:
- [ ] Test email sent and received successfully
- [ ] Authentication passes on test email
- [ ] Email renders correctly across devices
- [ ] All links functional and tracking properly
- [ ] Images load correctly with alt text

### Post-Campaign Monitoring Checklist

**Immediate Monitoring (First 24 Hours)**:
- [ ] Open rate meets or exceeds baseline (25%+ target)
- [ ] Click rate meets expectations (2%+ target)
- [ ] Spam complaint rate under 0.1%
- [ ] Bounce rate under 2%
- [ ] No delivery errors or ESP warnings

**Weekly Performance Review**:
- [ ] Engagement metrics trending positively
- [ ] Unsubscribe rate under 0.5%
- [ ] No significant deliverability warnings
- [ ] Sender reputation scores stable
- [ ] List growth vs. churn ratio healthy

**Monthly Comprehensive Audit**:
- [ ] Inbox placement testing completed
- [ ] Sender reputation scores reviewed
- [ ] Authentication records verified
- [ ] List hygiene performed
- [ ] Engaged segment criteria optimized
- [ ] Content performance analyzed
- [ ] Deliverability trends documented

### Ongoing Maintenance Checklist

**Weekly Tasks**:
- [ ] Review engagement metrics dashboard
- [ ] Monitor for deliverability alerts or warnings
- [ ] Check for authentication or domain issues
- [ ] Review top-performing content for patterns

**Monthly Tasks**:
- [ ] Run comprehensive inbox placement test
- [ ] Check sender reputation across all platforms
- [ ] Clean list of unengaged subscribers
- [ ] Update engaged segment criteria if needed
- [ ] Review and optimize worst-performing campaigns
- [ ] Test subject line variations
- [ ] Audit email design and mobile optimization

**Quarterly Tasks**:
- [ ] Complete deliverability strategy review
- [ ] Benchmark against industry standards
- [ ] Review and update authentication policies
- [ ] Analyze year-over-year engagement trends
- [ ] Update content strategy based on performance
- [ ] Review and optimize sending frequency
- [ ] Conduct competitive analysis of email strategies

### Troubleshooting Checklist

**When Open Rates Drop**:
- [ ] Verify sending to engaged segment only
- [ ] Check inbox placement testing results
- [ ] Review recent subject line performance
- [ ] Confirm authentication records intact
- [ ] Analyze sending frequency changes
- [ ] Review content quality and value

**When Spam Complaints Increase**:
- [ ] Immediately segment to highly engaged only
- [ ] Review recent content for promotional overload
- [ ] Check unsubscribe link visibility and functionality
- [ ] Verify list source quality
- [ ] Review signup process and expectations
- [ ] Implement immediate list cleaning

**When Deliverability Fails**:
- [ ] Run complete authentication audit
- [ ] Check sender reputation scores
- [ ] Implement 6-week recovery protocol
- [ ] Review recent sending pattern changes
- [ ] Analyze engagement trend deterioration