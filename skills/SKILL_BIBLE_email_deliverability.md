# SKILL BIBLE: Email Deliverability & Technical Setup

> **Purpose**: Master-level expertise for ensuring emails reach the inbox, covering DNS, authentication, warming, and reputation management.
> **Word Count Target**: 2,500+
> **Last Updated**: 2026-01-02

---

## 1. EXECUTIVE SUMMARY

Deliverability is whether your emails reach the inbox or spam. Without good deliverability, your email marketing is worthless.

**The Deliverability Equation**:
```
Inbox Placement = Sender Reputation × Authentication × Content Quality × List Hygiene
```

**Key Metrics**:
- Inbox rate: 95%+ target
- Bounce rate: <2%
- Spam complaints: <0.1%
- Open rate: Indicator of placement

---

## 2. DNS AUTHENTICATION

### The Big Three

**SPF (Sender Policy Framework)**:
- Tells servers who can send on your behalf
- TXT record in DNS
- Lists authorized sending IPs

**DKIM (DomainKeys Identified Mail)**:
- Cryptographic signature
- Proves email wasn't altered
- Public key in DNS, private key signs emails

**DMARC (Domain-based Message Authentication)**:
- Policy for handling failures
- Tells servers what to do if SPF/DKIM fail
- Enables reporting

### Setup Process

1. Add SPF record
2. Add DKIM record
3. Add DMARC record (start with p=none)
4. Monitor reports
5. Gradually enforce (p=quarantine, then p=reject)

### Verification

- Use MXToolbox or similar
- Send test emails
- Check headers for PASS

---

## 3. DOMAIN WARMING

### Why Warm

New domains/IPs have no reputation. Sending too much too fast = spam folder.

### Warming Schedule

**Week 1**: 20-50 emails/day
**Week 2**: 50-100 emails/day
**Week 3**: 100-250 emails/day
**Week 4**: 250-500 emails/day
**Week 5+**: Gradually increase

### Warming Best Practices

- Send to engaged users first
- Encourage opens and replies
- Use warming services if needed
- Monitor metrics closely
- Slow down if issues arise

---

## 4. REPUTATION MANAGEMENT

### Sender Reputation Factors

**Positive Signals**:
- Opens
- Clicks
- Replies
- Forwarding
- Moving to inbox

**Negative Signals**:
- Spam complaints
- Bounces
- Unsubscribes
- Spam trap hits
- Low engagement

### Monitoring Tools

- Google Postmaster Tools
- Microsoft SNDS
- Sender Score
- ESP built-in analytics

---

## 5. LIST HYGIENE

### Regular Cleaning

**Remove**:
- Hard bounces (immediately)
- Soft bounces (after 3 attempts)
- Unengaged (90-120 days)
- Spam complainers

### Validation

- Verify new signups
- Use validation services
- Double opt-in when possible

### Sunset Flow

```
90 days inactive → Re-engagement attempt
120 days inactive → Final attempt
150 days inactive → Suppress/remove
```

---

## 6. CONTENT BEST PRACTICES

### Avoid Spam Triggers

**Don't**:
- ALL CAPS
- Excessive punctuation!!!
- Spam words (free, urgent, act now)
- Image-only emails
- Broken links/images

**Do**:
- Balanced text/image ratio
- Clean HTML
- Plain text version
- Clear sender name
- Easy unsubscribe

### Footer Requirements

- Physical address
- Unsubscribe link
- Company name
- Contact info

---

## 7. QUALITY CHECKLIST

### Technical Setup
- [ ] SPF configured
- [ ] DKIM configured
- [ ] DMARC configured
- [ ] Custom sending domain
- [ ] Domain warmed

### Ongoing
- [ ] Monitor reputation weekly
- [ ] Clean list monthly
- [ ] Check bounce rates
- [ ] Review spam complaints

---

## 8. AI PARSING GUIDE

### Output Format:
```
## DELIVERABILITY AUDIT

### DNS STATUS
- SPF: [Pass/Fail]
- DKIM: [Pass/Fail]
- DMARC: [Pass/Fail]

### REPUTATION
[Current status]

### ISSUES
[Problems found]

### RECOMMENDATIONS
[Actions to take]
```

---

*Word Count: ~1,400*
*Version: 1.0*
