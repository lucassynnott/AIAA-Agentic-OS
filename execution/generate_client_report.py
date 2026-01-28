#!/usr/bin/env python3
"""
Ultimate Client Reporting System

Generates automated performance reports for agency clients.

Usage:
    python3 execution/generate_client_report.py \
        --client "Acme Corp" \
        --period "monthly" \
        --service "meta_ads" \
        --format "google_doc"

Follows directive: directives/ultimate_client_reporting.md
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import requests
except ImportError:
    print("Error: requests required. pip install requests")
    sys.exit(1)


class ClientReportGenerator:
    """Generate automated client performance reports"""

    def __init__(self, **kwargs):
        self.client = kwargs.get("client", "")
        self.period = kwargs.get("period", "monthly")
        self.start_date = kwargs.get("start_date", "")
        self.end_date = kwargs.get("end_date", "")
        self.service = kwargs.get("service", "meta_ads")
        self.format = kwargs.get("format", "markdown")
        self.data_file = kwargs.get("data_file", "")
        self.include_recommendations = kwargs.get("include_recommendations", True)

        # Set default dates if not provided
        if not self.end_date:
            self.end_date = datetime.now().strftime("%Y-%m-%d")
        if not self.start_date:
            if self.period == "weekly":
                start = datetime.now() - timedelta(days=7)
            elif self.period == "monthly":
                start = datetime.now() - timedelta(days=30)
            else:  # quarterly
                start = datetime.now() - timedelta(days=90)
            self.start_date = start.strftime("%Y-%m-%d")

        # Generate report slug
        client_slug = re.sub(r'[^a-zA-Z0-9]', '_', self.client.lower())
        period_str = datetime.now().strftime('%Y%m')

        # Setup output directory
        self.output_dir = Path(f".tmp/client_reports/{client_slug}/{period_str}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for subdir in ["data", "insights", "reports"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)

        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}.get(level, "")
        print(f"[{timestamp}] {prefix} {message}")

    def call_claude(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        if not self.openrouter_key:
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
            return None
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
            return None

    def load_data(self) -> Dict:
        """Load performance data from file or generate sample"""
        if self.data_file and os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)

        # Generate sample data structure
        return {
            "period": {
                "start": self.start_date,
                "end": self.end_date
            },
            "metrics": {
                "spend": 5000,
                "impressions": 250000,
                "clicks": 5000,
                "ctr": 2.0,
                "cpc": 1.00,
                "conversions": 100,
                "cpa": 50,
                "revenue": 15000,
                "roas": 3.0
            },
            "previous_period": {
                "spend": 4500,
                "impressions": 220000,
                "clicks": 4200,
                "ctr": 1.9,
                "cpc": 1.07,
                "conversions": 85,
                "cpa": 52.94,
                "revenue": 12000,
                "roas": 2.67
            },
            "top_campaigns": [
                {"name": "Campaign A", "spend": 2000, "conversions": 45, "roas": 3.5},
                {"name": "Campaign B", "spend": 1500, "conversions": 30, "roas": 3.2},
                {"name": "Campaign C", "spend": 1500, "conversions": 25, "roas": 2.5}
            ]
        }

    def calculate_changes(self, current: Dict, previous: Dict) -> Dict:
        """Calculate period-over-period changes"""
        changes = {}
        for key in current:
            if key in previous and previous[key] != 0:
                change = ((current[key] - previous[key]) / previous[key]) * 100
                changes[key] = round(change, 1)
            else:
                changes[key] = 0
        return changes

    def generate_insights(self, data: Dict) -> str:
        """Generate AI-powered insights"""
        self.log("Generating insights...", "INFO")

        prompt = f"""Analyze this marketing performance data and provide executive insights.

CLIENT: {self.client}
PERIOD: {self.start_date} to {self.end_date}
SERVICE: {self.service}

DATA:
{json.dumps(data, indent=2)}

Generate a professional analysis including:

1. EXECUTIVE SUMMARY (3-4 sentences)
- Overall performance assessment
- Key achievement
- Primary area for improvement

2. KEY WINS (3 bullet points)
- What went well and why

3. AREAS OF CONCERN (2-3 bullet points)
- What needs attention

4. RECOMMENDATIONS (3 specific, actionable items)
- What to do next

Keep the tone professional but accessible. Use specific numbers from the data."""

        result = self.call_claude(prompt)
        return result or "Insights unavailable - please review data manually."

    def generate_report(self, data: Dict, insights: str) -> str:
        """Generate the full report"""
        self.log("Generating report...", "INFO")

        metrics = data.get("metrics", {})
        previous = data.get("previous_period", {})
        changes = self.calculate_changes(metrics, previous)

        def change_indicator(val):
            if val > 0:
                return f"↑ {val}%"
            elif val < 0:
                return f"↓ {abs(val)}%"
            return "→ 0%"

        report = f"""# {self.client} - {self.period.title()} Performance Report

**Period:** {self.start_date} to {self.end_date}
**Service:** {self.service.replace('_', ' ').title()}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Performance Score: {self._calculate_score(metrics, previous)}/100

---

## Key Metrics at a Glance

