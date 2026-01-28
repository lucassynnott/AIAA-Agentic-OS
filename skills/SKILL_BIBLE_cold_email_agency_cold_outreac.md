# SKILL BIBLE: Cold Email Agency Cold Outreach B2B Cold Email Copywriting Deliverability

> Sources: 3 expert videos analyzed from Lead Gen Jay
> Generated: 2026-01-08

---

## Executive Summary

Cold email has evolved into a sophisticated technical discipline requiring advanced infrastructure management, deliverability expertise, and multi-channel integration. The modern cold email landscape demands elimination of tracking fingerprints, diversified email infrastructure, and integration with LinkedIn automation to achieve sustainable results. Success requires mastering three core components: bulletproof technical setup that avoids ESP detection, cost-effective infrastructure scaling using hosting providers instead of expensive cold email platforms, and LinkedIn automation integration to multiply outreach capacity beyond traditional email limitations.

This skill bible synthesizes cutting-edge strategies for building enterprise-grade cold email operations that generate 100+ qualified leads monthly while maintaining high deliverability and avoiding account shutdowns. The approach combines technical infrastructure optimization, advanced automation, and multi-channel outreach to create a competitive advantage in B2B lead generation.

---

## Core Principles

**1. Fingerprint Elimination First**
Remove all technical traces that identify accounts as cold email operations. Custom tracking domains, open tracking, and click tracking create obvious fingerprints for ESPs to detect and shut down accounts.

**2. Infrastructure Diversification**
Never rely on a single email provider. Shift from 90% Google dependency to 30% Google, 30% Microsoft, 40% SMTP providers to eliminate single points of failure.

**3. Volume Discipline**
Keep sending under 20 emails per day per account. Higher volumes trigger automated detection systems and increase shutdown risk exponentially.

**4. Data-Driven Prospect Protection**
Use platform data to avoid hostile prospects, spam traps, and unlikely-to-reply contacts. One spam report can destroy weeks of reputation building.

**5. Multi-Channel Integration**
Combine email with LinkedIn automation to create multiple touchpoints and increase response rates by 200-300%.

**6. Cost Optimization Through Technical Innovation**
Use web hosting SMTP instead of expensive cold email providers to reduce infrastructure costs by 90% while maintaining deliverability.

**7. Continuous Monitoring and Adaptation**
Email rules change frequently. Implement weekly deliverability testing and adapt strategies based on performance data and platform updates.

---

## Complete Process (Step-by-Step)

### Phase 1: Infrastructure Foundation

**1. Remove All Tracking Fingerprints**
- Access cold email platform settings
- Navigate to mailbox configuration
- Remove all custom tracking domain CNAME records
- Delete DNS records pointing to tracking services
- Turn off open tracking, link tracking, and click tracking
- Remove unsubscribe links from templates

**2. Set Up Cost-Effective SMTP Infrastructure**
- Purchase domains from Spaceship, GoDaddy, or Namecheap
- Sign up for SiteGround GrowBig plan ($4.99/month)
- Add domains to SiteGround hosting
- Update name servers to point to SiteGround
- Wait 5 minutes to 48 hours for DNS propagation

**3. Configure DNS Authentication**
- Navigate to DNS Zone Editor in SiteGround
- Add SPF record: "v=spf1 include:siteground.com ~all"
- Generate and add DKIM record using EasyDMARC.com
- Add DMARC record: "v=DMARC1; p=quarantine; rua=mailto:admin@yourdomain.com"
- Verify all records using easydmarc.com scanner

### Phase 2: Email Account Creation

**4. Create SMTP Mailboxes**
- Navigate to Email Accounts in SiteGround
- Create maximum 5 mailboxes per domain
- Use consistent naming: j.feldman@, s.johnson@, etc.
- Generate strong, consistent passwords for easy management
- Extract SMTP configuration details for each account

**5. Diversify with Premium Providers**
- Set up Google Workspace accounts through official resellers ($2-3/month)
- Add Microsoft 365 accounts for additional coverage
- Maintain 30% Google, 30% Microsoft, 40% SMTP distribution
- Avoid legacy panels - use only subscription-based accounts

### Phase 3: Platform Configuration

**6. Import Accounts to Cold Email Platform**
- Use Instantly AI or similar platform with advanced deliverability features
- Import SMTP accounts via CSV bulk upload
- Connect using IMAP/SMTP configuration from hosting provider
- Test each account with sample emails before campaign launch

**7. Enable Advanced Deliverability Features**
- Navigate to Settings → Advanced Deliverability
- Check "Skip hostile prospects"
- Enable "Unlikely to reply" filtering
- Activate "Block list triggers"
- Enable recurring inbox placement testing
- Turn on "Bounce protect" and risk email blocking

### Phase 4: LinkedIn Integration Setup

**8. Set Up LinkedIn Automation**
- Subscribe to LinkedIn Sales Navigator ($90-100/month)
- Create Aimfox account starting with personal LinkedIn ($39/month)
- Rent additional LinkedIn accounts ($99/month each) for scaling
- Allow 1-2 weeks for account warming and SSI score building

