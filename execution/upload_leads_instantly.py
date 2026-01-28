#!/usr/bin/env python3
"""
Instantly Lead Uploader

Uploads leads to an Instantly campaign with proper variable formatting.

IMPORTANT API v2 Notes:
- Use 'campaign' field (NOT 'campaign_id') when adding leads
- Use 'personalization' field for {{personalization}} variable
- Custom variables go in 'custom_variables' object
- Use PATCH to update existing leads (personalization won't update on POST)
- Delete leads before re-uploading if you need to update personalization

Usage:
    python3 execution/upload_leads_instantly.py \
        --input leads.json \
        --campaign_id "your-campaign-id" \
        --api_key "your-api-key"
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

INSTANTLY_API_BASE = "https://api.instantly.ai/api/v2"


def get_api_headers(api_key: str) -> dict:
    """Get headers for Instantly API v2."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def load_leads(path: str) -> list:
    """Load leads from JSON file."""
    with open(path) as f:
        data = json.load(f)
        if isinstance(data, list):
            return data
        return data.get("leads", data.get("data", []))


def delete_existing_leads(api_key: str, campaign_id: str, emails: set) -> int:
    """Delete existing leads from account that match given emails."""
    headers = get_api_headers(api_key)
    deleted = 0

    # Paginate through all leads
    for page in range(20):
        resp = requests.post(
            f"{INSTANTLY_API_BASE}/leads/list",
            headers=headers,
            json={"limit": 100}
        )
        if resp.status_code != 200:
            break

        items = resp.json().get("items", [])
        if not items:
            break

        for lead in items:
            email = lead.get("email", "").lower()
            if email in emails:
                del_resp = requests.delete(
                    f"{INSTANTLY_API_BASE}/leads/{lead['id']}",
                    headers=headers
                )
                if del_resp.status_code in [200, 204]:
                    deleted += 1
                time.sleep(0.05)

        if len(items) < 100:
            break

    return deleted


def upload_lead(api_key: str, campaign_id: str, lead: dict) -> dict:
    """
    Upload a single lead to Instantly campaign.

    Returns dict with success status and lead ID or error.
    """
    headers = get_api_headers(api_key)

    email = lead.get("email")
    if not email:
        return {"success": False, "error": "No email provided"}

    first_name = lead.get("first_name", "")
    last_name = lead.get("last_name", "")
    company = lead.get("company_name", "")

    # Get personalization - check multiple possible field names
    personalization = (
        lead.get("personalized_first_line") or
        lead.get("personalization") or
        lead.get("icebreaker") or
        ""
    )

    # Build payload with correct field names for Instantly API v2
    payload = {
        "campaign": campaign_id,  # IMPORTANT: Use 'campaign' not 'campaign_id'
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "company_name": company,
        "personalization": personalization,  # For {{personalization}} variable
        "custom_variables": {
            "icebreaker": personalization,    # For {{icebreaker}} variable
            "companyName": company,           # For {{companyName}} variable
            "firstName": first_name,          # Backup for {{firstName}}
        }
    }

    # Add optional fields if present
    if lead.get("website"):
        payload["website"] = lead["website"]
    if lead.get("phone") or lead.get("mobile_number"):
        payload["phone"] = lead.get("phone") or lead.get("mobile_number")
    if lead.get("linkedin"):
        payload["custom_variables"]["linkedin"] = lead["linkedin"]

    try:
        resp = requests.post(
            f"{INSTANTLY_API_BASE}/leads",
            headers=headers,
            json=payload,
            timeout=30
        )

        if resp.status_code in [200, 201]:
            data = resp.json()
            return {
                "success": True,
                "id": data.get("id"),
                "personalization_set": bool(data.get("personalization"))
            }
        else:
            return {
                "success": False,
                "error": f"API error {resp.status_code}: {resp.text[:200]}"
            }

    except Exception as e:
        return {"success": False, "error": str(e)}


