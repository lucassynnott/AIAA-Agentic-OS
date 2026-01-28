#!/usr/bin/env python3
"""
Google Doc Creator

Creates formatted Google Docs from Markdown content.
Supports both OAuth (token.pickle) and service account authentication.
Follows directive: directives/google_doc_creator.md
"""

import argparse
import json
import os
import pickle
from pathlib import Path

try:
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: Google API libraries not installed")
    print("   Install with: pip install google-api-python-client google-auth google-auth-oauthlib")
    exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]


def markdown_to_google_doc_requests(markdown_content: str) -> tuple:
    """
    Convert markdown to Google Docs API requests with proper formatting.
    Returns (plain_text, formatting_requests) tuple.
    
    We insert all text first, then apply formatting in a second batch.
    """
    import re
    
    formatting_requests = []
    lines = markdown_content.split('\n')
    
    # First pass: build clean text and track formatting positions
    clean_lines = []
    line_metadata = []  # (start_index, length, header_level, bold_ranges, italic_ranges)
    
    current_index = 1  # Google Docs starts at index 1
    
    for line in lines:
        # Determine header level
        header_level = 0
        if line.startswith('######'):
            header_level = 6
            line = line[6:].strip()
        elif line.startswith('#####'):
            header_level = 5
            line = line[5:].strip()
        elif line.startswith('####'):
            header_level = 4
            line = line[4:].strip()
        elif line.startswith('###'):
            header_level = 3
            line = line[3:].strip()
        elif line.startswith('##'):
            header_level = 2
            line = line[2:].strip()
        elif line.startswith('#'):
            header_level = 1
            line = line[1:].strip()
        
        # Handle horizontal rules
        if line.strip() in ['---', '***', '___']:
            line = '─' * 50
        
        # Process inline formatting
        clean_line = line
        bold_ranges = []
        italic_ranges = []
        
        # Find and process bold text (**text**)
        offset = 0
        for match in re.finditer(r'\*\*(.+?)\*\*', line):
            text = match.group(1)
            start_in_clean = match.start() - offset
            end_in_clean = start_in_clean + len(text)
            bold_ranges.append((start_in_clean, end_in_clean))
            offset += 4
        clean_line = re.sub(r'\*\*(.+?)\*\*', r'\1', clean_line)
        
        # Handle bullet points
        if clean_line.startswith('- '):
            clean_line = '• ' + clean_line[2:]
        elif clean_line.startswith('* ') and not clean_line.startswith('**'):
            clean_line = '• ' + clean_line[2:]
        
        # Store metadata for this line
        line_text = clean_line + '\n'
        line_metadata.append({
            'start': current_index,
            'length': len(clean_line),
            'header_level': header_level,
            'bold_ranges': bold_ranges,
            'italic_ranges': italic_ranges
        })
        clean_lines.append(line_text)
        current_index += len(line_text)
    
    # Combine all clean text
    full_text = ''.join(clean_lines)
    
    # Build formatting requests based on metadata
    heading_style_map = {
        1: "HEADING_1",
        2: "HEADING_2", 
        3: "HEADING_3",
        4: "HEADING_4",
        5: "HEADING_5",
        6: "HEADING_6"
    }
    
    for meta in line_metadata:
        # Header formatting
        if meta['header_level'] > 0 and meta['length'] > 0:
            formatting_requests.append({
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": meta['start'],
                        "endIndex": meta['start'] + meta['length']
                    },
                    "paragraphStyle": {
                        "namedStyleType": heading_style_map.get(meta['header_level'], "HEADING_3")
                    },
                    "fields": "namedStyleType"
                }
            })
        
        # Bold formatting
        for start, end in meta['bold_ranges']:
            if end > start:
                formatting_requests.append({
                    "updateTextStyle": {
                        "range": {
                            "startIndex": meta['start'] + start,
                            "endIndex": meta['start'] + end
                        },
                        "textStyle": {"bold": True},
                        "fields": "bold"
                    }
                })
        
        # Italic formatting
        for start, end in meta['italic_ranges']:
            if end > start:
                formatting_requests.append({
                    "updateTextStyle": {
                        "range": {
                            "startIndex": meta['start'] + start,
                            "endIndex": meta['start'] + end
                        },
                        "textStyle": {"italic": True},
                        "fields": "italic"
                    }
                })
    
    return full_text, formatting_requests


