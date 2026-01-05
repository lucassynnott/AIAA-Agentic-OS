# Setup Calendar Automations

## Purpose
Configure GoHighLevel (GHL) calendar with automated booking, reminders, and follow-ups to maximize show rates and streamline sales operations.

## When to Use
- Setting up new sales calendar system
- Improving show rates for existing calendar
- Onboarding new sales team members
- Integrating calendar with marketing funnels
- Scaling appointment-based sales operations

## Prerequisites
- GoHighLevel account (sub-account access)
- Google Calendar or Office 365 connected
- Domain configured for emails
- SMS credits loaded (for text reminders)

## Core Philosophy

**Your calendar is a conversion tool, not just a scheduling tool.**

Every touchpoint from booking to call is an opportunity to:
- Build urgency
- Set expectations
- Increase commitment
- Reduce no-shows
- Warm up the prospect

Done right, your calendar system pre-sells prospects before they ever get on the call.

## Complete GHL Calendar Setup

### Step 1: Create Calendar in GHL

**Navigate:**
```
GoHighLevel Dashboard
→ Calendars
→ Create Calendar
```

**Calendar Settings:**

```
Calendar Name: "Sales Call" (or specific offer name)
Calendar Type: Round Robin or Assign to specific user
Duration: 30 min or 45 min (recommend 30 for discovery calls)
Buffer Time:
  - Before: 5 min (prep time)
  - After: 10 min (notes + decompression)
Availability:
  - Mon-Fri: 9am-5pm (or your preferred hours)
  - Block lunch: 12pm-1pm
  - No weekends (unless you want them)
```

**Booking Window:**
```
Minimum Notice: 2 hours (prevents last-minute bookings you're not ready for)
Maximum Days in Future: 30 days (creates urgency)
```

**Forms & Questions:**

Add these booking form fields:

```
1. First Name (Required)
2. Last Name (Required)
3. Email (Required)
4. Phone (Required)
5. Company/Business Name (Required)
6. What's your current monthly revenue? (Required, Text)
7. What's your biggest challenge right now? (Required, Text area)
8. How soon are you looking to solve this? (Required, Dropdown)
   - Immediately (this week)
   - Within 30 days
   - Within 90 days
   - Just exploring

Optional but useful:
9. Website URL
10. How did you hear about us?
```

**Qualification Questions Strategy:**

The questions serve three purposes:
1. **Pre-qualify** prospects (filter out tire-kickers)
2. **Give you intel** for the call (research done)
3. **Increase commitment** (effort = investment)

---

### Step 2: Configure Calendar Notifications (Your Side)

**Internal Notifications:**

```
Email Notification: ON
- Send to: [Your Email]
- When: Immediately when booking happens

SMS Notification: ON (optional)
- Send to: [Your Phone]
- When: 15 minutes before call

Calendar Sync: ON
- Sync to: Google Calendar / Office 365
- Update frequency: Real-time
```

**Booking Slack/Discord Webhook (Optional but Powerful):**

Set up webhook to notify your team channel:

```
Webhook URL: [Your Slack Webhook]
Message Format:
"🚨 New Call Booked
Name: {{contact.first_name}} {{contact.last_name}}
Company: {{contact.company}}
Revenue: {{contact.custom_field.revenue}}
Challenge: {{contact.custom_field.challenge}}
Time: {{appointment.start_time}}
Link: {{appointment.calendar_link}}"
```

---

### Step 3: Confirmation Page Setup

**Immediately After Booking:**

