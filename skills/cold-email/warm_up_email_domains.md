# Warm Up Email Domains

## Skill Overview
This skill guides you through the complete 14-day email warmup process in Smartlead to establish domain reputation and ensure maximum deliverability before launching cold email campaigns.

## Table of Contents
1. [Understanding Email Warmup](#understanding-email-warmup)
2. [Custom Tracking Domain Setup](#custom-tracking-domain-setup)
3. [Warmup Configuration in Smartlead](#warmup-configuration-in-smartlead)
4. [14-Day Warmup Protocol](#14-day-warmup-protocol)
5. [Monitoring Warmup Progress](#monitoring-warmup-progress)
6. [Post-Warmup Launch](#post-warmup-launch)

## Understanding Email Warmup

Email warmup is the process of gradually building sender reputation with email service providers (ESPs) before sending cold emails at scale.

### Why Warmup is Critical

**Without warmup:**
- Emails land in spam
- Sender reputation damaged
- Campaigns fail from day one
- Risk of domain blacklisting

**With proper warmup:**
- High inbox placement rates
- Established sender reputation
- Better deliverability throughout campaign
- Protected domain reputation

### Warmup Timeline

**Minimum warmup period:** 14 days

This gives you time to:
- Complete targeting and messaging strategy
- Build landing pages and VSLs
- Create lead lists
- Write and test email scripts

## Custom Tracking Domain Setup

Before enabling warmup, set up a custom tracking domain for each email account. This improves deliverability by using your own domain for tracking instead of Smartlead's shared domains.

### Step 1: Enable Custom Tracking Domain in Smartlead

1. Go to **Email Accounts** section in Smartlead
2. Click into each individual email account
3. Navigate to **General** settings
4. Toggle **Custom Tracking Domain** to ON

### Step 2: Add DNS Record in Your Domain Registrar

Navigate to your domain registrar (Google Domains, Namecheap, GoDaddy, etc.) and add the following CNAME record:

**DNS Record Configuration:**
- **Host:** `email-tracking` (spelled exactly this way)
- **Type:** CNAME
- **TTL:** Default (or 3600)
- **Value:** `open.sleadtrack.com`

**Example for Google Domains:**
1. Go to your domain (e.g., clientascend.com)
2. Click **Manage**
3. Go to **DNS** section
4. Select **Manage custom records**
5. Create new record:
   - Host: `email-tracking`
   - Type: CNAME
   - Data: `open.sleadtrack.com`
6. Click **Save**

### Step 3: Verify Custom Tracking Domain in Smartlead

Back in Smartlead:

1. In the Custom Tracking Domain field, enter:
   ```
   http://email-tracking.yourdomain.com
   ```

   Example: `http://email-tracking.clientascend.com`

2. Click **Verify CNAME**
3. Should show "Verified successfully"
4. Click **Save** in bottom right

### Step 4: Verify in General Settings

1. Exit the email account settings
2. Return to **General Settings**
3. Confirm the custom tracking domain shows as:
   ```
   http://email-tracking.yourdomain.com
   ```

**Repeat this process for all 10 email accounts.**

## Warmup Configuration in Smartlead

### Accessing Warmup Settings

1. Go to **Email Accounts** in Smartlead
2. Click into individual email account
3. Scroll to **Warmup** section
4. Click **Enable Warmup** toggle (bottom right)

### Exact Warmup Settings

Configure these exact settings for optimal warmup:

| Setting | Value | Purpose |
|---------|-------|---------|
| **Warmup Enabled** | YES | Activates warmup process |
| **Total warmup emails per day** | 40 | Target daily volume |
| **Ramp up** | 4 | Emails added per day |
| **Randomize number** | 25 to 40 | Daily volume range |
| **Reply rate percentage** | 45% | Simulated engagement |
| **Auto adjust warmup setting ratio** | ENABLED | Dynamic optimization |

### Detailed Setting Explanations

**Total warmup emails per day: 40**
- This is your target by end of warmup
- You won't send 40 emails immediately
- Ramp up gradually to this number

**Ramp up: 4**
- Adds 4 emails per day to your volume
- Day 1: 4 emails
- Day 2: 8 emails
- Day 3: 12 emails
- Day 10: 40 emails (stays at 40 through day 14)

**Randomize number: 25 to 40**
- Adds natural variation to daily volume
- Some days: 25 warmup emails
- Other days: 40 warmup emails
- Prevents robotic patterns

**Reply rate percentage: 45%**
- 45% of warmup emails receive replies
- High engagement signals positive reputation
- Simulates real conversations

**Auto adjust warmup setting ratio: ENABLED**
- Smartlead dynamically optimizes settings
- Adjusts based on your account's performance
- Maximizes reputation building

### Applying Settings to All Accounts

After configuring one account:

1. Click **Update** to save settings
2. Return to **Email Accounts** list
3. Verify "Warmup Enabled" shows "YES" for that account
4. Repeat for remaining 9 accounts
5. All 10 accounts should show "Warmup Enabled: YES"

## 14-Day Warmup Protocol

### Warmup Schedule Breakdown

| Day | Daily Volume | Total Sent | Status |
|-----|-------------|------------|---------|
| 1 | 4 | 4 | Ramp start |
| 2 | 8 | 12 | Building |
| 3 | 12 | 24 | Building |
| 4 | 16 | 40 | Building |
| 5 | 20 | 60 | Building |
| 6 | 24 | 84 | Building |
| 7 | 28 | 112 | Building |
| 8 | 32 | 144 | Building |
| 9 | 36 | 180 | Building |
| 10 | 40 | 220 | Peak reached |
| 11 | 25-40 | 245-260 | Randomizing |
| 12 | 25-40 | 270-300 | Randomizing |
| 13 | 25-40 | 295-340 | Randomizing |
| 14 | 25-40 | 320-380 | Ready to launch |

### What Happens During Warmup

**Smartlead automatically:**
- Sends emails to other warmup inboxes
- Receives emails from warmup network
- Replies to incoming warmup emails (45% rate)
- Moves emails between folders
- Simulates natural email behavior
- Marks emails as read/unread
- Stars/favorites emails occasionally

**This creates:**
- Positive engagement signals
- Natural email patterns
- Established sender history
- Trust with ISPs (Gmail, Outlook, etc.)

### During the 14-Day Period

**What to do:**
- Complete targeting section of training
- Complete messaging section of training
- Build your landing page
- Create your VSL
- Build lead lists
- Write email scripts
- Test email copy

**What NOT to do:**
- Do not send cold emails yet
- Do not disable warmup
- Do not change warmup settings
- Do not delete email accounts
- Do not modify DNS records

### Day 14: Ready to Launch

On day 14, your accounts are ready for cold email campaigns.

**Checklist before launching:**
- [ ] All 10 accounts show "Warmup Enabled: YES"
- [ ] Custom tracking domains verified for all accounts
- [ ] 14 full days have passed since enabling warmup
- [ ] Lead list is built and validated
- [ ] Email script is written and tested
- [ ] Landing page is live
- [ ] VSL is complete
- [ ] Campaign settings configured in Smartlead

## Monitoring Warmup Progress

### Daily Checks (Optional)

**Week 1 (Days 1-7):**
- Check 2-3 accounts daily
- Verify warmup emails are sending
- Confirm volume is ramping up

**Week 2 (Days 8-14):**
- Check all accounts every 2-3 days
- Verify hitting 25-40 daily volume
- Confirm no error messages

### Key Metrics to Monitor

**Warmup emails sent:**
- Should increase by 4 per day
- Should plateau at 25-40 range by day 10

**Warmup replies received:**
- Should be approximately 45% of sent
- Example: 40 sent = 18 replies

**Bounce rate:**
- Should be 0% during warmup
- Warmup emails go to verified inboxes
- Any bounces indicate configuration issue

### Troubleshooting Common Issues

**Issue: Warmup not sending emails**
- Verify warmup toggle is ENABLED
- Check email account connection status
- Confirm DNS records are correct
- Re-save warmup settings

**Issue: Low reply rate during warmup**
- Don't worry - this is automated
- Smartlead manages reply simulation
- 45% is target, not requirement

**Issue: Custom tracking domain not verifying**
- Wait 10-15 minutes for DNS propagation
- Can take up to 24 hours in some cases
- Verify CNAME record is exactly: `open.sleadtrack.com`
- Check for typos in record configuration

**Issue: Email account disconnected**
- Reconnect account in Smartlead
- Re-enable warmup with same settings
- May need to extend warmup period by disconnection days

## Post-Warmup Launch

### Maintaining Warmup During Campaigns

**CRITICAL:** Keep warmup enabled even after launching cold campaigns.

**Why:**
- Maintains sender reputation
- Continues positive engagement signals
- Protects against deliverability drops
- Balances cold sending with warm activity

**How it works:**
- Smartlead sends warmup emails + campaign emails
- Respects daily sending limits
- Example: 50 total daily limit = 40 campaign + 10 warmup

### Transitioning to Cold Email

**Day 14 launch strategy:**

1. **Keep warmup enabled** at current settings
2. Start cold campaigns at conservative volume
3. Monitor deliverability closely
4. Gradually increase cold volume over 7 days

**Volume ramp for cold emails:**
- Days 1-3: 10 cold emails per account per day
- Days 4-7: 15 cold emails per account per day
- Days 8-14: 20 cold emails per account per day
- Day 15+: Full volume (up to 40-50 per account)

### Long-Term Warmup Maintenance

**Ongoing warmup settings:**
- Reduce to 10-15 warmup emails per day
- Continue running indefinitely
- Maintains reputation baseline
- Provides safety buffer

**When to increase warmup:**
- After campaign pauses (vacation, holidays)
- If deliverability drops
- When adding new email accounts
- After high bounce rate incidents

## Warmup Best Practices

### Do's

- Enable warmup for all accounts simultaneously
- Wait full 14 days before launching campaigns
- Keep warmup running during active campaigns
- Monitor first week closely
- Use custom tracking domains
- Follow exact settings provided

### Don'ts

- Don't skip warmup period
- Don't send cold emails during warmup
- Don't disable warmup after launching
- Don't modify settings mid-warmup
- Don't add accounts without warming them up
- Don't rush the process

## Configuration Summary

For quick reference when setting up each account:

### Custom Tracking Domain
```
DNS Record:
- Host: email-tracking
- Type: CNAME
- Value: open.sleadtrack.com

Smartlead Entry:
- Format: http://email-tracking.yourdomain.com
```

### Warmup Settings
```
- Warmup Enabled: YES
- Total per day: 40
- Ramp up: 4
- Randomize: 25 to 40
- Reply rate: 45%
- Auto adjust: ENABLED
```

### Timeline
```
- Setup: Day 0 (today)
- Warmup: Days 1-14
- Launch: Day 14
- Full volume: Day 21
```

## Related Skills
- [Setup Cold Email Infrastructure](./setup_cold_email_infrastructure.md)
- [Setup Smartlead](./setup_smartlead.md)
- [Analyze Cold Email Performance](./analyze_cold_email_performance.md)

## Completion Checklist

Before proceeding to campaign launch, verify:

- [ ] All 10 email accounts added to Smartlead
- [ ] Custom tracking domain configured for each account
- [ ] All tracking domains verified successfully
- [ ] Warmup enabled for all 10 accounts
- [ ] Warmup settings match specifications exactly
- [ ] All accounts show "Warmup Enabled: YES"
- [ ] 14 full days have passed since enabling warmup
- [ ] No email accounts disconnected or erroring
- [ ] Ready to launch campaign on day 14
