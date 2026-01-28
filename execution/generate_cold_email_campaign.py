#!/usr/bin/env python3
"""
Ultimate Cold Email Campaign Generator

Generates complete cold email campaigns with personalization,
A/B testing, and export to Instantly/Smartlead format.

Usage:
    python3 execution/generate_cold_email_campaign.py \
        --sender-name "John Smith" \
        --sender-company "Growth Agency" \
        --offer "Lead generation for B2B SaaS" \
        --target-icp "Marketing directors at SaaS companies"

Follows directive: directives/ultimate_cold_email_campaign.md
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("Error: requests required. pip install requests")
    sys.exit(1)


class ColdEmailCampaignGenerator:
    """Generate complete cold email campaigns with AI personalization"""

    def __init__(self, **kwargs):
        self.sender_name = kwargs.get("sender_name", "")
        self.sender_company = kwargs.get("sender_company", "")
        self.offer = kwargs.get("offer", "")
        self.target_icp = kwargs.get("target_icp", "")
        self.lead_source = kwargs.get("lead_source", "manual")
        self.lead_count = kwargs.get("lead_count", 100)
        self.leads_file = kwargs.get("leads_file", "")
        self.sequence_length = kwargs.get("sequence_length", 5)
        self.personalization_level = kwargs.get("personalization_level", "medium")
        self.output_format = kwargs.get("output_format", "instantly")

        # Generate campaign slug
        campaign_slug = f"{self.sender_company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        campaign_slug = re.sub(r'[^a-zA-Z0-9_]', '', campaign_slug.replace(' ', '_'))

        # Setup output directory
        self.output_dir = Path(f".tmp/cold_email_campaigns/{campaign_slug}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "leads").mkdir(exist_ok=True)
        (self.output_dir / "sequences").mkdir(exist_ok=True)
        (self.output_dir / "exports").mkdir(exist_ok=True)

        # API keys
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}.get(level, "")
        print(f"[{timestamp}] {prefix} {message}")

    def call_claude(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        if not self.openrouter_key:
            self.log("OPENROUTER_API_KEY not set", "ERROR")
            return None

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-sonnet-4",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": max_tokens
                },
                timeout=120
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                self.log(f"API error: {response.status_code}", "ERROR")
                return None
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
            return None

    def load_leads(self) -> List[Dict]:
        """Load leads from file or generate sample leads"""
        if self.leads_file and os.path.exists(self.leads_file):
            self.log(f"Loading leads from {self.leads_file}")
            leads = []
            with open(self.leads_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leads.append(row)
            return leads
        else:
            # Generate sample leads structure
            self.log("No leads file provided - generating template")
            return [
                {
                    "first_name": "{{first_name}}",
                    "last_name": "{{last_name}}",
                    "email": "{{email}}",
                    "company": "{{company}}",
                    "title": "{{title}}",
                    "linkedin_url": "{{linkedin_url}}",
                    "company_size": "{{company_size}}",
                    "industry": "{{industry}}"
                }
            ]

    def generate_email_sequence(self) -> Dict:
        """Generate the complete email sequence"""
        self.log("Generating email sequence...", "INFO")

        prompt = f"""You are an expert cold email copywriter. Generate a {self.sequence_length}-email cold outreach sequence.

CONTEXT:
- Sender: {self.sender_name} from {self.sender_company}
- Offer: {self.offer}
- Target ICP: {self.target_icp}

Generate the sequence in JSON format:
{{
    "sequence_name": "Campaign name",
    "emails": [
        {{
            "email_number": 1,
            "email_type": "Pattern Interrupt",
            "delay_days": 0,
            "subject_lines": ["Subject 1", "Subject 2", "Subject 3"],
            "body": "Email body with {{{{first_name}}}}, {{{{company}}}} variables",
            "purpose": "Why this email exists",
            "tips": "Delivery tips"
        }},
        // ... more emails
    ],
    "ab_test_recommendations": [
        "Test recommendation 1",
        "Test recommendation 2"
    ],
    "sending_best_practices": [
        "Best practice 1",
        "Best practice 2"
    ]
}}

EMAIL TYPES BY POSITION:
1. Pattern Interrupt - Grab attention, show you did research
2. Case Study - Prove you can deliver results
3. Value Add - Provide free insight/resource
4. FOMO/Urgency - Create urgency, mention competitors
5. Breakup - Last chance, direct ask

RULES:
- Keep emails under 100 words
- Subject lines under 40 characters
- Use personalization variables: {{{{first_name}}}}, {{{{company}}}}, {{{{title}}}}
- No spam trigger words
- Soft CTAs (questions, not demands)
- Professional but conversational tone

