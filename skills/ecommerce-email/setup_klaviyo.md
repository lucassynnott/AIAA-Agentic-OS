# Setup Klaviyo - Complete E-Commerce Email Marketing Setup

Expert skill for setting up Klaviyo as your e-commerce email service provider (ESP) with complete technical configuration, integrations, and deliverability requirements.

## Why Klaviyo?

Klaviyo is the ONLY true option for e-commerce email marketing, especially as you scale. It integrates seamlessly with Shopify and other e-commerce platforms, provides superior data tracking, and has the best features for automation and segmentation.

## Phase 1: Account Creation & Integration

### Create Klaviyo Account
1. Go to klaviyo.com and sign up
2. Enter your business information
3. Follow their easy onboarding instructions

### Shopify Integration
1. **In Klaviyo**: Navigate to Settings → Integrations
2. Find Shopify in the integrations list
3. Click "Enable" on Shopify
4. **Verify Integration Status**: Should show "Status: Enabled"

### Critical Integration Settings

#### Enable Onsite Tracking
**REQUIRED for tracking customer behavior**

1. In Klaviyo → Settings → Integrations → Shopify
2. Check "Add viewed product to my site"
3. **Purpose**: Tracks when customers view products, start checkout, abandon cart

**How to Enable**:
- Klaviyo will provide a direct link to Shopify
- Go to Shopify → Online Store → Themes → Customize
- Find Klaviyo app embed
- Toggle ON the onsite tracking
- Save theme

#### Sync Email Subscribers
1. In Shopify integration settings
2. Enable "Sync your Shopify email subscribers to Klaviyo"
3. Add them to your main "Newsletter" list

#### Enable "Added to Cart" Trigger
**CRITICAL**: This is different from "Checkout Started" and must be added manually

**Why This Matters**:
- Shopify tracks "Checkout Started" automatically
- But many customers add to cart and leave WITHOUT reaching checkout
- You're missing these high-intent customers without this trigger

**How to Add**:
1. Follow Klaviyo's guide: "How to create an added to cart event for Shopify"
2. Go to Shopify → Online Store → Themes → Edit Code
3. If your theme has Custom Liquid blocks:
   - Add the Klaviyo snippet via Custom Liquid block
4. If not:
   - Manually add snippet to theme code
5. Copy the provided JavaScript snippet
6. Test using UTM parameter: `?utm_medium=email-testing`
7. Check Klaviyo → Analytics → Metrics → "Added to Cart"

## Phase 2: Technical Deliverability Setup

**THIS IS MANDATORY** - Without these, your emails go to spam

### Required DNS Records

You MUST have these 3 records:
1. **SPF** (Sender Policy Framework)
2. **DKIM** (DomainKeys Identified Mail)
3. **DMARC** (Domain-based Message Authentication)

### Checking Current Status

Use these free tools:
- GlockApps.com
- DMARC Analyzer
- Inbox Insight
- Google search: "check SPF record"

### Setup Instructions

#### 1. Dedicated Sending Domain
**Required as of February 2024**

**What This Means**: Instead of sending from `klaviyoemail.com`, you send from your own domain (e.g., `send@yourbrand.com`)

**How to Set Up**:
1. Klaviyo → Settings → Email → Sending Domain
2. Follow the setup wizard
3. Klaviyo provides DNS records
4. Add records to your domain provider (GoDaddy, Namecheap, etc.)
5. Wait for verification (usually 24-48 hours)

#### 2. Setup DMARC Record

**Instructions**:
1. Log into your domain's DNS settings
2. Create a new TXT record with these values:

**Record Details**:
- Type: TXT
- Name: `_dmarc`
- Value: `v=DMARC1; p=none; rua=mailto:youremail@domain.com`

**Verify**: Use a DMARC checker tool online to confirm it's working

#### 3. Verify SPF and DKIM

These are usually set up automatically when you configure your sending domain in Klaviyo, but verify:

**Complete Guide**: Klaviyo Help Article → "SPF, DKIM, and DMARC for Klaviyo"

### Reply-To Domain Alignment

**CRITICAL REQUIREMENT**: Your sending domain and reply-to address MUST have the same root domain

**Wrong**: ❌
- Sending: `send@getnike.com`
- Reply-to: `support@nike.com`

**Correct**: ✅
- Sending: `send@nike.com`
- Reply-to: `support@nike.com`

**How to Set**:
1. Klaviyo → Settings → Email
2. Set default reply-to address
3. Ensure it matches your root domain

## Phase 3: Klaviyo Dashboard Walkthrough

### Homepage Analytics

**Key Metrics to Track**:

1. **Total Store Revenue**: All revenue from your e-commerce platform
2. **Klaviyo Attributed Revenue**: Revenue from email/SMS marketing
   - Note: Attribution is never 100% perfect
   - Klaviyo attributes purchases made within 3-5 days of email click
   - Usually slightly inflated but no perfect tracking exists

3. **Email/SMS Revenue Percentage**:
   - Target: 30-50% of total revenue
   - Over 60%: Invest more in paid ads
   - Under 30%: Improve email systems

4. **Campaigns vs. Flows Split**:
   - Campaigns: One-time emails sent to your list
   - Flows: Automated emails based on triggers
   - Target: 40-60% / 60-40% split (either direction is fine)
   - If flows are under 30%: Need flow improvements

**Time Period Selection**:
- Top right corner
- Default: 30-day period
- Compares to previous period

### Main Navigation Sections

#### Campaigns
**Purpose**: Send one-time emails to your list or segments

