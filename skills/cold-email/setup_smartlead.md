# Setup Smartlead

## Skill Overview
This skill guides you through the complete setup of a cold email campaign inside Smartlead, including lead import, sequence configuration, spintax implementation, and campaign settings optimization.

## Table of Contents
1. [Understanding Smartlead](#understanding-smartlead)
2. [Creating a Campaign](#creating-a-campaign)
3. [Importing Leads](#importing-leads)
4. [Writing Email Sequences](#writing-email-sequences)
5. [Spintax Configuration](#spintax-configuration)
6. [Campaign Setup Settings](#campaign-setup-settings)
7. [Campaign Settings Optimization](#campaign-settings-optimization)
8. [Final Review and Launch](#final-review-and-launch)

## Understanding Smartlead

Smartlead is a cold email automation platform that enables high-volume email sending while maintaining deliverability. The platform manages:

- Email account rotation
- Sending schedule optimization
- Deliverability protection
- AI-powered inbox categorization
- Campaign analytics

## Creating a Campaign

### Step 1: Navigate to Campaign Creation
1. Go to the **Email Campaign** section in Smartlead
2. Press **Create Campaign**
3. You'll be prompted to import leads

### Step 2: Name Your Campaign
Use a clear naming convention that includes:
- Campaign identifier (e.g., "Hormozy followers")
- Date stamp (e.g., "12-15-24")
- Example: "Hormozy followers 12-15-24"

## Importing Leads

### Lead Import Settings

Configure these settings when importing your lead list:

**Import Settings:**
- **Import leads in global block list:** NO (respect the block list)
- **Import leads in unsubscribed list:** NO (respect unsubscribes)
- **Ignore global bounce list:** YES (Smartlead's bounce list is not super accurate)
- **Ignore leads in other campaigns:** Depends on your use case
  - Enable if you want to filter out leads already in other campaigns
  - Disable if you want to re-contact leads across campaigns

### Field Mapping

Map your CSV/Google Sheet columns to Smartlead fields:

**Standard Fields:**
- First Name
- Last Name
- Email
- Company Name
- LinkedIn Profile
- Website

**Custom Fields:**
Use the "Custom Field" button to add any additional variables from your sheet (e.g., follower count, industry, location)

### Upload Process
- Upload takes a few seconds to a few minutes depending on list size
- Smartlead will show a preview of imported data
- Review the data before continuing
- **Do not validate inside Smartlead** - validate externally before import

## Writing Email Sequences

### Adding Your First Email

1. Navigate to the **Sequences** section
2. Add your subject line
3. Insert email body content
4. Use the **Variable** button to insert personalization tokens

**Variable Examples:**
- {{first_name}}
- {{company_name}}
- {{custom_field}}

**Important:** Avoid pressing Enter after inserting variables, as this can cause "undefined" errors. Use Shift+Enter or space instead.

### Adding Follow-Up Steps

1. Press **Add Step** at the bottom
2. Select **Add Email**
3. Plug in your next email content
4. Continue adding steps as needed

### A/B Split Testing

Use the **Add Variant** button to create split tests:
- Test different subject lines
- Test different email structures
- Test different CTAs
- Smartlead will automatically distribute variants evenly

**Note:** Use A/B testing for performance testing, not deliverability variations (use Spintax for that).

### Formatting Best Practices

**For maximum deliverability:**
- No links (99% of scenarios)
- No images (99% of scenarios)
- Plain text only
- No HTML formatting
- Keep it conversational and natural

## Spintax Configuration

Spintax adds micro-variations to improve deliverability by making each email unique.

### Spintax Syntax

Format: `{option1|option2|option3}`

**Examples:**
- `{Hi|Hello|Hey}` - Randomizes greeting
- `{book a call|schedule a meeting|set up a time}` - Randomizes CTA
- `{I wanted to|I'd like to|Looking to}` - Randomizes sentence starts

### When to Use Spintax

**Use Spintax for:**
- Greetings (Hi vs Hello)
- CTAs (book a call vs schedule a meeting)
- Transition words
- Sentence structure variations

**Do NOT use Spintax for:**
- Critical information
- Custom variables (use A/B testing instead)
- Testing different value propositions (use A/B testing)

### Spintax Example

```
{Hi|Hello|Hey} {{first_name}},

{I noticed|I saw|I came across} your work at {{company_name}}.

{I wanted to reach out|Reaching out|Getting in touch} because [value proposition].

{Would you be open to|Are you interested in|Could we} {booking a quick call|scheduling a brief chat|setting up a 15-min call}?

{Best|Thanks|Cheers},
[Signature]
```

### Verifying Spintax

In the Final Review section, check multiple email previews to ensure:
- Spintax is rendering correctly
- All variations read naturally
- No syntax errors (missing brackets, etc.)

## Campaign Setup Settings

### Choose Sender Accounts

1. Navigate to **Setup** > **Choose sender accounts**
2. Select all email accounts you want to use for this campaign
3. Smartlead automatically respects daily sending limits per account
4. Add all relevant accounts to the campaign (no need to split campaigns)

### Schedule Campaign

**Time Zone:**
- Select the recipient's time zone (not your own)

**Days to Send:**
- Monday - Friday (standard)
- Include weekends if relevant to your audience

**Time of Day:**
- **Recommended:** 7:00 AM - 2:00 PM (recipient's local time)
- Rationale: Email arrives during workday, not at end of day

**Email Sending Interval:**
- Configure "An email will be sent every X minutes"
- Ensure this matches your daily sending limit
- Example: 15 emails/day per account = set interval to send 15+ emails/day
- Default settings usually work fine as long as above your limit

**Max New Leads Reached Per Day:**
- Set this to a high number (e.g., 1000)
- Smartlead respects individual account limits regardless
- If you have 10 accounts sending 15 emails/day = 150 emails/day max
- This setting won't override account-level limits

**Email Account Start Date:**
- Leave default (start immediately)
- Use only if scheduling campaign for future launch

## Campaign Settings Optimization

### Optimize Email Deliverability

**Enable: YES**
This critical setting tells Smartlead to remove all additional tracking baggage from emails to maximize inbox placement.

### Force Plain Text Content Type

**Enable: NO (in most cases)**
- Can improve deliverability by forcing plain text
- May mess up formatting in some cases
- Test on your campaigns - your mileage may vary
- Not necessary if "Optimize email deliverability" is enabled

### Track Email Opens and Link Clicks

**Enable: NO**
- These features reduce deliverability
- Automatically disabled when "Optimize email deliverability" is enabled
- Focus on reply rate, not open rate

### Prioritize Sending Pattern

**Recommended:** 50% new leads, 50% follow-ups

**Alternative:** 100% new leads if you want:
- Faster initial results
- To contact new prospects ASAP
- New leads typically respond better than follow-ups

### Company Level Auto Pause

**Enable: NO**
- This pauses all leads from a company if one person replies
- Often counterproductive - different people at same company may have different responses
- One person says no, another might say yes

### Enhanced Email Sending

**Enable: NO (in most cases)**
- Routes Outlook emails to Outlook accounts, Gmail to Gmail
- Can help in some cases, can hurt in others
- Sending across providers often performs better

### Isolated Sending Provider Matching

**Enable: YES (as of December 2024)**
- Filters out specific email providers (e.g., Outlook)
- Useful if certain providers have high rejection rates
- Example: Outlook accounts currently reject emails at higher rates
- Enable to only send to Gmail/other providers
- Disable to send to all providers

### Intelligent AI Categorization

**Enable: YES**
This feature tags incoming replies with sentiment categories for easier inbox management.

**Recommended Tags:**
- Do Not Contact
- Out of Office
- Interested
- Not Interested
- Meeting Request

**Ignore Auto-Categorize Out of Office from Reply Rate:**
- **Disable** - Include out of office in reply rate calculations

**Automatically Restart AI-Categorized Out of Office:**
- **Enable: YES**
- Pauses leads who are out of office
- Automatically resumes them when they return
- Example: "Out until January 15th" pauses lead, resumes on Jan 15th

### High Bounce Rate Auto Protection

**Enable: YES**
- Pauses campaign if bounce rate exceeds 4%
- Protects email account reputation
- Critical safety feature

## Final Review and Launch

### Review Email Previews

1. Navigate to **Final Review** section
2. Check multiple email previews to verify:
   - Spintax variations are working
   - All variables are populating correctly
   - Formatting looks correct
   - No "undefined" errors

### Send Test Email

**CRITICAL:** Always send a test email before launching

**Check for:**
- Subject line rendering
- Spintax variations
- Variable population ({{first_name}}, etc.)
- Email signature (doesn't show in preview section)
- Overall formatting and readability
- Spacing and line breaks

### Launch Campaign

1. Verify all email accounts are selected
2. Press **Save**
3. Press **Launch Campaign**
4. Monitor initial results for deliverability issues

### Post-Launch Monitoring

**First 24-48 Hours:**
- Check bounce rate (should be under 4%)
- Monitor reply rate
- Review any error messages
- Check inbox for responses

**If issues arise:**
- High bounce rate: Check lead validation
- Low deliverability: Review email content for spam triggers
- Formatting issues: Send more test emails

## Key Settings Summary

| Setting | Recommended Value | Rationale |
|---------|------------------|-----------|
| Optimize Email Deliverability | YES | Removes tracking, maximizes inbox placement |
| Force Plain Text | NO | May break formatting |
| Track Opens/Clicks | NO | Reduces deliverability |
| Prioritize Sending | 50/50 or 100% new | Faster results with new leads |
| Company Auto Pause | NO | Misses opportunities |
| Enhanced Sending | NO | Cross-provider often better |
| AI Categorization | YES | Easier inbox management |
| Bounce Protection | YES | Protects reputation |
| Sending Hours | 7 AM - 2 PM | During workday |
| Days | Mon-Fri | Standard business days |

## Troubleshooting

### Common Issues

**Variables showing as "undefined":**
- Don't press Enter immediately after inserting variable
- Use Shift+Enter or space instead

**Email signature not showing in preview:**
- Signature only appears in actual sent emails
- Always send test email to verify

**Campaign won't launch:**
- Verify email accounts are selected
- Check that sequences are saved
- Ensure leads are imported

**High bounce rate:**
- Validate leads externally before importing
- Check email format accuracy
- Review bounce rate protection setting (4% threshold)

## Resources

- Have your email script ready before starting
- Prepare lead list with proper formatting
- Review the "Write Cold Email Script" skill first
- For questions: Reach out in Slack or outbound channel

## Related Skills
- [Write Cold Email Script](./write_cold_email_script.md)
- [Setup Cold Email Infrastructure](./setup_cold_email_infrastructure.md)
- [Warm Up Email Domains](./warm_up_email_domains.md)
