# Testimonial Request Automation

## What This Workflow Is
This workflow automatically requests testimonials from happy clients after milestones, with follow-up sequences and easy submission options.

## What It Does
1. Identifies clients ready for testimonial ask
2. Sends personalized request email
3. Provides easy submission options (video, text)
4. Follows up if no response
5. Collects and organizes testimonials

## Prerequisites

### Required API Keys (add to .env)
```
SENDGRID_API_KEY=your_sendgrid_key
HUBSPOT_API_KEY=your_hubspot_key
```

### Installation
```bash
pip install requests
```

## How to Run
```bash
python3 execution/request_testimonial.py --client_email "[EMAIL]" --milestone "project_complete"
```

## Goal
Automatically request and collect testimonials from happy clients at optimal moments.

## Inputs
- **Trigger Event**: What prompts the request
- **Client Segment**: Who to ask
- **Format**: Written, video, or both

## Process

### 1. Identify Candidates
Trigger testimonial request when:
- NPS score 9-10
- Major milestone achieved
- Positive feedback received
- Renewal completed
- Results exceeded expectations

### 2. Request Email
```
Subject: Would you share your experience?

Hi [NAME],

I'm thrilled about the results we've achieved together - 
[SPECIFIC RESULT]!

Would you be willing to share a quick testimonial? It 
really helps other [ROLE]s discover us.

Two easy options:

📝 Written (2 minutes)
Just reply with a few sentences about your experience.

🎥 Video (optional, 60 seconds)
Record a quick video here: [LOOM/VIDEOASK LINK]

Either one would mean the world to us!

Some questions to inspire you:
• What problem were you facing before?
• How has working with us helped?
• What results have you seen?

Thanks so much for considering!

[YOUR NAME]
```

### 3. Follow-up (if no response)
**Day 3:**
```
Subject: Re: Quick testimonial?

Hey [NAME],

Just a gentle nudge on the testimonial request.

If you're short on time, even one sentence helps:
"[COMPANY] helped us [RESULT]."

Thanks again!
```

### 4. Testimonial Formats

**Written:**
- Email reply
- Form submission
- LinkedIn recommendation

**Video:**
- Loom recording
- VideoAsk
- Zoom interview

**Audio:**
- Voice memo
- Podcast snippet

### 5. After Collection
- Thank you email
- Add to testimonial library
- Request permission for use
- Feature on website/materials

### 6. Usage Rights
```
Subject: Quick permission request

Hi [NAME],

Thank you SO much for the testimonial! 

Quick question - would you be okay with us featuring 
it on our website and marketing materials?

Happy to include:
☐ Full name and title
☐ First name only
☐ Company name
☐ Anonymous

Let me know what works!
```

## Integrations
- CRM (trigger data)
- Email platform
- Video tools (Loom, VideoAsk)

## Cost
- Automation: Free
- Video tools: Free-$30/mo
