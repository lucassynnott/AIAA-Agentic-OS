#!/usr/bin/env python3
"""
Formatted Google Doc Creator

Creates properly formatted Google Docs from markdown content using native
Google Docs API formatting (headings, bold, italic, bullets, links).

Usage:
    python3 execution/create_formatted_google_doc.py \
        --content "path/to/content.md" \
        --title "Document Title" \
        --folder-id "optional_folder_id"
        
    # Or programmatically:
    from create_formatted_google_doc import create_formatted_doc
    result = create_formatted_doc(title, markdown_content, folder_id)
"""

import argparse
import json
import os
import re
import pickle
import requests
from pathlib import Path
from typing import List, Dict, Tuple, Optional

try:
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Error: Google API libraries not installed")
    print("Install: pip install google-api-python-client google-auth google-auth-oauthlib")
    exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CONTENT_CHANNEL_ID = os.getenv("SLACK_CONTENT_CHANNEL_ID")


def strip_emojis(text: str) -> str:
    """Remove emojis and other special Unicode characters that cause position issues."""
    import regex
    # Remove emojis, symbols, and other non-standard characters
    # Keep basic ASCII, extended Latin, and common punctuation
    return regex.sub(r'[\U0001F000-\U0001FFFF]|[\U00002600-\U000027BF]|[\U0001F300-\U0001F9FF]', '', text)


def preprocess_markdown(markdown: str) -> str:
    """
    Preprocess markdown to handle special cases before parsing.
    - Strip emojis that cause UTF-16 position issues
    - Convert markdown tables to clean key-value format
    - Convert <br> tags to newlines
    """
    # Strip emojis first to avoid position calculation issues
    try:
        markdown = strip_emojis(markdown)
    except ImportError:
        # If regex module not available, do basic emoji removal
        pass
    
    # Process markdown tables FIRST - before <br> conversion breaks them
    lines = markdown.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Detect table start: | Header1 | Header2 |
        if re.match(r'^\s*\|.+\|.+\|\s*$', line):
            # Check if next line is separator |---|---|
            if i + 1 < len(lines) and re.match(r'^\s*\|[-:\s|]+\|\s*$', lines[i + 1]):
                # This is a markdown table - convert it
                table_lines = [line]
                i += 1  # Move past header
                table_lines.append(lines[i])  # Add separator
                i += 1
                
                # Collect all table rows
                while i < len(lines) and re.match(r'^\s*\|.+\|\s*$', lines[i]):
                    table_lines.append(lines[i])
                    i += 1
                
                # Convert table to clean format
                converted = convert_table_to_clean_format(table_lines)
                result_lines.extend(converted)
                continue
        
        result_lines.append(line)
        i += 1
    
    result = '\n'.join(result_lines)
    
    # NOW convert <br> tags to newlines (after tables are processed)
    result = re.sub(r'<br\s*/?>', '\n', result, flags=re.IGNORECASE)
    
    return result


def convert_table_to_clean_format(table_lines: List[str]) -> List[str]:
    """
    Convert markdown table to clean key-value format.
    Just plain text, no special formatting markers.
    
    Input:
    | Field | Value |
    |-------|-------|
    | **Name** | John |
    
    Output:
    Name: John
    """
    if len(table_lines) < 3:
        return table_lines
    
    result = []
    
    for row_line in table_lines[2:]:
        cells = [c.strip() for c in row_line.split('|') if c.strip()]
        
        if len(cells) >= 2:
            key = cells[0].strip('*').strip()  # Remove ** markers
            value = cells[1] if len(cells) > 1 else ''
            
            if value:
                result.append(f"{key}: {value}")
            else:
                result.append(key)
    
    return result


def parse_markdown_to_plain_text(markdown: str) -> Tuple[str, List[Dict]]:
    """
    Convert markdown to plain text with ONLY heading formatting.
    No bold, no special styling - just clean text with headings.
    """
    # Preprocess: convert tables to simple key: value format, handle <br> tags
    markdown = preprocess_markdown(markdown)
    
    lines = markdown.split('\n')
    result_lines = []
    formatting = []
    current_pos = 1  # Google Docs starts at index 1
    
    for line in lines:
        # Horizontal rule - just a simple line
        if line.strip() in ['---', '***', '___', '- - -', '* * *']:
            rule = '─' * 50
            result_lines.append(rule)
            current_pos += len(rule) + 1
            continue
        
        # Headers - apply heading style only
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
        
        # Bullet points - convert to bullet character
        bullet_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if bullet_match:
            content = bullet_match.group(2)
            clean_content = strip_markdown_inline(content)
            # Remove {{BOLD}} markers if present
            clean_content = clean_content.replace('{{BOLD}}', '').replace('{{/BOLD}}', '')
            bullet_line = '• ' + clean_content
            result_lines.append(bullet_line)
            current_pos += len(bullet_line) + 1
            continue
        
        # Regular line - strip all formatting markers, bold text before colon
        if line.strip():
            clean_line = strip_markdown_inline(line)
            clean_line = clean_line.replace('{{BOLD}}', '').replace('{{/BOLD}}', '')
            result_lines.append(clean_line)
            
            # Bold everything before the first colon (if there is one)
            if ':' in clean_line:
                colon_pos = clean_line.index(':')
                if colon_pos > 0:  # Only if there's text before the colon
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
    
    plain_text = '\n'.join(result_lines)
    return plain_text, formatting


