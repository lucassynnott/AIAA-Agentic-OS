#!/usr/bin/env python3
"""
VSL Funnel Orchestrator (Master Workflow)

Coordinates complete VSL funnel creation pipeline.
Follows directive: directives/vsl_funnel_orchestrator.md
"""

import argparse
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class VSLFunnelOrchestrator:
    """Orchestrates the complete VSL funnel generation pipeline"""

    def __init__(self, company: str, website: str, offer: str, **kwargs):
        self.company = company
        self.website = website
        self.offer = offer
        self.industry = kwargs.get("industry", "")
        self.price_point = kwargs.get("price_point", "")
        self.vsl_length = kwargs.get("vsl_length", "medium")
        self.vsl_style = kwargs.get("vsl_style", "education")
        self.email_sequence_length = kwargs.get("email_sequence_length", 7)

        # Generate unique workflow ID
        company_slug = company.lower().replace(" ", "_").replace(".", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.workflow_id = f"vsl_funnel_{company_slug}_{timestamp}"

        # Setup output directories
        self.output_dir = Path(f".tmp/{self.workflow_id}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.start_time = time.time()
        self.deliverables = []
        self.errors = []
        self.warnings = []

    def log(self, message: str, level: str = "INFO"):
        """Log workflow progress"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌"
        }.get(level, "")
        print(f"[{timestamp}] {prefix} {message}")

    def run_script(self, script: str, args: list) -> tuple:
        """Run execution script and return success status"""
        try:
            cmd = ["python3", f"execution/{script}"] + args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr

        except subprocess.TimeoutExpired:
            return False, "Script timeout (5 minutes)"
        except Exception as e:
            return False, str(e)

    def step1_market_research(self):
        """Step 1: Company & Offer Market Research"""
        self.log("Step 1/7: Market Research (Perplexity)", "INFO")

        research_file = self.output_dir / "01_research.json"

        args = [
            "--company", self.company,
            "--website", self.website,
            "--offer", self.offer,
            "--output", str(research_file),
        ]

        if self.industry:
            args.extend(["--industry", self.industry])

        success, output = self.run_script("research_company_offer.py", args)

        if success:
            self.log("Market research complete", "SUCCESS")
            return str(research_file)
        else:
            self.log(f"Market research failed: {output}", "ERROR")
            self.errors.append("Market research failed")
            return None

    def step2_vsl_script(self, research_file: str):
        """Step 2: VSL Script Generation"""
        self.log("Step 2/7: VSL Script Generation", "INFO")

        vsl_script_file = self.output_dir / "02_vsl_script.md"
        hooks_file = self.output_dir / "02_vsl_hooks.md"

        args = [
            "--research", research_file,
            "--length", self.vsl_length,
            "--style", self.vsl_style,
            "--output", str(vsl_script_file),
            "--hooks-output", str(hooks_file),
        ]

        success, output = self.run_script("generate_vsl_script.py", args)

        if success:
            self.log("VSL script generated", "SUCCESS")
            return str(vsl_script_file)
        else:
            self.log(f"VSL script generation failed: {output}", "ERROR")
            self.errors.append("VSL script generation failed")
            return None

    def step3_sales_page(self, research_file: str, vsl_script_file: str):
        """Step 3: Sales Page Copy"""
        self.log("Step 3/7: Sales Page Generation", "INFO")

        sales_page_file = self.output_dir / "03_sales_page.md"

        args = [
            "--research", research_file,
            "--vsl-script", vsl_script_file,
            "--style", "full",
            "--output", str(sales_page_file),
        ]

        success, output = self.run_script("generate_sales_page.py", args)

        if success:
            self.log("Sales page generated", "SUCCESS")
            return str(sales_page_file)
        else:
            self.log(f"Sales page generation failed: {output}", "WARNING")
            self.warnings.append("Sales page generation failed (continuing)")
            return None

    def step4_email_sequence(self, research_file: str, vsl_script_file: str, sales_page_file: str):
        """Step 4: Email Sequence"""
        self.log("Step 4/7: Email Sequence Generation", "INFO")

        email_sequence_file = self.output_dir / "04_email_sequence.md"

        # Use placeholder if sales page failed
        if not sales_page_file:
            sales_page_file = vsl_script_file

        args = [
            "--research", research_file,
            "--vsl-script", vsl_script_file,
            "--sales-page", sales_page_file,
            "--length", str(self.email_sequence_length),
            "--output", str(email_sequence_file),
        ]

        success, output = self.run_script("generate_email_sequence.py", args)

        if success:
            self.log(f"Email sequence generated ({self.email_sequence_length} emails)", "SUCCESS")
            return str(email_sequence_file)
        else:
            self.log(f"Email sequence generation failed: {output}", "WARNING")
            self.warnings.append("Email sequence generation failed (continuing)")
            return None

    def step5_create_google_docs(self, files: dict):
        """Step 5: Create Google Docs"""
        self.log("Step 5/7: Creating Google Docs", "INFO")

        docs_created = []

        for title, filepath in files.items():
            if not filepath or not os.path.exists(filepath):
                self.log(f"Skipping {title} (file not found)", "WARNING")
                continue

            doc_metadata_file = self.output_dir / f"{Path(filepath).stem}_doc.json"

            args = [
                "--content", filepath,
                "--title", f"{self.company} - {title}",
                "--folder-id", "1M_2lHBzVQuIv1fptf8BUfVcGJgL6jxf7",
            ]

            # Use centralized formatted doc creator
            success, output = self.run_script("create_formatted_google_doc.py", args)

            if success and os.path.exists(doc_metadata_file):
                with open(doc_metadata_file, "r") as f:
                    doc_data = json.load(f)
                    docs_created.append(doc_data)

        if docs_created:
            self.log(f"Created {len(docs_created)} Google Docs", "SUCCESS")
        else:
            self.log("No Google Docs created (credentials not configured)", "WARNING")
            self.warnings.append("Google Docs not created (using local files)")

        return docs_created

    def step6_slack_notification(self, docs_created: list, execution_time: str):
        """Step 6: Slack Notification"""
        self.log("Step 6/7: Sending Slack notification", "INFO")

        # Build deliverables list
        deliverables = []
        for doc in docs_created:
            if doc.get("documentUrl"):
                deliverables.append({
                    "name": doc["title"],
                    "url": doc["documentUrl"]
                })

        # Add local files if no docs created
        if not deliverables:
            local_files = [
                {"name": "Market Research", "url": None},
                {"name": "VSL Script", "url": None},
                {"name": "Sales Page", "url": None},
                {"name": "Email Sequence", "url": None},
            ]
            deliverables = local_files

        # Build metadata
        metadata = {
            "execution_time": execution_time,
            "vsl_length": f"{self.vsl_length} style",
            "email_count": self.email_sequence_length,
            "status": "success" if not self.errors else "partial"
        }

        args = [
            "--workflow", "VSL Funnel Complete",
            "--status", "success" if not self.errors else "partial",
            "--company", self.company,
            "--deliverables", json.dumps(deliverables),
            "--metadata", json.dumps(metadata),
        ]

        success, output = self.run_script("send_slack_notification.py", args)

        if success:
            self.log("Slack notification sent", "SUCCESS")
        else:
            self.log("Slack notification skipped (not configured)", "WARNING")

    def execute(self):
        """Execute complete VSL funnel pipeline"""
        self.log(f"🚀 Starting VSL Funnel for: {self.company}", "INFO")
        self.log(f"   Offer: {self.offer}", "INFO")
        self.log(f"   Output: {self.output_dir}", "INFO")

        # Step 1: Market Research
        research_file = self.step1_market_research()
        if not research_file:
            return self.finalize_failure()

        # Step 2: VSL Script
        vsl_script_file = self.step2_vsl_script(research_file)
        if not vsl_script_file:
            return self.finalize_failure()

        # Step 3: Sales Page
        sales_page_file = self.step3_sales_page(research_file, vsl_script_file)

        # Step 4: Email Sequence
        email_sequence_file = self.step4_email_sequence(research_file, vsl_script_file, sales_page_file)

        # Step 5: Google Docs (use markdown files for proper formatting)
        files = {
            "Market Research": str(Path(research_file).with_suffix('.md')),  # Use formatted markdown
            "VSL Script": vsl_script_file,
            "Sales Page": sales_page_file,
            "Email Sequence": email_sequence_file,
        }
        docs_created = self.step5_create_google_docs(files)

        # Step 6: Slack Notification
        execution_time = self.format_execution_time()
        self.step6_slack_notification(docs_created, execution_time)

        # Step 7: Return Final Output
        return self.finalize_success(research_file, vsl_script_file, sales_page_file, email_sequence_file, docs_created)

    def format_execution_time(self) -> str:
        """Format execution time"""
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return f"{minutes}m {seconds}s"

    def finalize_success(self, research_file, vsl_script_file, sales_page_file, email_sequence_file, docs_created):
        """Finalize successful execution"""
        execution_time = self.format_execution_time()

        result = {
            "success": True,
            "company": self.company,
            "offer": self.offer,
            "executionTime": execution_time,
            "deliverables": {
                "marketResearch": {
                    "file": research_file,
                    "doc": next((d["documentUrl"] for d in docs_created if "Research" in d["title"]), None)
                },
                "vslScript": {
                    "file": vsl_script_file,
                    "doc": next((d["documentUrl"] for d in docs_created if "Script" in d["title"]), None)
                },
                "salesPage": {
                    "file": sales_page_file,
                    "doc": next((d["documentUrl"] for d in docs_created if "Sales" in d["title"]), None)
                },
                "emailSequence": {
                    "file": email_sequence_file,
                    "doc": next((d["documentUrl"] for d in docs_created if "Email" in d["title"]), None),
                    "emailCount": self.email_sequence_length
                }
            },
            "errors": self.errors,
            "warnings": self.warnings
        }

        # Save result
        result_file = self.output_dir / "result.json"
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)

        self.log("=" * 50, "INFO")
        self.log(f"✅ VSL FUNNEL COMPLETE: {self.company}", "SUCCESS")
        self.log(f"   Execution time: {execution_time}", "INFO")
        self.log(f"   Output directory: {self.output_dir}", "INFO")
        self.log(f"   Errors: {len(self.errors)}", "INFO")
        self.log(f"   Warnings: {len(self.warnings)}", "INFO")
        self.log("=" * 50, "INFO")

        return result

    def finalize_failure(self):
        """Finalize failed execution"""
        execution_time = self.format_execution_time()

        self.log("=" * 50, "ERROR")
        self.log(f"❌ VSL FUNNEL FAILED: {self.company}", "ERROR")
        self.log(f"   Execution time: {execution_time}", "INFO")
        self.log(f"   Errors: {self.errors}", "ERROR")
        self.log("=" * 50, "ERROR")

        return {
            "success": False,
            "company": self.company,
            "executionTime": execution_time,
            "errors": self.errors
        }


def main():
    parser = argparse.ArgumentParser(description="Generate complete VSL funnel")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--website", required=True, help="Company website")
    parser.add_argument("--offer", required=True, help="Offer/product name")
    parser.add_argument("--industry", help="Industry/niche")
    parser.add_argument("--price", help="Price point")
    parser.add_argument("--vsl-length", default="medium", choices=["mini", "medium", "long"], help="VSL length")
    parser.add_argument("--vsl-style", default="education", choices=["education", "story", "case-study"], help="VSL style")
    parser.add_argument("--email-count", type=int, default=7, choices=[5, 7], help="Email sequence length")

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = VSLFunnelOrchestrator(
        company=args.company,
        website=args.website,
        offer=args.offer,
        industry=args.industry,
        price_point=args.price,
        vsl_length=args.vsl_length,
        vsl_style=args.vsl_style,
        email_sequence_length=args.email_count,
    )

    # Execute pipeline
    result = orchestrator.execute()

    # Exit with appropriate code
    return 0 if result["success"] else 1


if __name__ == "__main__":
    exit(main())
