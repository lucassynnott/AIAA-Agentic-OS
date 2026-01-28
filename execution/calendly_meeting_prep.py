#!/usr/bin/env python3
"""
Calendly Meeting Prep Webhook Handler

Triggered when a meeting is booked on Calendly:
1. Sends Slack alert with prospect details
2. Researches prospect (company, LinkedIn, etc.)
3. Creates Google Doc with full research
4. Sends second Slack with summary + doc link

Usage (local test):
    python3 execution/calendly_meeting_prep.py --test --email "prospect@company.com" --name "John Smith"

Deploy to Modal:
    modal deploy execution/calendly_meeting_prep.py
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Error: pip install requests python-dotenv")
    sys.exit(1)

# =============================================================================
# Configuration
# =============================================================================

CALENDLY_API_KEY = os.getenv("CALENDLY_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")


# =============================================================================
# Calendly API Functions
# =============================================================================

def fetch_calendly_event_details(scheduled_event_uri: str) -> dict:
    """Fetch full event details from Calendly API using the scheduled_event URI."""
    if not CALENDLY_API_KEY:
        print("[WARN] CALENDLY_API_KEY not set - cannot fetch event details")
        return {}
    if not scheduled_event_uri:
        print("[WARN] No scheduled_event URI provided")
        return {}
    
    try:
        print(f"[DEBUG] Fetching from Calendly: {scheduled_event_uri}")
        resp = requests.get(
            scheduled_event_uri,
            headers={"Authorization": f"Bearer {CALENDLY_API_KEY}"},
            timeout=10
        )
        
        if resp.status_code == 200:
            data = resp.json().get("resource", {})
            print(f"[DEBUG] Calendly returned event: {data.get('name')} at {data.get('start_time')}")
            return data
        else:
            print(f"[WARN] Calendly API error {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"[ERROR] Calendly API exception: {e}")
    
    return {}

# =============================================================================
# Slack Messaging
# =============================================================================

def send_slack_message(message: str, blocks: list = None) -> bool:
    """Send a message to Slack via webhook."""
    if not SLACK_WEBHOOK_URL:
        print(f"[SLACK - NO WEBHOOK] {message}")
        return False
    
    payload = {"text": message}
    if blocks:
        payload["blocks"] = blocks
    
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"Slack error: {e}")
        return False


def send_meeting_alert(invitee_name: str, invitee_email: str, event_name: str, 
                       start_time: str, company: str = None) -> bool:
    """Send initial Slack alert when meeting is booked."""
    
    company_text = f" from *{company}*" if company else ""
    
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "📅 New Meeting Booked!", "emoji": True}
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Prospect:*\n{invitee_name}{company_text}"},
                {"type": "mrkdwn", "text": f"*Email:*\n{invitee_email}"},
                {"type": "mrkdwn", "text": f"*Meeting:*\n{event_name}"},
                {"type": "mrkdwn", "text": f"*When:*\n{start_time}"}
            ]
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": "🔍 Researching prospect now... I'll send you a prep brief shortly."}]
        }
    ]
    
    return send_slack_message(f"New meeting booked with {invitee_name}", blocks)


def send_prep_brief(invitee_name: str, company: str, summary: str, doc_url: str = None) -> bool:
    """Send prep brief to Slack with summary and doc link."""
    
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"📋 Meeting Prep: {invitee_name}", "emoji": True}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Company:* {company}\n\n*Quick Summary:*\n{summary}"}
        }
    ]
    
    # Add doc link button if we have a Google Doc
    if doc_url and doc_url.startswith("http"):
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "📄 View Full Research Doc", "emoji": True},
                    "url": doc_url,
                    "style": "primary"
                }
            ]
        })
    
    return send_slack_message(f"Meeting prep ready for {invitee_name}", blocks)


def send_detailed_research(research: dict) -> bool:
    """Send full research to Slack when Google Docs isn't available."""
    
    name = research.get('prospect_name', 'Unknown')
    company = research.get('company', 'Unknown')
    
    # Truncate sections to fit Slack's 3000 char limit per block
    def truncate(text, max_len=2800):
        if not text:
            return "_No information available_"
        if len(text) > max_len:
            return text[:max_len] + "..."
        return text
    
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"📋 Full Meeting Prep: {name}", "emoji": True}},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*🏢 Company:* {company}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*📧 Email:* {research.get('prospect_email', 'N/A')}"}},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*📝 Executive Summary*\n{truncate(research.get('summary'))}"}},
    ]
    
    # Send first message with summary
    send_slack_message(f"Meeting prep for {name}", blocks)
    
    # Send talking points in separate message (they're usually longer)
    talking_points = research.get('talking_points')
    if talking_points:
        tp_blocks = [
            {"type": "header", "text": {"type": "plain_text", "text": f"💡 Talking Points: {name}", "emoji": True}},
            {"type": "section", "text": {"type": "mrkdwn", "text": truncate(talking_points, 2900)}}
        ]
        send_slack_message(f"Talking points for {name}", tp_blocks)
    
    return True


