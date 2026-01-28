#!/usr/bin/env python3
"""
X Keyword Search to YouTube Content Generator

Uses Grok-4-fast via OpenRouter to search X for trending posts,
then generates YouTube video ideas and outlines.

Follows directive: directives/x_keyword_youtube_content.md

Usage:
    python3 execution/x_keyword_youtube_content.py

    python3 execution/x_keyword_youtube_content.py \
        --keywords "AI agents" "Claude Code" "automation" \
        --num_videos 5
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Error: Required libraries not installed")
    print("Run: pip install requests python-dotenv")
    sys.exit(1)

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GROK_MODEL = "x-ai/grok-4-fast"  # Grok 4 Fast model via OpenRouter

# Default keywords for @thelucassynnott
DEFAULT_KEYWORDS = [
    "AI agents",
    "AI automation",
    "Claude Code",
    "agentic workflows",
    "AI coding assistants"
]

# YouTube skill bible excerpts (key principles)
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
        "X-Title": "AIAA X YouTube Content Generator"
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
    """Use Grok to search X for high-performing posts on given keywords."""

    print(f"\n{'='*60}")
    print("STEP 1: Searching X for trending posts via Grok")
    print(f"{'='*60}")
    print(f"Keywords: {', '.join(keywords)}")
    print(f"Time range: {time_range}")

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

Find at least 10-15 high-performing posts across these topics. Focus on posts that would make great YouTube video inspiration - controversial takes, practical tutorials, surprising insights, or trending debates.

Format as a structured list with clear sections for each post."""

    messages = [
        {"role": "system", "content": "You are Grok, with full access to X (Twitter) posts and trends. Search for and analyze high-performing posts on the given topics. Be specific about actual posts you find, including real engagement metrics and author handles."},
        {"role": "user", "content": search_prompt}
    ]

    print("\nSearching X via Grok...")
    response = call_openrouter(messages)

    print(f"\nFound trending posts across {len(keywords)} keyword areas")

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

    print("Extracting themes...")
    analysis = call_openrouter(messages, model="anthropic/claude-sonnet-4")  # Use Claude for analysis

    return {
        "themes_analysis": analysis,
        "source_data": search_results
    }


def generate_video_ideas(analysis: dict, num_videos: int = 5, channel_handle: str = "@thelucassynnott") -> list:
    """Generate YouTube video ideas based on trending themes."""

    print(f"\n{'='*60}")
    print(f"STEP 3: Generating {num_videos} video ideas")
    print(f"{'='*60}")

    ideas_prompt = f"""Based on this analysis of trending X posts about AI, automation, and coding:

{analysis['themes_analysis']}

Generate exactly {num_videos} YouTube video ideas for the channel {channel_handle} (focused on AI, automation, and building with code).

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
        {"role": "system", "content": "You are an expert YouTube content strategist who creates viral video concepts. Apply YouTube algorithm best practices and create content that maximizes CTR and retention."},
        {"role": "user", "content": ideas_prompt}
    ]

    print("Generating video ideas and outlines...")
    ideas_content = call_openrouter(messages, model="anthropic/claude-sonnet-4")

    return {
        "video_ideas": ideas_content,
        "num_videos": num_videos,
        "channel": channel_handle,
        "analysis": analysis
    }


def format_output_document(video_ideas: dict, search_results: dict) -> str:
    """Format everything into a markdown document."""

    print(f"\n{'='*60}")
    print("STEP 4: Formatting output document")
    print(f"{'='*60}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    document = f"""# YouTube Content Ideas from X Trends

**Generated**: {timestamp}
**Channel**: {video_ideas['channel']}
**Keywords Searched**: {', '.join(search_results['keywords'])}

---

## Executive Summary

This document contains {video_ideas['num_videos']} YouTube video ideas generated from trending X (Twitter) posts about AI, automation, Claude Code, and agentic workflows.

Each idea includes:
- Optimized title and thumbnail concept
- Full hook script (first 30 seconds)
- Body outline with retention tactics
- Specific CTAs

---

## Trending Themes from X

{video_ideas['analysis']['themes_analysis']}

---

## Video Ideas & Outlines

{video_ideas['video_ideas']}

---

## Raw X Search Data

<details>
<summary>Click to expand raw search results</summary>

{search_results['raw_results']}

</details>

---

## Next Steps

1. Review video ideas and select 1-2 to produce this week
2. Create thumbnails based on concepts
3. Script out full videos using outlines
4. Schedule filming and editing

---

