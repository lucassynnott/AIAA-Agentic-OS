#!/usr/bin/env python3
"""
Convert N8N workflow JSON to directive markdown and optional execution scripts.
"""

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime

def slugify(name: str) -> str:
    """Convert workflow name to snake_case filename."""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = re.sub(r'_+', '_', slug)
    return slug.strip('_')

def extract_trigger_info(nodes: list) -> dict:
    """Extract trigger node information."""
    trigger_types = {
        'n8n-nodes-base.webhook': 'webhook',
        'n8n-nodes-base.formTrigger': 'form',
        '@n8n/n8n-nodes-langchain.formTrigger': 'form',
        'n8n-nodes-base.scheduleTrigger': 'schedule',
        'n8n-nodes-base.manualTrigger': 'manual',
    }
    
    for node in nodes:
        node_type = node.get('type', '')
        if node_type in trigger_types:
            return {
                'type': trigger_types[node_type],
                'name': node.get('name', 'Trigger'),
                'parameters': node.get('parameters', {})
            }
    
    return {'type': 'manual', 'name': 'Manual Trigger', 'parameters': {}}

def extract_form_fields(trigger: dict) -> list:
    """Extract form field definitions from form trigger."""
    fields = []
    params = trigger.get('parameters', {})
    
    form_fields = params.get('formFields', {}).get('values', [])
    for field in form_fields:
        fields.append({
            'name': field.get('fieldLabel', 'Unknown'),
            'type': field.get('fieldType', 'text'),
            'required': field.get('requiredField', False)
        })
    
    return fields

def extract_ai_agents(nodes: list) -> list:
    """Extract AI agent nodes and their prompts."""
    agents = []
    agent_types = [
        '@n8n/n8n-nodes-langchain.agent',
        '@n8n/n8n-nodes-langchain.chainLlm',
    ]
    
    for node in nodes:
        if node.get('type') in agent_types:
            params = node.get('parameters', {})
            agents.append({
                'name': node.get('name', 'AI Agent'),
                'prompt': params.get('text', params.get('prompt', '')),
                'system_message': params.get('options', {}).get('systemMessage', ''),
                'has_output_parser': params.get('hasOutputParser', False)
            })
    
    return agents

def extract_output_schemas(nodes: list) -> list:
    """Extract structured output schemas."""
    schemas = []
    parser_types = [
        '@n8n/n8n-nodes-langchain.outputParserStructured',
    ]
    
    for node in nodes:
        if node.get('type') in parser_types:
            params = node.get('parameters', {})
            schema_str = params.get('jsonSchema', '{}')
            try:
                schema = json.loads(schema_str)
                schemas.append({
                    'name': node.get('name', 'Output Parser'),
                    'schema': schema
                })
            except json.JSONDecodeError:
                schemas.append({
                    'name': node.get('name', 'Output Parser'),
                    'schema_raw': schema_str
                })
    
    return schemas

def extract_http_requests(nodes: list) -> list:
    """Extract HTTP request nodes for potential script generation."""
    requests = []
    http_types = [
        'n8n-nodes-base.httpRequest',
    ]
    
    for node in nodes:
        if node.get('type') in http_types:
            params = node.get('parameters', {})
            requests.append({
                'name': node.get('name', 'HTTP Request'),
                'method': params.get('method', 'GET'),
                'url': params.get('url', ''),
                'headers': params.get('headerParameters', {})
            })
    
    return requests

def extract_integrations(nodes: list) -> list:
    """Extract third-party integrations."""
    integrations = []
    known_integrations = {
        'n8n-nodes-base.googleSheets': 'Google Sheets',
        'n8n-nodes-base.gmail': 'Gmail',
        'n8n-nodes-base.slack': 'Slack',
        'n8n-nodes-base.airtable': 'Airtable',
        'n8n-nodes-base.notion': 'Notion',
        '@n8n/n8n-nodes-langchain.lmChatOpenAi': 'OpenAI',
        '@n8n/n8n-nodes-langchain.lmChatAnthropic': 'Anthropic',
        '@n8n/n8n-nodes-langchain.toolPerplexity': 'Perplexity',
    }
    
    for node in nodes:
        node_type = node.get('type', '')
        if node_type in known_integrations:
            integrations.append({
                'type': known_integrations[node_type],
                'name': node.get('name', ''),
                'node_type': node_type
            })
    
    return integrations

def build_process_steps(nodes: list, connections: dict) -> list:
    """Build ordered process steps from nodes."""
    steps = []
    skip_types = [
        'n8n-nodes-base.stickyNote',
        '@n8n/n8n-nodes-langchain.outputParserStructured',
        '@n8n/n8n-nodes-langchain.lmChatOpenAi',
        '@n8n/n8n-nodes-langchain.lmChatAnthropic',
        '@n8n/n8n-nodes-langchain.toolPerplexity',
    ]
    
    for node in nodes:
        if node.get('type') in skip_types:
            continue
        
        node_type = node.get('type', '')
        name = node.get('name', 'Unknown')
        
        if 'trigger' in node_type.lower() or 'Trigger' in name:
            step_type = 'trigger'
        elif 'agent' in node_type.lower():
            step_type = 'ai_agent'
        elif 'set' in node_type.lower():
            step_type = 'data_transform'
        elif 'merge' in node_type.lower():
            step_type = 'merge'
        elif 'http' in node_type.lower():
            step_type = 'api_call'
        elif 'googleSheets' in node_type:
            step_type = 'sheets'
        else:
            step_type = 'process'
        
        steps.append({
            'name': name,
            'type': step_type,
            'node_type': node_type
        })
    
    return steps