# =============================================================================
# Research Functions
# =============================================================================

def extract_company_from_email(email: str) -> str:
    """Extract company domain from email address."""
    if not email:
        return None
    
    domain = email.split("@")[-1].lower()
    
    # Skip common email providers
    free_providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", 
                      "icloud.com", "aol.com", "protonmail.com", "mail.com"]
    if domain in free_providers:
        return None
    
    # Extract company name from domain
    company = domain.split(".")[0].title()
    return company


def research_with_perplexity(query: str) -> str:
    """Use Perplexity for deep research."""
    if not PERPLEXITY_API_KEY:
        print("[WARN] PERPLEXITY_API_KEY not set")
        return None
    
    try:
        print(f"[DEBUG] Calling Perplexity API...")
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "sonar",
                "messages": [{"role": "user", "content": query}],
                "temperature": 0.2
            },
            timeout=60
        )
        
        if resp.status_code == 200:
            result = resp.json()["choices"][0]["message"]["content"]
            print(f"[DEBUG] Perplexity returned {len(result)} chars")
            return result
        else:
            print(f"[WARN] Perplexity API returned {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"[ERROR] Perplexity error: {e}")
    
    return None


def research_with_claude(query: str) -> str:
    """Use Claude via OpenRouter for research synthesis."""
    if not OPENROUTER_API_KEY:
        return None
    
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [{"role": "user", "content": query}],
                "temperature": 0.3,
                "max_tokens": 4000
            },
            timeout=120
        )
        
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Claude error: {e}")
    
    return None


def research_prospect(name: str, email: str, company: str = None) -> dict:
    """Research prospect and their company."""
    
    results = {
        "prospect_name": name,
        "prospect_email": email,
        "company": company,
        "company_research": None,
        "prospect_research": None,
        "linkedin_summary": None,
        "talking_points": None,
        "summary": None
    }
    
    # Extract company from email if not provided
    if not company:
        company = extract_company_from_email(email)
        results["company"] = company
    
    print(f"Researching: {name} at {company or 'Unknown Company'}")
    
    # 1. Company Research
    if company:
        print("  → Researching company...")
        company_query = f"""Research the company "{company}". Provide:
1. What the company does (products/services)
2. Company size and founding date
3. Target market/customers
4. Recent news or developments
5. Key competitors
6. Funding/financial info if available

Be concise but thorough. Use real, current information."""
        
        results["company_research"] = research_with_perplexity(company_query)
    
    # 2. Prospect Research
    print("  → Researching prospect...")
    prospect_query = f"""Research "{name}" who works at "{company or 'a company'}". 
Find information about:
1. Their current role and responsibilities
2. Professional background and experience
3. Any public content they've created (articles, podcasts, talks)
4. Professional interests or expertise areas

Email: {email}
Focus on professional/business information only."""
    
    results["prospect_research"] = research_with_perplexity(prospect_query)
    
    # 3. LinkedIn Summary
    print("  → Looking up LinkedIn profile...")
    linkedin_query = f"""Find and summarize the LinkedIn profile for "{name}" at "{company or 'their company'}".
Include:
- Current title and company
- Previous roles
- Education
- Skills and endorsements
- Any notable achievements or posts

Email hint: {email}"""
    
    results["linkedin_summary"] = research_with_perplexity(linkedin_query)
    
    # 4. Generate Talking Points with Claude
    print("  → Generating talking points...")
    
    context = f"""
PROSPECT: {name}
COMPANY: {company or 'Unknown'}
EMAIL: {email}

COMPANY RESEARCH:
{results['company_research'] or 'No company research available'}

PROSPECT RESEARCH:
{results['prospect_research'] or 'No prospect research available'}

LINKEDIN:
{results['linkedin_summary'] or 'No LinkedIn info available'}
"""
    
    talking_points_prompt = f"""Based on this research about a prospect I'm meeting with, generate:

{context}

1. **5 Personalized Talking Points** - Things to bring up that show I did my research
2. **3 Questions to Ask Them** - Thoughtful questions based on their background
3. **Potential Pain Points** - What challenges might they be facing based on their role/company
4. **Connection Points** - Any shared interests or experiences to bond over
5. **Meeting Goals** - What I should aim to learn/achieve in this meeting

Be specific and actionable. This is for a sales/business development call."""
    
    results["talking_points"] = research_with_claude(talking_points_prompt)
    
    # 5. Generate Executive Summary
    print("  → Creating executive summary...")
    
    summary_prompt = f"""Create a 3-4 sentence executive summary for a meeting prep brief.

{context}

TALKING POINTS:
{results['talking_points'] or 'Not available'}

The summary should tell me:
- Who this person is and what their company does
- Why they might be booking a meeting (likely pain points)
- One key thing to remember going into the call

Keep it brief but actionable."""
    
    results["summary"] = research_with_claude(summary_prompt)
    
    return results


