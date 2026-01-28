#!/usr/bin/env python3
"""
Google Doc Creator (OAuth)

Creates Google Docs using OAuth2 user authentication.
"""

import argparse
import json
import os
import pickle
from pathlib import Path

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: Google API libraries not installed")
    print("   Install: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    exit(1)

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]


def get_credentials():
    """Get OAuth credentials (prompts for login first time)"""
    creds = None
    token_file = "token.pickle"

    # Check if we have saved credentials
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing credentials...")
            creds.refresh(Request())
        else:
            # Need OAuth client credentials
            client_secrets = os.getenv("GOOGLE_CLIENT_SECRETS", "client_secrets.json")

            if not os.path.exists(client_secrets):
                print(f"❌ Error: OAuth client secrets not found: {client_secrets}")
                print("\nTo set up OAuth:")
                print("1. Go to: https://console.cloud.google.com/apis/credentials")
                print("2. Create OAuth 2.0 Client ID (Desktop app)")
                print("3. Download JSON and save as 'client_secrets.json'")
                return None

            print("🔐 First time setup - opening browser for Google login...")
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next time
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
        print("✅ Credentials saved")

    return creds


def create_google_doc_oauth(title: str, content: str, folder_id: str = None) -> dict:
    """Create Google Doc using OAuth"""
    print(f"📄 Creating Google Doc: {title}")

    creds = get_credentials()
    if not creds:
        return {"documentId": None, "documentUrl": None, "title": title, "status": "no_auth"}

    try:
        # Create doc
        docs_service = build('docs', 'v1', credentials=creds)
        doc = docs_service.documents().create(body={'title': title}).execute()
        doc_id = doc.get('documentId')

        print(f"✅ Created document: {doc_id}")

        # Insert content
        requests = [{
            'insertText': {
                'location': {'index': 1},
                'text': content
            }
        }]
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

        print("✅ Content inserted")

        # Move to folder if specified
        if folder_id:
            drive_service = build('drive', 'v3', credentials=creds)
            drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                fields='id, parents'
            ).execute()
            print(f"✅ Moved to folder")

        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

        return {
            "documentId": doc_id,
            "documentUrl": doc_url,
            "title": title,
            "status": "created"
        }

    except Exception as e:
        print(f"⚠️  Error: {e}")
        return {
            "documentId": None,
            "documentUrl": None,
            "title": title,
            "status": "error",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--folder-id", help="Google Drive folder ID")
    parser.add_argument("--output-json", help="Save doc metadata as JSON")

    args = parser.parse_args()

    with open(args.content, "r") as f:
        content = f.read()

    result = create_google_doc_oauth(args.title, content, args.folder_id)

    if args.output_json:
        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, "w") as f:
            json.dump(result, f, indent=2)

    print(f"\n✅ Complete!")
    if result["documentUrl"]:
        print(f"   URL: {result['documentUrl']}")
    else:
        print(f"   Status: {result['status']}")

    return 0 if result["documentUrl"] else 1


if __name__ == "__main__":
    exit(main())
