# SKILL BIBLE: Complete Klaviyo E-Commerce Email Marketing Setup & Configuration

## Executive Summary

This skill bible provides comprehensive expertise for setting up Klaviyo as your e-commerce email service provider (ESP), covering everything from initial account creation to advanced technical configuration and deliverability optimization. Klaviyo is positioned as the definitive choice for e-commerce email marketing due to its superior integration capabilities with Shopify and other e-commerce platforms, advanced data tracking, and sophisticated automation features.

The setup process encompasses four critical phases: account creation and platform integration, technical deliverability configuration (including mandatory DNS records), dashboard navigation and analytics understanding, and comprehensive testing and verification procedures. This skill is essential for establishing a robust email marketing foundation that can scale with business growth and maintain high deliverability rates.

The knowledge contained here addresses both the strategic positioning of Klaviyo within the e-commerce marketing stack and the tactical implementation details required for successful deployment, including common pitfalls that can severely impact email performance and revenue generation.

## Source
- **Type:** Internal SOP/Skill Document
- **Category:** ecommerce-email
- **Original File:** setup_klaviyo.md

## Core Principles

### 1. Platform Exclusivity Principle
Klaviyo is positioned as the ONLY viable option for serious e-commerce email marketing, particularly for scaling businesses. This exclusivity is based on superior Shopify integration, advanced data tracking capabilities, and best-in-class automation and segmentation features.

### 2. Technical Deliverability Foundation
Email deliverability is non-negotiable and requires three mandatory DNS records: SPF (Sender Policy Framework), DKIM (DomainKeys Identified Mail), and DMARC (Domain-based Message Authentication). Without these, emails will consistently land in spam folders regardless of content quality.

### 3. Comprehensive Tracking Implementation
Success depends on implementing complete behavioral tracking, including the critical "Added to Cart" trigger that captures high-intent customers who don't reach the checkout phase. This goes beyond Shopify's default "Checkout Started" tracking.

### 4. Domain Alignment Requirement
The sending domain and reply-to address must share the same root domain to maintain deliverability standards. Misalignment results in automatic spam classification by email providers.

### 5. Revenue Attribution Understanding
Klaviyo's revenue attribution is imperfect but valuable, typically attributing purchases made within 3-5 days of email interaction. Target attribution should represent 30-50% of total store revenue, with deviations indicating needed adjustments in marketing strategy.

### 6. Data Hygiene Priority
List quality directly impacts sender reputation and deliverability. Proper data hygiene includes removing invalid emails, eliminating duplicates, checking for spam traps, and verifying opt-in status.

### 7. Gradual Volume Scaling
New domains require careful warm-up procedures, starting with small engaged segments and gradually increasing volume over 2-4 weeks to establish positive sender reputation.

### 8. Integration Completeness
Partial integrations lead to data gaps and missed revenue opportunities. All tracking mechanisms, including onsite behavior monitoring and cart abandonment triggers, must be fully enabled and verified.

## Step-by-Step Process

### Phase 1: Account Creation & Platform Integration

#### Step 1: Initial Account Setup
1. Navigate to klaviyo.com and initiate the signup process
2. Complete business information fields accurately
3. Follow Klaviyo's guided onboarding sequence
4. Verify email address and complete account activation

#### Step 2: Shopify Integration Configuration
1. **Access Integration Settings**
   - Navigate to Settings → Integrations within Klaviyo dashboard
   - Locate Shopify in the available integrations list
   - Click "Enable" on the Shopify integration option

2. **Verify Integration Status**
   - Confirm status displays "Status: Enabled"
   - Check for any error messages or incomplete connections
   - Test data flow between platforms

#### Step 3: Critical Integration Settings Configuration

**Onsite Tracking Enablement (REQUIRED)**
1. Navigate to Klaviyo → Settings → Integrations → Shopify
2. Check the box for "Add viewed product to my site"
3. **Implementation Process:**
   - Klaviyo provides direct link to Shopify configuration
   - Access Shopify → Online Store → Themes → Customize
   - Locate Klaviyo app embed section
   - Toggle ON the onsite tracking feature
   - Save theme changes and verify implementation