def update_lead_personalization(api_key: str, lead_id: str, personalization: str) -> bool:
    """Update an existing lead's personalization field via PATCH."""
    headers = get_api_headers(api_key)

    try:
        resp = requests.patch(
            f"{INSTANTLY_API_BASE}/leads/{lead_id}",
            headers=headers,
            json={"personalization": personalization}
        )
        return resp.status_code == 200
    except:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Upload leads to Instantly campaign with proper variable formatting"
    )
    parser.add_argument("--input", "-i", required=True, help="Input leads JSON file")
    parser.add_argument("--campaign_id", "-c", required=True, help="Instantly campaign ID")
    parser.add_argument("--api_key", "-k", help="Instantly API key (or use INSTANTLY_API_KEY env var)")
    parser.add_argument("--clean", action="store_true", help="Delete existing matching leads before upload")
    parser.add_argument("--update_only", action="store_true", help="Only update personalization for existing leads")

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("Error: INSTANTLY_API_KEY required (via --api_key or .env)")
        sys.exit(1)

    # Load leads
    leads = load_leads(args.input)
    print(f"Loaded {len(leads)} leads from {args.input}")

    # Clean existing leads if requested
    if args.clean:
        emails = set(lead.get("email", "").lower() for lead in leads if lead.get("email"))
        print(f"\nCleaning {len(emails)} existing leads...")
        deleted = delete_existing_leads(api_key, args.campaign_id, emails)
        print(f"Deleted {deleted} existing leads")

    # Upload leads
    print(f"\nUploading {len(leads)} leads to campaign {args.campaign_id}...")
    print()

    success_count = 0
    error_count = 0
    personalization_set = 0

    for i, lead in enumerate(leads, 1):
        email = lead.get("email")
        if not email:
            print(f"[{i}] Skipping - no email")
            continue

        name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
        company = lead.get("company_name", "")

        result = upload_lead(api_key, args.campaign_id, lead)

        if result["success"]:
            success_count += 1
            if result.get("personalization_set"):
                personalization_set += 1
                print(f"[{i}] + {name} @ {company}")
            else:
                print(f"[{i}] + {name} @ {company} (no personalization)")
        else:
            error_count += 1
            print(f"[{i}] x {name}: {result['error'][:50]}")

        time.sleep(0.3)  # Rate limiting

    # If personalization wasn't set on upload, try PATCH
    if success_count > 0 and personalization_set == 0:
        print("\nPersonalization not set on upload. Updating via PATCH...")
        headers = get_api_headers(api_key)

        # Get leads in campaign
        resp = requests.post(
            f"{INSTANTLY_API_BASE}/leads/list",
            headers=headers,
            json={"campaign": args.campaign_id, "limit": 100}
        )
        campaign_leads = resp.json().get("items", [])

        # Create email to personalization lookup
        email_to_pers = {}
        for lead in leads:
            email = lead.get("email", "").lower()
            pers = (
                lead.get("personalized_first_line") or
                lead.get("personalization") or
                lead.get("icebreaker") or
                ""
            )
            if email and pers:
                email_to_pers[email] = pers

        # Update each lead
        updated = 0
        for lead in campaign_leads:
            email = lead.get("email", "").lower()
            if email in email_to_pers and not lead.get("personalization"):
                if update_lead_personalization(api_key, lead["id"], email_to_pers[email]):
                    updated += 1
                time.sleep(0.2)

        print(f"Updated personalization for {updated} leads")
        personalization_set = updated

    # Summary
    print(f"\n{'='*50}")
    print("UPLOAD COMPLETE")
    print(f"{'='*50}")
    print(f"Total leads: {len(leads)}")
    print(f"Uploaded: {success_count}")
    print(f"With personalization: {personalization_set}")
    print(f"Errors: {error_count}")

    # Output JSON summary
    output = {
        "status": "success" if error_count == 0 else "partial",
        "campaign_id": args.campaign_id,
        "leads_uploaded": success_count,
        "personalization_set": personalization_set,
        "errors": error_count
    }

    print(f"\n{json.dumps(output, indent=2)}")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
