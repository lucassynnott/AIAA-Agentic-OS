# Convert N8N Workflow to Directive + Execution

## What This Workflow Is
This utility converts n8n workflow JSON files into markdown directives and Python execution scripts following the 3-layer architecture.

## What It Does
1. Parses n8n workflow JSON
2. Extracts trigger, nodes, and AI prompts
3. Generates markdown directive
4. Creates Python scripts for API operations
5. Outputs ready-to-use files

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For parsing complex workflows
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install openai
```

## How to Run

### Convert Single Workflow
```bash
python3 execution/convert_n8n_to_directive.py \
  "N8N Workflows/Workflows/Cold Email Lead Generation Agency/Cold Email Scriptwriter.json"
```

### Batch Convert All Workflows
```bash
python3 execution/convert_n8n_to_directive.py \
  "N8N Workflows/Workflows/Cold Email Lead Generation Agency/" \
  --batch
```

### Quick One-Liner
```bash
python3 execution/convert_n8n_to_directive.py "path/to/workflow.json"
```

## Goal
Parse an n8n workflow JSON file and generate:
1. A directive (markdown SOP) that explains the workflow purpose, inputs, outputs, and process
2. Python execution scripts for any deterministic/API operations that can be extracted

## Inputs
- **workflow_path**: Path to n8n workflow JSON file (e.g., `N8N Workflows/Workflows/Cold Email Lead Generation Agency/Cold Email Scriptwriter.json`)

## Tools/Scripts
- Script: `execution/convert_n8n_to_directive.py`

## Process

### 1. Parse the N8N Workflow
Run the conversion script:
```bash
python3 execution/convert_n8n_to_directive.py "path/to/workflow.json"
```

The script extracts:
- **Workflow name** from JSON `name` field
- **Trigger type** (webhook, form, schedule, manual)
- **Node sequence** and their purposes
- **AI Agent prompts** (for LLM-based nodes)
- **API integrations** (HTTP requests, service nodes)
- **Input/output schemas** from structured output parsers

### 2. Generate Directive Structure
The script outputs a directive with:

```markdown
# [Workflow Name]

## Goal
[Extracted from workflow purpose/description]

## Trigger
[How the workflow is initiated - form, webhook, schedule]

## Inputs
[Fields from trigger node or form]

## Process
1. [Step derived from node sequence]
2. [Next step...]

## AI Agent Instructions
[Prompts extracted from LangChain agent nodes]

## Outputs
[Schema from output parser nodes]

## Edge Cases
[Common failure modes based on node types]
```

### 3. Generate Execution Scripts (if applicable)
For workflows with deterministic API calls, generate Python scripts:
- HTTP request nodes → `requests` calls
- Google Sheets nodes → sheets API functions
- Email nodes → email sending functions

### 4. Review and Refine
After generation, review the directive and:
- Add any missing context
- Clarify ambiguous steps
- Add error handling notes

## Output
- `directives/[workflow_name_snake_case].md` - The generated directive
- `execution/[workflow_name_snake_case].py` - Python script (if API operations exist)

## Example Usage
```bash
# Convert a single workflow
python3 execution/convert_n8n_to_directive.py "N8N Workflows/Workflows/Cold Email Lead Generation Agency/Cold Email Scriptwriter.json"

# Convert all workflows in a category
python3 execution/convert_n8n_to_directive.py "N8N Workflows/Workflows/Cold Email Lead Generation Agency/" --batch
```
