#!/usr/bin/env python3
"""
Google Doc Creator with Formatting

Standalone utility - can be called by ANY agentic workflow.
Creates Google Docs with proper formatting from Markdown.

Usage:
    python3 execution/create_google_doc_formatted.py \\
        --content path/to/file.md \\
        --title "Document Title" \\
        --folder-id "GOOGLE_DRIVE_FOLDER_ID"
"""

import argparse
import json
import os
import pickle
import re
from pathlib import Path
from typing import List, Dict, Any

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: Google API libraries not installed")
    exit(1)

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']


def get_credentials():
    """Get OAuth credentials"""
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("client_secrets.json"):
                return None
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", 'wb') as token:
            pickle.dump(creds, token)

    return creds


def parse_markdown_to_segments(markdown_text: str) -> List[Dict[str, Any]]:
    """
    Parse markdown into segments with formatting info.
    Returns list of: {text, type, formatting}
    """
    segments = []
    lines = markdown_text.split('\n')

    for line in lines:
        # Empty line
        if not line.strip():
            segments.append({'text': '\n', 'type': 'newline', 'formatting': {}})
            continue

        # Header
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            level = len(header_match.group(1))
            text = header_match.group(2).replace('**', '').replace('*', '')
            segments.append({
                'text': text + '\n',
                'type': 'header',
                'level': level,
                'formatting': {}
            })
            continue

        # Bullet point
        bullet_match = re.match(r'^[\-\*]\s+(.+)$', line)
        if bullet_match:
            text = bullet_match.group(1).replace('**', '').replace('*', '')
            segments.append({
                'text': text + '\n',
                'type': 'bullet',
                'formatting': {}
            })
            continue

        # Numbered list
        number_match = re.match(r'^\d+\.\s+(.+)$', line)
        if number_match:
            text = number_match.group(1).replace('**', '').replace('*', '')
            segments.append({
                'text': text + '\n',
                'type': 'numbered',
                'formatting': {}
            })
            continue

        # Regular text (check for bold)
        has_bold = '**' in line
        text = line.replace('**', '').replace('*', '').replace('__', '').replace('_', '')

        segments.append({
            'text': text + '\n',
            'type': 'text',
            'formatting': {'bold': has_bold}
        })

    return segments


def create_google_doc_from_segments(title: str, segments: List[Dict], folder_id: str, creds) -> dict:
    """Create Google Doc from parsed segments"""
    try:
        docs_service = build('docs', 'v1', credentials=creds)

        # Create doc
        doc = docs_service.documents().create(body={'title': title}).execute()
        doc_id = doc.get('documentId')
        print(f"✅ Created document: {doc_id}")

        # Build requests
        requests = []
        current_index = 1

        for segment in segments:
            text = segment['text']
            seg_type = segment['type']

            # Insert text
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': text
                }
            })

            text_start = current_index
            text_end = current_index + len(text)

            # Apply type-specific formatting
            if seg_type == 'header':
                level = segment.get('level', 1)
                requests.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': text_start, 'endIndex': text_end - 1},
                        'paragraphStyle': {'namedStyleType': f'HEADING_{min(level, 6)}'},
                        'fields': 'namedStyleType'
                    }
                })

            elif seg_type == 'bullet':
                requests.append({
                    'createParagraphBullets': {
                        'range': {'startIndex': text_start, 'endIndex': text_end},
                        'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                    }
                })

            elif seg_type == 'numbered':
                requests.append({
                    'createParagraphBullets': {
                        'range': {'startIndex': text_start, 'endIndex': text_end},
                        'bulletPreset': 'NUMBERED_DECIMAL_ALPHA_ROMAN'
                    }
                })

            elif seg_type == 'text' and segment['formatting'].get('bold'):
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': text_start, 'endIndex': text_end - 1},
                        'textStyle': {'bold': True},
                        'fields': 'bold'
                    }
                })

            current_index = text_end

        # Apply all requests in batches
        batch_size = 300
        for i in range(0, len(requests), batch_size):
            batch = requests[i:i + batch_size]
            docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': batch}).execute()

        print(f"✅ Applied {len(requests)} formatting operations")

        # Move to folder
        if folder_id:
            drive_service = build('drive', 'v3', credentials=creds)
            drive_service.files().update(fileId=doc_id, addParents=folder_id, fields='id, parents').execute()

        return {
            "documentId": doc_id,
            "documentUrl": f"https://docs.google.com/document/d/{doc_id}/edit",
            "title": title,
            "status": "created"
        }

    except Exception as e:
        print(f"⚠️  Error: {e}")
        return {"documentId": None, "documentUrl": None, "title": title, "status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", required=True, help="Markdown file path")
    parser.add_argument("--title", required=True, help="Document title")
    parser.add_argument("--folder-id", help="Google Drive folder ID")
    parser.add_argument("--output-json", help="Output JSON metadata file")

    args = parser.parse_args()

    print("🚀 Standalone Google Doc Creator")
    print(f"   Input: {args.content}")
    print(f"   Title: {args.title}")

    # Get credentials
    creds = get_credentials()
    if not creds:
        print("❌ Authentication failed")
        return 1

    # Read content
    with open(args.content, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Parse markdown
    print("📝 Parsing markdown...")
    segments = parse_markdown_to_segments(markdown_content)
    print(f"   Found {len(segments)} text segments")

    # Create formatted doc
    result = create_google_doc_from_segments(args.title, segments, args.folder_id, creds)

    # Save metadata
    if args.output_json:
        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, "w") as f:
            json.dump(result, f, indent=2)

    print(f"\n{'✅' if result['documentUrl'] else '❌'} Complete!")
    if result["documentUrl"]:
        print(f"   URL: {result['documentUrl']}")
        print(f"\n🔗 Open document: {result['documentUrl']}")
    else:
        print(f"   Status: {result.get('status', 'error')}")
        if 'error' in result:
            print(f"   Error: {result['error']}")

    return 0 if result["documentUrl"] else 1


if __name__ == "__main__":
    exit(main())