# =============================================================================
# Google Docs Integration
# =============================================================================

def parse_markdown_to_plain_text(markdown: str):
    """Convert markdown to plain text with heading formatting for Google Docs."""
    import re
    
    def strip_markdown_inline(text):
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'(?<![*_])\*([^*]+)\*(?![*_])', r'\1', text)
        text = re.sub(r'(?<![*_])_([^_]+)_(?![*_])', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        return text
    
    lines = markdown.split('\n')
    result_lines = []
    formatting = []
    current_pos = 1
    
    for line in lines:
        if line.strip() in ['---', '***', '___', '- - -', '* * *']:
            rule = '─' * 50
            result_lines.append(rule)
            current_pos += len(rule) + 1
            continue
        
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            level = len(header_match.group(1))
            content = header_match.group(2)
            clean_content = strip_markdown_inline(content)
            result_lines.append(clean_content)
            
            style_map = {1: "HEADING_1", 2: "HEADING_2", 3: "HEADING_3", 
                        4: "HEADING_4", 5: "HEADING_5", 6: "HEADING_6"}
            formatting.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": current_pos, "endIndex": current_pos + len(clean_content)},
                    "paragraphStyle": {"namedStyleType": style_map.get(level, "HEADING_3")},
                    "fields": "namedStyleType"
                }
            })
            current_pos += len(clean_content) + 1
            continue
        
        bullet_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if bullet_match:
            content = bullet_match.group(2)
            clean_content = strip_markdown_inline(content)
            bullet_line = '• ' + clean_content
            result_lines.append(bullet_line)
            current_pos += len(bullet_line) + 1
            continue
        
        if line.strip():
            clean_line = strip_markdown_inline(line)
            result_lines.append(clean_line)
            
            if ':' in clean_line:
                colon_pos = clean_line.index(':')
                if colon_pos > 0:
                    formatting.append({
                        "updateTextStyle": {
                            "range": {"startIndex": current_pos, "endIndex": current_pos + colon_pos},
                            "textStyle": {"bold": True},
                            "fields": "bold"
                        }
                    })
            
            current_pos += len(clean_line) + 1
        else:
            result_lines.append('')
            current_pos += 1
    
    return '\n'.join(result_lines), formatting