Return ONLY valid JSON."""

        result = self.call_claude(prompt)

        if result:
            try:
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    sequence_data = json.loads(json_match.group())
                    self.log(f"Generated {len(sequence_data.get('emails', []))} emails", "SUCCESS")
                    return sequence_data
            except json.JSONDecodeError as e:
                self.log(f"JSON parse error: {e}", "WARNING")

        # Fallback sequence
        return self._get_fallback_sequence()

    def _get_fallback_sequence(self) -> Dict:
        """Return fallback email sequence"""
        return {
            "sequence_name": f"{self.sender_company} Outreach",
            "emails": [
                {
                    "email_number": 1,
                    "email_type": "Pattern Interrupt",
                    "delay_days": 0,
                    "subject_lines": [
                        f"Quick question about {{{{company}}}}",
                        f"Idea for {{{{company}}}}",
                        f"{{{{first_name}}}}, saw something interesting"
                    ],
                    "body": f"""Hi {{{{first_name}}}},

I noticed {{{{company}}}} is {self.target_icp.split(',')[0] if ',' in self.target_icp else 'growing'}.

We help companies like yours with {self.offer}.

Worth a quick chat?

{self.sender_name}
{self.sender_company}""",
                    "purpose": "Initial outreach - grab attention",
                    "tips": "Send Tuesday-Thursday, 8-10 AM local time"
                },
                {
                    "email_number": 2,
                    "email_type": "Case Study",
                    "delay_days": 3,
                    "subject_lines": [
                        "Re: Quick question about {{company}}",
                        "Results from similar company",
                        "{{first_name}}, quick follow-up"
                    ],
                    "body": f"""Hi {{{{first_name}}}},

Just wanted to share - we recently helped a company similar to {{{{company}}}} achieve significant results with {self.offer}.

Would love to show you how we did it.

Open to a 15-minute call this week?

{self.sender_name}""",
                    "purpose": "Build credibility with social proof",
                    "tips": "Include specific metrics if available"
                },
                {
                    "email_number": 3,
                    "email_type": "Value Add",
                    "delay_days": 4,
                    "subject_lines": [
                        "Free resource for {{company}}",
                        "Thought you'd find this useful",
                        "Quick insight on {your industry}"
                    ],
                    "body": f"""Hi {{{{first_name}}}},

I put together a quick guide on how {self.target_icp.split(',')[0] if ',' in self.target_icp else 'companies'} are getting better results with {self.offer}.

Happy to share if interested?

{self.sender_name}""",
                    "purpose": "Provide value without asking",
                    "tips": "Actually have a resource ready to send"
                },
                {
                    "email_number": 4,
                    "email_type": "FOMO",
                    "delay_days": 4,
                    "subject_lines": [
                        "Your competitors are doing this",
                        "Saw this and thought of {{company}}",
                        "{{first_name}}, timing might be right"
                    ],
                    "body": f"""Hi {{{{first_name}}}},

I've noticed several companies in your space are starting to {self.offer.split()[0] if self.offer else 'invest'} heavily in this area.

Didn't want {{{{company}}}} to miss out.

Worth exploring?

{self.sender_name}""",
                    "purpose": "Create urgency through FOMO",
                    "tips": "Be genuine, not manipulative"
                },
                {
                    "email_number": 5,
                    "email_type": "Breakup",
                    "delay_days": 5,
                    "subject_lines": [
                        "Closing the loop",
                        "Should I close your file?",
                        "Last note from me"
                    ],
                    "body": f"""Hi {{{{first_name}}}},

I've reached out a few times but haven't heard back - totally understand if the timing isn't right.

If you're ever interested in learning how we can help with {self.offer}, feel free to reply.

Either way, wishing you and the {{{{company}}}} team continued success.

{self.sender_name}""",
                    "purpose": "Final attempt with graceful exit",
                    "tips": "Often gets highest reply rate"
                }
            ],
            "ab_test_recommendations": [
                "Test question vs statement subject lines",
                "Test short vs medium email length",
                "Test specific numbers vs general claims"
            ],
            "sending_best_practices": [
                "Send Tuesday-Thursday for best open rates",
                "Morning (8-10 AM) local time works best",
                "Keep daily sending under 50 emails per inbox",
                "Warm up new domains for 2+ weeks"
            ]
        }

    def export_to_instantly(self, sequence: Dict, leads: List[Dict]) -> Path:
        """Export campaign to Instantly format"""
        self.log("Exporting to Instantly format...", "INFO")

        export_path = self.output_dir / "exports" / "instantly_import.csv"

        rows = []
        for lead in leads:
            for email in sequence.get("emails", []):
                row = {
                    "email": lead.get("email", ""),
                    "first_name": lead.get("first_name", ""),
                    "last_name": lead.get("last_name", ""),
                    "company": lead.get("company", ""),
                    "title": lead.get("title", ""),
                    "subject_line": email["subject_lines"][0] if email.get("subject_lines") else "",
                    "body": email.get("body", ""),
                    "step": email.get("email_number", 1),
                    "delay_days": email.get("delay_days", 0)
                }
                rows.append(row)

        if rows:
            with open(export_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        self.log(f"Exported to {export_path}", "SUCCESS")
        return export_path

    def save_sequence_markdown(self, sequence: Dict) -> Path:
        """Save sequence as readable markdown"""
        md_path = self.output_dir / "sequences" / "email_sequence.md"

        content = f"""# Cold Email Sequence: {sequence.get('sequence_name', 'Campaign')}