**Email Subscriber Synchronization**
1. Within Shopify integration settings
2. Enable "Sync your Shopify email subscribers to Klaviyo"
3. Assign synchronized subscribers to main "Newsletter" list
4. Configure sync frequency and data mapping

**Added to Cart Trigger Implementation (CRITICAL)**
This trigger captures customers who add products to cart but don't proceed to checkout, representing significant missed revenue opportunities.

**Implementation Steps:**
1. Reference Klaviyo's guide: "How to create an added to cart event for Shopify"
2. Access Shopify → Online Store → Themes → Edit Code
3. **For themes with Custom Liquid blocks:**
   - Add Klaviyo snippet via Custom Liquid block interface
4. **For themes without Custom Liquid support:**
   - Manually insert snippet into theme code files
5. Copy and implement the provided JavaScript snippet
6. **Testing Protocol:**
   - Use UTM parameter: `?utm_medium=email-testing`
   - Add product to cart while using test parameter
   - Verify trigger in Klaviyo → Analytics → Metrics → "Added to Cart"

### Phase 2: Technical Deliverability Setup

#### Step 4: DNS Records Configuration (MANDATORY)

**Required Records Assessment**
Before configuration, verify current status using these tools:
- GlockApps.com for comprehensive deliverability analysis
- DMARC Analyzer for DMARC record verification
- Inbox Insight for spam filter testing
- Generic SPF record checkers via Google search

**Dedicated Sending Domain Setup (Required as of February 2024)**
1. **Configuration Process:**
   - Navigate to Klaviyo → Settings → Email → Sending Domain
   - Follow the guided setup wizard
   - Klaviyo generates required DNS records automatically
   - Access domain provider's DNS management (GoDaddy, Namecheap, etc.)
   - Add provided DNS records to domain configuration
   - Wait 24-48 hours for verification completion

**DMARC Record Implementation**
1. **DNS Record Creation:**
   - Access domain's DNS settings through provider
   - Create new TXT record with following specifications:
     - Type: TXT
     - Name: `_dmarc`
     - Value: `v=DMARC1; p=none; rua=mailto:youremail@domain.com`
2. **Verification Process:**
   - Use online DMARC checker tools
   - Confirm record propagation and proper formatting
   - Monitor for any configuration errors

**SPF and DKIM Verification**
1. These records are typically configured automatically during sending domain setup
2. **Verification Steps:**
   - Reference Klaviyo Help Article: "SPF, DKIM, and DMARC for Klaviyo"
   - Use online SPF record checkers
   - Verify DKIM signature validation
   - Confirm all records are properly aligned

#### Step 5: Reply-To Domain Alignment
**Critical Requirement:** Sending domain and reply-to address must share the same root domain.

**Configuration Steps:**
1. Navigate to Klaviyo → Settings → Email
2. Set default reply-to address
3. **Verification Examples:**
   - ❌ Wrong: Sending from `send@getnike.com`, replying to `support@nike.com`
   - ✅ Correct: Sending from `send@nike.com`, replying to `support@nike.com`

### Phase 3: Dashboard Navigation & Analytics Setup

#### Step 6: Homepage Analytics Configuration

**Key Metrics Monitoring:**
1. **Total Store Revenue:** Complete revenue from e-commerce platform
2. **Klaviyo Attributed Revenue:** Revenue from email/SMS marketing efforts
   - Attribution window: 3-5 days post-email click
   - Expected slight inflation due to attribution modeling limitations
3. **Email/SMS Revenue Percentage Analysis:**
   - Target range: 30-50% of total revenue
   - Over 60%: Increase paid advertising investment
   - Under 30%: Improve email marketing systems
4. **Campaign vs. Flow Revenue Split:**
   - Campaigns: One-time broadcast emails
   - Flows: Automated trigger-based sequences
   - Target split: 40-60% either direction acceptable
   - Flow revenue under 30%: Requires automation improvements

