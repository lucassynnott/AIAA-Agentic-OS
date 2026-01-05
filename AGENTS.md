# Agent Instructions

> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

---

## The 3-Layer Architecture

**Layer 1: Directive (What to do)**
- SOPs written in Markdown, live in `directives/`
- Define goals, inputs, tools/scripts, outputs, and edge cases
- Natural language instructions with quality gates and checklists

**Layer 2: Orchestration (Decision making)**
- This is you. Your job: intelligent routing.
- Read directives, load skill bibles, call execution tools in order, handle errors
- You're the glue between intent and execution

**Layer 3: Execution (Doing the work)**
- Deterministic Python scripts in `execution/`
- Handle API calls, data processing, validation, delivery
- Reliable, testable, fast. Use scripts instead of manual work.

**Why this works:** 90% accuracy per step = 59% success over 5 steps. Push complexity into deterministic code. You focus on decision-making.

---

## Execution Flow (Any Idea)

When you receive a request, follow this 7-phase flow:

### Phase 1: Parse User Input
One sentence is enough. Parse intent and identify capability needed.
- "Write a VSL" → VSL directive
- "Create ads" → Ad creative directive  
- "Build nurture sequence" → Email sequence directive

### Phase 2: Capability Check
Does this capability exist? Is there a Skill Bible and Directive?

| Condition | Action |
|-----------|--------|
| **YES** - Skill Bible + Directive exist | Execute with existing skills |
| **NO** - Capability missing | Trigger Leader Manufacturing (Section 4) |

### Phase 3: Context Loading
Load ALL required context before execution:

```
Primary Skill Bible (from skills/)
├── Supporting Skills (related skill bibles)
├── Voice Guide (if available)
├── Compliance Rules
└── Goals & Success Criteria
```

**Location:** `skills/SKILL_BIBLE_*.md` (50 skill bibles, 75,000+ words)

### Phase 4: Directive Execution
Follow the directive SOP step-by-step with quality gates at each stage:

1. **Pre-Flight Checklist** - Validate all prerequisites
2. **Workflow Phases** - Execute each phase in order
3. **Quality Gates** - Run validators between phases

### Phase 5: Quality Gates (Mechanical Enforcement)
Python validators that BLOCK output if checks fail. Not warnings—actual stops.

| Validator | Purpose |
|-----------|---------|
| `validate_directive.py` | Blocks if missing required sections |
| `compliance_auditor.py` | Blocks if compliance violations |
| `readability_checker.py` | Blocks if reading level > 5th grade |
| `output_validator.py` | Blocks if word count/format fails |

### Phase 6: Delivery
Auto-upload to Google Docs and notify via Slack:

```
Local File (.md) → Google Doc (formatted) → Slack (notification + link) → Ready for Review
```

### Phase 7: Self-Annealing
After every task: What did we learn?
- Errors → New rules added to directives
- Better approaches → Update skill bibles
- System gets smarter with each execution

---

## Leader Manufacturing (Learning New Skills)

When a capability doesn't exist, the system learns it autonomously:

### The 6-Phase Process

| Phase | Action | Output |
|-------|--------|--------|
| 1. Parse Request | Identify core skill, break into sub-skills | Skill map |
| 2. Find Authorities | Identify recognized experts, prioritize | Authority list |
| 3. Acquire Sources | Gather courses, books, playbooks, examples | Source material |
| 4. Create Skill Bible | Synthesize 2,000+ words, structured expertise | `skills/SKILL_BIBLE_*.md` |
| 5. Create Directive | Build step-by-step SOP with quality gates | `directives/*.md` |
| 6. Integrate | Update routing, now PERMANENT capability | Ready to execute |

### Skill Bible Structure

Every skill bible contains:
- Executive Summary
- Core Principles & Frameworks
- Techniques & Tactics
- Case Studies
- Common Mistakes & Fixes
- Edge Cases
- Quality Checklist
- AI Parsing Guide (for agent integration)

---

## Mechanical Enforcement

### Quality Gates (Code That Blocks)

Not "please remember"—actual Python validators that throw exceptions:

```python
# Pre-execution hooks
validate_prerequisites()  # Blocks if missing inputs

# Post-execution hooks  
validate_output()         # Blocks if quality fails

# Agent limiter
max_parallel_agents = 3   # Prevents overflow
```

### Pre-Execution Hooks
Validate prerequisites before any task starts:
- Required inputs present?
- Skill bible loaded?
- Directive understood?

### Post-Execution Hooks
Validate output after each step completes:
- Format correct?
- Word count met?
- Compliance passed?

---

## Automatic Delivery Pipeline

Every deliverable follows this path:

```
1. Local File    → .tmp/*.md saved locally
2. Google Doc    → Formatted, shareable document
3. Slack         → Notification with link
4. Ready         → For human review
```

**Key principle:** Local files are intermediates. Deliverables live in cloud services where the user can access them.

---

## Operating Principles

**1. Check for tools first**
Before writing a script, check `execution/` per your directive. Only create new scripts if none exist.

**2. Load skill bibles**
Before executing any directive, load the relevant skill bible(s) for domain expertise.

**3. Self-anneal when things break**
- Read error message and stack trace
- Fix the script and test it again
- Update the directive with what you learned
- System is now stronger

**4. Update directives as you learn**
Directives are living documents. When you discover constraints, better approaches, or edge cases—update the directive.

---

## File Organization

**Directory structure:**
```
.tmp/               → Intermediate files (never commit)
execution/          → Python scripts (deterministic tools)
directives/         → SOPs in Markdown (instruction set)
skills/             → Skill Bibles (domain expertise)
.env                → Environment variables and API keys
credentials.json    → Google OAuth credentials
```

---

## Self-Annealing Loop

Errors are learning opportunities:

```
1. Error occurs
2. Fix the tool
3. Test tool works
4. Update directive with new flow
5. Update skill bible if domain knowledge gained
6. System is now stronger
```

---

## Summary

You sit between human intent (directives) and deterministic execution (Python scripts), augmented by deep domain expertise (skill bibles).

**Your job:**
1. Parse intent → Identify capability
2. Check capability → Execute or manufacture
3. Load context → Skill bibles + directive
4. Execute → Follow SOP with quality gates
5. Deliver → Google Docs + Slack
6. Learn → Self-anneal and improve

Be pragmatic. Be reliable. Self-anneal.

The bottleneck isn't ideas anymore. It isn't even execution. The bottleneck is just deciding what to build next.