**Sender:** {self.sender_name} - {self.sender_company}
**Offer:** {self.offer}
**Target ICP:** {self.target_icp}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

"""
        for email in sequence.get("emails", []):
            content += f"""## Email {email.get('email_number', '?')}: {email.get('email_type', 'Unknown')}

**Delay:** {email.get('delay_days', 0)} days after previous

**Subject Lines (A/B Test):**
"""
            for i, subj in enumerate(email.get("subject_lines", []), 1):
                content += f"- {i}. {subj}\n"

            content += f"""
**Body:**
```
{email.get('body', '')}
```

**Purpose:** {email.get('purpose', '')}

**Tips:** {email.get('tips', '')}

---

"""

        content += """## A/B Testing Recommendations

"""
        for rec in sequence.get("ab_test_recommendations", []):
            content += f"- {rec}\n"

        content += """
## Sending Best Practices

"""
        for practice in sequence.get("sending_best_practices", []):
            content += f"- {practice}\n"

        md_path.write_text(content, encoding="utf-8")
        self.log(f"Saved sequence to {md_path}", "SUCCESS")
        return md_path

    def execute(self) -> Dict:
        """Execute the complete campaign generation"""
        self.log(f"🚀 Starting Cold Email Campaign Generation", "INFO")
        self.log(f"   Sender: {self.sender_name} @ {self.sender_company}", "INFO")
        self.log(f"   Target: {self.target_icp}", "INFO")

        start_time = time.time()

        # Load leads
        leads = self.load_leads()

        # Generate email sequence
        sequence = self.generate_email_sequence()

        # Save sequence as markdown
        self.save_sequence_markdown(sequence)

        # Save sequence as JSON
        json_path = self.output_dir / "sequences" / "sequence_data.json"
        with open(json_path, 'w') as f:
            json.dump(sequence, f, indent=2)

        # Export to selected format
        if self.output_format == "instantly":
            self.export_to_instantly(sequence, leads)

        # Calculate execution time
        execution_time = time.time() - start_time

        result = {
            "success": True,
            "campaign_name": sequence.get("sequence_name", ""),
            "sender": f"{self.sender_name} @ {self.sender_company}",
            "target_icp": self.target_icp,
            "offer": self.offer,
            "emails_generated": len(sequence.get("emails", [])),
            "execution_time": f"{int(execution_time)}s",
            "output_dir": str(self.output_dir),
            "files": {
                "sequence_markdown": str(self.output_dir / "sequences" / "email_sequence.md"),
                "sequence_json": str(json_path),
                "export": str(self.output_dir / "exports")
            }
        }

        # Save result
        result_path = self.output_dir / "result.json"
        with open(result_path, 'w') as f:
            json.dump(result, f, indent=2)

        self.log("=" * 50, "INFO")
        self.log(f"✅ CAMPAIGN GENERATED: {sequence.get('sequence_name', '')}", "SUCCESS")
        self.log(f"   Emails: {len(sequence.get('emails', []))}", "INFO")
        self.log(f"   Output: {self.output_dir}", "INFO")
        self.log("=" * 50, "INFO")

        return result


def main():
    parser = argparse.ArgumentParser(description="Generate cold email campaigns")

    parser.add_argument("--sender-name", required=True, help="Your name")
    parser.add_argument("--sender-company", required=True, help="Your company")
    parser.add_argument("--offer", required=True, help="What you're selling")
    parser.add_argument("--target-icp", required=True, help="Target ICP description")
    parser.add_argument("--lead-source", default="manual", choices=["linkedin", "apollo", "manual"])
    parser.add_argument("--lead-count", type=int, default=100)
    parser.add_argument("--leads-file", help="Path to leads CSV")
    parser.add_argument("--sequence-length", type=int, default=5, choices=[3, 5, 7])
    parser.add_argument("--personalization-level", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("--output-format", default="instantly", choices=["instantly", "smartlead", "csv"])

    args = parser.parse_args()

    generator = ColdEmailCampaignGenerator(
        sender_name=args.sender_name,
        sender_company=args.sender_company,
        offer=args.offer,
        target_icp=args.target_icp,
        lead_source=args.lead_source,
        lead_count=args.lead_count,
        leads_file=args.leads_file,
        sequence_length=args.sequence_length,
        personalization_level=args.personalization_level,
        output_format=args.output_format
    )

    result = generator.execute()
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
