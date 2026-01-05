# Cold Email Infrastructure Setup - Complete Technical Guide

## Skill Overview
This is the foundational skill for setting up a professional cold email infrastructure from scratch. You'll learn the exact technical setup process for domains, email accounts, DNS records, and verification systems that enable high-deliverability cold email campaigns. This guide is based on proven methods used by successful cold email agencies.

**Time Required**: 2-4 hours for complete setup
**Technical Level**: Intermediate (detailed instructions provided)
**Prerequisites**: Domain registrar account, email sending platform account

---

## Table of Contents
1. [Understanding Cold Email Infrastructure](#understanding-cold-email-infrastructure)
2. [Domain Acquisition Strategy](#domain-acquisition-strategy)
3. [Email Account Setup Process](#email-account-setup-process)
4. [DNS Configuration Deep Dive](#dns-configuration-deep-dive)
5. [Domain Verification Systems](#domain-verification-systems)
6. [Troubleshooting Common Issues](#troubleshooting-common-issues)
7. [Quality Assurance Checklist](#quality-assurance-checklist)

---

## Understanding Cold Email Infrastructure

### Why You Need Multiple Domains

**The Core Problem**: When sending cold emails, you cannot use your primary business domain (e.g., yourbusiness.com) because:
- Cold emailing will damage your primary domain's reputation
- If your domain gets blacklisted, all your business emails are affected
- You need to protect your main brand reputation

**The Solution**: Create a separate "sending infrastructure" using secondary domains that:
- Look similar to your main domain
- Can be replaced if they get blacklisted
- Don't affect your primary business operations

### Infrastructure Components Overview

A complete cold email infrastructure consists of:

1. **Primary Domain** (yourbusiness.com)
   - Your main business website and email
   - NEVER used for cold outreach
   - Protected at all costs

2. **Secondary Sending Domains** (3-5 variations)
   - Used exclusively for cold email
   - Examples: yourbiz.com, yourbusiness.co, yourbusiness.io
   - Each needs separate DNS configuration

3. **Email Accounts** (3-10 per domain)
   - Gmail Workspace or Outlook accounts
   - Each account sends limited volume daily
   - Distributed sending protects infrastructure

4. **Tracking & Forwarding**
   - All replies forward to your main inbox
   - Centralized management despite distributed sending
   - Maintains professional response workflow

### The Numbers That Matter

For a typical cold email campaign:
- **Accounts needed**: 3-10 email accounts
- **Domains needed**: 2-5 secondary domains
- **Sending volume**: 40-50 emails per account per day
- **Total daily capacity**: 120-500 emails with proper setup
- **Cost**: $100-300/month for complete infrastructure

---

## Domain Acquisition Strategy

### Step 1: Choose Your Domain Registrar

**Recommended Registrars**:
1. **Namecheap** (Most Popular)
   - Pros: Cheap, easy DNS management, good customer support
   - Cons: Sometimes slow customer service
   - Cost: $8-15/year per domain
   - Best for: Beginners and most agencies

2. **GoDaddy** (Alternative)
   - Pros: Fast setup, familiar interface
   - Cons: More expensive, upsell-heavy
   - Cost: $12-20/year per domain
   - Best for: Quick setup needs

3. **Cloudflare** (Advanced)
   - Pros: At-cost pricing, excellent DNS, built-in security
   - Cons: Steeper learning curve
   - Cost: $8-10/year per domain
   - Best for: Technical users

### Step 2: Select Your Domain Variations

**Naming Strategy - The "Close Cousin" Method**:

If your primary domain is **yourbusiness.com**, consider:

**Option A - TLD Variations** (Recommended):
- yourbusiness.co
- yourbusiness.io
- yourbusiness.net
- yourbusiness.agency

**Option B - Name Variations**:
- yourbiz.com
- yourbusinesshq.com
- getyourbusiness.com
- yourbusinessteam.com

**Option C - Hybrid Approach**:
- yourbiz.io
- yourbusinesshq.co
- getyourbusiness.agency

**Critical Rules**:
- Must be believable as part of your brand
- Should pass the "squint test" (looks similar at quick glance)
- Avoid hyphens, numbers, or strange spellings
- Check trademark availability
- Verify domain isn't on spam blacklists

### Step 3: Domain Purchase Walkthrough (Namecheap Example)

**Exact Steps**:

1. **Search for Domain**:
   - Go to namecheap.com
   - Enter your desired domain in search bar
   - Click "Search"

2. **Add to Cart**:
   - Select your domain from results
   - Click "Add to Cart"
   - **DO NOT** add extra services:
     - ❌ Domain Privacy (optional, but not required)
     - ❌ Premium DNS (we'll configure manually)
     - ❌ SSL Certificate (not needed for email)
     - ❌ Website hosting (we're only using for email)

3. **Configure Purchase**:
   - Select 1-year registration (standard)
   - Auto-renew: Your choice (recommended ON)
   - Click "Confirm Order"

4. **Account Creation**:
   - Create Namecheap account or log in
   - Enter payment information
   - Complete purchase

5. **Verify Purchase**:
   - Check email for confirmation
   - Log into Namecheap dashboard
   - Verify domain appears in "Domain List"

**Screenshot Checkpoint**: You should see your new domain in the Namecheap dashboard with status "Active"

### Step 4: Bulk Domain Purchase (For Multiple Domains)

If buying 3-5 domains at once:

1. Search for first domain
2. Add to cart but DON'T checkout
3. Search for second domain
4. Add to cart
5. Repeat for all domains
6. Checkout once with all domains in cart
7. Apply bulk discount code if available (search "Namecheap coupon codes")

**Pro Tip**: Namecheap offers discounts for multiple domain purchases. Always search for current promo codes before checkout.

### Step 5: Domain Privacy Consideration

**What is Domain Privacy?**
- Hides your personal information from WHOIS lookups
- Shows registrar's information instead of yours
- Costs $5-10/year extra per domain

**Do you need it?**
- ✅ YES if using personal information
- ✅ YES if you want extra privacy layer
- ❌ NO if using business information that's already public
- ❌ NO if trying to minimize costs

**Recommendation**: Add it for the first year, can remove later if needed.

---

## Email Account Setup Process

### Platform Choice: Gmail Workspace vs Microsoft 365

**Gmail Workspace** (Recommended):
- **Cost**: $6/user/month (Business Starter)
- **Pros**:
  - Better deliverability for cold email
  - Easier integration with sending tools
  - More familiar interface
  - Better spam filter reputation
- **Cons**:
  - Requires credit card
  - Monthly recurring cost
- **Best for**: Most cold email campaigns

**Microsoft 365**:
- **Cost**: $6/user/month (Business Basic)
- **Pros**:
  - Good deliverability
  - Professional appearance
  - Better for B2B corporate targets
- **Cons**:
  - Slightly more complex setup
  - Less common in cold email space
- **Best for**: B2B campaigns targeting corporate decision-makers

**For this guide, we'll use Gmail Workspace** (most common and best results).

### Gmail Workspace Setup - Complete Walkthrough

#### Phase 1: Create Google Workspace Account

**Step-by-Step Process**:

1. **Navigate to Google Workspace**:
   - Go to workspace.google.com
   - Click "Get Started"

2. **Business Information**:
   - Business name: Your actual business name
   - Number of employees: Select "Just you" or "2-9"
   - Country: Select your country
   - Click "Next"

3. **Contact Information**:
   - First and Last Name: Your name
   - Current email: Your personal email (for account recovery)
   - Click "Next"

4. **Domain Setup**:
   - Select "Yes, I have one I can use"
   - Enter your secondary domain (e.g., yourbiz.com)
   - Click "Next"

5. **Username Creation**:
   - Create your first admin account
   - Format: firstname@yourbiz.com
   - Set strong password (save this!)
   - Click "Next"

6. **Verification Method Selection**:
   - Select "Verify with your domain host"
   - We'll complete this in next section
   - Click "Next"

7. **Checkout**:
   - Select "Business Starter" plan ($6/month)
   - Number of licenses: Start with 3-5
   - Enter payment information
   - **Important**: Set calendar reminder for before renewal
   - Complete purchase

**Screenshot Checkpoint**: You should land on Google Workspace Admin Console

#### Phase 2: Domain Verification

This is THE MOST CRITICAL step. If done incorrectly, your emails won't send.

**What is Domain Verification?**
Domain verification proves to Google that you own the domain you're trying to use for email. Without verification, Google won't let you send/receive emails.

**Verification Method - TXT Record** (Recommended):

1. **Get Your Verification Code**:
   - In Google Workspace Admin Console
   - Look for "Verify domain" alert/button
   - Click it
   - You'll see a verification code like: `google-site-verification=xxxxxxxxxxxxxxxxxxx`
   - Copy this entire code

2. **Add TXT Record to Namecheap**:
   - Open new tab, go to namecheap.com
   - Log into your account
   - Click "Domain List"
   - Find your domain (yourbiz.com)
   - Click "Manage"
   - Go to "Advanced DNS" tab

3. **Create Verification Record**:
   - Click "Add New Record"
   - Type: Select "TXT Record"
   - Host: Enter `@` (this means root domain)
   - Value: Paste your Google verification code
   - TTL: Select "Automatic" or "1 min"
   - Click "Save All Changes" (green checkmark)

4. **Verify in Google Workspace**:
   - Return to Google Workspace Admin tab
   - Click "Verify" button
   - Wait 5-10 seconds
   - **If successful**: You'll see "Verified" confirmation
   - **If unsuccessful**: See troubleshooting section below

**Critical Notes**:
- DNS changes can take 1-48 hours to propagate
- Usually works within 5-10 minutes
- Don't delete the TXT record after verification
- Keep it permanently in your DNS

**Troubleshooting Verification Issues**:

**Problem**: "Could not verify domain"
**Solutions**:
1. Wait 10 more minutes and try again
2. Check for typos in TXT record value
3. Ensure Host is exactly `@`
4. Clear browser cache and try again
5. Try verification from incognito/private window

**Problem**: "TXT record not found"
**Solutions**:
1. Check DNS propagation at dnschecker.org
2. Verify you're editing correct domain
3. Ensure you clicked "Save All Changes"
4. Wait 24 hours and try again

#### Phase 3: MX Records Setup (Email Routing)

**What are MX Records?**
MX (Mail Exchange) records tell the internet where to send emails for your domain. Without correct MX records, emails sent to yourname@yourbiz.com will bounce.

**Google Workspace MX Records**:

You need to add these EXACT records to your DNS:

| Priority | Host | Value |
|----------|------|-------|
| 1 | @ | ASPMX.L.GOOGLE.COM |
| 5 | @ | ALT1.ASPMX.L.GOOGLE.COM |
| 5 | @ | ALT2.ASPMX.L.GOOGLE.COM |
| 10 | @ | ALT3.ASPMX.L.GOOGLE.COM |
| 10 | @ | ALT4.ASPMX.L.GOOGLE.COM |

**Step-by-Step MX Record Setup**:

1. **Access DNS Management**:
   - Log into Namecheap
   - Domain List → Your domain → Manage
   - Advanced DNS tab

2. **Add First MX Record**:
   - Click "Add New Record"
   - Type: Select "MX Record"
   - Host: Enter `@`
   - Value: Enter `ASPMX.L.GOOGLE.COM`
   - Priority: Enter `1`
   - TTL: Automatic
   - Click "Save"

3. **Add Remaining MX Records**:
   Repeat the process for all 5 records above
   - Make sure priorities match exactly
   - All hosts should be `@`
   - Double-check spelling of values

4. **Remove Old MX Records**:
   - If you see any existing MX records
   - Delete them (click red X)
   - Only Google's MX records should exist

5. **Save Changes**:
   - Click "Save All Changes" (green checkmark)
   - Wait 5-10 minutes for propagation

**Verification**:

Test your MX records at mxtoolbox.com:
1. Go to mxtoolbox.com
2. Enter your domain (yourbiz.com)
3. Click "MX Lookup"
4. Should show all 5 Google MX records
5. Priority should be in correct order

**Screenshot Checkpoint**: MXToolbox should show all 5 Google MX records with correct priorities.

#### Phase 4: SPF Record Setup (Sender Authentication)

**What is SPF?**
SPF (Sender Policy Framework) tells receiving email servers that Google is authorized to send emails on behalf of your domain. Without SPF, your emails will likely go to spam.

**Google Workspace SPF Record**:

Add this TXT record:
- Host: `@`
- Value: `v=spf1 include:_spf.google.com ~all`
- TTL: Automatic

**Step-by-Step**:

1. **Access Advanced DNS** (Namecheap):
   - Domain List → Your domain → Manage → Advanced DNS

2. **Add SPF Record**:
   - Click "Add New Record"
   - Type: Select "TXT Record"
   - Host: Enter `@`
   - Value: Enter `v=spf1 include:_spf.google.com ~all`
   - TTL: Automatic
   - Click "Save All Changes"

**Important SPF Notes**:
- Only ONE SPF record per domain (multiple will break it)
- If you already have an SPF record, edit it to include Google's directive
- The `~all` at the end means "softfail" (recommended for cold email)
- Alternative: `-all` means "hardfail" (stricter, but may cause issues)

**SPF Record Verification**:

Test at mxtoolbox.com:
1. Go to mxtoolbox.com/spf.aspx
2. Enter your domain
3. Should show: "SPF record passed validation test"
4. Should include _spf.google.com in the record

#### Phase 5: DKIM Setup (Email Signing)

**What is DKIM?**
DKIM (DomainKeys Identified Mail) adds a digital signature to your emails, proving they haven't been tampered with. This dramatically improves deliverability.

**Google Workspace DKIM Setup**:

1. **Generate DKIM Key in Google Workspace**:
   - Go to Google Admin Console
   - Navigate to: Apps → Google Workspace → Gmail → Authenticate email
   - Find "DKIM Authentication" section
   - Click "Generate New Record"
   - Select your domain from dropdown
   - Click "Generate"
   - You'll see a record like:

```
Domain name: google._domainkey.yourbiz.com
TXT record value: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNA... (very long string)
```

2. **Add DKIM Record to DNS**:
   - Copy the TXT record value
   - Go to Namecheap → Advanced DNS
   - Click "Add New Record"
   - Type: TXT Record
   - Host: Enter `google._domainkey`
   - Value: Paste the entire DKIM value (starts with v=DKIM1...)
   - TTL: Automatic
   - Save All Changes

3. **Activate DKIM in Google Workspace**:
   - Return to Google Admin Console
   - In the DKIM section
   - Click "Start Authentication"
   - Status should change to "Authenticating email"
   - Wait 24-48 hours
   - Check back - status should show "Authenticating email" with checkmark

**DKIM Verification**:

After 24-48 hours:
1. Go to Google Admin Console → Gmail → Authenticate email
2. DKIM status should show green checkmark
3. Test with mail-tester.com (send test email)

**Common DKIM Issues**:

**Problem**: "DKIM not authenticating"
**Solutions**:
- Wait full 48 hours (Google's stated time)
- Verify TXT record at dnschecker.org
- Check for spaces or line breaks in DKIM value
- Make sure host is exactly `google._domainkey`

#### Phase 6: DMARC Setup (Email Policy)

**What is DMARC?**
DMARC (Domain-based Message Authentication, Reporting & Conformance) tells receiving servers what to do if your SPF or DKIM checks fail. It's the final piece of email authentication.

**DMARC Record for Cold Email**:

Add this TXT record:
- Host: `_dmarc`
- Value: `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com`
- TTL: Automatic

**Step-by-Step**:

1. **Add DMARC Record**:
   - Namecheap → Advanced DNS
   - Add New Record
   - Type: TXT Record
   - Host: `_dmarc`
   - Value: `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com`
   - Replace yourdomain.com with your actual domain
   - Save All Changes

**DMARC Policy Options**:
- `p=none` - Monitor only, don't reject (best for cold email)
- `p=quarantine` - Send failures to spam folder
- `p=reject` - Reject failures completely (too strict for cold email)

**For Cold Email**: Always use `p=none` to avoid false rejections.

**DMARC Verification**:

Test at mxtoolbox.com/dmarc.aspx:
1. Enter your domain
2. Should show valid DMARC record
3. Policy should show "none"

#### Phase 7: Create Additional Email Accounts

After setting up your first account, create more accounts for distributed sending:

1. **Access User Management**:
   - Google Admin Console
   - Directory → Users
   - Click "Add New User"

2. **Create User**:
   - First name: Use real first names (John, Sarah, Mike)
   - Last name: Use real last names or company name
   - Primary email: firstname@yourbiz.com
   - Password: Set strong password
   - Click "Add New User"

3. **Recommended Account Names**:
   For a 5-account setup:
   - john@yourbiz.com (Main outreach)
   - sarah@yourbiz.com (Outreach 2)
   - mike@yourbiz.com (Outreach 3)
   - team@yourbiz.com (Outreach 4)
   - hello@yourbiz.com (Outreach 5)

**Pro Tips for Account Creation**:
- Use real-sounding names (helps deliverability)
- Avoid generic names like "info" or "noreply" for main senders
- Keep passwords secure but accessible to team
- Set up 2FA for security (optional but recommended)

#### Phase 8: Email Forwarding Setup (Critical!)

This ensures all replies to your sending accounts come to your main inbox.

**Why Email Forwarding?**
- You're sending from john@yourbiz.com
- But you want replies to go to your main inbox: you@yourbusiness.com
- Forwarding makes this automatic

**Setup Process**:

1. **For Each Sending Account**:
   - Log into that Gmail account (e.g., john@yourbiz.com)
   - Click gear icon → See all settings
   - Go to "Forwarding and POP/IMAP" tab
   - Click "Add a forwarding address"
   - Enter your main email: you@yourbusiness.com
   - Click "Next" → "Proceed" → "OK"

2. **Verify Forwarding Address**:
   - Check your main inbox
   - Find confirmation email from Gmail
   - Click verification link
   - Return to sending account settings
   - Select "Forward a copy of incoming mail to..."
   - Choose your main email from dropdown
   - Select "delete Gmail's copy" (optional, keeps inbox clean)
   - Click "Save Changes"

3. **Test Forwarding**:
   - Send test email to john@yourbiz.com
   - Check if it appears in you@yourbusiness.com inbox
   - Should arrive within 30 seconds

**Repeat for all sending accounts**.

---

## DNS Configuration Deep Dive

### Understanding DNS Records for Email

**What is DNS?**
DNS (Domain Name System) is like a phone book for the internet. It translates domain names (yourbiz.com) into instructions for email servers, web browsers, and other internet services.

### Complete DNS Configuration for Cold Email

For a properly configured cold email domain, you need these DNS records:

| Record Type | Purpose | Critical for Email? |
|-------------|---------|---------------------|
| MX | Routes incoming email | ✅ YES - Essential |
| TXT (SPF) | Authorizes email senders | ✅ YES - Essential |
| TXT (DKIM) | Signs emails cryptographically | ✅ YES - Essential |
| TXT (DMARC) | Sets email authentication policy | ✅ YES - Essential |
| TXT (Verification) | Proves domain ownership | ✅ YES - For setup |
| A | Points domain to IP address | ❌ NO - Only for website |
| CNAME | Aliases for subdomains | ❌ NO - Not needed |

### DNS Propagation and Timing

**What is DNS Propagation?**
When you add a DNS record, it doesn't take effect instantly. It needs to "propagate" across the internet's DNS servers.

**Typical Propagation Times**:
- Minimum: 5 minutes
- Average: 30 minutes to 4 hours
- Maximum: 24-48 hours

**How to Check DNS Propagation**:

1. **DNSChecker.org** (Recommended):
   - Go to dnschecker.org
   - Select record type (A, MX, TXT, etc.)
   - Enter your domain
   - Shows propagation status worldwide
   - Green checkmarks = propagated

2. **MXToolbox.com**:
   - Go to mxtoolbox.com
   - Select test type from dropdown
   - Enter domain
   - Shows detailed results and errors

3. **WhatsMyDNS.net**:
   - Go to whatsmydns.net
   - Select record type
   - Enter your domain
   - Shows global DNS servers' responses

**Pro Tip**: Always wait at least 30 minutes after DNS changes before testing email sending.

### Advanced DNS Configuration

#### Custom Tracking Domain (Optional but Recommended)

**Why Use a Tracking Domain?**
- Separates email sending from link tracking
- Improves deliverability
- Protects primary domain reputation
- Professional appearance

**Setup Process**:

1. **Purchase Tracking Domain**:
   - Get another domain variation (track-yourbiz.com)
   - Or use subdomain of main (track.yourbiz.com)

2. **Configure in Sending Platform**:
   - Most platforms (SmartLead, Instantly) have tracking domain setup
   - Follow their specific instructions
   - Usually requires CNAME record

3. **Add CNAME Record**:
   - In your DNS (Namecheap)
   - Add CNAME record per platform instructions
   - Usually points to platform's tracking server

#### Subdomain for Sending (Advanced Strategy)

**Strategy**: Use subdomain for sending to protect root domain.

Example:
- Root domain: yourbiz.com (for landing page)
- Sending subdomain: mail.yourbiz.com (for cold email)

**Setup**:
1. All DNS records use subdomain instead of `@`
2. MX Host: `mail` instead of `@`
3. SPF Host: `mail` instead of `@`
4. DKIM Host: `google._domainkey.mail` instead of `google._domainkey`
5. Email addresses: john@mail.yourbiz.com

**Pros**:
- Protects root domain
- Can blacklist subdomain without affecting root
- Professional appearance

**Cons**:
- Slightly more complex setup
- Longer email addresses
- May confuse some recipients

**Recommendation**: Use root domain unless you have strong technical skills and specific need for subdomain protection.

---

## Domain Verification Systems

### Why Verification Matters

Domain verification proves you own the domain. Without it:
- Google Workspace won't let you send emails
- Sending platforms won't accept your domain
- Your infrastructure is unusable

### Google Workspace Verification

Already covered in detail above, but critical points:

**TXT Record Method** (Recommended):
- Host: `@`
- Value: Your unique verification code from Google
- Leave permanently in DNS

**CNAME Method** (Alternative):
- Host: Unique string provided by Google
- Points to: google.com
- More complex, no real benefit

**HTML File Upload** (Not Applicable):
- Requires website hosting
- We're only setting up email
- Don't use this method

### Sending Platform Verification

Most cold email sending platforms (SmartLead, Instantly, Lemlist) require domain verification:

**Common Verification Methods**:

1. **TXT Record Verification**:
   - Platform provides unique code
   - Add as TXT record
   - Host: Usually `@` or platform-specific
   - Value: Their verification code

2. **CNAME Verification**:
   - For tracking domains
   - Add CNAME record pointing to platform
   - Enables link tracking and open tracking

3. **Sender Authentication**:
   - Some platforms want to authenticate on your behalf
   - May ask to modify SPF record
   - ⚠️ **WARNING**: Be careful adding multiple SPF directives

**Multiple Platform SPF Handling**:

If using multiple platforms, your SPF record must include all:

```
v=spf1 include:_spf.google.com include:sparkpostmail.com include:_spf.instantly.ai ~all
```

**Important**:
- Only ONE SPF record per domain
- Can have multiple `include:` statements
- Max 10 DNS lookups (rarely an issue)
- Must end with `~all` or `-all`

### Verification Troubleshooting

**Issue**: "Domain already verified by another account"
**Solution**:
- Domain was previously verified by different Google Workspace
- Contact Google Workspace support
- Prove ownership through domain registrar
- They'll remove old verification

**Issue**: "TXT record not found"
**Solution**:
- Check DNS propagation (dnschecker.org)
- Wait 24-48 hours
- Verify no typos in record
- Try CNAME method instead

**Issue**: "MX records incorrect"
**Solution**:
- Delete ALL existing MX records first
- Add Google's 5 MX records
- Verify priorities are exactly as specified
- Wait 4-6 hours for propagation

---

## Troubleshooting Common Issues

### Email Sending Issues

**Problem**: "Emails not sending from Gmail"
**Diagnostic Steps**:
1. Check if MX records are configured
2. Verify SPF, DKIM, DMARC records exist
3. Confirm domain verification is complete
4. Check Google Workspace admin console for errors
5. Look for "Message blocked" in sent folder

**Problem**: "Emails going to spam"
**Solutions**:
- Warm up accounts before cold emailing (see warmup guide)
- Check authentication with mail-tester.com
- Verify SPF, DKIM, DMARC are passing
- Reduce sending volume
- Improve email content (avoid spam triggers)

**Problem**: "Emails bouncing"
**Diagnostic**:
1. Check bounce message in sender inbox
2. Common causes:
   - MX records incorrect → Fix MX records
   - Recipient doesn't exist → Clean your list
   - Domain blacklisted → Check MXToolbox blacklists
   - SPF failure → Fix SPF record

### DNS Configuration Issues

**Problem**: "DNS changes not taking effect"
**Solutions**:
- Wait 24-48 hours (propagation time)
- Check dnschecker.org for global propagation
- Clear local DNS cache:
  - Mac: `sudo dscacheutil -flushcache`
  - Windows: `ipconfig /flushdns`
  - Linux: `sudo systemd-resolve --flush-caches`
- Verify changes saved in Namecheap (green checkmark)

**Problem**: "Multiple SPF records error"
**Solution**:
- Delete all SPF records
- Create ONE SPF record with all necessary includes
- Format: `v=spf1 include:domain1.com include:domain2.com ~all`
- Save and wait for propagation

**Problem**: "DKIM not authenticating"
**Solutions**:
- Wait full 48 hours after setup
- Check for spaces/line breaks in DKIM value
- Verify host is exactly `google._domainkey`
- Regenerate DKIM key in Google Workspace
- Contact Google Workspace support if still failing

### Account Access Issues

**Problem**: "Can't access Gmail account"
**Solutions**:
- Verify you're using correct email and password
- Check if 2FA is enabled (need phone)
- Try password reset
- Ensure domain verification is complete
- Check Google Workspace admin for account status

**Problem**: "Google Workspace suspended account"
**Diagnostic**:
1. Check admin console for suspension reason
2. Common causes:
   - Payment failed → Update payment method
   - TOS violation → Contact support
   - Suspicious activity → Verify identity
   - Domain verification lost → Re-verify domain

### Integration Issues

**Problem**: "Can't connect to sending platform"
**Solutions**:
- Enable "Less secure app access" (if using SMTP)
- Use App Passwords instead (Google Security settings)
- Check platform supports Google Workspace
- Verify OAuth permissions granted
- Try re-authenticating connection

**Problem**: "Forwarding not working"
**Solutions**:
- Verify forwarding address confirmed
- Check spam folder of receiving address
- Ensure "Keep/Delete Gmail's copy" selected
- Test with manual email send
- Check Google Admin hasn't disabled forwarding

---

## Quality Assurance Checklist

Before launching any cold email campaign, complete this checklist:

### Domain Setup Checklist

- [ ] Secondary domain purchased
- [ ] Domain privacy configured (if desired)
- [ ] Domain not on any blacklists (check MXToolbox)
- [ ] Domain name makes sense for brand
- [ ] Domain registered for at least 1 year

### Google Workspace Checklist

- [ ] Google Workspace account created
- [ ] Payment method added and verified
- [ ] Domain verified with TXT record
- [ ] Verification record still in DNS

### DNS Records Checklist

- [ ] All 5 MX records added with correct priorities
- [ ] SPF record added and passing tests
- [ ] DKIM record generated and added
- [ ] DKIM status shows "Authenticating email"
- [ ] DMARC record added with p=none policy
- [ ] All records showing propagated on dnschecker.org

### Email Accounts Checklist

- [ ] 3-5 email accounts created
- [ ] Real-sounding names used
- [ ] Strong passwords set and saved
- [ ] All accounts accessible via Gmail
- [ ] Forwarding configured to main inbox
- [ ] Forwarding tested and working

### Testing Checklist

- [ ] Send test email from each account
- [ ] Receive test email to each account
- [ ] Verify forwarding delivers to main inbox
- [ ] Check mail-tester.com score (aim for 8+/10)
- [ ] Verify SPF passing on mail-tester
- [ ] Verify DKIM passing on mail-tester
- [ ] Verify DMARC passing on mail-tester
- [ ] Test reply to forwarded email works

### Platform Integration Checklist

- [ ] Sending platform account created
- [ ] Domain verified in platform
- [ ] Email accounts connected to platform
- [ ] SMTP or OAuth authentication working
- [ ] Test email sent through platform
- [ ] Tracking domain configured (if using)
- [ ] Unsubscribe links working

---

## Advanced Configurations

### Dedicated IP vs Shared IP

**Shared IP** (Default):
- Your emails send from Google's shared IP pool
- Good reputation already established
- No extra cost
- Perfect for most cold email campaigns

**Dedicated IP**:
- Your own unique sending IP address
- Must build reputation from scratch
- Costs extra ($30-50/month)
- Only needed for very high volume (10,000+ emails/day)

**Recommendation**: Use shared IPs. Dedicated IPs are overkill for cold email and require extensive warmup.

### Domain Age Considerations

**New Domain Challenges**:
- Lower trust score
- Easier to flag as spam
- Requires longer warmup period

**Solution**:
- Buy domains 30+ days before launching campaigns
- Set up DNS immediately
- Start warmup process right away
- Consider buying aged domains (domains that already exist)

**Aged Domain Benefits**:
- Existing trust score
- Historical email reputation
- Skip some warmup time
- Higher initial deliverability

**Where to Buy Aged Domains**:
- Odys.global
- ExpiredDomains.net
- GoDaddy Auctions

**Vetting Aged Domains**:
- Check Wayback Machine (web.archive.org) for history
- Verify no spam history on MXToolbox
- Ensure not on any blacklists
- Check for existing backlinks (Ahrefs, SEMrush)

### Multiple Domain Strategy

**The Setup**:
- Primary business: yourbusiness.com
- Sending domain 1: yourbiz.com (campaigns A, B, C)
- Sending domain 2: yourbusiness.io (campaigns D, E, F)
- Sending domain 3: yourbusiness.co (campaigns G, H, I)

**Benefits**:
- If one domain gets blacklisted, others unaffected
- Higher total sending volume
- Can test different approaches simultaneously
- Protects primary business domain

**Management Considerations**:
- 3x the setup work
- 3x the monthly costs
- More complex tracking
- Need system to manage multiple inboxes

**When to Use Multiple Domains**:
- Sending 1,000+ emails per day
- Running campaigns for multiple clients
- Testing different industries/offers
- Have experienced team to manage

### Backup MX Records

**What are Backup MX Records?**
- Secondary email servers that receive email if primary is down
- Google Workspace already has 4 backup MX records (the ALT servers)
- Don't need to add additional backups

**Do You Need More Backups?**
- ❌ No - Google's infrastructure is 99.9% uptime
- ❌ No - Cold email doesn't require extra redundancy
- ✅ Yes - Only if you're using email for critical business operations

---

## Infrastructure Costs Breakdown

### Monthly Costs (For 3 Domains, 5 Accounts Each)

**Domains**:
- 3 domains × $12/year = $36/year = $3/month

**Google Workspace**:
- 15 accounts × $6/month = $90/month

**Optional Add-ons**:
- Domain privacy: 3 domains × $0.50/month = $1.50/month
- Sending platform: $30-100/month (separate guide)

**Total Monthly Cost**: ~$95-195/month

**Cost Optimization Tips**:
- Start with 1 domain, 3 accounts ($18/month)
- Scale up as you prove ROI
- Use annual domain registration for slight discount
- Share accounts across multiple clients if agency

### ROI Calculation

If you book just 2 clients per month at $1,000 each:
- Revenue: $2,000/month
- Infrastructure cost: $95/month
- ROI: 2,000% (20x return)

Cold email infrastructure pays for itself with 1-2 successful campaigns.

---

## Next Steps

After completing infrastructure setup:

1. **Start Warmup Process** → See "warm_up_email_domains.md"
2. **Set Up Sending Platform** → See "setup_smartlead.md"
3. **Build Lead Lists** → See "build_lead_list.md"
4. **Write Cold Emails** → See "personalize_cold_emails_with_ai.md"
5. **Launch Campaigns** → See sending platform guide

---

## Maintenance Schedule

### Daily Maintenance
- [ ] Check forwarded replies in main inbox
- [ ] Respond to interested prospects
- [ ] Monitor bounce rates in sending platform

### Weekly Maintenance
- [ ] Check Google Workspace billing
- [ ] Review account health in sending platform
- [ ] Clear spam from sending accounts
- [ ] Update any bounced email addresses

### Monthly Maintenance
- [ ] Verify all DNS records still correct
- [ ] Check domain blacklist status (MXToolbox)
- [ ] Review and renew domain registrations as needed
- [ ] Audit email authentication (mail-tester.com)
- [ ] Optimize underperforming campaigns

### Quarterly Maintenance
- [ ] Full infrastructure audit
- [ ] Consider adding/removing domains based on performance
- [ ] Update passwords for security
- [ ] Review and optimize costs
- [ ] Test disaster recovery (can you access everything?)

---

## Emergency Procedures

### Domain Blacklisted

**Immediate Actions**:
1. Stop all sending from affected domain
2. Check blacklist status: MXToolbox → Blacklist Check
3. Identify which blacklist(s)
4. Follow delisting process for each blacklist:
   - Spamhaus: spamhaus.org/dbl
   - Barracuda: barracudacentral.org/rbl/removal-request
   - Spamcop: spamcop.net/fom-serve/cache/298.html
5. Fix underlying issue (reduce volume, improve targeting)
6. Request delisting
7. Wait 2-7 days for review
8. Once delisted, slowly restart campaigns

**Prevention**:
- Never send more than 50 emails/account/day when starting
- Warm up accounts properly (14 days minimum)
- Clean your lead lists
- Monitor bounce rates
- Stop immediately if bounce rate >5%

### Google Workspace Account Suspended

**Immediate Actions**:
1. Log into Google Workspace Admin Console
2. Check notification for suspension reason
3. Common fixes:
   - **Payment issue**: Update payment method
   - **TOS violation**: Appeal via support ticket
   - **Suspicious activity**: Complete verification
4. Contact Google Workspace support (phone faster than email)
5. Provide verification documents if requested
6. Wait for reinstatement (1-48 hours)

**Prevention**:
- Keep payment method current
- Don't send spam content
- Follow Google's email sending policies
- Maintain good sender reputation

### Lost Access to Domain Registrar

**Recovery Steps**:
1. Find domain registrar: whois.com lookup
2. Use "Forgot Password" on registrar site
3. Check email for recovery messages
4. Contact registrar support if still locked out
5. Provide verification:
   - Domain name
   - Registrant email
   - Last 4 of payment method
   - Purchase date
6. May require ID verification

**Prevention**:
- Save registrar login details in password manager
- Set up 2FA on registrar account
- Keep recovery email current
- Document which domains are at which registrar

### DNS Changes Broke Email

**Diagnostic Process**:
1. Check what changed: Compare current DNS to backup
2. Common issues:
   - MX records deleted/modified
   - SPF record corrupted
   - DKIM record removed
3. Restore correct records from this guide
4. Wait 1-4 hours for propagation
5. Test with mail-tester.com
6. If still broken, contact platform support

**Prevention**:
- Screenshot DNS settings before making changes
- Keep documented backup of all DNS records
- Make one change at a time
- Test after each change
- Use Namecheap's DNS backup feature (if available)

---

## Frequently Asked Questions

**Q: Can I use my main business domain for cold email?**
A: NO! Never use your primary domain (yourbusiness.com) for cold outreach. You'll damage its reputation and risk blacklisting your main business email.

**Q: How many domains do I need?**
A: Start with 1 secondary domain. Scale to 2-3 domains if sending 500+ emails per day. More than 3 domains is overkill unless running agency with multiple clients.

**Q: Can I use free Gmail accounts instead of Google Workspace?**
A: No. Free Gmail (@gmail.com) addresses:
- Look unprofessional
- Can't use custom domain
- Have much lower sending limits
- Get flagged as spam more easily
You MUST use Google Workspace or Microsoft 365 with custom domain.

**Q: Do I need domain privacy protection?**
A: Optional but recommended:
- Protects personal information in WHOIS
- Adds layer of professionalism
- Only costs $5-10/year
- Can add/remove anytime

**Q: How long does complete setup take?**
A: Timeline:
- Domain purchase: 5 minutes
- Google Workspace setup: 30 minutes
- DNS configuration: 30 minutes
- Verification: 24-48 hours
- Total: 2-3 days start to finish (mostly waiting for DNS)

**Q: Can I use Outlook/Microsoft 365 instead of Gmail?**
A: Yes! Process is very similar:
- Same domain setup
- Same DNS records (with Microsoft's MX records)
- Slightly different admin interface
- Gmail generally has better deliverability for cold email

**Q: What if my domain is already used for a website?**
A: No problem! You can:
- Keep website on yourbiz.com
- Use email accounts from same domain
- DNS records for website (A/CNAME) and email (MX/TXT) work together
- They don't interfere with each other

**Q: How do I know if my setup is working correctly?**
A: Run these tests:
1. Send test email from each account - should deliver
2. Reply to test email - should forward to main inbox
3. Check mail-tester.com - should score 8+/10
4. Verify MXToolbox shows all correct records
5. All accounts accessible via Gmail web interface

**Q: What's the most common setup mistake?**
A: Forgetting to set up email forwarding! You'll be sending from john@yourbiz.com but replies will go there, and you won't see them unless forwarding is configured.

**Q: Can I share accounts across multiple clients?**
A: Not recommended. Best practice:
- One infrastructure per business
- Separate domains for different industries
- Don't mix client campaigns on same accounts
Exception: If you're an agency, you might use your own infrastructure for client campaigns, but keep their replies separate.

**Q: How often should I buy new domains?**
A: Replacement schedule:
- If domain gets blacklisted → Immediately
- Proactive rotation → Every 6-12 months
- If deliverability drops → As needed
- Growing volume → Add domain when hitting limits

**Q: Is there a cheaper alternative to Google Workspace?**
A: Not really:
- Zoho Mail ($1/user/month) - Lower quality deliverability
- ProtonMail - Not suitable for cold email
- Self-hosted email - Too complex and low deliverability
Google Workspace $6/month is industry standard for good reason.

---

## Tools & Resources

### Essential Tools

**DNS Management**:
- Namecheap DNS (included with domain)
- Cloudflare DNS (free, advanced)

**DNS Testing**:
- dnschecker.org - Check propagation
- mxtoolbox.com - Comprehensive DNS/email testing
- whatsmydns.net - Alternative propagation checker
- mail-tester.com - Complete email deliverability test

**Email Verification**:
- Google Toolbox Messageheader - Analyze email headers
- mail-tester.com - Score your email setup (aim for 8+/10)
- GlockApps - Inbox placement testing ($$$)

**Blacklist Checking**:
- mxtoolbox.com/blacklists.aspx
- multirbl.valli.org
- whatismyipaddress.com/blacklist-check

**Documentation**:
- Google Workspace Admin Help
- Namecheap Knowledge Base
- DKIM.org - DKIM technical documentation

### Learning Resources

**Email Deliverability**:
- Google's Email Sender Guidelines
- M3AAWG (Messaging Anti-Abuse Working Group)
- SendGrid's Email Deliverability Guide

**Cold Email Communities**:
- Cold Email FTW (Facebook Group)
- r/EmailMarketing (Reddit)
- Instantly.ai Community
- SmartLead Community

### Support Contacts

**Google Workspace Support**:
- Phone: Available to paid accounts
- Chat: Through admin console
- Email: support@googleworkspace.com
- Hours: 24/7 for critical issues

**Namecheap Support**:
- Live Chat: 24/7
- Tickets: support.namecheap.com
- Phone: Toll-free for account holders
- Knowledge Base: Extensive self-help

**Platform Support**:
- SmartLead: Live chat + email
- Instantly: Live chat + email
- Lemlist: Email support
- Response time: Usually 2-24 hours

---

## Conclusion

You now have a complete, enterprise-level cold email infrastructure. This setup provides:

✅ **Professional Appearance**: Custom domain emails (john@yourbiz.com)
✅ **High Deliverability**: Proper authentication (SPF, DKIM, DMARC)
✅ **Scalability**: Multiple accounts for distributed sending
✅ **Protection**: Main business domain stays clean
✅ **Efficiency**: Centralized inbox management via forwarding
✅ **Compliance**: Proper unsubscribe and authentication

**Infrastructure Investment**:
- Time: 2-4 hours setup + 24-48 hours DNS propagation
- Money: $95-195/month ongoing
- ROI: 2,000%+ with successful campaigns

**Next Step**: Begin 14-day warmup process (see warm_up_email_domains.md)

Remember: Your infrastructure is the foundation of all cold email success. Take time to set it up correctly once, and it will serve you for months or years.

---

**Document Version**: 1.0
**Last Updated**: 2024
**Related Skills**:
- warm_up_email_domains.md
- setup_smartlead.md
- build_lead_list.md