Create custom confirmation page (don't use default):

```
Headline: "You're Confirmed! 🎉"

Subheadline: "Your call with [Your Name] is scheduled for [Date & Time]"

Body Copy:
"Thanks for booking, [First Name]!

Here's what happens next:

1️⃣ Check your email for calendar invite (check spam)
2️⃣ You'll receive reminder texts leading up to our call
3️⃣ Before we talk, please [pre-call action - see below]

This call is worth your time. We'll cover:
✓ Your current situation with [problem]
✓ Exactly what's holding you back
✓ A clear plan to get from where you are to where you want to be

See you on [Day]!

[Your Name]
[Phone Number]"

CTA Button: "Add to Calendar" (ics download)
```

**Pre-Call Action Options:**

Include ONE of these:

**Option 1: Application Form**
```
"Before our call, fill out this quick questionnaire so I can prepare: [Link]"
```

**Option 2: Video to Watch**
```
"Watch this 3-minute video about our process: [Loom/YouTube Link]"
```

**Option 3: Case Study**
```
"Check out how we helped [Similar Client] solve [similar problem]: [Link]"
```

This accomplishes:
- Further qualifies them
- Warms them up
- Increases commitment
- Gives you more data

---

### Step 4: Email Automation Sequence

Set up automated emails in GHL:

#### Email 1: Immediate Confirmation (0 minutes after booking)

```
Subject: "Your call is confirmed - [Date & Time]"

Hey [First Name],

You're all set for your call on [Day], [Date] at [Time].

Calendar invite is attached. Add it to your calendar so you don't miss it.

Before we talk, I'm going to review your responses:
- Revenue: [Their Answer]
- Challenge: [Their Answer]

If anything changes or you need to reschedule, just click here: [Reschedule Link]

See you on [Day]!

[Your Name]
[Phone]
[Calendar Link]
```

#### Email 2: 24 Hours Before Call

```
Subject: "Tomorrow: Our call at [Time]"

Hey [First Name],

Quick reminder - we're meeting tomorrow at [Time].

I've been prepping for our call and I'm looking forward to helping you solve [their challenge from form].

Make sure you're ready:
✅ Be in a quiet place (not driving)
✅ Have a pen and paper
✅ Have [any prep work] done
✅ Block the full [30/45] minutes

Zoom/Calendar link: [Link]

See you tomorrow!

[Your Name]
```

#### Email 3: 1 Hour Before Call

```
Subject: "In 1 hour: Our [Time] call"

[First Name] -

We're on in 1 hour.

Here's the link: [Meeting Link]

If you need to reschedule, let me know ASAP: [Phone Number]

Otherwise, see you soon!

[Your Name]
```

#### Email 4: 5 Minutes Before (Optional)

```
Subject: "We're starting in 5 minutes"

[First Name] -

Starting in 5 minutes.

Join here: [Link]

See you in a sec!
```

---

### Step 5: SMS Automation Sequence

Set up text reminders (HUGE for show rates):

#### SMS 1: Immediate Confirmation (0 minutes)

```
"Hey [First Name], it's [Your Name].

Your call is confirmed for [Day] at [Time].

Calendar link: [Short Link]

See you then! 📅"
```

#### SMS 2: 24 Hours Before

```
"Hey [First Name] - tomorrow at [Time] we're talking about [their challenge].

Don't forget:
- Block the full [30] minutes
- Be in quiet place
- Have questions ready

Link: [Short Link]

See you tomorrow! - [Your Name]"
```

#### SMS 3: 2 Hours Before

```
"[First Name] - we're on in 2 hours ([Time]).

Link: [Short Link]

Ready to help you solve [problem] 💪

- [Your Name]"
```

#### SMS 4: 15 Minutes Before

```
"[First Name] - starting in 15 min.

Join here: [Link]

See you soon! 🚀"
```

**SMS Best Practices:**
- Keep under 160 characters when possible
- Use their first name
- Include link in every message
- Add emoji (makes it feel human)
- Sign your actual name
- Escalate urgency as time gets closer

---

### Step 6: No-Show Automation

**If They Don't Join (5 minutes after start time):**

#### SMS 1: Immediate (5 min after start)

```
"Hey [First Name] - looks like we missed each other.

I'm here for the next 10 minutes if you can still join: [Link]

If not, reschedule here: [Reschedule Link]

- [Your Name]"
```

#### Email 1: Immediate (5 min after start)

```
Subject: "We missed you - reschedule?"

Hey [First Name],

Looks like something came up for our [Time] call today.

No worries - stuff happens.

Click here to book a new time: [Reschedule Link]

Or if you'd rather not reschedule, just let me know.

[Your Name]
[Phone]
```

#### SMS 2: 2 Hours Later

```
"[First Name] - still want to solve [their challenge]?

Grab a new time here: [Link]

- [Your Name]"
```

#### Email 2: 24 Hours Later

```
Subject: "Last chance - [First Name]"

[First Name],

I'm going to assume you're no longer interested in solving [their challenge].

If I'm wrong and you still want help, book here: [Link]

Otherwise, I'll close your file.

Best,
[Your Name]

P.S. - We help [target audience] achieve [outcome]. If timing's just not right, reach out when it is.
```

---

### Step 7: Reschedule Automation

**If They Reschedule:**

#### Email: Immediate

```
Subject: "New time confirmed - [New Date & Time]"

Hey [First Name],

No problem - your new call time is [Day], [Date] at [Time].

You'll get the same reminders as before.

See you on [Day]!

[Your Name]
```

#### SMS: Immediate

```
"[First Name] - new call time confirmed: [Day] at [Time].

You'll get reminders.

See you then! - [Your Name]"
```

---

### Step 8: Post-Call Automation (For Shows)

**After Call Ends:**

#### If They Closed (Tag: "Closed"):

```
Email: "Welcome to [Company]!"

[Onboarding sequence]
```

#### If They Didn't Close (Tag: "Pitched Not Closed"):

```
Email (1 hour later):

Subject: "Following up on our call"

Hey [First Name],

Thanks for taking the time to chat today.

As we discussed, [summarize their problem and your solution].

Here's what we'd need to move forward:
- [Step 1]
- [Step 2]
- [Step 3]

Any questions? Just reply to this email or text me: [Phone]

[Your Name]

P.S. - Remember: every day you wait is another $[X] lost. Let's get this solved.
```

```
SMS (4 hours later):

"Hey [First Name] - any questions from our call earlier?

Ready to get started? - [Your Name]"
```

```
Email (24 hours later):

Subject: "Still thinking about it?"

[First Name],

Just checking in.

Where are you at with [solution]?

[Your Name]
```

[Continue follow-up sequence - see follow_up_after_call.md]

---

## Advanced Calendar Hacks

### Hack 1: Time Slot Scarcity

Limit available slots to create urgency:

```
Instead of: All day open
Use: 3-4 specific time slots per day

Example:
- 10:00 AM
- 1:00 PM
- 3:30 PM

This creates "limited availability" even if you're free all day.
```

### Hack 2: Conditional Availability

Show different calendars based on source:

```
Warm Traffic (Webinar attendees): See all available slots
Cold Traffic (Ad clicks): See limited slots + higher friction questions
```

### Hack 3: Multi-Step Booking

For high-ticket or to filter better:

```
Step 1: Application form (filters)
Step 2: (Conditional) If qualified → Calendar appears
Step 3: Booking confirmation
```

### Hack 4: Bump Questions

Add qualification at confirmation page:

```
"Before we confirm:
- Are you the decision maker? (Y/N)
- Can you invest $[X] to solve this? (Y/N)"

If they answer No → Show different message or don't book
```

### Hack 5: Video Confirmation Page

Instead of text confirmation, show video of you:

```
"Hey [First Name]! Quick video about what to expect on our call..."

[30-60 second Loom video]

Builds rapport before call even starts.
```

---

## Show Rate Optimization Checklist

To maximize show rates, ensure:

- [ ] SMS reminders enabled (most important)
- [ ] Multiple touchpoints (email + SMS)
- [ ] Increasing urgency in messaging
- [ ] Clear calendar link in every message
- [ ] Pre-call assignment (increases commitment)
- [ ] Confirmation page sets expectations
- [ ] 24hr and 2hr reminders at minimum
- [ ] No-show sequence triggers automatically
- [ ] Easy reschedule option provided
- [ ] Your calendar is synced (no double bookings)

**Target Show Rate:** 60-80% (industry standard is 40-50%)

With proper automation, you should hit 70%+.

---

## Calendar Settings Best Practices

### Duration:
- **30 minutes:** Discovery calls, consultations
- **45 minutes:** In-depth strategy sessions
- **60 minutes:** Only if absolutely necessary (fatigue)

**Recommendation:** 30 minutes. Forces you to be efficient.

### Buffer Time:
- **Before:** 5 minutes (prep + bathroom break)
- **After:** 10 minutes (notes, follow-up tasks)

### Meeting Buffer Between Calls:
- Minimum 15 minutes total buffer
- Prevents back-to-back exhaustion
- Gives time for urgent follow-ups

### Minimum Notice:
- **2 hours minimum** (prevents last-minute scrambles)
- **4 hours** if you need more prep time

### Booking Window:
- **Max 30 days out** (urgency)
- **14 days** if you want even more urgency

---

## Integration Points

### Connect to CRM:

Booking triggers:
- Create/update contact
- Add tags (e.g., "Booked Call")
- Start automation sequences
- Notify sales team

### Connect to Ad Platforms:

Track conversions:
- Facebook Pixel: Schedule event
- Google Ads: Conversion tracking
- Track source/medium in contact record

### Connect to Email Platform:

Sync contacts to:
- Email sequences
- Segmentation lists
- Nurture campaigns

---

## Calendar Link Distribution

Where to place your calendar link:

1. **Landing Pages** (primary CTA)
2. **Email Signatures** (for warm outreach)
3. **Website Footer** (persistent access)
4. **Social Media Bios** (Instagram, LinkedIn, Twitter)
5. **Cold Email Campaigns** (CTA)
6. **VSL End Screens** (after pitch)
7. **Chatbots** (automated response)
8. **Thank You Pages** (after lead magnet)

**Pro Tip:** Use branded short link (e.g., book.yourdomain.com)

Set up redirect:
```
book.yourdomain.com → [Your GHL Calendar Link]
```

Looks more professional and easier to share.

---

## Common Calendar Mistakes to Avoid

❌ No SMS reminders (kills show rates)
❌ Too many available slots (no urgency)
❌ Generic confirmation page (missed selling opportunity)
❌ No buffer between calls (burnout)
❌ Too many form fields (friction)
❌ No pre-call assignment (low commitment)
❌ Weak reminder copy (no urgency)
❌ No no-show sequence (lost leads)
❌ Calendar not synced (double bookings)
❌ No reschedule option (lost opportunities)

---

## Testing & Optimization

Test these variables:

1. **Confirmation Page Copy**
   - Headline variations
   - With/without video
   - Different pre-call assignments

2. **Reminder Frequency**
   - More vs fewer touchpoints
   - Timing of reminders

3. **Form Fields**
   - Number of questions
   - Types of questions
   - Required vs optional

4. **Availability Windows**
   - Limited slots vs open availability
   - Morning vs afternoon vs evening

5. **SMS Copy**
   - Formal vs casual
   - Length
   - Emoji use

**Track:**
- Booking conversion rate (page view → booking)
- Show rate (booking → showed)
- Close rate (showed → closed)

---

## Quick Start Checklist

To get your calendar up and running:

- [ ] Create calendar in GHL
- [ ] Set availability and buffer times
- [ ] Add booking form fields
- [ ] Create custom confirmation page
- [ ] Set up email sequence (3 emails minimum)
- [ ] Set up SMS sequence (3 texts minimum)
- [ ] Configure no-show automation
- [ ] Test booking as prospect
- [ ] Sync to Google Calendar
- [ ] Create branded short link
- [ ] Add to website and landing pages
- [ ] Monitor show rates

---

## Maintenance & Monitoring

Weekly tasks:
- Review show rate trends
- Check automation delivery rates
- Update availability as needed
- Review no-show reasons (if they reply)

Monthly tasks:
- Analyze conversion funnel (page → book → show → close)
- Test new reminder copy
- Update form questions based on learning
- Review competitor calendar flows

---

## Related Skills
- maximize_show_rates.md
- follow_up_after_no_show.md
- conduct_discovery_call.md
- pre_call_research.md
