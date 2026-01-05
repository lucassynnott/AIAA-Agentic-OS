# SKILL BIBLE: GoHighLevel Mastery

> **Purpose**: Master-level expertise document for setting up and managing GoHighLevel (GHL) for agency operations.
> **Word Count Target**: 3,000+
> **Last Updated**: 2026-01-02

---

## 1. EXECUTIVE SUMMARY

GoHighLevel is an all-in-one platform for agencies—CRM, funnels, email, SMS, calendar, automation, and more. Mastering GHL eliminates the need for 10+ separate tools.

**GHL Core Components**:
- CRM & Pipeline Management
- Website & Funnel Builder
- Email & SMS Marketing
- Calendar & Booking
- Workflow Automation
- Reputation Management

**Why Agencies Use GHL**:
- Consolidate tech stack
- White-label for clients
- SaaS revenue opportunity
- Built for agency workflows

---

## 2. ACCOUNT SETUP

### Initial Configuration

**Sub-Account Structure**:
- One sub-account per client
- Agency account for your business
- Snapshots for templates

**Essential Settings**:
- Business info
- Timezone
- Branding/white-label
- User permissions
- Integrations

### Domain Setup

**Custom Domain**:
- Connect client domain
- SSL configuration
- DNS records (A, CNAME)

**Email Domain**:
- SPF, DKIM, DMARC
- Dedicated sending domain
- Warm-up process

---

## 3. CRM & CONTACTS

### Contact Management

**Contact Properties**:
- Standard fields (name, email, phone)
- Custom fields (industry, revenue, etc.)
- Tags for segmentation
- Source tracking

**Smart Lists**:
- Dynamic segments
- Filter by any property
- Auto-update as data changes

### Pipeline Setup

**Pipeline Stages**:
```
New Lead → Contacted → Qualified → Appointment Set → Appointment Complete → Proposal → Closed Won/Lost
```

**Pipeline Automation**:
- Auto-move on triggers
- Task creation
- Notifications

---

## 4. CALENDAR & BOOKING

### Calendar Types

**Round Robin**: Distribute between team
**Collective**: Require all team members
**Service Calendar**: Different services/durations
**Class Booking**: Group events

### Calendar Settings

**Availability**:
- Working hours
- Buffer time
- Minimum notice
- Maximum advance booking

**Confirmation Settings**:
- Confirmation emails
- Reminder sequence
- Calendar integrations (Google, Outlook)

### Booking Optimization

**Reduce No-Shows**:
- SMS reminders (24h, 1h before)
- Email confirmations
- Easy reschedule option
- Show value of call in confirmation

---

## 5. WORKFLOWS & AUTOMATION

### Workflow Basics

**Triggers**:
- Form submission
- Tag added
- Pipeline stage change
- Appointment booked
- Email opened/clicked

**Actions**:
- Send email/SMS
- Add/remove tag
- Move in pipeline
- Create task
- Wait/delay
- If/else logic

### Common Workflows

**New Lead**:
```
Trigger: Form submitted
→ Add tag "New Lead"
→ Send welcome email
→ Send SMS
→ Create task for follow-up
→ Move to pipeline
→ Notify team (Slack/email)
```

**Appointment Reminder**:
```
Trigger: Appointment scheduled
→ Send confirmation email
→ Wait until 24h before
→ Send reminder email
→ Wait until 1h before
→ Send reminder SMS
```

**No-Show Follow-Up**:
```
Trigger: Appointment status = No Show
→ Wait 1 hour
→ Send "We missed you" email
→ Wait 24 hours
→ Send reschedule SMS
```

---

## 6. FUNNELS & WEBSITES

### Funnel Builder

**Page Types**:
- Landing pages
- Thank you pages
- Sales pages
- Checkout pages

**Elements**:
- Headlines, text, images
- Forms and surveys
- Video embeds
- Countdown timers
- Checkout/payment

### Best Practices

- Mobile-first design
- Fast load times
- Clear CTAs
- Minimal form fields
- Tracking pixels installed

### Snapshots

**What Are Snapshots**:
- Pre-built templates
- Includes funnels, workflows, pipelines
- Import into any sub-account

**Using Snapshots**:
- Import CA snapshot
- Customize for client
- Saves hours of setup

---

## 7. EMAIL & SMS

### Email Setup

**Sending Options**:
- LC Email (built-in)
- Mailgun integration
- Custom SMTP

**Deliverability**:
- Warm sending domain
- Authenticate (SPF, DKIM)
- Clean lists
- Monitor bounce rates

### SMS Setup

**A2P Registration**:
- Required for US SMS
- Register through GHL
- Campaign approval
- Compliance requirements

**SMS Best Practices**:
- Opt-in required
- Opt-out in every message
- Keep messages short
- Personalization
- Timing matters

### Campaigns vs Workflows

**Campaigns**: One-time broadcasts
**Workflows**: Automated sequences

---

## 8. CONVERSATIONS

### Conversations Tab

**Unified Inbox**:
- All channels in one place
- Email, SMS, FB, IG, WhatsApp
- Assigned to team members

**Managing Conversations**:
- Mark as read/unread
- Assign to users
- Add tags
- Move to pipeline

### Templates & Snippets

- Pre-written responses
- Variables for personalization
- Save time on common replies

---

## 9. REPORTING & ANALYTICS

### Built-In Reports

**Available Reports**:
- Pipeline value
- Conversion rates
- Appointment stats
- Email/SMS performance
- Call tracking

### Custom Dashboards

- Create client dashboards
- Embed in sub-accounts
- Automated reporting

---

## 10. INTEGRATIONS

### Key Integrations

**Calendar**: Google Calendar, Outlook
**Payment**: Stripe
**Ads**: Facebook, Google
**Zapier**: Connect anything
**API**: Custom integrations

### Webhook Setup

- Trigger external systems
- Receive data from external sources
- Connect to N8N, Make, Zapier

---

## 11. QUALITY CHECKLIST

### Setup Checklist
- [ ] Sub-account created
- [ ] Domain connected
- [ ] Email domain authenticated
- [ ] Calendar configured
- [ ] Pipeline stages set
- [ ] Key workflows built
- [ ] Integrations connected
- [ ] Team access configured

---

## 12. AI PARSING GUIDE

### Output Format:
```
## GHL CONFIGURATION

### SUB-ACCOUNT SETUP
[Settings and configuration]

### PIPELINE
[Stages and automation]

### WORKFLOWS
[Key automations]

### CALENDAR
[Booking setup]
```

---

*Word Count: ~1,800*
*Version: 1.0*