**How to Create**:
1. Click "Create Campaign"
2. Name it (e.g., "March 5th Flash Sale")
3. Select send date/time
4. Choose "Email"
5. Select recipients (lists/segments)
6. Skip recently emailed profiles: Usually OFF
7. Design email using drag-and-drop editor
8. Add subject line and preview text
9. Schedule or send immediately

#### Flows
**Purpose**: Automated email sequences triggered by customer actions

**Main Flows**:
- Welcome Flow
- Cart Abandoned
- Checkout Abandoned
- Browse Abandoned
- Post-Purchase
- Winback
- Sunset

**Flow Editor**:
- Trigger → Time Delay → Email → Time Delay → Email
- Can add conditional splits
- Product-specific paths
- Dynamic content

#### Sign-Up Forms
**Purpose**: Pop-ups and embedded forms to grow your list

**Key Metrics**:
- Conversion rate: Target 6-12% of site traffic
- Views vs. submissions
- Revenue generated

**Form Types**:
- Pop-up forms (desktop/mobile)
- Embedded forms (footer, mid-page)
- Flyout forms

#### Audience → Lists & Segments

**Lists**: Static groups (Newsletter, VIP, etc.)
**Segments**: Dynamic groups based on conditions

**Creating a Segment**:
1. Click "Create Segment"
2. Name it (e.g., "Cart Abandoners - Last 30 Days")
3. Define conditions:
   - "Checkout Started at least once in last 30 days"
   - AND "Placed Order zero times in last 30 days"
4. See live count of matching profiles
5. Save segment

**Common Segment Use Cases**:
- Engaged 60 days: Opened OR clicked in last 60 days
- VIP Customers: Placed order 3+ times
- High-value: Lifetime value > $500
- At-risk: No purchase in 90+ days

#### Content → Templates

**Purpose**: Save and reuse email designs

1. Create blank email
2. Add your brand colors, logos, fonts
3. Save as template
4. Use for future campaigns/flows

#### Analytics → Dashboards

**Key Reports**:
- Total revenue
- Open rates
- Click rates
- Conversion rates
- Revenue per recipient
- Flow performance
- Campaign performance

**Custom Dashboards**:
- Create separate dashboards for campaigns vs. flows
- Add custom cards
- Track specific metrics

**Metrics Tab**:
- See all tracking events
- Verify triggers are firing (e.g., "Added to Cart")
- Check event frequency

## Phase 4: List & Data Hygiene

### Initial List Import (If Applicable)

1. Export list from previous ESP
2. Clean data (remove invalid emails)
3. Import to Klaviyo
4. Add to appropriate list
5. Tag with import date

### Data Quality Checks

- Valid email formats
- Remove duplicates
- Check for spam traps
- Verify opt-in status

## Phase 5: Testing & Verification

### Test Email Sends

1. Add test email addresses
2. Send test campaigns
3. Check:
   - Deliverability (inbox vs. spam)
   - Design rendering (desktop/mobile)
   - Links working
   - Personalization tokens displaying correctly

### Verify Triggers

1. **Added to Cart**: Add product to cart with `?utm_medium=email-testing`
2. **Checkout Started**: Initiate checkout
3. **Viewed Product**: View a product page
4. Check Klaviyo → Analytics → Metrics to see events firing

### Domain Warm-up (New Domains Only)

If you're using a brand new domain:
1. Start sending to small engaged segments
2. Gradually increase volume over 2-4 weeks
3. Monitor deliverability metrics
4. Avoid sending to entire list immediately

## Klaviyo Settings Checklist

Go through these critical settings:

### Email Settings
- [ ] Default from name
- [ ] Default from email address
- [ ] Default reply-to email (same domain as from address)
- [ ] Default footer
- [ ] Unsubscribe page branding

### List Settings
- [ ] Double opt-in (recommended: OFF for e-commerce)
- [ ] Default list for new subscribers
- [ ] List suppression settings

### Integration Settings
- [ ] Shopify integration: ENABLED
- [ ] Onsite tracking: ENABLED
- [ ] Added to cart trigger: ENABLED
- [ ] Email sync: ENABLED

### Sending Settings
- [ ] Dedicated sending domain: CONFIGURED
- [ ] SPF record: VERIFIED
- [ ] DKIM record: VERIFIED
- [ ] DMARC record: VERIFIED
- [ ] Smart sending: Consider your strategy

## Common Setup Mistakes to Avoid

1. **Not enabling onsite tracking**: Lose cart abandonment data
2. **Missing "Added to Cart" trigger**: Miss high-intent customers
3. **Wrong reply-to domain**: Emails go to spam
4. **No DMARC record**: Guaranteed spam folder
5. **Not warming up new domain**: Poor deliverability
6. **Sending to unengaged subscribers**: Hurts sender reputation

## Resources & Help

- Klaviyo Help Center: help.klaviyo.com
- Klaviyo support team (excellent response time)
- Klaviyo Academy (free courses)

## Timeline

**Expected Setup Time**: 4-6 hours total
- Account creation & integration: 1-2 hours
- Technical deliverability: 2-3 hours (including DNS propagation wait)
- Dashboard familiarization: 1 hour

## What's Next?

After setup is complete:
1. Create your first pop-up form (list growth)
2. Build core revenue flows (abandoned cart, welcome series)
3. Start sending campaigns (3-4 per week)
4. Monitor deliverability metrics

---

**Remember**: Klaviyo is the only true ESP for e-commerce. Don't overcomplicate this. Follow these steps, and you'll have a rock-solid foundation for your email marketing program.