**Time Period Configuration:**
- Access controls in top right corner of dashboard
- Default setting: 30-day period with previous period comparison
- Adjust based on analysis requirements

#### Step 7: Main Navigation Sections Mastery

**Campaigns Section Management**
1. **Campaign Creation Process:**
   - Click "Create Campaign" button
   - Assign descriptive name (e.g., "March 5th Flash Sale")
   - Select send date and time
   - Choose "Email" as campaign type
   - Define recipient lists or segments
   - Configure "Skip recently emailed profiles" (typically OFF)
   - Design email using drag-and-drop editor
   - Add compelling subject line and preview text
   - Schedule or send immediately based on strategy

**Flows Section Configuration**
1. **Essential Flow Types:**
   - Welcome Flow: New subscriber onboarding
   - Cart Abandoned: Recovery for added items
   - Checkout Abandoned: Recovery for initiated purchases
   - Browse Abandoned: Re-engagement for product viewers
   - Post-Purchase: Order confirmation and upselling
   - Winback: Re-engagement for inactive customers
   - Sunset: Final engagement attempt before removal

2. **Flow Editor Navigation:**
   - Structure: Trigger → Time Delay → Email → Time Delay → Email
   - Advanced features: Conditional splits, product-specific paths, dynamic content
   - Testing protocols for trigger verification

**Sign-Up Forms Optimization**
1. **Performance Metrics:**
   - Target conversion rate: 6-12% of site traffic
   - Monitor views vs. submissions ratio
   - Track revenue generated per form
2. **Form Types Available:**
   - Pop-up forms (desktop and mobile optimized)
   - Embedded forms (footer, mid-page placement)
   - Flyout forms for subtle engagement

**Audience Management: Lists & Segments**
1. **Lists vs. Segments Understanding:**
   - Lists: Static groups (Newsletter, VIP, etc.)
   - Segments: Dynamic groups based on behavioral conditions

2. **Segment Creation Process:**
   - Click "Create Segment"
   - Assign descriptive name (e.g., "Cart Abandoners - Last 30 Days")
   - Define conditions:
     - "Checkout Started at least once in last 30 days"
     - AND "Placed Order zero times in last 30 days"
   - Review live count of matching profiles
   - Save segment for campaign targeting

3. **Common Segment Examples:**
   - Engaged 60 days: Opened OR clicked in last 60 days
   - VIP Customers: Placed order 3+ times
   - High-value: Lifetime value > $500
   - At-risk: No purchase in 90+ days

#### Step 8: Content & Template Management
1. **Template Creation Process:**
   - Create blank email template
   - Add brand colors, logos, and fonts
   - Save as reusable template
   - Apply to future campaigns and flows

2. **Brand Consistency Maintenance:**
   - Establish template library
   - Standardize design elements
   - Create seasonal variations

#### Step 9: Analytics Dashboard Configuration
1. **Key Reports Setup:**
   - Total revenue tracking
   - Open rate monitoring
   - Click rate analysis
   - Conversion rate measurement
   - Revenue per recipient calculation
   - Flow performance comparison
   - Campaign performance evaluation

2. **Custom Dashboard Creation:**
   - Separate dashboards for campaigns vs. flows
   - Add custom metric cards
   - Track specific KPIs relevant to business goals

3. **Metrics Tab Utilization:**
   - Monitor all tracking events
   - Verify triggers are firing correctly
   - Check event frequency and patterns

### Phase 4: Data Management & List Hygiene

#### Step 10: Initial List Import (If Applicable)
1. **Data Migration Process:**
   - Export list from previous ESP
   - Clean data for invalid emails
   - Remove duplicates and inactive addresses
   - Import to Klaviyo with proper formatting
   - Add to appropriate list categories
   - Tag with import date for tracking

#### Step 11: Data Quality Maintenance
1. **Ongoing Hygiene Practices:**
   - Validate email formats regularly
   - Remove bounced addresses promptly
   - Check for spam trap identification
   - Verify opt-in status compliance
   - Monitor engagement metrics for list health

### Phase 5: Testing & Verification Protocols

