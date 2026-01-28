#!/usr/bin/env python3
"""
X Keyword Search → YouTube Content Generator
Railway Cron Runner

This script runs every 3 hours to:
1. Search X for trending AI/automation posts via Grok-4-fast
2. Generate 5 YouTube video ideas with outlines
3. Create Google Doc with results
4. Send Slack notification

Schedule: Every 3 hours (0 */3 * * *)
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GROK_MODEL = "x-ai/grok-4-fast"

DEFAULT_KEYWORDS = [
    "AI agents",
    "AI automation",
    "Claude Code",
    "agentic workflows",
    "AI coding assistants"
]

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
"""


def call_openrouter(messages: list, model: str = GROK_MODEL, max_retries: int = 3) -> str:
    """Call OpenRouter API with retry logic."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set")

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
                return response.json()["choices"][0]["message"]["content"]
            elif response.status_code == 429:
                time.sleep(10 * (attempt + 1))
            else:
                print(f"API error {response.status_code}: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(5)
        except Exception as e:
            print(f"Request error: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)

    raise Exception("Failed to get response from OpenRouter")


def search_x_for_keywords(keywords: list, time_range: str = "24h") -> dict:
    """Use Grok to search X for high-performing posts."""
    print(f"Searching X for: {', '.join(keywords)}")

    keyword_list = ", ".join([f'"{k}"' for k in keywords])
    search_prompt = f"""Search X (Twitter) for high-performing posts from the last {time_range} about: {keyword_list}

Focus on posts with high engagement from credible accounts (tech founders, AI researchers, developers).

For each post, provide:
1. Author: @handle
2. Content: The post text
3. Engagement: Likes/retweets
4. Why It's Trending
5. Video Potential

Find 10-15 high-performing posts."""

    messages = [
        {"role": "system", "content": "You are Grok with full X access. Search for and analyze high-performing posts."},
        {"role": "user", "content": search_prompt}
    ]

    response = call_openrouter(messages)
    return {"keywords": keywords, "raw_results": response, "timestamp": datetime.now().isoformat()}


def analyze_themes(search_results: dict) -> dict:
    """Analyze search results and extract themes."""
    print("Analyzing themes...")

    analysis_prompt = f"""Based on these X search results:

{search_results['raw_results']}

Extract:
1. Top 5 Trending Themes
2. Viral Angles
3. Content Gaps
4. Controversy Points
5. Tutorial Opportunities"""

    messages = [
        {"role": "system", "content": "You are a content strategist analyzing social media trends."},
        {"role": "user", "content": analysis_prompt}
    ]

    analysis = call_openrouter(messages, model="anthropic/claude-sonnet-4")
    return {"themes_analysis": analysis, "source_data": search_results}


def generate_video_ideas(analysis: dict, num_videos: int = 5) -> dict:
    """Generate YouTube video ideas."""
    print(f"Generating {num_videos} video ideas...")

    ideas_prompt = f"""Based on this analysis of trending X posts:

{analysis['themes_analysis']}

Generate {num_videos} YouTube video ideas for @thelucassynnott (AI/automation channel).

{YOUTUBE_PRINCIPLES}

For EACH video, provide:
- Title (under 60 chars)
- Thumbnail Concept
- Target Length
- Format (Tutorial/Case Study/List/Story/Hot Take)
- Hook Script (first 30 seconds)
- Body Outline with 3 points
- Retention Tactics
- CTA
- Source Inspiration (which X posts)"""

    messages = [
        {"role": "system", "content": "You are an expert YouTube content strategist."},
        {"role": "user", "content": ideas_prompt}
    ]

    ideas = call_openrouter(messages, model="anthropic/claude-sonnet-4")
    return {"video_ideas": ideas, "num_videos": num_videos, "analysis": analysis}


def format_document(video_ideas: dict, search_results: dict) -> str:
    """Format everything into markdown."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""# YouTube Content Ideas from X Trends

**Generated**: {timestamp}
**Channel**: @thelucassynnott
**Keywords**: {', '.join(search_results['keywords'])}