def strip_markdown_inline(text: str) -> str:
    """Remove all inline markdown formatting, returning plain text."""
    # Remove links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove bold **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    # Remove italic *text* or _text_
    text = re.sub(r'(?<![*_])\*([^*]+)\*(?![*_])', r'\1', text)
    text = re.sub(r'(?<![*_])_([^_]+)_(?![*_])', r'\1', text)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text


def extract_inline_formatting(original_line: str, base_pos: int) -> List[Dict]:
    """
    Extract inline formatting (bold, italic, links, code) from original markdown line.
    Returns list of formatting requests with correct positions in the clean text.
    """
    formats = []
    
    # We need to track position in clean text as we find formatting
    # Strategy: walk through and find each format marker, calculate clean position
    
    # Find bold **text**
    clean_text = original_line
    for match in re.finditer(r'\*\*(.+?)\*\*', original_line):
        bold_content = match.group(1)
        # Find where this content appears in clean text
        clean_text_before = strip_markdown_inline(original_line[:match.start()])
        start_in_clean = len(clean_text_before)
        end_in_clean = start_in_clean + len(strip_markdown_inline(bold_content))
        
        formats.append({
            "updateTextStyle": {
                "range": {"startIndex": base_pos + start_in_clean, "endIndex": base_pos + end_in_clean},
                "textStyle": {"bold": True},
                "fields": "bold"
            }
        })
    
    # Find italic *text* (not **bold**)
    for match in re.finditer(r'(?<!\*)\*([^*]+)\*(?!\*)', original_line):
        italic_content = match.group(1)
        clean_text_before = strip_markdown_inline(original_line[:match.start()])
        start_in_clean = len(clean_text_before)
        end_in_clean = start_in_clean + len(strip_markdown_inline(italic_content))
        
        formats.append({
            "updateTextStyle": {
                "range": {"startIndex": base_pos + start_in_clean, "endIndex": base_pos + end_in_clean},
                "textStyle": {"italic": True},
                "fields": "italic"
            }
        })
    
    # Find links [text](url)
    for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', original_line):
        link_text = match.group(1)
        link_url = match.group(2)
        clean_text_before = strip_markdown_inline(original_line[:match.start()])
        start_in_clean = len(clean_text_before)
        end_in_clean = start_in_clean + len(link_text)
        
        formats.append({
            "updateTextStyle": {
                "range": {"startIndex": base_pos + start_in_clean, "endIndex": base_pos + end_in_clean},
                "textStyle": {
                    "link": {"url": link_url},
                    "foregroundColor": {"color": {"rgbColor": {"red": 0.06, "green": 0.46, "blue": 0.88}}}
                },
                "fields": "link,foregroundColor"
            }
        })
    
    # Find inline code `text`
    for match in re.finditer(r'`([^`]+)`', original_line):
        code_content = match.group(1)
        clean_text_before = strip_markdown_inline(original_line[:match.start()])
        start_in_clean = len(clean_text_before)
        end_in_clean = start_in_clean + len(code_content)
        
        formats.append({
            "updateTextStyle": {
                "range": {"startIndex": base_pos + start_in_clean, "endIndex": base_pos + end_in_clean},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Courier New"},
                    "backgroundColor": {"color": {"rgbColor": {"red": 0.95, "green": 0.95, "blue": 0.95}}}
                },
                "fields": "weightedFontFamily,backgroundColor"
            }
        })
    
    return formats


def get_credentials():
    """Get Google credentials."""
    project_root = Path(__file__).parent.parent
    
    # Try token_docs.json first
    token_docs_path = project_root / "token_docs.json"
    if token_docs_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_docs_path), SCOPES)
            if creds and creds.valid:
                return creds
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(token_docs_path, 'w') as f:
                    f.write(creds.to_json())
                return creds
        except Exception as e:
            print(f"   token_docs.json error: {e}")
    
    # Try token.pickle
    token_path = project_root / "token.pickle"
    if token_path.exists():
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
        if creds and creds.valid:
            return creds
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, "wb") as token:
                pickle.dump(creds, token)
            return creds
    
    # Try credentials.json for new OAuth flow
    creds_path = project_root / "credentials.json"
    if creds_path.exists():
        flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_docs_path, 'w') as f:
            f.write(creds.to_json())
        return creds
    
    # Service account fallback
    sa_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_path and os.path.exists(sa_path):
        return service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    
    return None