#### Step 12: Email Delivery Testing
1. **Test Email Configuration:**
   - Add multiple test email addresses across providers
   - Send test campaigns to verify delivery
   - Check deliverability (inbox vs. spam placement)
   - Verify design rendering across desktop and mobile
   - Test all links for functionality
   - Confirm personalization tokens display correctly

#### Step 13: Trigger Verification Process
1. **Behavioral Trigger Testing:**
   - **Added to Cart Test:** Add product with `?utm_medium=email-testing`
   - **Checkout Started Test:** Initiate checkout process
   - **Viewed Product Test:** View product page
   - **Verification:** Check Klaviyo → Analytics → Metrics for event firing

#### Step 14: Domain Warm-up (New Domains Only)
1. **Gradual Volume Increase:**
   - Start with small engaged segments
   - Gradually increase volume over 2-4 weeks
   - Monitor deliverability metrics closely
   - Avoid sending to entire list immediately
   - Track sender reputation development

## Frameworks & Templates

### Klaviyo Settings Configuration Checklist

**Email Settings Framework:**
- [ ] Default from name configured
- [ ] Default from email address set
- [ ] Default reply-to email (same domain as from address)
- [ ] Default footer content created
- [ ] Unsubscribe page branding applied

**List Settings Framework:**
- [ ] Double opt-in setting (recommended: OFF for e-commerce)
- [ ] Default list for new subscribers designated
- [ ] List suppression settings configured

**Integration Settings Framework:**
- [ ] Shopify integration: ENABLED
- [ ] Onsite tracking: ENABLED
- [ ] Added to cart trigger: ENABLED
- [ ] Email sync: ENABLED

**Sending Settings Framework:**
- [ ] Dedicated sending domain: CONFIGURED
- [ ] SPF record: VERIFIED
- [ ] DKIM record: VERIFIED
- [ ] DMARC record: VERIFIED
- [ ] Smart sending: Strategy defined

### Revenue Attribution Analysis Framework

**Target Metrics:**
- Email/SMS attribution: 30-50% of total revenue
- Campaign vs. Flow split: 40-60% (either direction)
- Flow revenue minimum: 30% of email revenue

**Analysis Actions:**
- Over 60% attribution: Increase paid advertising
- Under 30% attribution: Improve email systems
- Low flow percentage: Enhance automation sequences

### Segmentation Strategy Template

**Engagement-Based Segments:**
- Engaged 30 days: Opened OR clicked in last 30 days
- Engaged 60 days: Opened OR clicked in last 60 days
- Engaged 90 days: Opened OR clicked in last 90 days

**Purchase-Based Segments:**
- VIP Customers: Placed order 3+ times
- High-value: Lifetime value > $X (define based on AOV)
- Recent purchasers: Placed order in last 30 days
- At-risk: No purchase in 90+ days

**Behavioral Segments:**
- Cart abandoners: Added to cart, no purchase in X days
- Browse abandoners: Viewed product, no purchase in X days
- Category browsers: Viewed specific product categories

## Best Practices

### Integration Best Practices

1. **Complete Implementation Priority**
   - Enable all available tracking options during initial setup
   - Verify each integration component individually
   - Test data flow between platforms before launching campaigns
   - Document all configuration settings for future reference

2. **Onsite Tracking Optimization**
   - Implement tracking on all customer touchpoints
   - Use UTM parameters for testing and verification
   - Monitor tracking event frequency in analytics
   - Regularly audit tracking implementation for accuracy

3. **Data Synchronization Management**
   - Schedule regular sync verification between platforms
   - Monitor for data discrepancies or gaps
   - Maintain backup data sources for critical information
   - Document data mapping for troubleshooting

### Deliverability Best Practices

1. **DNS Record Management**
   - Implement all three required records (SPF, DKIM, DMARC) simultaneously
   - Use dedicated sending domains for professional appearance
   - Maintain consistent domain alignment across all email elements
   - Monitor DNS record status regularly for any changes

2. **Domain Warm-up Strategy**
   - Start with highly engaged subscribers only
   - Gradually increase sending volume over 2-4 weeks
   - Monitor deliverability metrics throughout warm-up period
   - Avoid sending to purchased or old lists during warm-up