*Generated by AIAA X-to-YouTube Content Workflow*
*Powered by Grok-4-fast and Claude*
"""

    return document


def save_locally(document: str, search_results: dict, video_ideas: dict) -> dict:
    """Save outputs locally."""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(".tmp/x_youtube_content")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save markdown
    md_file = output_dir / f"{timestamp}_video_ideas.md"
    with open(md_file, "w") as f:
        f.write(document)
    print(f"Saved markdown: {md_file}")

    # Save raw data as JSON
    json_file = output_dir / f"{timestamp}_data.json"
    with open(json_file, "w") as f:
        json.dump({
            "search_results": search_results,
            "video_ideas_raw": video_ideas['video_ideas'],
            "timestamp": timestamp
        }, f, indent=2, default=str)
    print(f"Saved JSON: {json_file}")

    return {
        "markdown_file": str(md_file),
        "json_file": str(json_file),
        "timestamp": timestamp
    }


def create_google_doc(markdown_content: str, title: str) -> dict:
    """Create Google Doc from markdown content."""

    print(f"\n{'='*60}")
    print("STEP 5: Creating Google Doc")
    print(f"{'='*60}")

    # Save temp markdown file
    temp_file = Path(".tmp/x_youtube_content/temp_doc.md")
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    with open(temp_file, "w") as f:
        f.write(markdown_content)

    # Call the Google Doc creator
    import subprocess

    try:
        result = subprocess.run(
            [
                "python3", "execution/create_google_doc_formatted.py",
                "--content", str(temp_file),
                "--title", title,
                "--output-json", ".tmp/x_youtube_content/doc_result.json"
            ],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent)
        )

        if result.returncode == 0:
            # Read result
            result_file = Path(".tmp/x_youtube_content/doc_result.json")
            if result_file.exists():
                with open(result_file) as f:
                    doc_result = json.load(f)
                print(f"Google Doc created: {doc_result.get('documentUrl', 'No URL')}")
                return doc_result

        print(f"Google Doc creation output: {result.stdout}")
        if result.stderr:
            print(f"Errors: {result.stderr}")

    except Exception as e:
        print(f"Error creating Google Doc: {e}")

    return {"documentUrl": None, "status": "failed"}


def send_slack_notification(workflow_name: str, status: str, doc_url: str, themes: str, num_videos: int) -> dict:
    """Send Slack notification."""

    print(f"\n{'='*60}")
    print("STEP 6: Sending Slack notification")
    print(f"{'='*60}")

    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL not configured - skipping notification")
        return {"sent": False, "reason": "No webhook URL"}

    # Status emoji
    status_emoji = "✅" if status == "success" else "⚠️"

    # Build message
    message = {
        "text": f"{status_emoji} {workflow_name}",
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
                    "text": f"*{num_videos} Video Ideas Ready*\n\nBased on trending X posts about AI, automation, and Claude Code."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Document:* <{doc_url}|Open Google Doc>" if doc_url else "*Document:* Saved locally (Google Doc failed)"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)

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
    parser = argparse.ArgumentParser(
        description="Generate YouTube content ideas from trending X posts"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=DEFAULT_KEYWORDS,
        help="Keywords to search on X"
    )
    parser.add_argument(
        "--num_videos",
        type=int,
        default=5,
        help="Number of video ideas to generate"
    )
    parser.add_argument(
        "--time_range",
        default="24h",
        choices=["24h", "7d", "30d"],
        help="Time range for X search"
    )
    parser.add_argument(
        "--channel",
        default="@thelucassynnott",
        help="YouTube channel handle for context"
    )
    parser.add_argument(
        "--skip_google_doc",
        action="store_true",
        help="Skip Google Doc creation"
    )
    parser.add_argument(
        "--skip_slack",
        action="store_true",
        help="Skip Slack notification"
    )

    args = parser.parse_args()

    print("="*60)
    print("X KEYWORD SEARCH → YOUTUBE CONTENT GENERATOR")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Keywords: {args.keywords}")
    print(f"Video count: {args.num_videos}")
    print(f"Channel: {args.channel}")

    # Check API key
    if not OPENROUTER_API_KEY:
        print("\nERROR: OPENROUTER_API_KEY not set in environment")
        print("Please add to your .env file")
        sys.exit(1)

    try:
        # Step 1: Search X
        search_results = search_x_for_keywords(args.keywords, args.time_range)

        # Step 2: Analyze themes
        analysis = analyze_and_extract_themes(search_results)

        # Step 3: Generate video ideas
        video_ideas = generate_video_ideas(
            analysis,
            num_videos=args.num_videos,
            channel_handle=args.channel
        )

        # Step 4: Format document
        document = format_output_document(video_ideas, search_results)

        # Step 5: Save locally
        local_files = save_locally(document, search_results, video_ideas)

        # Step 6: Create Google Doc
        doc_result = {"documentUrl": None}
        if not args.skip_google_doc:
            doc_title = f"YouTube Ideas - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            doc_result = create_google_doc(document, doc_title)

        # Step 7: Send Slack notification
        if not args.skip_slack:
            send_slack_notification(
                workflow_name="X → YouTube Content",
                status="success" if doc_result.get("documentUrl") else "partial",
                doc_url=doc_result.get("documentUrl"),
                themes="AI, automation, Claude Code",
                num_videos=args.num_videos
            )

        # Summary
        print(f"\n{'='*60}")
        print("WORKFLOW COMPLETE")
        print(f"{'='*60}")
        print(f"Video ideas generated: {args.num_videos}")
        print(f"Local file: {local_files['markdown_file']}")
        if doc_result.get("documentUrl"):
            print(f"Google Doc: {doc_result['documentUrl']}")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return 0

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

        # Try to send error notification
        if not args.skip_slack and SLACK_WEBHOOK_URL:
            try:
                requests.post(SLACK_WEBHOOK_URL, json={
                    "text": f"❌ X → YouTube workflow failed: {str(e)[:100]}"
                })
            except:
                pass

        return 1


if __name__ == "__main__":
    sys.exit(main())
