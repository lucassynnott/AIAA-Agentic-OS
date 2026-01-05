#!/usr/bin/env python3
"""
Team Task Assignment - Generate task assignments based on team capacity.

Usage:
    python3 execution/assign_team_tasks.py \
        --tasks tasks.json \
        --team team.json \
        --output .tmp/assignments.md
"""

import argparse, json, os, sys
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"

def main():
    parser = argparse.ArgumentParser(description="Assign tasks to team members")
    parser.add_argument("--tasks", "-t", required=True, help="Tasks JSON")
    parser.add_argument("--team", "-m", required=True, help="Team members JSON")
    parser.add_argument("--output", "-o", default=".tmp/assignments.md")
    args = parser.parse_args()

    # Load data
    def load_json(path):
        if Path(path).exists():
            with open(path) as f:
                return json.load(f)
        return json.loads(path)

    tasks = load_json(args.tasks)
    team = load_json(args.team)

    if isinstance(tasks, dict):
        tasks = tasks.get("tasks", [tasks])
    if isinstance(team, dict):
        team = team.get("members", team.get("team", [team]))

    print(f"\n📋 Task Assignment\n   Tasks: {len(tasks)}\n   Team: {len(team)}\n")
    client = get_client()

    assignments = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You optimize task assignments based on skills, capacity, and priorities."},
            {"role": "user", "content": f"""Assign these tasks to team members:

TASKS:
{json.dumps(tasks, indent=2)}

TEAM MEMBERS:
{json.dumps(team, indent=2)}

PROVIDE:

## Assignment Summary

| Task | Assignee | Priority | Due Date | Rationale |
|------|----------|----------|----------|-----------|
(fill for each task)

## By Team Member

### [Member Name]
- Tasks assigned: X
- Estimated hours: X
- Priority items: list

(repeat for each)

## Workload Analysis
- Most loaded team member
- Least loaded team member
- Capacity concerns

## Recommendations
- Rebalancing suggestions
- Skill gaps identified
- Priority conflicts

Optimize for skills match, capacity, and deadline urgency."""}
        ],
        temperature=0.5,
        max_tokens=2000
    ).choices[0].message.content

    output = f"""# Task Assignments

**Tasks:** {len(tasks)}
**Team:** {len(team)}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{assignments}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Assignments saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
