# Webinar Follow-up Sequence

## What This Workflow Is
This workflow automates post-webinar follow-up sequences with different messaging for attendees, partial attendees, and no-shows to maximize conversions.

## What It Does
1. Pulls attendee data from webinar platform
2. Segments by attendance status
3. Triggers appropriate email sequence for each segment
4. Sends replay links with urgency
5. Tracks clicks and conversions

## Prerequisites

### Required API Keys (add to .env)
```
ZOOM_API_KEY=your_zoom_key                # Or WEBINARJAM, DEMIO
CONVERTKIT_API_KEY=your_convertkit_key    # Email platform
```

### Required Tools
- Python 3.10+
- Webinar platform API access
- Email platform

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Segment Attendees
```bash
python3 execution/segment_webinar_attendees.py \
  --webinar_id "[WEBINAR_ID]" \
  --output .tmp/segments.json
```

### Step 2: Trigger Follow-up Sequences
```bash
python3 execution/trigger_webinar_followup.py \
  --segments .tmp/segments.json \
  --replay_url "[REPLAY_URL]" \
  --offer_url "[OFFER_URL]"
```

### Quick One-Liner
```bash
python3 execution/segment_webinar_attendees.py --webinar_id "[ID]" && \
python3 execution/trigger_webinar_followup.py --segments .tmp/segments.json
```

## Goal
Automate post-webinar follow-up to maximize conversions from attendees and no-shows.

## Inputs
- **Webinar Platform**: Zoom, WebinarJam, etc.
- **Attendee List**: Who registered and attended
- **Offer**: What you're selling
- **Replay Access**: How long replay is available

## Process

### 1. Segment Attendees
```bash
python3 execution/segment_webinar_attendees.py \
  --webinar_id "[ID]" \
  --output .tmp/segments.json
```

**Segments:**
- Registered + Attended full
- Registered + Attended partial
- Registered + No-show
- Clicked offer link
- Purchased

### 2. Sequence: Full Attendees

**Immediately:**
- Thank you email
- Replay link
- Offer reminder

**Day 1:**
- Recap + key takeaways
- Bonus content
- Offer with deadline

**Day 2:**
- Case study/testimonial
- FAQ addressed

**Day 3:**
- Scarcity reminder
- Final call

### 3. Sequence: No-Shows

**Immediately:**
- "Missed you" email
- Replay link (time-sensitive)

**Day 1:**
- Key insights they missed
- Strong CTA to watch replay

**Day 2:**
- "Replay expiring soon"

### 4. Sequence: Partial Attendees

**Immediately:**
- "Here's what you missed"
- Replay with timestamp

**Day 1:**
- Key points from end
- Offer details

### 5. Email Templates

**Post-Webinar (Attendees):**
```
Subject: [WEBINAR NAME] replay + your bonus

Hey [NAME],

Thanks for joining today!

Here's your replay: [LINK]
(Available for 48 hours)

Quick reminder - [OFFER] is available until [DATE].

[CTA BUTTON]

See you inside!
```

## Integrations
- Webinar platform API
- Email platform
- Payment processor

## Cost
- Email sending: Based on list size
- Automation: Free (n8n)