**9. Configure LinkedIn Campaigns**
- Create outbound campaigns using Sales Navigator targeting
- Target recent job changers in specific industries
- Send blank connection requests (no notes)
- Set up post reactions and skill endorsements
- Auto-withdraw connection requests after 30 days

### Phase 5: Campaign Execution

**10. Create Email Sequences**
- Write 3-4 email sequence focusing on value, not sales
- Use AI for personalization based on prospect research
- Implement 2-3 day delays between emails
- A/B test different subject lines and messaging approaches

**11. Set Up LinkedIn Messaging**
- Message 1: Immediate value proposition after connection
- Message 2: Case study or specific value (1 day + 1 hour delay)
- Message 3: AI-personalized based on posts/achievements (2 days delay)
- Integrate with email sequences for multi-channel approach

### Phase 6: Monitoring and Optimization

**12. Implement Tracking and Analytics**
- Monitor inbox placement testing weekly
- Track spam complaint rates across all accounts
- Maintain cross-campaign block lists in Google Sheets
- Monitor LinkedIn SSI scores and connection acceptance rates

**13. Continuous Optimization**
- A/B test email templates and LinkedIn messages
- Adjust sending patterns based on deliverability data
- Update block lists with hostile prospects
- Scale successful campaigns to additional accounts

---

## Best Practices

**Email Infrastructure:**
✅ Limit to 5 mailboxes maximum per domain
✅ Use official reseller accounts only for Google Workspace
✅ Maintain updated block lists across all campaigns
✅ Enable all advanced deliverability features in platform
✅ Monitor inbox placement testing weekly
✅ Diversify email infrastructure across multiple providers
✅ Keep email volume under 20 per day per account

**LinkedIn Automation:**
✅ Send blank connection requests for maximum acceptance
✅ Personalize messages using prospect research
✅ React to posts before sending direct messages
✅ Keep initial messages focused on value, not sales
✅ Monitor SSI scores and account health regularly
✅ Work with automation platform team for account optimization
✅ Use Sales Navigator for precise targeting

**Campaign Management:**
✅ Target recent job changers for higher response rates
✅ Implement multi-touch sequences across email and LinkedIn
✅ Use AI for personalization at scale
✅ A/B test messaging approaches continuously
✅ Maintain professional account appearances
✅ Focus on relationship building over immediate sales

**Technical Setup:**
✅ Set up proper DNS authentication (SPF, DKIM, DMARC)
✅ Test deliverability before launching campaigns
✅ Use consistent passwords for easy bulk management
✅ Warm up new accounts gradually
✅ Monitor bounce rates and spam reports closely

---

## Common Mistakes

**Infrastructure Errors:**
❌ Using custom tracking domains that create ESP fingerprints
❌ Exceeding 20 emails per day per account
❌ Over-reliance on single email provider (90% Google)
❌ Using legacy panels instead of official resellers
❌ Skipping DNS authentication setup
❌ Creating more than 5 mailboxes per domain

**LinkedIn Automation Mistakes:**
❌ Including sales pitches in connection requests
❌ Using obviously fake or poorly optimized profiles
❌ Rushing the account warming process
❌ Sending generic, templated messages without personalization
❌ Scaling too quickly without testing messaging first
❌ Ignoring response rates and optimization opportunities

**Campaign Management Failures:**
❌ Continuing to email previously hostile prospects
❌ Ignoring spam complaint indicators
❌ Not using platform data protection features
❌ Failing to maintain cross-campaign block lists
❌ Skipping A/B testing and optimization
❌ Focusing on sales instead of value in initial outreach

**Technical Oversights:**
❌ Attempting setup before DNS propagation completes
❌ Using inconsistent passwords across accounts
❌ Ignoring IP reputation management
❌ Not monitoring deliverability metrics regularly
❌ Skipping account warming periods

---

## Tools & Resources

**Primary Platforms:**
- **Instantly AI** - Cold email platform with advanced deliverability features
- **Aimfox** - LinkedIn automation with account rental capabilities
- **SiteGround** - Web hosting for unlimited SMTP mailboxes ($4.99/month)
- **LinkedIn Sales Navigator** - Advanced prospect targeting ($90-100/month)

**Infrastructure Providers:**
- **Google Workspace Resellers** - Official subscription accounts ($2-3/month)
- **Microsoft 365** - Alternative email provider for diversification
- **Spaceship/GoDaddy/Namecheap** - Domain registration
- **Email Bison** - Private server solution for agencies ($500/month)

**Monitoring and Optimization:**
- **EasyDMARC.com** - Free DNS record generator and domain scanner
- **Make.com** - Workflow automation for lead research
- **Google Sheets** - Block list management and campaign tracking
- **Clay** - Advanced prospect research and data enrichment

**Alternative Tools:**
- Hey Reach, Meet Alfred, Closely - LinkedIn automation alternatives
- GreenGeeks - Alternative hosting provider
- Zapier - Workflow automation alternative to Make.com

---

## Advanced Techniques

