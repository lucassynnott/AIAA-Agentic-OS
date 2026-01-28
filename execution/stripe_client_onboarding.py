#!/usr/bin/env python3
"""
Stripe Client Onboarding Automation

Triggered by Stripe webhook when subscription is paid:
1. Creates Slack channel and invites client
2. Sends welcome email via Gmail
3. Researches client company
4. Searches Fathom for past calls
5. Generates internal report
6. Creates Google Doc
7. Notifies #content-approval

Usage:
    python3 execution/stripe_client_onboarding.py \
        --client_name "Acme Store" \
        --client_email "john@acmestore.com" \
        --company_website "acmestore.com"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Configuration
# =============================================================================

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_WORKSPACE_ID = os.getenv("SLACK_WORKSPACE_ID", "T05D5C7RCTF")
SLACK_OWNER_USER_ID = os.getenv("SLACK_OWNER_USER_ID", "U05D1LH2JG6")
SLACK_CONTENT_CHANNEL_ID = os.getenv("SLACK_CONTENT_CHANNEL_ID")  # #content-approval

GMAIL_SENDER = os.getenv("GMAIL_SENDER", "stopmoclay@gmail.com")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "1Xhgr63LTNqRI8ofFaVE-_zXYJLgjbBiF")

FATHOM_API_KEY = os.getenv("FATHOM_API_KEY")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# =============================================================================
# Slack Functions
# =============================================================================

def slack_api(method: str, endpoint: str, data: dict = None) -> dict:
    """Make Slack API call."""
    url = f"https://slack.com/api/{endpoint}"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}
    
    if method == "GET":
        resp = requests.get(url, headers=headers, params=data, timeout=30)
    else:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
    
    return resp.json()


def invite_to_slack(email: str) -> dict:
    """Invite user to Slack workspace by email."""
    return slack_api("POST", "admin.users.invite", {
        "email": email,
        "team_id": SLACK_WORKSPACE_ID,
        "channel_ids": ""  # Will add to channel separately
    })


def create_private_channel(name: str) -> str:
    """Create private Slack channel, return channel ID."""
    # Sanitize channel name (lowercase, no spaces, max 80 chars)
    channel_name = name.lower().replace(" ", "-").replace("_", "-")[:80]
    
    result = slack_api("POST", "conversations.create", {
        "name": channel_name,
        "is_private": True
    })
    
    if result.get("ok"):
        return result["channel"]["id"]
    elif result.get("error") == "name_taken":
        # Channel exists, find it
        channels = slack_api("GET", "conversations.list", {"types": "private_channel"})
        for ch in channels.get("channels", []):
            if ch["name"] == channel_name:
                return ch["id"]
    return None


def invite_to_channel(channel_id: str, user_id: str) -> bool:
    """Invite user to channel."""
    result = slack_api("POST", "conversations.invite", {
        "channel": channel_id,
        "users": user_id
    })
    return result.get("ok", False)


def get_user_by_email(email: str) -> str:
    """Get Slack user ID by email."""
    result = slack_api("GET", "users.lookupByEmail", {"email": email})
    if result.get("ok"):
        return result["user"]["id"]
    return None


def post_message(channel_id: str, text: str, blocks: list = None) -> bool:
    """Post message to Slack channel."""
    data = {"channel": channel_id, "text": text}
    if blocks:
        data["blocks"] = blocks
    result = slack_api("POST", "chat.postMessage", data)
    return result.get("ok", False)


# =============================================================================
# Gmail Functions
# =============================================================================

def send_welcome_email(client_email: str, client_name: str) -> bool:
    """Send welcome email via Gmail API."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        import base64
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        
        creds = None
        if os.path.exists('token_gmail.json'):
            creds = Credentials.from_authorized_user_file('token_gmail.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token_gmail.json', 'w') as token:
                token.write(creds.to_json())
        
        service = build('gmail', 'v1', credentials=creds)
        
        # Create email
        first_name = client_name.split()[0] if client_name else "there"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
        .header {{ background: #1a1a2e; color: white; padding: 30px; text-align: center; }}
        .content {{ padding: 30px; }}
        .highlight {{ background: #f8f9fa; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0; }}
        .cta {{ background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; display: inline-block; border-radius: 5px; margin: 20px 0; }}
        .footer {{ background: #f1f1f1; padding: 20px; text-align: center; font-size: 12px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome to INOVATIV! 🚀</h1>
    </div>
    <div class="content">
        <p>Hey {first_name},</p>
        
        <p>Welcome aboard! We're thrilled to have you join INOVATIV.</p>
        
        <p>You've just made a decision that's going to transform how your e-commerce store converts and retains customers. No more leaving money on the table.</p>
        
        <div class="highlight">
            <strong>Here's what happens next:</strong>
            <ul>
                <li><strong>Within 24 hours:</strong> You'll receive a Slack invite to your private VIP channel where you'll have direct access to our team</li>
                <li><strong>Within 48 hours:</strong> We'll schedule your kickoff call to dive deep into your store, goals, and opportunities</li>
                <li><strong>Week 1:</strong> Full audit of your current funnel, email flows, and conversion paths</li>
            </ul>
        </div>
        
        <p><strong>What we're going to do together:</strong></p>
        <ul>
            <li>🎯 <strong>CRO:</strong> High-converting PDPs, landing pages, and funnel architecture</li>
            <li>📧 <strong>Email + SMS:</strong> Full lifecycle flows that drive repeat purchases (Klaviyo)</li>
            <li>🎨 <strong>Creative:</strong> Ad creatives, advertorials, and funnel assets that convert</li>
        </ul>
        
        <p>Remember: We guarantee a <strong>30% revenue increase</strong> or we work for free until we hit it. That's how confident we are in what we do.</p>
        
        <p>Got questions before our kickoff? Just reply to this email.</p>
        
        <p>Let's turn your store into a conversion machine.</p>
        
        <p>— The INOVATIV Team</p>
    </div>
    <div class="footer">
        <p>INOVATIV | E-commerce Growth Agency</p>
        <p>CRO + Email/SMS + Creative — All Working Together</p>
    </div>
</body>
</html>
"""
        
        message = MIMEMultipart('alternative')
        message['to'] = client_email
        message['from'] = GMAIL_SENDER
        message['subject'] = f"Welcome to INOVATIV, {first_name}! Here's what happens next 🚀"
        
        # Plain text version
        plain_text = f"""
Welcome to INOVATIV, {first_name}!

You've just made a decision that's going to transform how your e-commerce store converts and retains customers.

Here's what happens next:
- Within 24 hours: Slack invite to your private VIP channel
- Within 48 hours: Kickoff call scheduled
- Week 1: Full audit of your funnel, email flows, and conversion paths

We guarantee a 30% revenue increase or we work for free until we hit it.

Got questions? Just reply to this email.

— The INOVATIV Team
"""
        
        message.attach(MIMEText(plain_text, 'plain'))
        message.attach(MIMEText(html_content, 'html'))
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        
        return True
    except Exception as e:
        print(f"   ⚠️ Gmail error: {e}")
        return False


# =============================================================================
# Fathom Functions
# =============================================================================

def search_fathom_calls(email_domain: str) -> list:
    """Search Fathom for past calls with this client's domain."""
    if not FATHOM_API_KEY:
        return []
    
    try:
        url = "https://api.fathom.ai/external/v1/meetings"
        headers = {"X-Api-Key": FATHOM_API_KEY}
        params = {
            "calendar_invitees_domains[]": email_domain,
            "include_transcript": "true",
            "include_summary": "true",
            "include_action_items": "true"
        }
        
        resp = requests.get(url, headers=headers, params=params, timeout=60)
        if resp.ok:
            data = resp.json()
            return data.get("items", [])
    except Exception as e:
        print(f"   ⚠️ Fathom error: {e}")
    
    return []


def format_fathom_calls(calls: list) -> str:
    """Format Fathom calls for report."""
    if not calls:
        return "No prior calls found in Fathom."
    
    output = []
    for call in calls:
        title = call.get("meeting_title") or call.get("title", "Untitled")
        date = call.get("scheduled_start_time", "")[:10]
        url = call.get("url", "")
        summary = call.get("default_summary", {}).get("markdown_formatted", "No summary")
        
        # Get transcript highlights
        transcript = call.get("transcript", [])
        transcript_preview = ""
        if transcript:
            first_few = transcript[:5]
            transcript_preview = "\n".join([f"- {t.get('speaker', {}).get('display_name', 'Speaker')}: {t.get('text', '')}" for t in first_few])
        
        output.append(f"""
### {title} ({date})
**Link:** {url}

**Summary:**
{summary}

**Transcript Preview:**
{transcript_preview}
""")
    
    return "\n---\n".join(output)


# =============================================================================
# Research Functions
# =============================================================================

def run_market_research(company_name: str, website: str) -> str:
    """Run market research on client company using Perplexity API."""
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    
    if perplexity_key:
        try:
            # Use Perplexity for real web research
            resp = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {perplexity_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a business research analyst at an e-commerce growth agency. Provide detailed, factual research based on real information found online. Format with clear markdown headings."
                        },
                        {
                            "role": "user",
                            "content": f"""Research this company for client onboarding. Search their website and any online presence:

Company: {company_name}
Website: {website}

Provide a detailed research report with these sections:

## Company Overview
- What they do/sell
- Their target market/ideal customer
- Company history/founding (if available)

## Business Model
- Products/services offered
- Pricing (if visible)
- E-commerce platform (Shopify, WooCommerce, etc.)

## Online Presence
- Website quality assessment
- Social media presence
- Content/blog activity

## Market Position
- Key competitors
- Unique value proposition
- Market segment

## Opportunities for INOVATIV
Based on what you found, identify:
- CRO opportunities (conversion rate optimization)
- Email/SMS marketing opportunities
- Funnel and creative opportunities

## Key Contacts
- Founder/CEO name if available
- Any team members mentioned

Be specific and factual based on what you find online."""
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                },
                timeout=90
            )
            
            if resp.ok:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"   ⚠️ Perplexity error: {resp.status_code}")
        except Exception as e:
            print(f"   ⚠️ Perplexity research error: {e}")
    
    # Fallback to basic AI research
    return generate_basic_research(company_name, website)


def generate_basic_research(company_name: str, website: str) -> str:
    """Generate basic research using AI (fallback when Perplexity unavailable)."""
    try:
        from openai import OpenAI
        
        if OPENROUTER_API_KEY:
            client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")
            model = "anthropic/claude-sonnet-4"
        else:
            client = OpenAI(api_key=OPENAI_API_KEY)
            model = "gpt-4o"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a business research analyst. Provide a structured company research report with clear markdown headings."},
                {"role": "user", "content": f"""Create a research report template for this company:

Company: {company_name}
Website: {website}

Since you cannot browse the web, create a structured template with:

## Company Overview
[To be filled after manual review of {website}]

## Business Model
[Products/services, pricing, platform]

## Online Presence
[Website, social media, content]

## Market Position
[Competitors, value proposition]

## Opportunities for INOVATIV
- CRO opportunities
- Email/SMS opportunities  
- Funnel/creative opportunities

## Action Items
- [ ] Review website manually
- [ ] Check social media profiles
- [ ] Identify tech stack

Provide any information you DO know about this company or industry."""}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Research unavailable: {e}"


# =============================================================================
# Report Generation
# =============================================================================

def generate_internal_report(client_name: str, client_email: str, website: str, 
                             research: str, fathom_calls: str) -> str:
    """Generate internal client report."""
    try:
        from openai import OpenAI
        
        if OPENROUTER_API_KEY:
            client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")
            model = "anthropic/claude-sonnet-4"
        else:
            client = OpenAI(api_key=OPENAI_API_KEY)
            model = "gpt-4o"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": """You are an internal strategist at INOVATIV, an e-commerce growth agency.
Generate a concise internal client report to help the team prepare for this new client.
Focus on actionable insights and recommended approach."""},
                {"role": "user", "content": f"""Generate an internal client report:

CLIENT: {client_name}
EMAIL: {client_email}
WEBSITE: {website}

MARKET RESEARCH:
{research}

PAST CONVERSATIONS (Fathom):
{fathom_calls}

Create an internal report with:
1. Client Summary (who they are, what they do)
2. Key Insights (from research and past calls)
3. Identified Opportunities (CRO, email, creative)
4. Potential Challenges
5. Recommended Approach
6. Questions for Kickoff Call
7. Priority Actions for Week 1

Make it actionable for the team."""}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Report generation error: {e}"


# =============================================================================
# Google Docs (using centralized formatted doc creator)
# =============================================================================

def create_google_doc(title: str, content: str) -> str:
    """Create Google Doc with proper formatting and return URL."""
    try:
        # Import the centralized formatted doc creator
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from create_formatted_google_doc import create_formatted_doc
        
        result = create_formatted_doc(
            title=title,
            content=content,
            folder_id=GOOGLE_DRIVE_FOLDER_ID,
            notify_slack=False  # We handle our own notifications
        )
        
        return result.get("documentUrl")
    except ImportError:
        print("   ⚠️ Formatted doc creator not available, using basic method")
        # Fallback to basic method
        return _create_google_doc_basic(title, content)
    except Exception as e:
        print(f"   ⚠️ Google Docs error: {e}")
        return None


def _create_google_doc_basic(title: str, content: str) -> str:
    """Fallback basic Google Doc creation."""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        creds = Credentials.from_authorized_user_file('token_docs.json')
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        
        doc = docs_service.documents().create(body={"title": title}).execute()
        doc_id = doc['documentId']
        
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': [{'insertText': {'location': {'index': 1}, 'text': content}}]}
        ).execute()
        
        if GOOGLE_DRIVE_FOLDER_ID:
            drive_service.files().update(fileId=doc_id, addParents=GOOGLE_DRIVE_FOLDER_ID, fields='id').execute()
        
        return f"https://docs.google.com/document/d/{doc_id}"
    except Exception as e:
        print(f"   ⚠️ Basic doc creation error: {e}")
        return None


# =============================================================================
# Main Orchestration
# =============================================================================

def onboard_client(client_name: str, client_email: str, company_website: str = None):
    """Main onboarding orchestration."""
    
    print(f"\n🚀 INOVATIV Client Onboarding")
    print(f"   Client: {client_name}")
    print(f"   Email: {client_email}")
    print(f"   Website: {company_website or 'Not provided'}\n")
    
    # Extract domain from email if no website provided
    email_domain = client_email.split('@')[1] if '@' in client_email else None
    if not company_website and email_domain:
        company_website = email_domain
    
    results = {
        "client_name": client_name,
        "client_email": client_email,
        "company_website": company_website,
        "timestamp": datetime.now().isoformat()
    }
    
    # 1. Create Slack channel
    print("📱 Setting up Slack...")
    channel_name = f"{client_name} - VIP"
    channel_id = create_private_channel(channel_name)
    
    if channel_id:
        print(f"   ✓ Created channel: {channel_name}")
        results["slack_channel_id"] = channel_id
        
        # Add owner to channel
        invite_to_channel(channel_id, SLACK_OWNER_USER_ID)
        print(f"   ✓ Added you to channel")
        
        # Try to find and add client
        client_slack_id = get_user_by_email(client_email)
        if client_slack_id:
            invite_to_channel(channel_id, client_slack_id)
            print(f"   ✓ Added client to channel")
        else:
            # Invite to workspace
            invite_result = invite_to_slack(client_email)
            if invite_result.get("ok"):
                print(f"   ✓ Sent Slack invite to {client_email}")
            else:
                print(f"   ⚠️ Could not invite client: {invite_result.get('error', 'unknown')}")
        
        # Post welcome message
        welcome_msg = f"""👋 Welcome to your VIP channel, {client_name}!

This is your direct line to the INOVATIV team. We'll use this channel for:
• Project updates & progress
• Quick questions & feedback
• Sharing deliverables & assets
• Strategy discussions

We're excited to start transforming your e-commerce performance! 🚀

Your kickoff call will be scheduled within 48 hours."""
        
        post_message(channel_id, welcome_msg)
        print(f"   ✓ Posted welcome message")
    else:
        print(f"   ⚠️ Could not create Slack channel")
    
    # 2. Send welcome email
    print("\n📧 Sending welcome email...")
    if send_welcome_email(client_email, client_name):
        print(f"   ✓ Welcome email sent")
        results["welcome_email_sent"] = True
    else:
        print(f"   ⚠️ Welcome email failed")
        results["welcome_email_sent"] = False
    
    # 3. Search Fathom for past calls
    print("\n🎙️ Searching Fathom for past calls...")
    fathom_calls = []
    # Use company website domain for Fathom search (not email domain)
    fathom_search_domain = company_website.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0] if company_website else email_domain
    if fathom_search_domain:
        print(f"   Searching by domain: {fathom_search_domain}")
        fathom_calls = search_fathom_calls(fathom_search_domain)
        if fathom_calls:
            print(f"   ✓ Found {len(fathom_calls)} past call(s)")
        else:
            print(f"   ℹ️ No prior calls found")
    results["fathom_calls_found"] = len(fathom_calls)
    
    # 4. Run market research
    print("\n🔍 Running market research...")
    research = run_market_research(client_name, company_website)
    print(f"   ✓ Research complete")
    
    # 5. Generate internal report
    print("\n📝 Generating internal report...")
    fathom_formatted = format_fathom_calls(fathom_calls)
    internal_report = generate_internal_report(
        client_name, client_email, company_website,
        research, fathom_formatted
    )
    print(f"   ✓ Report generated")
    
    # 6. Create Google Doc
    print("\n📄 Creating Google Doc...")
    doc_title = f"Client Research - {client_name} - {datetime.now().strftime('%Y-%m-%d')}"
    full_doc_content = f"""# {doc_title}

## Client Information
- **Name:** {client_name}
- **Email:** {client_email}
- **Website:** {company_website}
- **Onboarded:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Market Research

{research}

---

## Past Conversations (Fathom)

{fathom_formatted}

---

## Internal Strategy Report

{internal_report}
"""
    
    doc_url = create_google_doc(doc_title, full_doc_content)
    if doc_url:
        print(f"   ✓ Doc created: {doc_url}")
        results["google_doc_url"] = doc_url
    else:
        print(f"   ⚠️ Could not create Google Doc")
    
    # 7. Notify #content-approval
    print("\n📢 Notifying #content-approval...")
    if SLACK_CONTENT_CHANNEL_ID:
        # Extract key points from internal report for clean Slack formatting
        report_lines = internal_report.split('\n')
        clean_summary = []
        for line in report_lines[:15]:  # First 15 lines
            # Skip markdown headers and empty lines for Slack
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('---') and not line.startswith('**Date'):
                # Convert markdown bold to Slack bold
                line = line.replace('**', '*')
                clean_summary.append(line)
        
        # Get Fathom call titles
        fathom_summary = ""
        if fathom_calls:
            call_titles = [f"• {c.get('meeting_title') or c.get('title', 'Call')} ({c.get('scheduled_start_time', '')[:10]})" for c in fathom_calls[:3]]
            fathom_summary = "\n".join(call_titles)
        
        # Build Slack blocks for better formatting
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🆕 New Client Onboarded: {client_name}", "emoji": True}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Email:*\n{client_email}"},
                    {"type": "mrkdwn", "text": f"*Website:*\n{company_website}"}
                ]
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Fathom Calls:*\n{len(fathom_calls)} found"},
                    {"type": "mrkdwn", "text": f"*VIP Channel:*\n#{channel_name.lower().replace(' ', '-')}"}
                ]
            }
        ]
        
        if fathom_summary:
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*📞 Past Conversations:*\n{fathom_summary}"}
            })
        
        if doc_url:
            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*📄 Research Doc:*\n<{doc_url}|View Full Report>"}
            })
        
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Quick Summary:*\n{chr(10).join(clean_summary[:5])}"}
        })
        
        fallback_msg = f"New Client: {client_name} | {client_email} | {company_website}"
        
        if post_message(SLACK_CONTENT_CHANNEL_ID, fallback_msg, blocks):
            print(f"   ✓ Posted to #content-approval")
        else:
            print(f"   ⚠️ Could not post to #content-approval")
    else:
        print(f"   ⚠️ SLACK_CONTENT_CHANNEL_ID not configured")
    
    # Save results
    results_path = Path(".tmp") / f"onboarding_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Onboarding complete!")
    print(f"   📄 Results saved to: {results_path}")
    
    return results


# =============================================================================
# Stripe Webhook Handler (for Modal deployment)
# =============================================================================

def handle_stripe_webhook(payload: dict, sig_header: str = None) -> dict:
    """Handle incoming Stripe webhook."""
    import stripe
    
    stripe.api_key = os.getenv("STRIPE_API_KEY")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    # Verify webhook signature if provided
    if sig_header and webhook_secret:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except Exception as e:
            return {"error": f"Webhook verification failed: {e}"}
    else:
        event = payload
    
    # Handle subscription events
    event_type = event.get("type", "")
    
    if event_type in ["customer.subscription.created", "invoice.payment_succeeded"]:
        data = event.get("data", {}).get("object", {})
        
        # Extract client info
        customer_email = data.get("customer_email") or data.get("email")
        customer_name = data.get("customer_name") or data.get("name") or "New Client"
        
        # Get customer details from Stripe if needed
        if not customer_email and data.get("customer"):
            try:
                customer = stripe.Customer.retrieve(data["customer"])
                customer_email = customer.email
                customer_name = customer.name or customer_email.split("@")[0]
            except:
                pass
        
        if customer_email:
            results = onboard_client(customer_name, customer_email)
            return {"success": True, "results": results}
        else:
            return {"error": "No customer email found in webhook"}
    
    return {"message": f"Event type {event_type} not handled"}


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="INOVATIV Client Onboarding")
    parser.add_argument("--client_name", "-n", required=True, help="Client name")
    parser.add_argument("--client_email", "-e", required=True, help="Client email")
    parser.add_argument("--company_website", "-w", default="", help="Company website")
    
    args = parser.parse_args()
    
    results = onboard_client(args.client_name, args.client_email, args.company_website)
    
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