def create_google_doc(research: dict) -> str:
    """Create a formatted Google Doc with the research and return the URL."""
    
    try:
        from google.oauth2 import service_account
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        import pickle
        import json
        
        SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
        
        creds = None
        
        # First, try service account from environment (Modal)
        # NOTE: Service accounts have storage limits - if quota exceeded, return None to use Slack fallback
        service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if service_account_json:
            print("  → Using service account credentials (may have storage limits)")
            sa_info = json.loads(service_account_json)
            creds = service_account.Credentials.from_service_account_info(sa_info, scopes=SCOPES)
        
        # Fall back to local OAuth credentials
        if not creds:
            token_path = Path(__file__).parent.parent / "token.pickle"
            creds_path = Path(__file__).parent.parent / "credentials.json"
            
            if token_path.exists():
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                elif creds_path.exists():
                    flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    print("No Google credentials available")
                    return save_local_doc(research)
                
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
        
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Shared folder for meeting prep docs
        MEETING_PREP_FOLDER_ID = "1Xhgr63LTNqRI8ofFaVE-_zXYJLgjbBiF"
        
        title = f"Meeting Prep: {research['prospect_name']} - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Create doc directly in shared folder using Drive API (service accounts need this)
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [MEETING_PREP_FOLDER_ID]
        }
        
        try:
            # Create in shared folder first
            file = drive_service.files().create(body=file_metadata, fields='id').execute()
            doc_id = file.get('id')
            print(f"  → Created doc in shared folder: {doc_id}")
        except Exception as e:
            print(f"  → Could not create in shared folder: {e}")
            # Fallback: try creating without folder (might fail for service accounts)
            doc = docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')
            print(f"  → Created doc without folder: {doc_id}")
        
        content = build_doc_content(research)
        plain_text, formatting_requests = parse_markdown_to_plain_text(content)
        
        # Insert text
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': [{'insertText': {'location': {'index': 1}, 'text': plain_text}}]}
        ).execute()
        
        # Apply formatting
        if formatting_requests:
            doc_length = len(plain_text) + 1
            valid_requests = []
            for req in formatting_requests:
                if "updateTextStyle" in req:
                    range_info = req["updateTextStyle"].get("range", {})
                elif "updateParagraphStyle" in req:
                    range_info = req["updateParagraphStyle"].get("range", {})
                else:
                    valid_requests.append(req)
                    continue
                
                start_idx = range_info.get("startIndex", 0)
                end_idx = range_info.get("endIndex", 0)
                
                if 0 < start_idx < doc_length and 0 < end_idx <= doc_length and end_idx > start_idx:
                    valid_requests.append(req)
            
            if valid_requests:
                try:
                    docs_service.documents().batchUpdate(
                        documentId=doc_id,
                        body={'requests': valid_requests}
                    ).execute()
                    print(f"  → Applied {len(valid_requests)} formatting rules")
                except Exception as e:
                    print(f"  → Formatting error (continuing): {e}")
        
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
        print(f"  → Created formatted Google Doc: {doc_url}")
        return doc_url
        
    except Exception as e:
        print(f"Google Docs error: {e}")
        # Return None so we use Slack fallback instead of local file
        # (local files aren't accessible on Modal anyway)
        if os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"):
            print("  → Will send via Slack instead")
            return None
        return save_local_doc(research)


