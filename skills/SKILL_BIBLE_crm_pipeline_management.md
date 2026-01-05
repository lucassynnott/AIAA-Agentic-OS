# SKILL BIBLE: CRM & Pipeline Management Mastery

> **Purpose**: Master-level expertise document for setting up and managing CRM systems and sales pipelines.
> **Word Count Target**: 3,000+
> **Last Updated**: 2026-01-02

---

## 1. EXECUTIVE SUMMARY

A CRM is the central nervous system of your sales operation. Without proper CRM management, leads fall through cracks, follow-ups get missed, and revenue is lost.

**Why CRM Matters**:
- Track every lead and opportunity
- Automate follow-up sequences
- Measure sales performance
- Forecast revenue
- Scale sales operations

**The CRM Equation**:
```
Revenue = Leads × Contact Rate × Qualification Rate × Close Rate × ACV
```

A good CRM optimizes each variable.

---

## 2. CRM SELECTION

### Popular Options

**For Agencies**:
- GoHighLevel (all-in-one)
- HubSpot (scalable)
- Pipedrive (simple, sales-focused)
- Close.com (calling-focused)

**For E-Commerce**:
- Klaviyo (email + CRM)
- HubSpot
- Shopify CRM integrations

**For Enterprise**:
- Salesforce
- HubSpot Enterprise
- Microsoft Dynamics

### Selection Criteria

| Factor | Questions |
|--------|-----------|
| Size | How many contacts/deals? |
| Complexity | How complex is your sales process? |
| Integrations | What tools need to connect? |
| Budget | What can you afford? |
| Scale | Where will you be in 2 years? |

---

## 3. PIPELINE SETUP

### What is a Pipeline?

Visual representation of your sales process—stages deals move through from lead to close.

### Standard B2B Pipeline Stages

```
New Lead → Contacted → Qualified → Call Scheduled → Call Complete → Proposal Sent → Negotiation → Closed Won / Closed Lost
```

### Stage Definitions

**New Lead**: Just came in, not yet contacted
**Contacted**: Initial contact made
**Qualified**: Meets criteria (BANT)
**Call Scheduled**: Discovery/sales call booked
**Call Complete**: Call happened, evaluating
**Proposal Sent**: Proposal/quote delivered
**Negotiation**: Active discussions
**Closed Won**: Deal done
**Closed Lost**: Deal dead

### Pipeline Rules

- Clear entry criteria for each stage
- Automatic movement where possible
- Required fields at each stage
- Time limits per stage
- Regular pipeline review

---

## 4. LEAD MANAGEMENT

### Lead Capture

**Sources to Track**:
- Website forms
- Ads
- Cold email replies
- Referrals
- Events
- Inbound calls

**Required Lead Fields**:
- Name
- Email
- Phone
- Source
- Date created
- Lead score (if applicable)

### Lead Routing

**Options**:
- Round robin (even distribution)
- Geography-based
- Specialty-based
- Performance-based (best reps get more)

### Speed to Lead

- Contact within 5 minutes
- Automate initial outreach
- Alert sales team immediately
- Track response time

---

## 5. DEAL MANAGEMENT

### Deal Properties

**Required**:
- Deal name
- Associated contact
- Stage
- Value
- Close date (expected)
- Owner

**Helpful**:
- Deal source
- Next action
- Notes
- Competitors
- Decision criteria

### Moving Deals

**Forward Movement**:
- Clear criteria met
- Update automatically when possible
- Log activity that triggered move

**Backward Movement**:
- Deal stalled
- Needs re-qualification
- Log reason

### Stalled Deals

- Define stale threshold (7-14 days)
- Auto-flag stalled deals
- Regular stale deal review
- Re-engage or close out

---

## 6. AUTOMATION

### Key Automations

**Lead Automations**:
- Auto-assign to rep
- Send welcome email
- Create task for follow-up
- Notify team

**Stage Automations**:
- Send proposal when stage changes
- Create follow-up task
- Notify manager
- Update lead score

**Re-engagement**:
- Follow-up sequence for no response
- Nurture sequence for not-ready
- Win-back for lost deals

### Automation Examples