def generate_directive(workflow: dict, output_dir: str) -> str:
    """Generate directive markdown from parsed workflow."""
    name = workflow.get('name', 'Unknown Workflow')
    nodes = workflow.get('nodes', [])
    connections = workflow.get('connections', {})
    
    trigger = extract_trigger_info(nodes)
    form_fields = extract_form_fields(trigger) if trigger['type'] == 'form' else []
    ai_agents = extract_ai_agents(nodes)
    output_schemas = extract_output_schemas(nodes)
    http_requests = extract_http_requests(nodes)
    integrations = extract_integrations(nodes)
    process_steps = build_process_steps(nodes, connections)
    
    # Build directive content
    lines = [f"# {name}", ""]
    
    # Goal section
    lines.append("## Goal")
    if ai_agents:
        first_agent = ai_agents[0]
        prompt_preview = first_agent['prompt'][:200] + "..." if len(first_agent['prompt']) > 200 else first_agent['prompt']
        lines.append(f"This workflow uses AI to process inputs and generate structured outputs.")
    else:
        lines.append(f"[Describe the purpose of this workflow]")
    lines.append("")
    
    # Trigger section
    lines.append("## Trigger")
    lines.append(f"- **Type**: {trigger['type'].title()}")
    lines.append(f"- **Node**: {trigger['name']}")
    lines.append("")
    
    # Inputs section
    lines.append("## Inputs")
    if form_fields:
        for field in form_fields:
            req = " (required)" if field['required'] else ""
            lines.append(f"- **{field['name']}**: {field['type']}{req}")
    else:
        lines.append("- [Define inputs based on trigger type]")
    lines.append("")
    
    # Integrations section
    if integrations:
        lines.append("## Integrations Required")
        seen = set()
        for integration in integrations:
            if integration['type'] not in seen:
                lines.append(f"- {integration['type']}")
                seen.add(integration['type'])
        lines.append("")
    
    # Process section
    lines.append("## Process")
    step_num = 1
    for step in process_steps:
        if step['type'] == 'trigger':
            lines.append(f"### {step_num}. {step['name']}")
            lines.append(f"Workflow is triggered via {trigger['type']}.")
        elif step['type'] == 'ai_agent':
            lines.append(f"### {step_num}. {step['name']}")
            agent = next((a for a in ai_agents if a['name'] == step['name']), None)
            if agent:
                lines.append(f"AI agent processes the input with the following instructions:")
                lines.append("```")
                prompt_lines = agent['prompt'].split('\n')[:20]
                lines.extend(prompt_lines)
                if len(agent['prompt'].split('\n')) > 20:
                    lines.append("... [truncated]")
                lines.append("```")
        elif step['type'] == 'data_transform':
            lines.append(f"### {step_num}. {step['name']}")
            lines.append("Data is normalized/transformed for the next step.")
        else:
            lines.append(f"### {step_num}. {step['name']}")
            lines.append(f"[Describe what this step does]")
        lines.append("")
        step_num += 1
    
    # Output section
    lines.append("## Output Schema")
    if output_schemas:
        for schema in output_schemas:
            lines.append(f"### {schema['name']}")
            lines.append("```json")
            if 'schema' in schema:
                lines.append(json.dumps(schema['schema'], indent=2))
            else:
                lines.append(schema.get('schema_raw', '{}'))
            lines.append("```")
    else:
        lines.append("[Define expected output structure]")
    lines.append("")
    
    # Edge cases
    lines.append("## Edge Cases")
    lines.append("- Handle empty/missing input fields")
    lines.append("- API rate limits for external services")
    lines.append("- AI model failures or timeouts")
    lines.append("")
    
    # Original n8n reference
    lines.append("## Original N8N Workflow")
    lines.append(f"This directive was generated from: `{workflow.get('_source_path', 'unknown')}`")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}")
    
    return '\n'.join(lines)

def convert_workflow(json_path: str, output_dir: str = None) -> dict:
    """Convert a single n8n workflow JSON to directive."""
    path = Path(json_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Workflow file not found: {json_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    workflow['_source_path'] = str(path)
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / 'directives'
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate directive
    directive_content = generate_directive(workflow, str(output_dir))
    
    # Save directive
    slug = slugify(workflow.get('name', 'unknown'))
    directive_path = output_dir / f"{slug}.md"
    
    with open(directive_path, 'w', encoding='utf-8') as f:
        f.write(directive_content)
    
    return {
        'workflow_name': workflow.get('name'),
        'directive_path': str(directive_path),
        'slug': slug
    }

def convert_batch(directory: str, output_dir: str = None) -> list:
    """Convert all workflow JSONs in a directory."""
    results = []
    dir_path = Path(directory)
    
    for json_file in dir_path.glob('*.json'):
        try:
            result = convert_workflow(str(json_file), output_dir)
            results.append(result)
            print(f"✓ Converted: {result['workflow_name']} → {result['directive_path']}")
        except Exception as e:
            print(f"✗ Failed: {json_file.name} - {e}")
            results.append({'file': str(json_file), 'error': str(e)})
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_n8n_to_directive.py <workflow.json|directory> [--batch]")
        print("\nExamples:")
        print("  python convert_n8n_to_directive.py workflow.json")
        print("  python convert_n8n_to_directive.py workflows/ --batch")
        sys.exit(1)
    
    path = sys.argv[1]
    batch_mode = '--batch' in sys.argv
    
    if batch_mode or os.path.isdir(path):
        results = convert_batch(path)
        print(f"\nConverted {len([r for r in results if 'error' not in r])} workflows")
    else:
        result = convert_workflow(path)
        print(f"✓ Created directive: {result['directive_path']}")

if __name__ == '__main__':
    main()