def create_formatted_doc(
    title: str,
    content: str,
    folder_id: str = None,
    notify_slack: bool = False
) -> Dict:
    """
    Create a Google Doc with proper formatting from markdown content.
    """
    print(f"📄 Creating formatted Google Doc: {title}")
    
    creds = get_credentials()
    if not creds:
        print("   ⚠️ No Google credentials found")
        return {"documentId": None, "documentUrl": None, "title": title, "status": "no_credentials"}
    
    try:
        docs_service = build("docs", "v1", credentials=creds)
        drive_service = build("drive", "v3", credentials=creds)
        
        # Create empty document
        doc = docs_service.documents().create(body={"title": title}).execute()
        doc_id = doc.get("documentId")
        print(f"   Created document: {doc_id}")
        
        # Parse markdown
        plain_text, formatting_requests = parse_markdown_to_plain_text(content)
        
        # Step 1: Insert all text
        if plain_text:
            insert_request = [{
                "insertText": {
                    "location": {"index": 1},
                    "text": plain_text
                }
            }]
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": insert_request}
            ).execute()
            print(f"   Inserted {len(plain_text)} characters")
        
        # Step 2: Apply formatting (filter invalid ranges)
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
            
            # Apply in batches
            if valid_requests:
                batch_size = 100
                for i in range(0, len(valid_requests), batch_size):
                    batch = valid_requests[i:i + batch_size]
                    try:
                        docs_service.documents().batchUpdate(
                            documentId=doc_id,
                            body={"requests": batch}
                        ).execute()
                    except Exception as e:
                        print(f"   ⚠️ Formatting error: {e}")
                print(f"   Applied {len(valid_requests)} formatting rules")
        
        # Move to folder if specified
        if folder_id:
            try:
                drive_service.files().update(
                    fileId=doc_id,
                    addParents=folder_id,
                    removeParents='root',
                    fields="id, parents"
                ).execute()
            except Exception as e:
                print(f"   ⚠️ Folder move error: {e}")
        
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
        
        if notify_slack:
            send_slack_notification(title, doc_url)
        
        print(f"   ✓ Document created: {doc_url}")
        
        return {
            "documentId": doc_id,
            "documentUrl": doc_url,
            "title": title,
            "status": "created"
        }
        
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
        return {
            "documentId": None,
            "documentUrl": None,
            "title": title,
            "status": "error",
            "error": str(e)
        }


def send_slack_notification(title: str, doc_url: str):
    """Send Slack notification."""
    if not SLACK_BOT_TOKEN or not SLACK_CONTENT_CHANNEL_ID:
        return
    
    try:
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"},
            json={
                "channel": SLACK_CONTENT_CHANNEL_ID,
                "text": f"Created: {title}",
                "blocks": [
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"📄 *{title}*\n<{doc_url}|Open in Google Docs>"}}
                ]
            },
            timeout=30
        )
        print("   ✓ Slack notification sent")
    except Exception as e:
        print(f"   ⚠️ Slack error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Create formatted Google Doc from markdown")
    parser.add_argument("--content", "-c", help="Path to markdown file or raw content")
    parser.add_argument("--title", "-t", help="Document title")
    parser.add_argument("--folder-id", "-f", help="Google Drive folder ID")
    parser.add_argument("--notify", "-n", action="store_true", help="Send Slack notification")
    parser.add_argument("--test", action="store_true", help="Create a test document")
    
    args = parser.parse_args()
    
    if args.test:
        test_content = """# Test Document

This tests the **Google Doc** formatter.

## Section One

Regular paragraph with **bold text** and *italic text*.

### Bullet Points

- First item
- Second item with **bold**
- Third item

---

## Links and Code

Check out [Google](https://google.com) for more info.

Here is `inline code` example.

## Conclusion

Document created successfully.
"""
        result = create_formatted_doc(
            title="Formatting Test - " + __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M"),
            content=test_content,
            notify_slack=True
        )
    else:
        if not args.content or not args.title:
            print("Error: --content and --title required")
            return 1
        
        if os.path.exists(args.content):
            with open(args.content, 'r') as f:
                content = f.read()
        else:
            content = args.content
        
        result = create_formatted_doc(
            title=args.title,
            content=content,
            folder_id=args.folder_id,
            notify_slack=args.notify
        )
    
    return 0 if result['status'] == 'created' else 1


if __name__ == "__main__":
    exit(main())
