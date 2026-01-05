# Lead Magnet Delivery Automation

## What This Workflow Is
This workflow automates the delivery of lead magnets (PDFs, templates, videos) and triggers nurture email sequences when someone opts in.

## What It Does
1. Captures lead from form submission
2. Immediately delivers lead magnet via email
3. Adds contact to email list with tags
4. Triggers nurture sequence
5. Tracks conversion source

## Prerequisites

### Required API Keys (add to .env)
```
CONVERTKIT_API_KEY=your_convertkit_key    # Or MAILCHIMP, SENDGRID
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Email platform with API
- File hosting (Google Drive, S3)

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Process New Lead
```bash
python3 execution/process_lead_magnet.py \
  --email "lead@example.com" \
  --lead_magnet "cold_email_templates" \
  --source "linkedin_ad"
```

### Step 2: Start Nurture Sequence
```bash
python3 execution/start_nurture_sequence.py \
  --email "lead@example.com" \
  --sequence "lead_magnet_nurture"
```

### Quick One-Liner
```bash
python3 execution/process_lead_magnet.py --email "[EMAIL]" --lead_magnet "[NAME]" --source "[SOURCE]"
```

## Goal
Automatically deliver lead magnets and trigger nurture sequences on opt-in.

## Inputs
- **Lead Magnet**: PDF, video, template, etc.
- **Delivery Method**: Email, redirect, or both
- **Nurture Sequence**: Follow-up emails after delivery

## Process

### 1. Capture Lead
Form submission triggers:
```bash
python3 execution/process_lead_magnet.py \
  --email "[EMAIL]" \
  --lead_magnet "cold_email_templates" \
  --source "[SOURCE]"
```

### 2. Immediate Actions
- Add to email list with tags
- Send delivery email
- Redirect to thank you page
- Track conversion

### 3. Delivery Email
```
Subject: Your [LEAD MAGNET NAME] is ready!

Hey [NAME],

Thanks for grabbing [LEAD MAGNET NAME]!

👉 Download it here: [LINK]

Here's how to get the most out of it:
1. [Quick win tip]
2. [How to implement]
3. [What to do next]

Got questions? Just reply to this email.

[YOUR NAME]

P.S. Keep an eye on your inbox - I'll be sharing 
[TEASE NEXT EMAIL] tomorrow.
```

### 4. Nurture Sequence

**Day 1:** Implementation tips
**Day 3:** Case study/results
**Day 5:** Related resource
**Day 7:** Soft pitch
**Day 10:** Value + harder pitch
**Day 14:** Final offer

### 5. Tagging System
- `lead_magnet:[name]`
- `source:[channel]`
- `date:[signup_date]`
- `engaged:yes/no`

## Double Opt-in (Optional)
- Send confirmation email first
- Only deliver after confirm click
- Better list quality

## Integrations
- Form provider (Typeform, Tally)
- Email platform (ConvertKit, Mailchimp)
- File hosting (Google Drive, S3)

## Cost
- Automation: Free
- Email: Based on list size
