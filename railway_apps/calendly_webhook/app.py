#!/usr/bin/env python3
"""
AIAA Webhooks Dashboard - Railway Deployment

Beautiful monitoring dashboard + webhook handlers for agentic workflows.
"""

import os
import json
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
import requests
from collections import deque
import threading
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

app = Flask(__name__)

# =============================================================================
# Configuration
# =============================================================================

CALENDLY_API_KEY = os.getenv("CALENDLY_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GOOGLE_OAUTH_TOKEN_JSON = os.getenv("GOOGLE_OAUTH_TOKEN_JSON")

# Shared Google Drive folder for meeting prep docs
MEETING_PREP_FOLDER_ID = "1Xhgr63LTNqRI8ofFaVE-_zXYJLgjbBiF"

# Event storage (in-memory, max 100 events)
events_log = deque(maxlen=100)
events_lock = threading.Lock()

# File-based deduplication that survives worker restarts
DEDUP_FILE = "/tmp/processed_webhooks.json"

def load_processed_webhooks():
    """Load processed webhooks from file."""
    try:
        if os.path.exists(DEDUP_FILE):
            with open(DEDUP_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_processed_webhook(key: str):
    """Save a processed webhook to file."""
    try:
        data = load_processed_webhooks()
        data[key] = datetime.now().isoformat()
        # Keep only last 1000 entries
        if len(data) > 1000:
            sorted_keys = sorted(data.keys(), key=lambda k: data[k])
            for old_key in sorted_keys[:len(data)-1000]:
                del data[old_key]
        with open(DEDUP_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"[WARN] Could not save dedup: {e}")

def log_event(event_type: str, status: str, data: dict):
    """Log an event to the dashboard."""
    with events_lock:
        events_log.appendleft({
            "id": len(events_log) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "status": status,
            "data": data
        })

# =============================================================================
# Dashboard HTML Template
# =============================================================================

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webhooks — AIAA</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #1a1a1a;
            --bg-surface: #232323;
            --bg-elevated: #2a2a2a;
            --bg-hover: #333333;
            --text-primary: #f5f5f5;
            --text-secondary: #a3a3a3;
            --text-muted: #737373;
            --border: #333333;
            --border-subtle: #2a2a2a;
            --accent: #e07a3a;
            --accent-hover: #f08a4a;
            --accent-muted: rgba(224, 122, 58, 0.15);
            --success: #4ade80;
            --success-muted: rgba(74, 222, 128, 0.15);
            --error: #f87171;
            --error-muted: rgba(248, 113, 113, 0.15);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-base);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 2.5rem 2rem;
        }
        
        /* ===== HEADER ===== */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3rem;
        }
        
        .brand {
            display: flex;
            align-items: center;
            gap: 0.875rem;
        }
        
        .brand-icon {
            width: 36px;
            height: 36px;
            background: var(--accent);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .brand-icon svg {
            width: 20px;
            height: 20px;
            fill: white;
        }
        
        .brand-text h1 {
            font-size: 1.125rem;
            font-weight: 600;
            letter-spacing: -0.01em;
            color: var(--text-primary);
        }
        
        .brand-text span {
            font-size: 0.8125rem;
            color: var(--text-muted);
        }
        
        .status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.875rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 9999px;
            font-size: 0.8125rem;
            color: var(--text-secondary);
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--success);
        }
        
        /* ===== STATS ===== */
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 2.5rem;
        }
        
        .stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1.25rem;
            transition: all 0.2s ease;
        }
        
        .stat-card:hover {
            background: var(--bg-elevated);
            border-color: var(--border);
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 0.25rem;
        }
        
        .stat-value.orange { color: var(--accent); }
        .stat-value.green { color: var(--success); }
        .stat-value.muted { color: var(--text-muted); }
        .stat-value.red { color: var(--error); }
        
        .stat-label {
            font-size: 0.8125rem;
            color: var(--text-muted);
        }
        
        /* ===== SECTION ===== */
        .section {
            margin-bottom: 2rem;
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .section-title {
            font-size: 0.9375rem;
            font-weight: 500;
            color: var(--text-primary);
        }
        
        .btn-refresh {
            font-family: inherit;
            font-size: 0.8125rem;
            color: var(--accent);
            background: none;
            border: none;
            cursor: pointer;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            transition: background 0.15s ease;
        }
        
        .btn-refresh:hover {
            background: var(--accent-muted);
        }
        
        /* ===== EVENTS TABLE ===== */
        .events-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .events-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .events-table th {
            text-align: left;
            padding: 0.75rem 1rem;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            background: var(--bg-elevated);
            border-bottom: 1px solid var(--border-subtle);
        }
        
        .events-table td {
            padding: 0.875rem 1rem;
            font-size: 0.875rem;
            border-bottom: 1px solid var(--border-subtle);
            vertical-align: middle;
        }
        
        .events-table tr:last-child td {
            border-bottom: none;
        }
        
        .events-table tbody tr {
            transition: background 0.15s ease;
        }
        
        .events-table tbody tr:hover {
            background: var(--bg-hover);
        }
        
        .time {
            font-family: 'DM Mono', monospace;
            font-size: 0.8125rem;
            color: var(--text-muted);
        }
        
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .badge-meeting {
            background: var(--accent-muted);
            color: var(--accent);
        }
        
        .badge-default {
            background: var(--bg-elevated);
            color: var(--text-secondary);
        }
        
        .detail-name {
            font-weight: 500;
            color: var(--text-primary);
        }
        
        .detail-company {
            color: var(--text-muted);
            margin-left: 0.25rem;
        }
        
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.375rem;
            font-size: 0.8125rem;
        }
        
        .status-indicator::before {
            content: '';
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: currentColor;
        }
        
        .status-indicator.success { color: var(--success); }
        .status-indicator.error { color: var(--error); }
        .status-indicator.duplicate { color: var(--text-muted); }
        .status-indicator.processing { color: var(--accent); }
        
        .empty {
            padding: 3rem 1rem;
            text-align: center;
            color: var(--text-muted);
        }
        
        /* ===== ENDPOINTS ===== */
        .endpoints {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .endpoint-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            transition: border-color 0.15s ease;
        }
        
        .endpoint-row:hover {
            border-color: var(--border);
        }
        
        .method-badge {
            font-family: 'DM Mono', monospace;
            font-size: 0.6875rem;
            font-weight: 500;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            min-width: 3rem;
            text-align: center;
        }
        
        .method-badge.get {
            background: var(--success-muted);
            color: var(--success);
        }
        
        .method-badge.post {
            background: var(--accent-muted);
            color: var(--accent);
        }
        
        .endpoint-path {
            font-family: 'DM Mono', monospace;
            font-size: 0.8125rem;
            color: var(--text-primary);
            flex: 1;
        }
        
        .endpoint-desc {
            font-size: 0.8125rem;
            color: var(--text-muted);
        }
        
        /* ===== FOOTER ===== */
        footer {
            margin-top: 2.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-subtle);
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        
        footer a {
            color: var(--accent);
            text-decoration: none;
        }
        
        footer a:hover {
            text-decoration: underline;
        }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .container { padding: 1.5rem 1rem; }
            header { flex-direction: column; gap: 1rem; align-items: flex-start; }
            .stats { grid-template-columns: repeat(2, 1fr); }
            .events-table th:nth-child(2),
            .events-table td:nth-child(2) { display: none; }
        }
        
        @media (max-width: 480px) {
            .stats { grid-template-columns: 1fr 1fr; gap: 0.75rem; }
            .stat-card { padding: 1rem; }
            .stat-value { font-size: 1.5rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="brand">
                <div class="brand-icon">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" style="stroke: white;"/>
                    </svg>
                </div>
                <div class="brand-text">
                    <h1>AIAA Webhooks</h1>
                    <span>Agentic workflow monitor</span>
                </div>
            </div>
            <div class="status">
                <span class="status-dot"></span>
                <span>Operational</span>
            </div>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value orange">{{ stats.total }}</div>
                <div class="stat-label">Total events</div>
            </div>
            <div class="stat-card">
                <div class="stat-value green">{{ stats.success }}</div>
                <div class="stat-label">Successful</div>
            </div>
            <div class="stat-card">
                <div class="stat-value muted">{{ stats.duplicates }}</div>
                <div class="stat-label">Duplicates</div>
            </div>
            <div class="stat-card">
                <div class="stat-value red">{{ stats.errors }}</div>
                <div class="stat-label">Errors</div>
            </div>
        </div>
        
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Recent events</h2>
                <button class="btn-refresh" onclick="location.reload()">Refresh</button>
            </div>
            
            <div class="events-card">
                <table class="events-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Type</th>
                            <th>Details</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if events %}
                            {% for event in events %}
                            <tr>
                                <td><span class="time">{{ event.timestamp[11:19] }}</span></td>
                                <td>
                                    <span class="badge {% if event.type == 'meeting_booked' %}badge-meeting{% else %}badge-default{% endif %}">
                                        {{ event.type.replace('_', ' ') }}
                                    </span>
                                </td>
                                <td>
                                    {% if event.data.name %}
                                        <span class="detail-name">{{ event.data.name }}</span>
                                        {% if event.data.company %}
                                            <span class="detail-company">@ {{ event.data.company }}</span>
                                        {% endif %}
                                    {% elif event.data.message %}
                                        {{ event.data.message }}
                                    {% else %}
                                        —
                                    {% endif %}
                                </td>
                                <td>
                                    <span class="status-indicator {{ event.status }}">{{ event.status }}</span>
                                </td>
                            </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="4" class="empty">No events yet. Book a meeting to see activity here.</td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </section>
        
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">API endpoints</h2>
            </div>
            
            <div class="endpoints">
                <div class="endpoint-row">
                    <span class="method-badge post">POST</span>
                    <span class="endpoint-path">/webhook/calendly</span>
                    <span class="endpoint-desc">Meeting prep automation</span>
                </div>
                <div class="endpoint-row">
                    <span class="method-badge get">GET</span>
                    <span class="endpoint-path">/health</span>
                    <span class="endpoint-desc">Health check</span>
                </div>
                <div class="endpoint-row">
                    <span class="method-badge get">GET</span>
                    <span class="endpoint-path">/api/events</span>
                    <span class="endpoint-desc">Events JSON</span>
                </div>
            </div>
        </section>
        
        <footer>
            <span>Auto-refreshes every 30s</span>
            <span>Built with <a href="#">AIAA Agentic OS</a></span>
        </footer>
    </div>
    
    <script>
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
'''

# =============================================================================
# Calendly API
# =============================================================================

def fetch_calendly_event_details(scheduled_event_uri: str) -> dict:
    """Fetch full event details from Calendly API."""
    if not CALENDLY_API_KEY or not scheduled_event_uri:
        return {}
    
    try:
        resp = requests.get(
            scheduled_event_uri,
            headers={"Authorization": f"Bearer {CALENDLY_API_KEY}"},
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json().get("resource", {})
    except Exception as e:
        print(f"[ERROR] Calendly API: {e}")
    return {}

# =============================================================================
# Slack Messaging
# =============================================================================

def send_slack_message(message: str, blocks: list = None) -> bool:
    """Send a message to Slack."""
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
        print(f"[ERROR] Slack: {e}")
        return False


def send_meeting_alert(name: str, email: str, event_name: str, start_time: str, company: str = None):
    """Send initial meeting booked alert."""
    company_text = f" from *{company}*" if company else ""
    
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": "📅 New Meeting Booked!", "emoji": True}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*Prospect:*\n{name}{company_text}"},
            {"type": "mrkdwn", "text": f"*Email:*\n{email}"},
            {"type": "mrkdwn", "text": f"*Meeting:*\n{event_name}"},
            {"type": "mrkdwn", "text": f"*When:*\n{start_time}"}
        ]},
        {"type": "context", "elements": [
            {"type": "mrkdwn", "text": "🔍 Researching prospect now... I'll send prep notes shortly."}
        ]}
    ]
    send_slack_message(f"New meeting with {name}", blocks)


def send_research_to_slack(research: dict, doc_url: str = None):
    """Send short summary to Slack with Google Doc link."""
    name = research.get('prospect_name', 'Unknown')
    company = research.get('company', 'Unknown')
    summary = research.get('summary', 'Research complete.')
    
    # Keep it short - 5 lines max + doc link
    # Truncate summary to ~3-4 sentences
    summary_short = summary[:400] + "..." if len(summary) > 400 else summary
    
    doc_link = f"📄 <{doc_url}|*View Full Research Doc*>" if doc_url else "_No doc created_"
    
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"📋 Meeting Prep Ready: {name}", "emoji": True}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Company:* {company}\n\n{summary_short}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": doc_link}},
    ]
    send_slack_message(f"Meeting prep for {name}", blocks)

# =============================================================================
# Google Docs
# =============================================================================

def create_google_doc(research: dict) -> str:
    """Create a formatted Google Doc with research and return URL."""
    if not GOOGLE_OAUTH_TOKEN_JSON:
        print("[WARN] No Google OAuth token configured")
        return None
    
    try:
        token_data = json.loads(GOOGLE_OAUTH_TOKEN_JSON)
        creds = Credentials(
            token=token_data.get('token'),
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data.get('token_uri'),
            client_id=token_data.get('client_id'),
            client_secret=token_data.get('client_secret'),
            scopes=token_data.get('scopes')
        )
        
        # Refresh if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("[INFO] Refreshed Google OAuth token")
        
        drive_service = build('drive', 'v3', credentials=creds)
        docs_service = build('docs', 'v1', credentials=creds)
        
        # Create document title
        name = research.get('prospect_name', 'Unknown')
        company = research.get('company', 'Unknown')
        date_str = datetime.now().strftime('%Y-%m-%d')
        title = f"Meeting Prep: {name} ({company}) - {date_str}"
        
        # Create doc directly in shared folder using Drive API
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [MEETING_PREP_FOLDER_ID]
        }
        
        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        doc_id = file.get('id')
        print(f"[INFO] Created Google Doc: {doc_id}")
        
        # Build document content
        content = build_doc_content(research)
        
        # Format and insert content
        requests_batch = []
        
        # Insert all text first
        requests_batch.append({
            'insertText': {
                'location': {'index': 1},
                'text': content
            }
        })
        
        # Apply formatting
        # Title (first line)
        title_end = content.find('\n') + 1
        requests_batch.append({
            'updateParagraphStyle': {
                'range': {'startIndex': 1, 'endIndex': title_end},
                'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                'fields': 'namedStyleType'
            }
        })
        
        # Find and format section headers
        sections = ['EXECUTIVE SUMMARY', 'COMPANY RESEARCH', 'PROSPECT RESEARCH', 'TALKING POINTS', 'QUESTIONS TO ASK', 'MEETING DETAILS']
        for section in sections:
            idx = content.find(section)
            if idx > 0:
                requests_batch.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': idx + 1, 'endIndex': idx + len(section) + 2},
                        'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                        'fields': 'namedStyleType'
                    }
                })
        
        # Execute batch update
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests_batch}
        ).execute()
        
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
        print(f"[INFO] Google Doc ready: {doc_url}")
        return doc_url
        
    except Exception as e:
        print(f"[ERROR] Google Docs creation failed: {e}")
        return None


def strip_markdown(text: str) -> str:
    """Remove markdown formatting from text."""
    if not text:
        return text
    import re
    # Remove headers (### Header -> Header)
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    # Remove bold (**text** or __text__ -> text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    # Remove italic (*text* or _text_ -> text) - careful not to break asterisk lists
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'\1', text)
    # Remove links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove citation brackets [1], [2], etc
    text = re.sub(r'\[\d+\]', '', text)
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def build_doc_content(research: dict) -> str:
    """Build the document content string with clean formatting."""
    name = research.get('prospect_name', 'Unknown')
    company = research.get('company', 'Unknown')
    email = research.get('prospect_email', '')
    
    # Strip markdown from all research content
    summary = strip_markdown(research.get('summary', 'No summary available.'))
    company_research = strip_markdown(research.get('company_research', 'No company research available.'))
    prospect_research = strip_markdown(research.get('prospect_research', 'No prospect research available.'))
    talking_points = strip_markdown(research.get('talking_points', 'No talking points generated.'))
    
    content = f"""Meeting Prep: {name}

EXECUTIVE SUMMARY
{summary}

COMPANY RESEARCH
Company: {company}

{company_research}

PROSPECT RESEARCH
Name: {name}
Email: {email}

{prospect_research}

TALKING POINTS
{talking_points}

MEETING DETAILS
Prepared: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Generated by: AIAA Agentic OS
"""
    return content


# =============================================================================
# Research Functions
# =============================================================================

def research_with_perplexity(query: str) -> str:
    """Use Perplexity Sonar for research."""
    if not PERPLEXITY_API_KEY:
        return None
    
    try:
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
            return resp.json()["choices"][0]["message"]["content"]
        else:
            print(f"[WARN] Perplexity {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"[ERROR] Perplexity: {e}")
    return None


def research_with_claude(prompt: str) -> str:
    """Use Claude via OpenRouter."""
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
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 4000
            },
            timeout=120
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] Claude: {e}")
    return None


def extract_company_from_email(email: str) -> str:
    """Extract company from email domain."""
    if not email:
        return None
    domain = email.split("@")[-1].lower()
    free_providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"]
    if domain in free_providers:
        return None
    return domain.split(".")[0].title()


def research_prospect(name: str, email: str, company: str = None) -> dict:
    """Research prospect and company."""
    results = {
        "prospect_name": name,
        "prospect_email": email,
        "company": company or extract_company_from_email(email),
        "company_research": None,
        "prospect_research": None,
        "talking_points": None,
        "summary": None
    }
    
    company = results["company"]
    print(f"[INFO] Researching: {name} at {company or 'Unknown'}")
    
    # Company research
    if company:
        results["company_research"] = research_with_perplexity(
            f'Research "{company}". Provide: what they do, company size, target market, recent news.'
        )
    
    # Prospect research
    results["prospect_research"] = research_with_perplexity(
        f'Research "{name}" at "{company or "their company"}". Find: role, background, expertise.'
    )
    
    # Generate talking points
    context = f"""
PROSPECT: {name}
COMPANY: {company or 'Unknown'}
EMAIL: {email}

COMPANY RESEARCH:
{results['company_research'] or 'N/A'}

PROSPECT RESEARCH:
{results['prospect_research'] or 'N/A'}
"""
    
    results["talking_points"] = research_with_claude(f"""Based on this research, generate:
{context}

1. **5 Personalized Talking Points** - Show I did my research
2. **3 Questions to Ask** - Thoughtful questions based on their background
3. **Potential Pain Points** - What challenges might they face
4. **Meeting Goals** - What to learn/achieve

Be specific and actionable.""")
    
    # Summary
    results["summary"] = research_with_claude(f"""Create a 3-4 sentence executive summary:
{context}

Include: who they are, what their company does, why they might be booking, one key thing to remember.""")
    
    return results

# =============================================================================
# Routes
# =============================================================================

@app.route("/")
def dashboard():
    """Render the monitoring dashboard."""
    with events_lock:
        events = list(events_log)
    
    stats = {
        "total": len(events),
        "success": sum(1 for e in events if e["status"] == "success"),
        "duplicates": sum(1 for e in events if e["status"] == "duplicate"),
        "errors": sum(1 for e in events if e["status"] == "error")
    }
    
    return render_template_string(DASHBOARD_HTML, events=events, stats=stats)


@app.route("/api/events")
def api_events():
    """Get events as JSON."""
    with events_lock:
        return jsonify(list(events_log))


@app.route("/webhook/calendly", methods=["POST"])
def calendly_webhook():
    """Handle Calendly webhook."""
    payload = request.get_json()
    
    if not payload:
        log_event("webhook", "error", {"message": "No payload received"})
        return jsonify({"error": "No payload"}), 400
    
    event_type = payload.get("event")
    if event_type != "invitee.created":
        log_event("webhook", "ignored", {"message": f"Event type: {event_type}"})
        return jsonify({"status": "ignored", "reason": f"Event {event_type} not handled"}), 200
    
    invitee_data = payload.get("payload", {})
    
    # Deduplication - use file-based storage
    email = invitee_data.get("email", "")
    scheduled_event = invitee_data.get("scheduled_event", {})
    
    # scheduled_event can be a dict (embedded) or a string (URI)
    if isinstance(scheduled_event, dict):
        event_uri = scheduled_event.get("uri", "")
    else:
        event_uri = scheduled_event
    
    dedup_key = hashlib.md5(f"{email}:{event_uri}".encode()).hexdigest()
    
    # Check file-based dedup
    processed = load_processed_webhooks()
    if dedup_key in processed:
        log_event("meeting_booked", "duplicate", {"name": invitee_data.get("name"), "email": email})
        print(f"[INFO] Duplicate skipped: {email}")
        return jsonify({"status": "duplicate"}), 200
    
    # Save immediately before any processing
    save_processed_webhook(dedup_key)
    
    # Extract data
    name = invitee_data.get("name", "Unknown")
    
    # Get event details - either from embedded data or API
    if isinstance(scheduled_event, dict):
        event_details = scheduled_event
    else:
        event_details = fetch_calendly_event_details(scheduled_event) if scheduled_event else {}
    
    event_name = event_details.get("name", "Meeting")
    start_time = event_details.get("start_time", "")
    
    # Format time
    if start_time:
        try:
            dt = datetime.fromisoformat(start_time.replace("Z", "+00:00").split(".")[0] + "+00:00")
            start_time = dt.strftime("%B %d, %Y at %I:%M %p UTC")
        except:
            start_time = start_time.replace("T", " ").replace("Z", " UTC")
    else:
        start_time = "See calendar"
    
    # Extract company
    company = None
    for qa in invitee_data.get("questions_and_answers", []):
        if "company" in qa.get("question", "").lower():
            company = qa.get("answer")
            break
    if not company:
        company = extract_company_from_email(email)
    
    # Log event
    log_event("meeting_booked", "processing", {"name": name, "email": email, "company": company})
    
    # Send initial alert
    send_meeting_alert(name, email, event_name, start_time, company)
    
    # Research
    try:
        research = research_prospect(name, email, company)
        
        # Create Google Doc
        doc_url = create_google_doc(research)
        
        # Send to Slack with doc link
        send_research_to_slack(research, doc_url)
        
        log_event("meeting_booked", "success", {"name": name, "company": company, "doc_url": doc_url})
        print(f"[INFO] Complete: {name} - Doc: {doc_url}")
        return jsonify({"status": "success", "prospect": name, "doc_url": doc_url}), 200
    except Exception as e:
        log_event("meeting_booked", "error", {"name": name, "error": str(e)})
        print(f"[ERROR] {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "aiaa-webhooks",
        "timestamp": datetime.now().isoformat()
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"Starting AIAA Webhooks on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