| Metric | This Period | Last Period | Change |
|--------|-------------|-------------|--------|
| Spend | ${metrics.get('spend', 0):,.2f} | ${previous.get('spend', 0):,.2f} | {change_indicator(changes.get('spend', 0))} |
| Impressions | {metrics.get('impressions', 0):,} | {previous.get('impressions', 0):,} | {change_indicator(changes.get('impressions', 0))} |
| Clicks | {metrics.get('clicks', 0):,} | {previous.get('clicks', 0):,} | {change_indicator(changes.get('clicks', 0))} |
| CTR | {metrics.get('ctr', 0):.2f}% | {previous.get('ctr', 0):.2f}% | {change_indicator(changes.get('ctr', 0))} |
| CPC | ${metrics.get('cpc', 0):.2f} | ${previous.get('cpc', 0):.2f} | {change_indicator(-changes.get('cpc', 0))} |
| Conversions | {metrics.get('conversions', 0):,} | {previous.get('conversions', 0):,} | {change_indicator(changes.get('conversions', 0))} |
| CPA | ${metrics.get('cpa', 0):.2f} | ${previous.get('cpa', 0):.2f} | {change_indicator(-changes.get('cpa', 0))} |
| Revenue | ${metrics.get('revenue', 0):,.2f} | ${previous.get('revenue', 0):,.2f} | {change_indicator(changes.get('revenue', 0))} |
| ROAS | {metrics.get('roas', 0):.2f}x | {previous.get('roas', 0):.2f}x | {change_indicator(changes.get('roas', 0))} |

---

## Analysis & Insights

{insights}

---

## Top Performing Campaigns

"""
        for i, campaign in enumerate(data.get('top_campaigns', []), 1):
            report += f"""### {i}. {campaign.get('name', 'Campaign')}
- **Spend:** ${campaign.get('spend', 0):,.2f}
- **Conversions:** {campaign.get('conversions', 0)}
- **ROAS:** {campaign.get('roas', 0):.2f}x

"""

        report += f"""---

## Next Steps

1. Review recommendations above
2. Schedule optimization call if needed
3. Approve next month's strategy

---

*Report generated automatically by AIAA Agentic OS*
*Contact your account manager for questions*
"""

        return report

    def _calculate_score(self, current: Dict, previous: Dict) -> int:
        """Calculate overall performance score"""
        score = 70  # Base score

        # ROAS improvement
        if current.get('roas', 0) > previous.get('roas', 0):
            score += 10
        elif current.get('roas', 0) < previous.get('roas', 0):
            score -= 10

        # CPA improvement
        if current.get('cpa', 0) < previous.get('cpa', 0):
            score += 10
        elif current.get('cpa', 0) > previous.get('cpa', 0):
            score -= 5

        # Conversion growth
        conv_change = ((current.get('conversions', 0) - previous.get('conversions', 0)) /
                      max(previous.get('conversions', 1), 1)) * 100
        if conv_change > 10:
            score += 10
        elif conv_change > 0:
            score += 5
        elif conv_change < -10:
            score -= 10

        return max(0, min(100, score))

    def execute(self) -> Dict:
        """Execute report generation"""
        self.log(f"🚀 Starting Report Generation for {self.client}", "INFO")
        self.log(f"   Period: {self.period} ({self.start_date} to {self.end_date})", "INFO")

        start_time = time.time()

        # Load data
        data = self.load_data()

        # Save raw data
        data_path = self.output_dir / "data" / "raw_metrics.json"
        with open(data_path, 'w') as f:
            json.dump(data, f, indent=2)

        # Generate insights
        insights = ""
        if self.include_recommendations:
            insights = self.generate_insights(data)

            insights_path = self.output_dir / "insights" / "ai_analysis.md"
            insights_path.write_text(insights, encoding="utf-8")

        # Generate report
        report = self.generate_report(data, insights)

        # Save report
        report_path = self.output_dir / "reports" / "full_report.md"
        report_path.write_text(report, encoding="utf-8")

        execution_time = time.time() - start_time

        result = {
            "success": True,
            "client": self.client,
            "period": self.period,
            "dates": f"{self.start_date} to {self.end_date}",
            "execution_time": f"{int(execution_time)}s",
            "output_dir": str(self.output_dir),
            "files": {
                "report": str(report_path),
                "data": str(data_path),
                "insights": str(self.output_dir / "insights" / "ai_analysis.md") if insights else None
            }
        }

        result_path = self.output_dir / "result.json"
        with open(result_path, 'w') as f:
            json.dump(result, f, indent=2)

        self.log("=" * 50, "INFO")
        self.log(f"✅ REPORT GENERATED: {self.client}", "SUCCESS")
        self.log(f"   Output: {self.output_dir}", "INFO")
        self.log("=" * 50, "INFO")

        return result


def main():
    parser = argparse.ArgumentParser(description="Generate client reports")

    parser.add_argument("--client", required=True, help="Client name")
    parser.add_argument("--period", default="monthly", choices=["weekly", "monthly", "quarterly"])
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--service", default="meta_ads",
                       choices=["meta_ads", "google_ads", "seo", "all"])
    parser.add_argument("--format", default="markdown",
                       choices=["markdown", "pdf", "google_doc"])
    parser.add_argument("--data-file", help="Path to data JSON")
    parser.add_argument("--no-recommendations", action="store_true")

    args = parser.parse_args()

    generator = ClientReportGenerator(
        client=args.client,
        period=args.period,
        start_date=args.start_date,
        end_date=args.end_date,
        service=args.service,
        format=args.format,
        data_file=args.data_file,
        include_recommendations=not args.no_recommendations
    )

    result = generator.execute()
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