**Walled Garden Strategy:**
For agencies handling multiple clients, consider private server solutions like Email Bison ($500/month) that provide completely isolated infrastructure with dedicated IPs and custom authentication.

**AI-Powered Personalization:**
Integrate Clay or similar tools to automatically research prospects and generate personalized opening lines based on recent posts, company news, and mutual connections.

**Cross-Platform Attribution:**
Set up tracking to identify which channel (email vs LinkedIn) generates responses, allowing for optimization of multi-channel sequences.

**Dynamic Block List Management:**
Implement automated systems that add hostile prospects to block lists across all campaigns in real-time, preventing cross-contamination.

**IP Reputation Monitoring:**
Use services like Sender Score and BarracudaCentral to monitor IP reputation across multiple blacklists and proactively address issues.

**Advanced A/B Testing:**
Test not just message content but sending times, sequence timing, and channel order (email first vs LinkedIn first) to optimize conversion rates.

**Prospect Scoring Integration:**
Use platform data to score prospects based on likelihood to reply, engagement history, and spam risk before including in campaigns.

---

## Metrics & KPIs

**Deliverability Metrics:**
- Inbox placement rate: Target 90%+ to primary inbox
- Spam complaint rate: Keep under 0.1%
- Bounce rate: Maintain under 2%
- Unsubscribe rate: Target under 0.5%

**LinkedIn Performance:**
- Connection acceptance rate: Aim for 90%+
- SSI (Social Selling Index): Target 18-20+
- Reply rate: Target 30%+ positive responses
- Profile views: Monitor for account health

**Campaign Performance:**
- Open rate: 40-60% (when tracking enabled)
- Reply rate: 15-30% across all channels
- Positive reply rate: 5-15%
- Meeting booking rate: 2-8%
- Cost per qualified lead: Under $50

**Infrastructure Health:**
- Account shutdown rate: Target 0%
- DNS authentication score: 100% on all domains
- IP reputation score: Maintain above 80
- Platform compliance score: Monitor weekly

**Business Metrics:**
- Leads generated per month: 100+ qualified leads
- Cost per lead: Under $20 with optimized infrastructure
- Revenue per lead: Track for ROI calculation
- Campaign ROI: Target 300%+ return

---

## Quick Reference Checklist

**Pre-Launch Setup:**
□ Remove all custom tracking domains and fingerprints
□ Set up diversified email infrastructure (30% Google, 30% Microsoft, 40% SMTP)
□ Configure DNS authentication (SPF, DKIM, DMARC) on all domains
□ Enable advanced deliverability features in platform
□ Set up LinkedIn automation with properly warmed accounts
□ Create and test email sequences with value-focused messaging
□ Import prospect lists with hostile prospect filtering enabled

**Daily Operations:**
□ Monitor sending volume (max 20 emails per account per day)
□ Check spam complaint rates and bounce rates
□ Update block lists with any hostile responses
□ Review LinkedIn connection acceptance rates
□ Respond to positive replies within 2 hours
□ Monitor account health scores and SSI ratings

**Weekly Optimization:**
□ Run inbox placement testing across all accounts
□ Analyze campaign performance metrics
□ A/B test new message variations
□ Update prospect targeting based on performance data
□ Review and optimize LinkedIn messaging sequences
□ Check DNS authentication status on all domains

**Monthly Strategic Review:**
□ Evaluate overall campaign ROI and lead quality
□ Scale successful campaigns to additional accounts
□ Retire underperforming messaging approaches
□ Update ideal customer profile based on response data
□ Plan infrastructure expansion for growth
□ Review and update block lists and targeting criteria

---

## Expert Insights

**"Google's recent crackdown on cold email accounts has forced a complete redesign of cold email infrastructure, requiring the elimination of tracking fingerprints and adoption of new safety protocols."** - Lead Gen Jay on modern deliverability requirements

**"Keep email volume under 20 per day per account. Higher volumes trigger automated detection systems and increase shutdown risk exponentially."** - Critical volume discipline for account preservation

**"Send blank connection requests for maximum acceptance. Adding promotional content to connection requests kills acceptance rates."** - LinkedIn automation best practice

**"Use web hosting SMTP instead of expensive cold email providers to reduce infrastructure costs by 90% while maintaining deliverability."** - Cost optimization strategy

**"One spam report can destroy weeks of reputation building. Use platform data to avoid hostile prospects, spam traps, and unlikely-to-reply contacts."** - Importance of prospect filtering

**"Shift from 90% Google dependency to 30% Google, 30% Microsoft, 40% SMTP providers to eliminate single points of failure."** - Infrastructure diversification principle

**"The combination of email and LinkedIn automation creates multiple touchpoints and increases response rates by 200-300%."** - Multi-channel integration value

**"Most marketers don't implement advanced deliverability protections, creating a competitive advantage for those who do."** - Market opportunity insight

This skill bible provides a complete framework for building and scaling enterprise-grade cold email operations that generate consistent results while maintaining high deliverability and avoiding common pitfalls that destroy campaigns.