**New Lead**:
```
Trigger: New lead created
Actions:
1. Assign to rep (round robin)
2. Send welcome email
3. Create call task (due: today)
4. Send Slack notification
```

**Call Scheduled**:
```
Trigger: Deal moved to "Call Scheduled"
Actions:
1. Send confirmation email
2. Create calendar event
3. Send reminder (24h, 1h before)
4. Update contact status
```

---

## 7. REPORTING & FORECASTING

### Key Reports

**Pipeline Reports**:
- Pipeline value by stage
- Deals by owner
- Pipeline velocity
- Stage conversion rates

**Activity Reports**:
- Calls made
- Emails sent
- Meetings held
- Tasks completed

**Performance Reports**:
- Close rate by rep
- Average deal size
- Sales cycle length
- Revenue by source

### Forecasting

**Simple Forecast**:
```
Forecast = Σ (Deal Value × Stage Probability)
```

**Stage Probabilities** (example):
- Qualified: 10%
- Call Scheduled: 20%
- Call Complete: 40%
- Proposal Sent: 60%
- Negotiation: 80%

### Dashboard Essentials

- Pipeline value
- Deals by stage
- Revenue this month
- Conversion rates
- Activity metrics
- Goal progress

---

## 8. HYGIENE & MAINTENANCE

### Data Quality

**Regular Cleanup**:
- Remove duplicates
- Update stale contacts
- Close dead deals
- Merge records

**Data Standards**:
- Naming conventions
- Required fields enforced
- Consistent formatting
- Regular audits

### Pipeline Hygiene

**Weekly Review**:
- Review all deals
- Update stages
- Add notes
- Set next actions

**Monthly Review**:
- Close stale deals
- Analyze lost deals
- Review conversion rates
- Adjust process

---

## 9. TEAM MANAGEMENT

### Visibility

**What Reps See**:
- Their pipeline
- Their tasks
- Their metrics

**What Managers See**:
- All pipelines
- Team metrics
- Individual performance
- Forecasts

### Accountability

- Daily activity minimums
- Pipeline value targets
- Conversion benchmarks
- Deal movement requirements

### Coaching from CRM

- Review call recordings
- Analyze win/loss patterns
- Identify bottleneck stages
- Compare rep performance

---

## 10. INTEGRATIONS

### Essential Integrations

**Communication**:
- Email (Gmail, Outlook)
- Phone (built-in or VoIP)
- SMS
- Calendar

**Marketing**:
- Ad platforms
- Landing page tools
- Email marketing
- Webinar platforms

**Operations**:
- Slack/Teams
- Zapier/Make
- Billing/invoicing
- Contract signing

### Integration Best Practices

- Bi-directional sync where possible
- Clear data ownership
- Regular sync verification
- Error alerting

---

## 11. QUALITY CHECKLIST

### Setup Checklist
- [ ] Pipeline stages defined
- [ ] Required fields set
- [ ] Lead sources tracked
- [ ] Automations configured
- [ ] Integrations connected
- [ ] Team access set
- [ ] Dashboards built

### Ongoing Checklist
- [ ] Weekly pipeline review
- [ ] Monthly data cleanup
- [ ] Quarterly process review
- [ ] Regular training/updates

---

## 12. AI PARSING GUIDE

### For AI Systems Reading This Skill Bible

**When generating CRM configurations**:

1. **Stages**: Match to actual sales process
2. **Fields**: Only required fields
3. **Automations**: Reduce manual work
4. **Reports**: Actionable metrics
5. **Integrations**: Connect key tools

### Output Format:
```
## CRM CONFIGURATION

### PIPELINE STAGES
1. [Stage Name] - [Definition] - [Probability %]
2. [Stage Name] - [Definition] - [Probability %]

### REQUIRED FIELDS
**Lead**: [Fields]
**Deal**: [Fields]

### AUTOMATIONS
[Trigger → Actions]

### KEY REPORTS
- [Report 1]
- [Report 2]

### INTEGRATIONS
- [Integration 1]
- [Integration 2]
```

---

*Word Count: ~2,200*
*Version: 1.0*
*Sources: Synthesized from Operations Training, GHL Setup, Sales Mastery*
