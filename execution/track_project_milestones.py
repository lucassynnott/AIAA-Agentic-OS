#!/usr/bin/env python3
"""
Project Milestone Tracker - Track and report on project milestones.

Usage:
    python3 execution/track_project_milestones.py \
        --project "Website Redesign" \
        --milestones milestones.json \
        --output .tmp/milestone_report.md
"""

import argparse, json, sys
from datetime import datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Track project milestones")
    parser.add_argument("--project", "-p", required=True)
    parser.add_argument("--milestones", "-m", required=True, help="Milestones JSON file or inline JSON")
    parser.add_argument("--output", "-o", default=".tmp/milestone_report.md")
    args = parser.parse_args()

    # Load milestones
    if Path(args.milestones).exists():
        with open(args.milestones) as f:
            milestones = json.load(f)
    else:
        try:
            milestones = json.loads(args.milestones)
        except:
            print("Error: Invalid milestones JSON")
            return 1

    if isinstance(milestones, dict):
        milestones = milestones.get("milestones", [milestones])

    print(f"\n📊 Milestone Tracker\n   Project: {args.project}\n   Milestones: {len(milestones)}\n")

    # Calculate stats
    completed = [m for m in milestones if m.get("status") == "completed"]
    in_progress = [m for m in milestones if m.get("status") == "in_progress"]
    pending = [m for m in milestones if m.get("status") in ["pending", "not_started", None]]
    overdue = [m for m in milestones if m.get("status") != "completed" and m.get("due_date") and m.get("due_date") < datetime.now().strftime("%Y-%m-%d")]

    progress_pct = len(completed) / len(milestones) * 100 if milestones else 0

    # Generate report
    output = f"""# Project Milestone Report: {args.project}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Progress Summary

| Metric | Value |
|--------|-------|
| Total Milestones | {len(milestones)} |
| Completed | {len(completed)} |
| In Progress | {len(in_progress)} |
| Pending | {len(pending)} |
| Overdue | {len(overdue)} |
| **Progress** | **{progress_pct:.1f}%** |

---

## Progress Bar

{'█' * int(progress_pct // 5)}{'░' * (20 - int(progress_pct // 5))} {progress_pct:.1f}%

---

## Milestone Details

### ✅ Completed ({len(completed)})
"""

    for m in completed:
        output += f"- **{m.get('name', 'Unnamed')}** - Completed {m.get('completed_date', 'N/A')}\n"

    output += f"\n### 🔄 In Progress ({len(in_progress)})\n"
    for m in in_progress:
        output += f"- **{m.get('name', 'Unnamed')}** - Due: {m.get('due_date', 'TBD')}\n"

    output += f"\n### ⏳ Pending ({len(pending)})\n"
    for m in pending:
        output += f"- **{m.get('name', 'Unnamed')}** - Due: {m.get('due_date', 'TBD')}\n"

    if overdue:
        output += f"\n### ⚠️ Overdue ({len(overdue)})\n"
        for m in overdue:
            output += f"- **{m.get('name', 'Unnamed')}** - Was due: {m.get('due_date', 'N/A')}\n"

    output += f"""

---

## Recommendations

"""
    if overdue:
        output += "- **Address overdue items immediately** - Review blockers and reallocate resources\n"
    if progress_pct < 50:
        output += "- **Project behind schedule** - Consider scope review or timeline adjustment\n"
    if progress_pct >= 80:
        output += "- **Project on track** - Maintain momentum for final deliverables\n"

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")

    print(f"   Progress: {progress_pct:.1f}% ({len(completed)}/{len(milestones)})")
    if overdue:
        print(f"   ⚠️ Overdue: {len(overdue)}")
    print(f"\n✅ Report saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
