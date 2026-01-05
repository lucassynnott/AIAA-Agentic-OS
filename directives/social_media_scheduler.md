# Social Media Scheduler

## What This Workflow Is
This workflow schedules and auto-posts content across Twitter, LinkedIn, Instagram, and Facebook with optimized timing for maximum engagement.

## What It Does
1. Takes batch of content to schedule
2. Optimizes posting times per platform
3. Handles platform-specific formatting
4. Queues and auto-posts
5. Tracks performance

## Prerequisites

### Required API Keys (add to .env)
```
BUFFER_API_KEY=your_buffer_key            # Or native platform APIs
TWITTER_API_KEY=your_twitter_key
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
```

### Required Tools
- Python 3.10+
- Buffer account OR native platform APIs

### Installation
```bash
pip install requests tweepy
```

## How to Run

### Step 1: Prepare Content
Create `content_batch.json`:
```json
{
  "posts": [
    {"text": "Your post", "platforms": ["twitter", "linkedin"], "schedule": "2024-01-15 09:00"}
  ]
}
```

### Step 2: Schedule Posts
```bash
python3 execution/schedule_social.py \
  --content content_batch.json \
  --platforms "twitter,linkedin" \
  --timing optimal
```

### Quick One-Liner
```bash
python3 execution/schedule_social.py --content content.json --platforms "twitter,linkedin" --timing optimal
```

## Goal
Schedule and auto-post content across multiple social platforms with optimal timing.

## Inputs
- **Content**: Posts, images, videos
- **Platforms**: Twitter, LinkedIn, Instagram, Facebook
- **Schedule**: Posting times or "optimal"
- **Frequency**: Posts per day/week

## Process

### 1. Upload Content
```bash
python3 execution/schedule_social.py \
  --content content_batch.json \
  --platforms "twitter,linkedin" \
  --timing optimal
```

### 2. Content Format
```json
{
  "posts": [
    {
      "text": "[Post content]",
      "media": ["image.jpg"],
      "platforms": ["twitter", "linkedin"],
      "schedule": "2024-01-15 09:00",
      "hashtags": ["#tag1", "#tag2"]
    }
  ]
}
```

### 3. Optimal Posting Times
| Platform | Best Times |
|----------|------------|
| Twitter | 8-10am, 12pm, 5-6pm |
| LinkedIn | 7-8am, 12pm, 5-6pm (Tue-Thu) |
| Instagram | 11am-1pm, 7-9pm |
| Facebook | 1-4pm |

### 4. Auto-Scheduling Features
- Queue management
- Timezone handling
- Holiday awareness
- Engagement-based timing

### 5. Post Variations
Generate platform-specific versions:
- Twitter: Shorter, more hashtags
- LinkedIn: Professional tone, longer
- Instagram: Visual focus, caption style

## Automation Rules
- Never post same content twice in 24h
- Space posts 3+ hours apart
- Avoid weekends (optional)
- Pause during major events

## Integrations
- Buffer/Hootsuite API
- Native platform APIs
- Google Sheets (content calendar)

## Cost
- Buffer: $15-100/mo
- Native APIs: Free
