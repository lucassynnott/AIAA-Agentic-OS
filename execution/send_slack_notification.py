#!/usr/bin/env python3
"""
Slack Notifier

Sends completion notifications to Slack.
Follows directive: directives/slack_notifier.md
"""

import argparse
import json
import os
from datetime import datetime

try:
    import requests
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: requests library not installed")
    exit(1)


def send_slack_notification(workflow_name: str, status: str, deliverables: list, metadata: dict, company: str = None) -> dict:
    """Send formatted Slack notification"""

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        print("⚠️  SLACK_WEBHOOK_URL not configured")
        print("   Skipping Slack notification")
        return {"sent": False, "reason": "No webhook URL"}

    # Status emoji
    status_emoji = {
        "success": "✅",
        "failed": "❌",
        "partial": "⚠️"
    }.get(status, "ℹ️")

    # Build message
    company_text = f": {company}" if company else ""
    header = f"{status_emoji} {workflow_name}{company_text}"

    # Deliverables section
    deliverables_text = "\n".join([
        f"• {d.get('name', 'Deliverable')}: <{d.get('url', '#')}|View>"
        if d.get('url') else f"• {d.get('name', 'Deliverable')}: Local file"
        for d in deliverables
    ])

    # Metadata section
    metadata_text = "\n".join([
        f"*{key.replace('_', ' ').title()}:* {value}"
        for key, value in metadata.items()
    ])

    # Compose message
    message = {
        "text": header,
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": header
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Deliverables:*\n{deliverables_text}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": metadata_text
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
        print("📢 Sending Slack notification...")
        response = requests.post(webhook_url, json=message)

        if response.status_code == 200:
            print("✅ Slack notification sent!")
            return {
                "sent": True,
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }
        else:
            print(f"⚠️  Slack notification failed: {response.status_code}")
            return {
                "sent": False,
                "status_code": response.status_code,
                "error": response.text
            }

    except Exception as e:
        print(f"⚠️  Error sending Slack notification: {e}")
        return {
            "sent": False,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Send Slack notification")
    parser.add_argument("--workflow", required=True, help="Workflow name")
    parser.add_argument("--status", required=True, choices=["success", "failed", "partial"], help="Status")
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--deliverables", help="Deliverables JSON (array of {name, url})")
    parser.add_argument("--metadata", help="Metadata JSON (key-value pairs)")

    args = parser.parse_args()

    # Parse JSON inputs
    deliverables = json.loads(args.deliverables) if args.deliverables else []
    metadata = json.loads(args.metadata) if args.metadata else {}

    # Send notification
    result = send_slack_notification(
        workflow_name=args.workflow,
        status=args.status,
        deliverables=deliverables,
        metadata=metadata,
        company=args.company
    )

    print(f"\n{'✅' if result.get('sent') else '⚠️'} Notification result: {json.dumps(result, indent=2)}")

    return 0 if result.get("sent") else 1


if __name__ == "__main__":
    exit(main())