def save_local_doc(research: dict) -> str:
    """Save research to local file as fallback (only works locally, not on Modal)."""
    
    output_dir = Path(__file__).parent.parent / ".tmp" / "meeting_prep"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{research['prospect_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = output_dir / filename
    
    content = build_doc_content(research)
    filepath.write_text(content, encoding="utf-8")
    
    print(f"  → Saved locally: {filepath}")
    return str(filepath)


def build_doc_content(research: dict) -> str:
    """Build the document content from research."""
    
    doc = f"""# Meeting Prep: {research['prospect_name']}

**Company:** {research['company'] or 'Unknown'}
**Email:** {research['prospect_email']}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Executive Summary

{research['summary'] or 'No summary available.'}

---

## Company Research

{research['company_research'] or 'No company research available.'}

---

## Prospect Research

{research['prospect_research'] or 'No prospect research available.'}

---

## LinkedIn Profile

{research['linkedin_summary'] or 'No LinkedIn information available.'}

---

## Talking Points & Strategy

{research['talking_points'] or 'No talking points generated.'}

---

*Generated by AIAA Meeting Prep*
"""
    
    return doc


# =============================================================================
# Deduplication - Track processed webhooks
# =============================================================================

# Simple in-memory cache for processed webhook URIs (works per container)
_processed_webhooks = set()

def is_duplicate_webhook(invitee_uri: str) -> bool:
    """Check if we've already processed this webhook."""
    if not invitee_uri:
        return False
    if invitee_uri in _processed_webhooks:
        return True
    _processed_webhooks.add(invitee_uri)
    # Keep cache from growing too large
    if len(_processed_webhooks) > 1000:
        _processed_webhooks.clear()
    return False


# =============================================================================
# Calendly Webhook Handler
# =============================================================================

def handle_calendly_webhook(payload: dict) -> dict:
    """Handle incoming Calendly webhook payload."""
    
    # Debug: log the payload structure
    print(f"[DEBUG] Received payload keys: {payload.keys()}")
    
    event_type = payload.get("event")
    
    if event_type != "invitee.created":
        return {"status": "ignored", "reason": f"Event type {event_type} not handled"}
    
    # Extract invitee data
    invitee_data = payload.get("payload", {})
    
    # DEDUPLICATION: Check if we've already processed this invitee
    invitee_uri = invitee_data.get("uri", "") or invitee_data.get("scheduled_event", "")
    if is_duplicate_webhook(invitee_uri):
        print(f"[INFO] Skipping duplicate webhook for: {invitee_uri}")
        return {"status": "duplicate", "message": "Already processed this booking"}
    print(f"[DEBUG] Invitee data keys: {invitee_data.keys()}")
    
    invitee_name = invitee_data.get("name", "Unknown")
    invitee_email = invitee_data.get("email", "")
    
    # Calendly sends scheduled_event as a URI - fetch full details from API
    scheduled_event_uri = invitee_data.get("scheduled_event", "")
    print(f"[DEBUG] scheduled_event URI: {scheduled_event_uri}")
    
    # Fetch full event details from Calendly API
    event_details = {}
    if scheduled_event_uri and isinstance(scheduled_event_uri, str) and scheduled_event_uri.startswith("http"):
        print("[DEBUG] Fetching event details from Calendly API...")
        event_details = fetch_calendly_event_details(scheduled_event_uri)
        print(f"[DEBUG] Got event details: name={event_details.get('name')}, start_time={event_details.get('start_time')}")
    
    # Get event name from API response or fallback
    event_name = event_details.get("name", "")
    if not event_name:
        event_type_info = invitee_data.get("event_type", "")
        if isinstance(event_type_info, dict):
            event_name = event_type_info.get("name", "Meeting")
        elif invitee_data.get("event_type_name"):
            event_name = invitee_data.get("event_type_name")
        else:
            event_name = "30 Minute Meeting"
    
    # Get start time from API response or fallback
    start_time = event_details.get("start_time", "")
    if not start_time:
        for time_field in ["scheduled_event_start_time", "start_time", "event_start_time"]:
            if invitee_data.get(time_field):
                start_time = invitee_data.get(time_field)
                print(f"[DEBUG] Found start_time in webhook {time_field}: {start_time}")
                break
    
    # Parse and format the start time
    if start_time:
        try:
            # Handle both formats: with and without microseconds
            start_time_clean = start_time.replace("Z", "+00:00")
            if "." in start_time_clean:
                # Remove microseconds for parsing
                parts = start_time_clean.split(".")
                start_time_clean = parts[0] + "+00:00" if "+" not in parts[1] else parts[0] + "+" + parts[1].split("+")[1]
            dt = datetime.fromisoformat(start_time_clean)
            start_time = dt.strftime("%B %d, %Y at %I:%M %p %Z")
        except Exception as e:
            print(f"[DEBUG] Could not parse time '{start_time}': {e}")
            # Keep the raw time if we can't parse it
            if "T" in start_time:
                start_time = start_time.replace("T", " at ").replace("Z", " UTC").split(".")[0]
    
    if not start_time:
        event_name = "30 Minute Meeting"  # Default fallback
    
    # Extract company from questions or email
    company = None
    questions = invitee_data.get("questions_and_answers", [])
    for qa in questions:
        question = qa.get("question", "").lower()
        if "company" in question or "organization" in question:
            company = qa.get("answer")
            break
    
    if not company:
        company = extract_company_from_email(invitee_email)
    
    print(f"\n{'='*60}")
    print(f"NEW MEETING BOOKED")
    print(f"{'='*60}")
    print(f"Name: {invitee_name}")
    print(f"Email: {invitee_email}")
    print(f"Company: {company or 'Unknown'}")
    print(f"Event: {event_name}")
    print(f"Time: {start_time}")
    print(f"{'='*60}\n")
    
    # Step 1: Send initial Slack alert
    print("Step 1: Sending Slack alert...")
    send_meeting_alert(invitee_name, invitee_email, event_name, start_time, company)
    
    # Step 2: Research the prospect
    print("\nStep 2: Researching prospect...")
    research = research_prospect(invitee_name, invitee_email, company)
    
    # Step 3: Create Google Doc (or save locally if no credentials)
    print("\nStep 3: Creating research document...")
    doc_url = create_google_doc(research)
    
    # Step 4: Send prep brief to Slack
    print("\nStep 4: Sending prep brief to Slack...")
    summary = research.get("summary", "Research complete.")
    # Truncate summary for Slack if needed
    if summary and len(summary) > 500:
        summary = summary[:500] + "..."
    
    # If we have a Google Doc URL, send brief with link
    # Otherwise, send detailed research directly to Slack
    if doc_url and doc_url.startswith("http"):
        send_prep_brief(invitee_name, company or "Unknown Company", summary, doc_url)
    else:
        # No Google Doc available - send full research to Slack
        print("  → No Google Doc created, sending full research to Slack...")
        send_prep_brief(invitee_name, company or "Unknown Company", summary, None)
        send_detailed_research(research)
    
    print(f"\n✅ Meeting prep complete for {invitee_name}")
    
    return {
        "status": "success",
        "prospect": invitee_name,
        "company": company,
        "doc_url": doc_url
    }


# =============================================================================
# Modal Deployment
# =============================================================================

try:
    import modal
    
    app = modal.App("calendly-meeting-prep")
    
    image = modal.Image.debian_slim().pip_install(
        "requests", "python-dotenv", "fastapi", "google-auth", 
        "google-auth-oauthlib", "google-api-python-client", "regex"
    )
    
    # Persistent deduplication dict - survives across container restarts
    processed_webhooks = modal.Dict.from_name("calendly-processed-webhooks", create_if_missing=True)
    
    @app.function(
        image=image,
        secrets=[
            modal.Secret.from_name("openrouter-secret"),
            modal.Secret.from_name("perplexity-secret"),
            modal.Secret.from_name("slack-webhook"),
            modal.Secret.from_name("google-service-account"),
            modal.Secret.from_name("calendly-secret"),
        ],
        timeout=300
    )
    @modal.fastapi_endpoint(method="POST")
    def webhook(payload: dict):
        """Modal webhook endpoint for Calendly."""
        # DEDUPLICATION: Use multiple keys to ensure uniqueness
        invitee_data = payload.get("payload", {})
        
        # Create unique key from email + scheduled_event
        email = invitee_data.get("email", "")
        scheduled_event = invitee_data.get("scheduled_event", "")
        invitee_uri = invitee_data.get("uri", "")
        
        # Use combination of email + event URI as dedup key
        dedup_key = f"{email}:{scheduled_event}" if email and scheduled_event else invitee_uri
        
        if dedup_key:
            try:
                # Check if already processed
                existing = processed_webhooks.get(dedup_key)
                if existing:
                    print(f"[INFO] DUPLICATE - Already processed: {dedup_key}")
                    return {"status": "duplicate", "message": "Already processed this booking"}
                
                # Mark as processing IMMEDIATELY before doing anything else
                processed_webhooks[dedup_key] = datetime.now().isoformat()
                print(f"[INFO] Processing new booking: {dedup_key}")
            except Exception as e:
                print(f"[WARN] Dedup check failed (continuing): {e}")
        
        return handle_calendly_webhook(payload)
    
    @app.function(image=image)
    @modal.fastapi_endpoint(method="GET")
    def health():
        """Health check endpoint."""
        return {"status": "ok", "service": "calendly-meeting-prep"}

except ImportError:
    pass


# =============================================================================
# CLI for Testing
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Calendly Meeting Prep")
    parser.add_argument("--test", action="store_true", help="Run a test with mock data")
    parser.add_argument("--email", default="john@acmecorp.com", help="Test prospect email")
    parser.add_argument("--name", default="John Smith", help="Test prospect name")
    parser.add_argument("--company", default=None, help="Test company name")
    
    args = parser.parse_args()
    
    if args.test:
        print("\n🧪 Running test meeting prep...\n")
        
        # Create mock Calendly payload - use a real scheduled_event URI for testing
        # This allows us to test the Calendly API integration
        mock_payload = {
            "event": "invitee.created",
            "payload": {
                "name": args.name,
                "email": args.email,
                # Use a real scheduled_event URI to test API fetching
                "scheduled_event": "https://api.calendly.com/scheduled_events/8a79407a-4cc5-466f-a15f-faf83426667c",
                "event_type": "https://api.calendly.com/event_types/61fa8dbb-b31e-4a03-8019-7f4cfc834935",
                "questions_and_answers": []
            }
        }
        
        if args.company:
            mock_payload["payload"]["questions_and_answers"].append({
                "question": "Company name",
                "answer": args.company
            })
        
        result = handle_calendly_webhook(mock_payload)
        print(f"\nResult: {json.dumps(result, indent=2)}")
        return 0
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
