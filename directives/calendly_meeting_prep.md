# Calendly Meeting Prep Workflow

## What This Workflow Does
Automatically prepares you for sales calls when someone books a Calendly meeting:

1. **Instant Slack Alert** - Get notified immediately with prospect details and meeting time
2. **Deep Research** - Researches prospect and company via Perplexity AI
3. **Talking Points** - Claude generates personalized questions and discussion topics
4. **Google Doc** - Creates formatted prep document in your shared folder
5. **Summary to Slack** - Sends brief summary with link to full research doc

## Trigger
Calendly webhook fires on `invitee.created` event (when someone books a meeting).

## Research Performed

### Company Research
- What the company does
- Company size and target market
- Recent news and developments

### Prospect Research
- Role and background
- Professional expertise
- Relevant experience

### Generated Content
- 5 personalized talking points
- 3 thoughtful questions to ask
- Potential pain points to address
- Meeting goals and strategy

## Output

### Slack Message 1 (Immediate)
```
📅 New Meeting Booked!

Prospect: John Smith from Acme Corp
Email: john@acmecorp.com
Meeting: 30 Minute Meeting
When: January 15, 2026 at 2:00 PM UTC

🔍 Researching prospect now...
```

### Google Doc
Full meeting prep document with:
- Executive Summary (3-4 sentences)
- Company Research
- Prospect Research  
- Talking Points & Questions
- Meeting Details

### Slack Message 2 (After Research)
```
📋 Meeting Prep Ready: John Smith

Company: Acme Corp

[Brief 3-4 sentence summary]

📄 View Full Research Doc
```

## Required API Keys

| Key | Purpose |
|-----|---------|
| `CALENDLY_API_KEY` | Fetch event details from Calendly |
| `OPENROUTER_API_KEY` | Claude for generating talking points |
| `PERPLEXITY_API_KEY` | Research via Perplexity Sonar |
| `SLACK_WEBHOOK_URL` | Send Slack notifications |
| `GOOGLE_OAUTH_TOKEN_JSON` | Create Google Docs in your Drive |

## Local Testing

```bash
python3 execution/calendly_meeting_prep.py \
  --test \
  --email "prospect@company.com" \
  --name "John Smith" \
  --company "Acme Corp"
```

## How It Extracts Company Name

1. Checks Calendly form questions for "company" field
2. Falls back to extracting from email domain
3. Skips generic domains (gmail.com, yahoo.com, etc.)

## Quality Gates

- [ ] Slack alert sends within seconds of booking
- [ ] Company name extracted correctly
- [ ] Perplexity research returns relevant data
- [ ] Claude generates actionable talking points
- [ ] Google Doc created with proper formatting
- [ ] Summary + doc link sent to Slack

## Related Skills
- `skills/SKILL_BIBLE_sales_call_preparation.md`
- `skills/SKILL_BIBLE_prospect_research.md`
