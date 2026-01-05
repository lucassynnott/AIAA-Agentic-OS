# LinkedIn Profile Change Tracker

## What This Workflow Is
This workflow monitors LinkedIn profiles for changes (job changes, promotions, posts) that indicate buying intent or outreach triggers.

## What It Does
1. Loads profile list to monitor
2. Checks profiles on schedule
3. Detects job changes, promotions, posts
4. Classifies change priority
5. Sends alerts for triggers

## Prerequisites

### Required API Keys (add to .env)
```
PHANTOMBUSTER_API_KEY=your_key            # Or scraping tool
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- LinkedIn profile tracker

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Configure Monitoring
```bash
python3 execution/track_linkedin_profiles.py \
  --profiles profiles.csv \
  --check_frequency daily \
  --output .tmp/changes.json
```

### Quick One-Liner (Daily Cron)
```bash
python3 execution/track_linkedin_profiles.py --profiles profiles.csv
```

## Goal
Monitor LinkedIn profiles for changes that indicate buying intent or trigger outreach opportunities.

## Inputs
- **Profile List**: LinkedIn URLs to monitor
- **Change Types**: Job change, promotion, post, company update
- **Alert Rules**: What triggers notification

## Process

### 1. Configure Monitoring
```bash
python3 execution/track_linkedin_profiles.py \
  --profiles profiles.csv \
  --check_frequency daily \
  --output .tmp/changes.json
```

### 2. Changes to Track

**High Priority (Outreach Trigger):**
- New job/role change
- Promotion
- Company change
- Hiring announcement

**Medium Priority:**
- New post/article
- Profile update
- New connection milestone
- Skill endorsements

**Company Level:**
- Funding announced
- New product launch
- Team growth
- Office expansion

### 3. Alert Format
```markdown
# LinkedIn Change Alert

## Job Changes 🚀
**[Name]** - [Old Title] → [New Title]
Company: [Company]
[LinkedIn URL]
Action: Send congrats + reconnect

## Promotions 📈
**[Name]** promoted to [New Title]
Company: [Company]
Action: Congratulate, assess new budget authority

## New Posts 📝
**[Name]** posted about [Topic]
Engagement: [X] likes, [Y] comments
Action: Engage with comment, reference in outreach
```

### 4. Outreach Templates

**Job Change:**
```
Subject: Congrats on the new role!

Hi [NAME],

Just saw you started as [NEW_TITLE] at [NEW_COMPANY] - 
congrats! That's a great move.

As you settle in, I'd imagine [PAIN POINT] might be 
on your radar. Would love to share how we help 
[SIMILAR COMPANIES] with that.

Best of luck in the new role!
```

**Promotion:**
```
Subject: Well-deserved promotion!

Hi [NAME],

Congrats on the promotion to [TITLE]! Your work at 
[COMPANY] clearly speaks for itself.

With your expanded scope, I thought you might be 
interested in how we help leaders like you [VALUE].

Would love to connect if you're open to it.
```

### 5. Automation
- Daily scan of profiles
- Immediate alert on changes
- Auto-add to outreach sequence
- CRM update with change note

## Integrations
- LinkedIn (via Apify)
- Email/Slack alerts
- CRM

## Cost
- Monitoring: ~$0.02/profile/day
