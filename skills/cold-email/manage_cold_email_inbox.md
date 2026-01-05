# Manage Cold Email Inbox

## Skill Overview
This skill guides you through managing cold email campaign responses efficiently using RevReply AI inbox management and best practices for response handling.

## Table of Contents
1. [Understanding Inbox Management](#understanding-inbox-management)
2. [RevReply Setup](#revreply-setup)
3. [Response Categories](#response-categories)
4. [Automation Strategy](#automation-strategy)
5. [Manual Response Best Practices](#manual-response-best-practices)
6. [Scaling Inbox Management](#scaling-inbox-management)

## Understanding Inbox Management

Inbox management is the process of handling replies from your cold email campaigns to convert interested prospects into booked calls.

### Why Inbox Management Matters

**Campaign success depends on it:**
- 2-4% total reply rate = 20-40 responses per 1,000 emails
- Only 0.25-0.5% are positive replies
- Must respond quickly to convert
- Poor response handling kills conversions

**The challenge:**
- High volume of replies
- Multiple sentiment types (interested, not interested, out of office)
- Time-consuming to manually respond
- Need quick response times

**The solution:**
AI-powered inbox management (RevReply) + manual oversight for qualified leads.

## RevReply Setup

RevReply is an AI inbox manager that automatically categorizes and responds to cold email replies based on sentiment analysis.

### Step 1: Profile Configuration

**Access:** RevReply dashboard

**Profile Information:**
- **Your name** - How AI will sign responses
- **Company URL** - AI scrapes company info automatically
- **Auto-generate profile** - Takes 10 seconds to pull company data
- **Character limit:** 1,000 characters per text box (2 boxes available)

**Company description boxes:**
1. What your company does
2. Your value proposition/differentiators

**Example:**
```
Box 1:
We're a B2B lead generation agency that specializes in cold email campaigns
for SaaS companies. We handle everything from list building to inbox
management.

Box 2:
Unlike other agencies, we guarantee 10-15 qualified calls per month or you
don't pay. We've helped 50+ SaaS companies scale their outbound.
```

### Step 2: Meeting Scheduling Preferences

**Timezone:**
- Select your timezone (e.g., PST, EST)
- AI books meetings in your timezone

**Available Days:**
- Select weekdays
- Include/exclude weekends
- Recommended: Monday-Friday only

**Available Times:**
- Example: 7am-8pm PST
- AI only books within these hours
- Buffer time recommended (don't book until 9pm if you end at 8pm)

**Calendar Integration:**
- **Options:** Google Calendar or Outlook
- **Connection:** OAuth authentication
- **Purpose:** AI checks availability before booking

**Calendar Booking Link:**
- Your Calendly/Chili Piper/similar link
- AI includes in booking responses
- Required for self-booking

**Static Meeting Link (Optional):**
- Zoom/Google Meet permanent link
- Included in confirmations
- Alternative to calendar booking

### Step 3: Trigger Activation Controls

Triggers control when AI auto-responds vs when it stays silent.

**How triggers work:**
- Use "AND statement" triggers
- Must appear in prospect's **first** email reply
- Can be in subject line or body
- AI only responds if trigger is present

**Common trigger example:**
```
Trigger: #zoomwithme
```

**Usage in your cold email:**
```
Would you be open to a quick call? Just reply with "#zoomwithme" and I'll
send over some time slots.
```

**Why use triggers:**
- Prevents AI from responding to unqualified replies
- Gives you control over automation
- Only engages when prospect shows clear intent
- Protects your brand (AI doesn't respond inappropriately)

**Trigger best practices:**
- Use unique hashtags (#zoomwithme, #bookacall, #interested)
- Make it simple to type
- Include in every email in sequence
- Explain the trigger in your CTA

### Step 4: Inbox Manager Tone

**Tone options:**
- **Professional** - Formal, corporate language
- **Laid back** - Casual, friendly language

**Length options:**
- **Standard** - Normal response length
- **Brief** - Short, concise responses

**Recommended:** Professional + Standard
- Maintains brand credibility
- Appropriate for B2B
- Not too robotic, not too casual

### Step 5: No Thanks Follow-ups

Automated responses for "not interested" replies.

**Purpose:**
- Leave positive impression
- Offer resources/value
- Keep door open for future
- Courtesy response

**Configuration:**
- Enable "No Thanks Follow-ups"
- AI sends polite response
- Includes leave-behind materials
- Ends conversation gracefully

**Example AI response:**
```
No problem at all, {{first_name}}. I completely understand.

If anything changes down the line, feel free to reach out. In the meantime,
I'll send over our free cold email guide that might be helpful.

Best,
[Your name]
```

### Step 6: Reply Restrictions

**1-3 Punch Rule:**
- Limit AI to 1-3 automated responses per thread
- Prevents endless back-and-forth
- Forces human takeover after X responses
- Recommended: 3 responses max

**Why it matters:**
- AI shouldn't close deals
- Complex questions need human
- Brand protection
- Escalation to human at right time

**Example flow:**
1. Prospect: "Tell me more"
2. AI: Sends info, asks qualifying question
3. Prospect: "Sounds interesting"
4. AI: Shares case study, offers call
5. Prospect: "Yes, let's talk"
6. **Human takes over** - Books call, handles details

### Step 7: Follow-up Settings

**Day spacing options:**
- 1 day after last auto response
- 3 days after last auto response
- 5 days after last auto response
- Custom interval

**Recommended:** 3 days
- Not too aggressive
- Keeps conversation warm
- Allows time for prospect to review

**Follow-up strategy:**
```
Day 1: AI responds to initial interest
Day 4: AI follows up if no response
Day 7: AI final follow-up
Day 8+: Human takes over if still no response
```

### Step 8: Adaptive Templates

Custom instructions for different sentiment responses.

**Positive Sentiments:**
- Interested
- Information requests
- Pricing questions
- "Tell me more"

**Custom instructions:**
```
When prospect shows interest:
- Thank them for reply
- Ask qualifying question (budget, timeline, authority)
- Offer specific call times
- Include calendar link
- Keep response under 100 words
```

**Follow-up Sentiments:**
- "Circle back later"
- "Not right now"
- "Check in Q2"

**Custom instructions:**
```
When prospect asks to follow up:
- Acknowledge their timeline
- Set reminder for specified date
- Offer to send resources in meantime
- Keep door open
```

### Step 9: Automatic Sending Options

**Full Auto Mode:**
- AI sends responses immediately
- No human review
- Fast response time
- Higher risk

**Custom Mode (Recommended):**
- AI drafts response
- Sends to Slack for approval
- Human reviews before sending
- Slight delay, but safer

**Slack Integration:**
- Different channels for different sentiments
- Positive replies → #hot-leads channel
- Not interested → #cold-replies channel
- Out of office → #ooo-channel
- Manual review option

**Review workflow:**
1. AI categorizes reply
2. Sends draft to Slack
3. Human reviews draft
4. Approves or edits
5. AI sends approved response

### Step 10: Sentiment Categories

RevReply automatically categorizes replies:

**Positive:**
- Interested
- Information requests
- Pricing inquiries
- "Tell me more"
- **Action:** AI responds with qualification questions

**Follow-up:**
- "Circle back later"
- "Not right now"
- "Check in [future date]"
- **Action:** AI schedules follow-up reminder

**Not Interested:**
- "No thanks"
- "Not a good fit"
- "Remove me"
- **Action:** AI sends courtesy response, stops outreach

**Out of Office:**
- Auto-responders
- "On vacation until X"
- **Action:** AI pauses outreach, resumes when they're back

### Step 11: AI Training

RevReply learns from your feedback.

**Training system:**
- Thumbs up - AI response was good
- Thumbs down - AI response needs improvement
- AI adapts to your preferences over time

**Training timeline:**
- **Needs 20+ responses** to learn your voice
- First 20 responses: Review every draft
- After 20 responses: AI improves accuracy
- Ongoing: Continue training with feedback

**What AI learns:**
- Your tone and language
- How you handle objections
- Qualification questions you ask
- Booking process preferences

### Step 12: Whitelist and Domains

**Whitelist label redirect:**
- For custom domains (app.revreply.com vs custom domain)
- Ensures emails route correctly
- Technical setup with IT team if needed

**Domain configuration:**
- Connect sending domains
- Verify email accounts
- Ensure deliverability
- Whitelist RevReply IPs

## Response Categories

### Category 1: Positive/Interested

**Indicators:**
- "Tell me more"
- "I'm interested"
- "What are your prices?"
- "Can we schedule a call?"
- "Send me more information"

**Response strategy:**
1. Thank them quickly
2. Ask 1-2 qualifying questions
3. Offer specific call times
4. Include calendar link
5. Keep it brief

**Example response:**
```
Thanks for getting back to me, {{first_name}}!

Quick questions: What's your current monthly revenue, and when are you
looking to start?

I have availability Tuesday at 2pm or Wednesday at 10am. Does either work?

Here's my calendar: [link]

Best,
[Name]
```

### Category 2: Need More Info

**Indicators:**
- "What exactly do you do?"
- "How does this work?"
- "Do you have case studies?"
- "Who have you worked with?"

**Response strategy:**
1. Answer their specific question
2. Provide proof (case study, testimonial)
3. Ask if they'd like to discuss further
4. Offer call

**Example response:**
```
Great question, {{first_name}}.

We run done-for-you cold email campaigns. We handle list building, email
copywriting, and inbox management. Clients typically see 10-15 qualified
calls per month.

Here's a case study: [link]

Would you like to hop on a quick call to see if we'd be a good fit?

Best,
[Name]
```

### Category 3: Not Right Now

**Indicators:**
- "Not right now"
- "Circle back in Q2"
- "Check back with me in 3 months"
- "Timing isn't right"

**Response strategy:**
1. Respect their timeline
2. Ask to set reminder
3. Offer resources
4. Keep door open

**Example response:**
```
No problem at all, {{first_name}}. Totally understand.

I'll set a reminder to follow up in Q2. In the meantime, would you like me
to send over our cold email guide?

Looking forward to reconnecting!

Best,
[Name]
```

### Category 4: Not Interested

**Indicators:**
- "Not interested"
- "Don't email me again"
- "Not a good fit"
- "Remove me from your list"

**Response strategy:**
1. Apologize politely
2. Immediately unsubscribe
3. Offer value (resource)
4. End gracefully

**Example response:**
```
No problem at all, {{first_name}}. I've removed you from our list.

If you ever need help with cold email in the future, feel free to reach out.

Best wishes,
[Name]
```

**Important:** Honor unsubscribe requests immediately. Add to suppression list.

### Category 5: Out of Office

**Indicators:**
- Auto-responder
- "On vacation until [date]"
- "Out of office"
- "Will respond when I return"

**Response strategy:**
1. Don't respond
2. Note return date
3. Set follow-up reminder
4. Resume outreach when they're back

**AI handling:**
- RevReply auto-detects OOO
- Pauses outreach automatically
- Resumes on return date
- No manual intervention needed

## Automation Strategy

### When to Automate

**Automate these:**
- Initial acknowledgment ("Thanks for reply!")
- Information requests (FAQ-style)
- Appointment scheduling back-and-forth
- Out of office detection
- "Not interested" courtesy replies

**Don't automate these:**
- Complex objection handling
- Pricing negotiations
- Contract discussions
- Custom requests
- High-value prospects (manual white-glove)

### Automation Levels

**Level 1: No Automation**
- Manual response to every reply
- **Pros:** Full control, personalized
- **Cons:** Time-consuming, slow response time
- **Use for:** Very high-value prospects only

**Level 2: Semi-Automated (Recommended)**
- AI drafts responses
- Human reviews before sending
- **Pros:** Fast + safe, brand protection
- **Cons:** Still requires review time
- **Use for:** Most campaigns

**Level 3: Full Automation**
- AI responds automatically
- No human review
- **Pros:** Fastest response time, scales infinitely
- **Cons:** Risk of wrong responses
- **Use for:** High-volume, lower-ticket offers

### Hybrid Approach (Best Practice)

**Tier 1: High-value prospects (Manual)**
- Enterprise clients
- Dream clients
- Complex deals
- Response SLA: Within 1 hour

**Tier 2: Mid-value prospects (Semi-auto)**
- Standard customers
- Clear intent
- Straightforward deals
- Response SLA: Within 4 hours

**Tier 3: Low-value/unclear (Full auto)**
- Info requests
- Unclear intent
- Early-stage nurture
- Response SLA: Immediate

## Manual Response Best Practices

### Rule 1: Speed Matters

**Benchmark:**
- Under 1 hour: Excellent
- 1-4 hours: Good
- 4-24 hours: Acceptable
- Over 24 hours: Poor

**Why speed matters:**
- Prospect is hot when they reply
- Competitors are reaching out too
- Interest fades over time
- Fast response = professionalism

### Rule 2: Keep It Short

**Goal:** Under 100 words per response

**Why:**
- Respects their time
- Easier to read on mobile
- Gets to the point
- Increases response rate

**Bad example (too long):**
```
Hi John, Thanks so much for your interest in our services! I'm so excited to
tell you all about what we do. We've been in business for 5 years and have
worked with over 100 clients across 20 industries. Our founder started the
company because... [300 more words]
```

**Good example:**
```
Thanks for replying, John!

Quick question: What's your current monthly revenue?

I have availability Tuesday at 2pm or Wednesday at 10am for a quick call.

Here's my calendar: [link]

Best,
[Name]
```

### Rule 3: Always Include CTA

**Every response needs:**
- Clear next step
- Specific action
- Easy to execute

**Good CTAs:**
- "Does Tuesday at 2pm work for a call?"
- "Here's my calendar: [link]"
- "Reply with your availability"
- "Click here to book: [link]"

**Bad CTAs:**
- "Let me know if you're interested"
- "Feel free to reach out"
- "Looking forward to connecting"

### Rule 4: Qualify Early

**Don't wait until the call to qualify.**

**Key qualification questions:**
1. What's your current [relevant metric]?
2. When are you looking to start?
3. What's your budget range?
4. Who else needs to be involved in the decision?

**Example:**
```
Great to hear from you!

Quick questions before we schedule:
- Current monthly revenue?
- Looking to start in next 30-60 days?

Based on that, I'll know if we're a good fit.

Best,
[Name]
```

### Rule 5: Match Their Tone

**If they're casual:**
```
"Hey Sarah, Thanks for the reply! ..."
```

**If they're formal:**
```
"Hi Ms. Johnson, Thank you for your response. ..."
```

**If they're brief:**
```
"Great. Tuesday at 2pm? [calendar link]"
```

**If they're detailed:**
```
"Thanks for the detailed response. To answer your questions: ..."
```

## Scaling Inbox Management

### For 1-10 Replies/Day

**Solution:** Manual responses
- **Time:** 15-30 minutes/day
- **Tool:** Gmail/Outlook
- **Cost:** $0
- **Quality:** Highest

### For 10-50 Replies/Day

**Solution:** Templates + Manual
- **Time:** 1-2 hours/day
- **Tools:** Text expander, Smartlead inbox
- **Cost:** $0-50/month
- **Quality:** High

**Template examples:**
- Interested reply template
- Info request template
- Booking template
- Not interested template

### For 50-200 Replies/Day

**Solution:** AI Inbox Manager (RevReply)
- **Time:** 30-60 minutes/day (review only)
- **Tools:** RevReply + Slack
- **Cost:** $200-400/month
- **Quality:** Medium-high

**Process:**
1. AI handles 80% automatically
2. Human reviews 20% edge cases
3. Human handles booking calls
4. Human takes over at qualification stage

### For 200+ Replies/Day

**Solution:** Team + AI
- **Time:** Full-time inbox manager
- **Tools:** RevReply + CRM + Team
- **Cost:** $3,000-5,000/month (salary + tools)
- **Quality:** Medium

**Team structure:**
- SDR 1: Handles qualified leads
- SDR 2: Handles info requests
- Manager: Reviews AI responses
- RevReply: Handles initial triage

## Common Inbox Management Mistakes

### Mistake 1: Slow Response Time

**Problem:** Waiting 24+ hours to respond
**Result:** Lost opportunities, lower conversion
**Fix:** Set up notifications, check inbox 3x/day minimum

### Mistake 2: Over-Automation

**Problem:** AI responds to everything, no human oversight
**Result:** Inappropriate responses, damaged brand
**Fix:** Use semi-automated mode with Slack review

### Mistake 3: No Qualification

**Problem:** Booking calls with unqualified leads
**Result:** Wasted time on calls that go nowhere
**Fix:** Ask qualifying questions before booking

### Mistake 4: Inconsistent Tone

**Problem:** Every response sounds different
**Result:** Unprofessional, confusing brand voice
**Fix:** Create response templates, train AI on your voice

### Mistake 5: No Follow-up System

**Problem:** Prospects fall through cracks
**Result:** Lost deals, no second touch
**Fix:** Set reminders, use CRM, automate follow-ups

## Key Metrics to Track

**Response Time:**
- Goal: Under 1 hour
- Track: Time from reply to response
- Tool: Smartlead analytics

**Reply-to-Call Conversion:**
- Goal: 50% of positive replies book calls
- Track: Positive replies ÷ calls booked
- Tool: CRM or spreadsheet

**Call Show Rate:**
- Goal: 70%+ show up
- Track: Booked calls ÷ attended calls
- Tool: Calendar analytics

**Call-to-Close Rate:**
- Goal: 20-30% close
- Track: Calls ÷ deals closed
- Tool: CRM

## RevReply Example Conversation

**9-Message Back-and-Forth:**

**Prospect:** "Tell me more"

**RevReply AI:** "Thanks for your interest! We help SaaS companies book 10-15 qualified demos per month through cold email. Quick question: What's your current monthly revenue?"

**Prospect:** "$50K MRR"

**RevReply AI:** "Perfect fit. We typically work with companies in the $50K-500K range. When are you looking to start?"

**Prospect:** "ASAP"

**RevReply AI:** "Great. I have availability Tuesday at 2pm or Thursday at 10am. Which works better? Here's my calendar: [link]"

**Prospect:** "Tuesday works"

**RevReply AI:** "Perfect! I've sent a calendar invite. Looking forward to speaking on Tuesday at 2pm EST. In the meantime, here's a case study: [link]"

**Prospect:** "Sounds good"

**RevReply AI:** "See you Tuesday!"

**Result:** Call booked in under 2 hours with 9 messages, fully automated.

## Related Skills
- [Setup Smartlead](./setup_smartlead.md)
- [Write Cold Email Script](./write_cold_email_script.md)
- [Analyze Cold Email Performance](./analyze_cold_email_performance.md)
- [Personalize Cold Emails with AI](./personalize_cold_emails_with_ai.md)

## Action Checklist

Before launching campaigns:

- [ ] RevReply account created and profile configured
- [ ] Calendar integration connected (Google/Outlook)
- [ ] Meeting availability times set
- [ ] Calendar booking link added
- [ ] Trigger activation controls configured
- [ ] Inbox manager tone selected (Professional + Standard)
- [ ] No Thanks follow-ups enabled
- [ ] Reply restrictions set (3-punch max)
- [ ] Follow-up spacing configured (3 days)
- [ ] Adaptive templates created for each sentiment
- [ ] Slack integration connected (if using semi-auto)
- [ ] Sentiment categories configured
- [ ] AI trained with first 20 responses
- [ ] Response templates created for manual handling
- [ ] Qualification questions defined
- [ ] CRM or tracking system ready
- [ ] Team briefed on escalation process (if applicable)