---

## Trending Themes from X

{video_ideas['analysis']['themes_analysis']}

---

## Video Ideas & Outlines

{video_ideas['video_ideas']}

---

*Generated by AIAA X-to-YouTube Content Workflow (Railway Cron)*
"""


def markdown_to_docs_requests(markdown_content: str) -> list:
    """Convert markdown to Google Docs API formatting requests."""
    import re

    # First, strip markdown syntax and build plain text with position tracking
    lines = markdown_content.split('\n')
    plain_text = ""
    formatting_instructions = []  # (start, end, format_type, extra_data)

    for line in lines:
        line_start = len(plain_text)

        # Check for horizontal rule
        if line.strip() == '---':
            plain_text += "─" * 50 + "\n"  # Unicode horizontal line
            continue

        # Check for headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            # Remove any bold markers from heading text for clean display
            clean_text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            plain_text += clean_text + "\n"
            formatting_instructions.append((line_start, len(plain_text) - 1, 'heading', level))
            continue

        # Process bold markers - remove them from text but track positions
        processed_line = ""
        last_end = 0
        for match in re.finditer(r'\*\*(.+?)\*\*', line):
            # Add text before this bold section
            processed_line += line[last_end:match.start()]
            bold_start = line_start + len(processed_line)
            # Add the bold text (without markers)
            processed_line += match.group(1)
            bold_end = line_start + len(processed_line)
            formatting_instructions.append((bold_start, bold_end, 'bold', None))
            last_end = match.end()

        # Add remaining text after last bold
        processed_line += line[last_end:]
        plain_text += processed_line + "\n"

    # Now build the requests - insert all text first, then apply formatting
    requests = [
        {
            'insertText': {
                'location': {'index': 1},
                'text': plain_text
            }
        }
    ]

    # Apply formatting (in reverse order to maintain indices)
    for start, end, fmt_type, extra in reversed(formatting_instructions):
        # Adjust for 1-based index in Google Docs
        doc_start = start + 1
        doc_end = end + 1

        if fmt_type == 'heading':
            level = extra
            heading_style = {1: 'HEADING_1', 2: 'HEADING_2', 3: 'HEADING_3', 4: 'HEADING_4'}.get(level, 'HEADING_4')
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': doc_start, 'endIndex': doc_end + 1},
                    'paragraphStyle': {'namedStyleType': heading_style},
                    'fields': 'namedStyleType'
                }
            })
        elif fmt_type == 'bold':
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': doc_start, 'endIndex': doc_end},
                    'textStyle': {'bold': True},
                    'fields': 'bold'
                }
            })

    return requests


def create_google_doc(content: str, title: str) -> dict:
    """Create Google Doc with proper formatting using OAuth2 user credentials."""
    try:
        import pickle
        import base64
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        # Try OAuth2 token first (user credentials with storage quota)
        token_pickle_b64 = os.getenv("GOOGLE_OAUTH_TOKEN_PICKLE")
        if token_pickle_b64:
            # Decode and load the pickle
            token_data = base64.b64decode(token_pickle_b64)
            creds = pickle.loads(token_data)

            # Refresh if expired
            if creds.expired and creds.refresh_token:
                print("Refreshing OAuth token...")
                creds.refresh(Request())

            print(f"Using OAuth2 user credentials")

            docs_service = build('docs', 'v1', credentials=creds)
            drive_service = build('drive', 'v3', credentials=creds)

            # Create empty Google Doc
            file_metadata = {
                'name': title,
                'mimeType': 'application/vnd.google-apps.document'
            }

            file = drive_service.files().create(
                body=file_metadata,
                fields='id, webViewLink'
            ).execute()

            doc_id = file.get('id')
            print(f"Doc created: {doc_id}")

            # Convert markdown to Google Docs formatted requests
            format_requests = markdown_to_docs_requests(content)

            # Apply formatting in batches (Google Docs API has limits)
            batch_size = 100
            for i in range(0, len(format_requests), batch_size):
                batch = format_requests[i:i + batch_size]
                docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': batch}
                ).execute()

            print(f"Content inserted with formatting")

            # Make accessible (anyone with link can view)
            drive_service.permissions().create(
                fileId=doc_id,
                body={'type': 'anyone', 'role': 'reader'},
                fields='id'
            ).execute()

            doc_url = file.get('webViewLink', f"https://docs.google.com/document/d/{doc_id}/edit")
            print(f"Google Doc created: {doc_url}")

            return {
                "documentId": doc_id,
                "documentUrl": doc_url,
                "status": "created"
            }
    except Exception as e:
        print(f"Google Doc creation failed: {e}")
        import traceback
        traceback.print_exc()

    return {"documentUrl": None, "status": "skipped"}


def upload_to_gist(content: str, title: str) -> str:
    """Upload content to GitHub Gist as fallback."""
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return None

    try:
        filename = f"{title.replace(' ', '_').replace('-', '_')}.md"
        response = requests.post(
            "https://api.github.com/gists",
            headers={
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            },
            json={
                "description": title,
                "public": False,
                "files": {filename: {"content": content}}
            },
            timeout=30
        )
        if response.status_code == 201:
            gist_url = response.json().get("html_url")
            print(f"Gist created: {gist_url}")
            return gist_url
    except Exception as e:
        print(f"Gist creation failed: {e}")
    return None


def send_slack(doc_url: str, num_videos: int, content: str = None) -> dict:
    """Send Slack notification with optional content fallback."""
    if not SLACK_WEBHOOK_URL:
        print("No Slack webhook configured")
        return {"sent": False}

    # Try Gist as fallback if no doc URL
    gist_url = None
    if not doc_url and content:
        gist_url = upload_to_gist(content, f"YouTube Ideas {datetime.now().strftime('%Y-%m-%d')}")
        if gist_url:
            doc_url = gist_url

    doc_text = f"*Document:* <{doc_url}|View Content>" if doc_url else "*Content:* See thread below"

    message = {
        "text": "YouTube Content Ideas Ready",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "X → YouTube Content Generated"}
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
                "text": {"type": "mrkdwn", "text": doc_text}
            },
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} via Railway Cron"}]
            }
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        sent = response.status_code == 200

        # If no doc URL and no gist, send content summary as follow-up
        if sent and not doc_url and content:
            # Extract just the video ideas section (truncate if too long)
            summary = content[:3900] + "..." if len(content) > 4000 else content
            requests.post(SLACK_WEBHOOK_URL, json={
                "text": f"```{summary}```"
            })

        return {"sent": sent, "gist_url": gist_url}
    except Exception as e:
        print(f"Slack error: {e}")
        return {"sent": False}


def main():
    print("=" * 60)
    print("X → YOUTUBE CONTENT GENERATOR (Railway Cron)")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")

    if not OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set")
        return 1

    try:
        # Step 1: Search X
        search_results = search_x_for_keywords(DEFAULT_KEYWORDS)

        # Step 2: Analyze themes
        analysis = analyze_themes(search_results)

        # Step 3: Generate video ideas
        video_ideas = generate_video_ideas(analysis, num_videos=5)

        # Step 4: Format document
        document = format_document(video_ideas, search_results)

        # Step 5: Create Google Doc
        doc_title = f"YouTube Ideas - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        doc_result = create_google_doc(document, doc_title)

        # Step 6: Send Slack (with content fallback if no doc)
        send_slack(doc_result.get("documentUrl"), 5, content=document)

        print("=" * 60)
        print("COMPLETE")
        print(f"Google Doc: {doc_result.get('documentUrl', 'N/A')}")
        print(f"Finished: {datetime.now().isoformat()}")
        print("=" * 60)

        return 0

    except Exception as e:
        print(f"ERROR: {e}")
        if SLACK_WEBHOOK_URL:
            try:
                requests.post(SLACK_WEBHOOK_URL, json={"text": f"X→YouTube workflow failed: {str(e)[:100]}"})
            except:
                pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
