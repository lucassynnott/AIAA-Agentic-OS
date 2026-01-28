#!/usr/bin/env python3
"""
Google Doc Creator (Alternative - Uses Drive API)

Creates Google Docs using Drive API instead of Docs API.
"""

import argparse
import json
import os
from pathlib import Path

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: Google API libraries not installed")
    exit(1)


def create_google_doc_via_drive(title: str, content: str, folder_id: str = None) -> dict:
    """Create Google Doc using Drive API (alternative method)"""
    print(f"📄 Creating Google Doc via Drive API: {title}")

    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

    if not os.path.exists(creds_path):
        print(f"⚠️  Google credentials not found: {creds_path}")
        return {"documentId": None, "documentUrl": None, "title": title, "status": "no_credentials"}

    try:
        # Authenticate
        creds = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=[
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/drive.file"
            ]
        )

        drive_service = build("drive", "v3", credentials=creds)

        # Create file metadata
        file_metadata = {
            "name": title,
            "mimeType": "application/vnd.google-apps.document",
        }

        if folder_id:
            file_metadata["parents"] = [folder_id]

        # Create empty Google Doc first
        file = drive_service.files().create(
            body=file_metadata,
            fields="id, webViewLink"
        ).execute()

        doc_id = file.get("id")
        doc_url = file.get("webViewLink")

        print(f"✅ Created document: {doc_id}")

        # Now update with content using Docs API
        try:
            docs_service = build("docs", "v1", credentials=creds)
            requests = [{
                "insertText": {
                    "location": {"index": 1},
                    "text": content
                }
            }]
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests}
            ).execute()
            print("✅ Content inserted")
        except Exception as e:
            print(f"⚠️  Could not insert content (doc created but empty): {e}")

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

    result = create_google_doc_via_drive(args.title, content, args.folder_id)

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
