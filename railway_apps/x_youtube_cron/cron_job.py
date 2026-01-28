#!/usr/bin/env python3
"""
X Keyword Search to YouTube Content Generator - Railway Cron Job

Runs every 3 hours via Railway cron schedule.
Searches X for trending posts and generates YouTube video ideas.

Environment Variables Required:
- OPENROUTER_API_KEY: For Grok-4-fast and Claude access
- SLACK_WEBHOOK_URL: For notifications
"""

import json
import os
import sys
import time
from datetime import datetime

import requests

# Configuration from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GROK_MODEL = "x-ai/grok-4-fast"
CLAUDE_MODEL = "anthropic/claude-sonnet-4"

# Default keywords
DEFAULT_KEYWORDS = [
    "AI agents",
    "AI automation",
    "Claude Code",
    "agentic workflows",
    "AI coding assistants"
]

# YouTube principles for video optimization
YOUTUBE_PRINCIPLES = """
## YouTube Video Optimization Principles

### Title Best Practices:
- Clear benefit/outcome
- Curiosity gap (not clickbait)
- Under 60 characters
- Formulas: "How I [result] in [time]", "The [X] That Changed My [Y]", "[Number] [Things] That [Outcome]"

### Hook Framework (First 30 seconds):
1. Immediate Context - Confirm they clicked the right video
2. Common Belief - What most people think
3. Contrarian Take - The truth bomb
4. Credibility - Why listen to you
5. The Plan - What will be covered

### Body Structure:
- 2nd best point goes FIRST
- Best point goes SECOND (ascending value)
- Re-hook every 2-3 minutes
- Simple language (6th grade vocabulary)

### Retention Tactics:
- Pattern interrupts every 20-30 seconds
- Open loops ("I'll show you exactly how in a minute...")
- Visual variety (cuts, B-roll, graphics)

### CTA:
- Subscribe with value proposition
- Next video recommendation
- Resource/template in description
"""


def call_openrouter(messages: list, model: str = GROK_MODEL, max_retries: int = 3) -> str:
    """Call OpenRouter API with retry logic."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in environment")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://aiaa.agency",
        "X-Title": "AIAA X YouTube Cron"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4096
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            elif response.status_code == 429:
                wait_time = 10 * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"API error {response.status_code}: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(5)

        except Exception as e:
            print(f"Request error: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)

    raise Exception("Failed to get response from OpenRouter after retries")


def search_x_for_keywords(keywords: list, time_range: str = "24h") -> dict:
    """Use Grok to search X for high-performing posts."""
    print(f"\n{'='*60}")
    print("STEP 1: Searching X for trending posts via Grok")
    print(f"{'='*60}")
    print(f"Keywords: {', '.join(keywords)}")

    keyword_list = ", ".join([f'"{k}"' for k in keywords])

    search_prompt = f"""Search X (Twitter) for high-performing posts from the last {time_range} about these topics: {keyword_list}

Focus on posts that are:
- Getting high engagement (lots of likes, retweets, replies)
- From credible accounts (tech founders, AI researchers, developers, creators)
- Discussing practical applications, insights, or hot takes
- Sparking conversation or debate

For each post found, provide:
1. **Author**: @handle and brief description
2. **Content**: The full post text
3. **Engagement**: Approximate likes/retweets/replies
4. **Why It's Trending**: What made this resonate
5. **Video Potential**: How this could become YouTube content

Find at least 10-15 high-performing posts across these topics."""

    messages = [
        {"role": "system", "content": "You are Grok, with full access to X (Twitter) posts and trends. Search for and analyze high-performing posts on the given topics."},
        {"role": "user", "content": search_prompt}
    ]

    print("Searching X via Grok...")
    response = call_openrouter(messages, model=GROK_MODEL)
    print(f"Found trending posts across {len(keywords)} keyword areas")

    return {
        "keywords": keywords,
        "time_range": time_range,
        "raw_results": response,
        "timestamp": datetime.now().isoformat()
    }


def analyze_and_extract_themes(search_results: dict) -> dict:
    """Analyze search results and extract common themes."""
    print(f"\n{'='*60}")
    print("STEP 2: Analyzing themes and patterns")
    print(f"{'='*60}")

    analysis_prompt = f"""Based on these X search results about AI, automation, and coding tools:

{search_results['raw_results']}

Analyze and extract:

1. **Top 5 Trending Themes**: What topics are getting the most engagement?
2. **Viral Angles**: What perspectives/takes are resonating?
3. **Content Gaps**: What questions are people asking that aren't being answered well?
4. **Controversy Points**: What debates are happening?
5. **Tutorial Opportunities**: What are people struggling to understand?

Be specific and cite the posts that support each theme."""

    messages = [
        {"role": "system", "content": "You are a content strategist analyzing social media trends to identify YouTube video opportunities."},
        {"role": "user", "content": analysis_prompt}
    ]

    print("Extracting themes via Claude...")
    analysis = call_openrouter(messages, model=CLAUDE_MODEL)

    return {
        "themes_analysis": analysis,
        "source_data": search_results
    }


def generate_video_ideas(analysis: dict, num_videos: int = 5, channel: str = "@thelucassynnott") -> dict:
    """Generate YouTube video ideas based on trending themes."""
    print(f"\n{'='*60}")
    print(f"STEP 3: Generating {num_videos} video ideas")
    print(f"{'='*60}")

    ideas_prompt = f"""Based on this analysis of trending X posts about AI, automation, and coding:

{analysis['themes_analysis']}

Generate exactly {num_videos} YouTube video ideas for the channel {channel} (focused on AI, automation, and building with code).

{YOUTUBE_PRINCIPLES}

For EACH video idea, provide:

## Video [Number]: [TITLE]

**Title**: [Under 60 characters, clear benefit + curiosity]
**Thumbnail Concept**: [Describe the visual - face expression, text overlay, background]
**Target Length**: [Minutes]
**Format**: [Tutorial / Case Study / List / Story / Hot Take]

### The Hook (First 30 seconds)
[Write out the actual script for the hook using the 5-part framework]

### Body Outline
1. [Point 1 - Second best point]
   - Key talking points
   - Visual/demo needed

2. [Point 2 - Best point]
   - Key talking points
   - Visual/demo needed

3. [Point 3]
   - Key talking points
   - Visual/demo needed

### Retention Tactics
- [Specific re-hooks to use]
- [Open loops to create]

### CTA
[Specific call to action for end of video]

### Source Inspiration
[Which X post(s) inspired this idea]

---

Make each idea distinct in format and angle. Include a mix of:
- One "how to" tutorial
- One hot take/opinion piece
- One case study/results video
- One list-style video
- One trend analysis/news video"""

    messages = [
        {"role": "system", "content": "You are an expert YouTube content strategist who creates viral video concepts."},
        {"role": "user", "content": ideas_prompt}
    ]

    print("Generating video ideas via Claude...")
    ideas_content = call_openrouter(messages, model=CLAUDE_MODEL)

    return {
        "video_ideas": ideas_content,
        "num_videos": num_videos,
        "channel": channel,
        "analysis": analysis
    }


def format_output_document(video_ideas: dict, search_results: dict) -> str:
    """Format everything into a markdown document."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    document = f"""# YouTube Content Ideas from X Trends

**Generated**: {timestamp}
**Channel**: {video_ideas['channel']}
**Keywords Searched**: {', '.join(search_results['keywords'])}
**Source**: Railway Cron Job (runs every 3 hours)

---

## Executive Summary

This document contains {video_ideas['num_videos']} YouTube video ideas generated from trending X (Twitter) posts about AI, automation, Claude Code, and agentic workflows.

---

## Trending Themes from X

{video_ideas['analysis']['themes_analysis']}

---

## Video Ideas & Outlines

{video_ideas['video_ideas']}

---

*Generated by AIAA X-to-YouTube Content Workflow (Railway Cron)*
*Powered by Grok-4-fast and Claude*
"""
    return document


def send_slack_notification(status: str, num_videos: int, themes_summary: str = "") -> dict:
    """Send Slack notification with results."""
    print(f"\n{'='*60}")
    print("STEP 4: Sending Slack notification")
    print(f"{'='*60}")

    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL not configured - skipping notification")
        return {"sent": False, "reason": "No webhook URL"}

    status_emoji = "✅" if status == "success" else "⚠️"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    message = {
        "text": f"{status_emoji} X → YouTube Content Generated",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{status_emoji} X → YouTube Content Generated"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{num_videos} Video Ideas Ready*\n\nBased on trending X posts about AI, automation, and Claude Code.\n\n*Source:* Railway Cron (every 3 hours)"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Generated on {timestamp}"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=30)
        if response.status_code == 200:
            print("Slack notification sent!")
            return {"sent": True}
        else:
            print(f"Slack notification failed: {response.status_code}")
            return {"sent": False, "status_code": response.status_code}
    except Exception as e:
        print(f"Error sending Slack notification: {e}")
        return {"sent": False, "error": str(e)}


def main():
    """Main execution flow."""
    print("=" * 60)
    print("X KEYWORD SEARCH → YOUTUBE CONTENT GENERATOR")
    print("Railway Cron Job - Runs Every 3 Hours")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Validate environment
    if not OPENROUTER_API_KEY:
        print("\nERROR: OPENROUTER_API_KEY not set")
        send_slack_notification("error", 0)
        sys.exit(1)

    try:
        # Step 1: Search X
        search_results = search_x_for_keywords(DEFAULT_KEYWORDS, "24h")

        # Step 2: Analyze themes
        analysis = analyze_and_extract_themes(search_results)

        # Step 3: Generate video ideas
        video_ideas = generate_video_ideas(analysis, num_videos=5)

        # Step 4: Format document
        document = format_output_document(video_ideas, search_results)

        # Print document (Railway logs)
        print(f"\n{'='*60}")
        print("GENERATED CONTENT:")
        print("=" * 60)
        print(document)

        # Step 5: Send notification
        send_slack_notification("success", 5)

        print(f"\n{'='*60}")
        print("WORKFLOW COMPLETE")
        print(f"{'='*60}")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return 0

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

        # Send error notification
        if SLACK_WEBHOOK_URL:
            try:
                requests.post(SLACK_WEBHOOK_URL, json={
                    "text": f"❌ X → YouTube cron failed: {str(e)[:100]}"
                }, timeout=30)
            except:
                pass

        return 1


if __name__ == "__main__":
    sys.exit(main())