3. **Sender Reputation Maintenance**
   - Maintain consistent sending patterns
   - Monitor bounce rates and remove invalid addresses promptly
   - Track spam complaints and address issues immediately
   - Regular list hygiene and engagement monitoring

### Analytics and Optimization Best Practices

1. **Dashboard Configuration**
   - Create separate dashboards for different analysis needs
   - Focus on revenue-driving metrics over vanity metrics
   - Set up automated reporting for key stakeholders
   - Regular review and optimization of tracked metrics

2. **Segmentation Strategy**
   - Create segments based on behavior, not just demographics
   - Regularly update segment criteria based on performance
   - Test different segmentation approaches for optimization
   - Use segments for both targeting and exclusion purposes

3. **Testing and Verification**
   - Implement systematic testing protocols for all new features
   - Use test parameters to isolate and verify functionality
   - Document testing procedures for team consistency
   - Regular audit of all automated systems and triggers

## Common Mistakes to Avoid

### Critical Setup Errors

1. **Incomplete Onsite Tracking Implementation**
   - **Mistake:** Not enabling onsite tracking during initial setup
   - **Impact:** Loss of valuable cart abandonment and browse abandonment data
   - **Prevention:** Verify tracking implementation using test parameters and analytics verification

2. **Missing "Added to Cart" Trigger**
   - **Mistake:** Relying only on Shopify's default "Checkout Started" tracking
   - **Impact:** Missing high-intent customers who add to cart but don't reach checkout
   - **Prevention:** Manually implement added to cart tracking and verify functionality

3. **Domain Misalignment**
   - **Mistake:** Using different root domains for sending and reply-to addresses
   - **Impact:** Automatic spam classification and poor deliverability
   - **Prevention:** Ensure all email addresses share the same root domain

### Technical Configuration Errors

4. **Incomplete DNS Record Setup**
   - **Mistake:** Missing DMARC record or improper SPF/DKIM configuration
   - **Impact:** Guaranteed spam folder placement and poor deliverability
   - **Prevention:** Implement all three required DNS records and verify using online tools

5. **Inadequate Domain Warm-up**
   - **Mistake:** Sending large volumes immediately with new domains
   - **Impact:** Poor sender reputation and deliverability issues
   - **Prevention:** Implement gradual volume increase over 2-4 weeks

6. **Improper Reply-To Configuration**
   - **Mistake:** Not aligning reply-to domain with sending domain
   - **Impact:** Email provider spam classification
   - **Prevention:** Verify domain alignment before sending any campaigns

### Strategic Implementation Errors

7. **Sending to Unengaged Subscribers**
   - **Mistake:** Including inactive subscribers in regular campaigns
   - **Impact:** Damaged sender reputation and reduced deliverability
   - **Prevention:** Implement engagement-based segmentation and sunset flows

8. **Ignoring Data Hygiene**
   - **Mistake:** Not removing bounced or invalid email addresses
   - **Impact:** High bounce rates and sender reputation damage
   - **Prevention:** Regular list cleaning and bounce management

9. **Incomplete Integration Testing**
   - **Mistake:** Not verifying all triggers and data flows before launch
   - **Impact:** Missed revenue opportunities and poor customer experience
   - **Prevention:** Systematic testing of all integration points and triggers

## Tools & Resources

### Essential Verification Tools

1. **Deliverability Testing Tools**
   - **GlockApps.com:** Comprehensive deliverability analysis and spam filter testing
   - **DMARC Analyzer:** Specialized DMARC record verification and monitoring
   - **Inbox Insight:** Real-time deliverability testing across major email providers
   - **Generic SPF Checkers:** Available through Google search for quick verification

2. **DNS Management Tools**
   - Domain provider DNS management interfaces (GoDaddy, Namecheap, etc.)
   - Online DNS propagation checkers
   - DNS record verification tools

### Klaviyo-Specific Resources