def get_credentials():
    """Get Google credentials - tries OAuth first, then service account."""
    project_root = Path(__file__).parent.parent
    
    # Try OAuth token first (token.pickle)
    token_path = project_root / "token.pickle"
    client_secrets_path = project_root / "client_secrets.json"
    
    if token_path.exists():
        print("   Using OAuth credentials (token.pickle)")
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
        
        # Refresh if expired
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(token_path, "wb") as token:
                    pickle.dump(creds, token)
            except Exception as e:
                print(f"   Token refresh failed: {e}")
                creds = None
        
        if creds and creds.valid:
            return creds
    
    # Try to create new OAuth token if client_secrets exists
    if client_secrets_path.exists() and not token_path.exists():
        print("   Creating new OAuth token...")
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets_path), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)
        return creds
    
    # Fall back to service account
    service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if service_account_path and os.path.exists(service_account_path):
        print("   Using service account credentials")
        return service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=SCOPES
        )
    
    return None


def create_google_doc(title: str, content: str, folder_id: str = None) -> dict:
    """Create Google Doc with content"""
    print(f"📄 Creating Google Doc: {title}")

    creds = get_credentials()
    
    if not creds:
        print(f"⚠️  No Google credentials found")
        print("   Skipping Google Doc creation (saving locally only)")
        return {
            "documentId": None,
            "documentUrl": None,
            "title": title,
            "status": "local_only"
        }

    try:

        # Create doc
        docs_service = build("docs", "v1", credentials=creds)

        doc = docs_service.documents().create(body={"title": title}).execute()
        doc_id = doc.get("documentId")

        print(f"✅ Created document: {doc_id}")

        # Convert markdown to plain text and formatting requests
        plain_text, formatting_requests = markdown_to_google_doc_requests(content)
        
        # Step 1: Insert all text first
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
        
        # Step 2: Apply formatting
        if formatting_requests:
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": formatting_requests}
            ).execute()
            print(f"   Applied {len(formatting_requests)} formatting rules")

        # Move to folder if specified
        if folder_id:
            drive_service = build("drive", "v3", credentials=creds)
            drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                fields="id, parents"
            ).execute()

        # Get shareable URL
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

        return {
            "documentId": doc_id,
            "documentUrl": doc_url,
            "title": title,
            "status": "created"
        }

    except Exception as e:
        print(f"⚠️  Error creating Google Doc: {e}")
        return {
            "documentId": None,
            "documentUrl": None,
            "title": title,
            "status": "error",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Create Google Doc from markdown")
    parser.add_argument("--content", required=True, help="Path to markdown file")
    parser.add_argument("--title", required=True, help="Document title")
    parser.add_argument("--folder-id", help="Google Drive folder ID (optional)")
    parser.add_argument("--output-json", help="Save doc metadata as JSON")

    args = parser.parse_args()

    print("🚀 Starting Google Doc creation...")

    # Read content
    with open(args.content, "r") as f:
        content = f.read()

    # Create doc
    result = create_google_doc(args.title, content, args.folder_id)

    # Save metadata
    if args.output_json:
        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, "w") as f:
            json.dump(result, f, indent=2)

    print(f"\n✅ Google Doc creation complete!")
    if result["documentUrl"]:
        print(f"   URL: {result['documentUrl']}")
    else:
        print(f"   Status: {result['status']}")

    return 0


if __name__ == "__main__":
    exit(main())