3. **Official Klaviyo Resources**
   - **Klaviyo Help Center:** help.klaviyo.com - Comprehensive documentation
   - **Klaviyo Support Team:** Direct support with excellent response times
   - **Klaviyo Academy:** Free educational courses and certification programs

4. **Integration Documentation**
   - Shopify integration guides
   - E-commerce platform specific setup instructions
   - API documentation for advanced integrations

### Testing and Monitoring Tools

5. **Email Testing Tools**
   - Multiple email provider accounts for delivery testing
   - UTM parameter generators for tracking verification
   - Email rendering testing tools for design verification

6. **Analytics and Reporting Tools**
   - Klaviyo's built-in analytics dashboard
   - Custom reporting tools for advanced analysis
   - Revenue attribution tracking systems

## Quality Checklist

### Pre-Launch Verification Checklist

**Account Setup Verification:**
- [ ] Klaviyo account created and verified
- [ ] Business information completed accurately
- [ ] Team member access configured appropriately

**Integration Verification:**
- [ ] Shopify integration enabled and verified
- [ ] Onsite tracking implemented and tested
- [ ] Added to cart trigger configured and firing
- [ ] Email subscriber sync enabled and functioning
- [ ] Data flow between platforms verified

**Technical Configuration Verification:**
- [ ] Dedicated sending domain configured
- [ ] SPF record implemented and verified
- [ ] DKIM record implemented and verified
- [ ] DMARC record implemented and verified
- [ ] Reply-to domain alignment confirmed
- [ ] DNS propagation completed (24-48 hours)

**Dashboard Configuration Verification:**
- [ ] Analytics dashboard configured with key metrics
- [ ] Revenue attribution tracking verified
- [ ] Campaign vs. flow split monitoring enabled
- [ ] Custom segments created and tested
- [ ] Template library established

**Testing Protocol Completion:**
- [ ] Test email sends completed across multiple providers
- [ ] Deliverability verified (inbox placement)
- [ ] All triggers tested and verified
- [ ] Design rendering confirmed on desktop and mobile
- [ ] Link functionality verified
- [ ] Personalization tokens tested

### Ongoing Maintenance Checklist

**Weekly Monitoring:**
- [ ] Deliverability metrics reviewed
- [ ] Bounce rates monitored and addressed
- [ ] Revenue attribution analysis completed
- [ ] Engagement metrics tracked

**Monthly Audits:**
- [ ] DNS record status verified
- [ ] Integration functionality tested
- [ ] List hygiene performed
- [ ] Segment performance analyzed
- [ ] Template library updated

**Quarterly Reviews:**
- [ ] Complete system audit performed
- [ ] Strategy optimization based on performance data
- [ ] New feature implementation considered
- [ ] Team training and documentation updates

## AI Implementation Notes

### AI Agent Configuration Guidelines

**Knowledge Base Integration:**
- AI agents should reference this skill bible as the definitive source for Klaviyo setup procedures
- Maintain awareness of the sequential nature of setup phases - each phase builds upon the previous
- Understand that technical deliverability setup is non-negotiable and must be completed before sending campaigns

**Decision-Making Framework:**
- When advising on ESP selection, position Klaviyo as the only viable option for e-commerce
- For deliverability issues, always verify DNS record configuration first
- When troubleshooting integration problems, follow the systematic verification process outlined

**Response Patterns:**
- Always emphasize the critical nature of complete integration setup
- Provide specific technical details rather than general guidance
- Reference exact settings locations and configuration options
- Include verification steps for all recommended actions

### Automated Task Execution

**Setup Automation Capabilities:**
- AI can guide users through account creation and basic configuration
- Provide step-by-step DNS record setup instructions
- Generate custom segments based on business requirements
- Create testing protocols for verification procedures

**Monitoring and Maintenance:**
- Track setup completion status across all phases
- Monitor for common configuration errors and provide alerts
- Generate regular audit checklists based on timeline requirements
- Provide performance optimization recommendations based on analytics data

**Troubleshooting Support:**
- Diagnose integration issues using systematic verification approaches
- Provide specific solutions for common deliverability problems
-