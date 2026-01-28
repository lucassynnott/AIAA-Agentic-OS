#!/usr/bin/env python3
"""
Deploy Workflow to Modal AI

Automatically deploys any directive as a separate Modal AI app with
auto-detected tools and webhook endpoint.

Usage:
    python3 execution/deploy_to_modal.py --directive vsl_funnel_writer
    python3 execution/deploy_to_modal.py --directive vsl_funnel_writer --dry-run
    python3 execution/deploy_to_modal.py --list
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DIRECTIVES_DIR = PROJECT_ROOT / "directives"
SKILLS_DIR = PROJECT_ROOT / "skills"
EXECUTION_DIR = PROJECT_ROOT / "execution"
MODAL_APPS_DIR = EXECUTION_DIR / "modal_apps"


def list_directives() -> list[str]:
    """List all available directives."""
    directives = []
    for f in DIRECTIVES_DIR.glob("*.md"):
        directives.append(f.stem)
    return sorted(directives)


def load_directive(name: str) -> str:
    """Load directive content by name."""
    path = DIRECTIVES_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Directive not found: {name}")
    return path.read_text()


def parse_directive(content: str) -> dict:
    """
    Parse a directive to extract:
    - execution_scripts: List of Python scripts referenced
    - integrations: List of integrations (Slack, Google, etc.)
    - inputs: Dict of input fields
    - description: Brief description
    """
    result = {
        "execution_scripts": [],
        "integrations": [],
        "inputs": {},
        "description": "",
        "has_llm": False,
    }
    
    # Extract description from first paragraph or "What This Workflow Is" section
    desc_match = re.search(r"## What This Workflow Is\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if desc_match:
        result["description"] = desc_match.group(1).strip().split("\n")[0][:200]
    
    # Find execution scripts: python3 execution/script.py patterns
    script_patterns = [
        r"python3?\s+execution/(\w+)\.py",
        r"execution/(\w+)\.py",
        r"`execution/(\w+)\.py`",
    ]
    for pattern in script_patterns:
        matches = re.findall(pattern, content)
        result["execution_scripts"].extend(matches)
    result["execution_scripts"] = list(set(result["execution_scripts"]))
    
    # Detect integrations from content
    integration_keywords = {
        "slack": ["Slack", "slack_notify", "SLACK_WEBHOOK"],
        "google_docs": ["Google Doc", "Google Docs", "create_google_doc", "googleapis"],
        "google_sheets": ["Google Sheet", "read_sheet", "update_sheet", "gspread"],
        "gmail": ["Gmail", "send_email", "email"],
        "openrouter": ["OpenRouter", "OPENROUTER_API_KEY", "openrouter.ai"],
        "anthropic": ["Claude", "Anthropic", "ANTHROPIC_API_KEY", "anthropic"],
        "openai": ["GPT", "OpenAI", "OPENAI_API_KEY", "gpt-4"],
    }
    
    content_lower = content.lower()
    for integration, keywords in integration_keywords.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                if integration not in result["integrations"]:
                    result["integrations"].append(integration)
                break
    
    # Check for LLM usage
    llm_indicators = ["openrouter", "anthropic", "openai", "claude", "gpt", "llm", "ai agent"]
    result["has_llm"] = any(ind in content_lower for ind in llm_indicators)
    
    # Parse inputs section
    inputs_match = re.search(r"## Inputs\s*\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
    if inputs_match:
        inputs_section = inputs_match.group(1)
        # Parse bullet points like: - **Field Name**: type (required)
        input_patterns = re.findall(
            r"-\s*\*\*([^*]+)\*\*:\s*(\w+)(?:\s*\((\w+)\))?",
            inputs_section
        )
        for name, field_type, required in input_patterns:
            result["inputs"][name.strip()] = {
                "type": field_type.strip(),
                "required": required == "required" if required else False
            }
    
    # Find skill bible references
    skill_patterns = [
        r"SKILL_BIBLE_(\w+)\.md",
        r"skills/SKILL_BIBLE_(\w+)",
        r"`SKILL_BIBLE_(\w+)`",
    ]
    skill_bibles = []
    for pattern in skill_patterns:
        matches = re.findall(pattern, content)
        skill_bibles.extend(matches)
    result["skill_bibles"] = list(set(skill_bibles))
    
    return result


def get_required_secrets(parsed: dict) -> list[str]:
    """Determine which Modal secrets are needed based on integrations."""
    secrets = []
    
    if "anthropic" in parsed["integrations"] or parsed["has_llm"]:
        secrets.append("anthropic-secret")
    
    if "openrouter" in parsed["integrations"]:
        secrets.append("openrouter-secret")
    
    if "slack" in parsed["integrations"]:
        secrets.append("slack-webhook")
    
    if any(g in parsed["integrations"] for g in ["google_docs", "google_sheets", "gmail"]):
        secrets.append("google-token")
    
    return secrets


def check_modal_secrets(required_secrets: list[str]) -> tuple[list[str], list[str]]:
    """Check which secrets exist in Modal. Returns (existing, missing)."""
    try:
        result = subprocess.run(
            ["modal", "secret", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        existing = []
        for secret in required_secrets:
            if secret in result.stdout:
                existing.append(secret)
        missing = [s for s in required_secrets if s not in existing]
        return existing, missing
    except Exception:
        return [], required_secrets


def generate_modal_app(directive_name: str, parsed: dict, available_secrets: list = None) -> str:
    """Generate a Modal app Python file for the directive."""
    
    all_secrets = get_required_secrets(parsed)
    # Only include secrets that exist if available_secrets is provided
    if available_secrets is not None:
        secrets = [s for s in all_secrets if s in available_secrets]
    else:
        secrets = all_secrets
    
    # Always need at least openrouter or anthropic for LLM
    if not secrets:
        secrets = ["openrouter-secret"]  # Default fallback
    
    secrets_code = ",\n    ".join([f'modal.Secret.from_name("{s}")' for s in secrets])
    
    # Build pip packages list - comprehensive defaults for most workflows
    pip_packages = [
        "anthropic",
        "python-dotenv",
        "requests",
        "fastapi",
        "pandas",
        "apify-client",
        "slack-sdk",
        "openai",  # Used by OpenRouter and direct OpenAI calls
    ]
    if any(g in parsed["integrations"] for g in ["google_docs", "google_sheets", "gmail"]):
        pip_packages.extend(["google-auth", "google-auth-oauthlib", "google-api-python-client", "gspread"])
    
    pip_install = ", ".join([f'"{p}"' for p in pip_packages])
    
    # Determine which execution scripts to include (only ones that exist)
    all_scripts = parsed["execution_scripts"] or [directive_name.replace("-", "_")]
    scripts_to_include = [s for s in all_scripts if (EXECUTION_DIR / f"{s}.py").exists()]
    if not scripts_to_include:
        # Fallback: try directive name as script
        fallback = directive_name.replace("-", "_")
        if (EXECUTION_DIR / f"{fallback}.py").exists():
            scripts_to_include = [fallback]
        else:
            scripts_to_include = all_scripts  # Use original list even if missing
    
    # Build skill files upload code (only referenced skills)
    skill_bibles = parsed.get("skill_bibles", [])
    if skill_bibles:
        skill_lines = []
        for skill in skill_bibles:
            skill_file = SKILLS_DIR / f"SKILL_BIBLE_{skill}.md"
            if skill_file.exists():
                skill_lines.append(f'    .add_local_file("{skill_file}", remote_path="/app/skills/SKILL_BIBLE_{skill}.md")')
        skill_files_code = "\n".join(skill_lines) if skill_lines else ""
    else:
        skill_files_code = ""
    
    # Include Google OAuth tokens if workflow uses Google integrations
    google_token_code = ""
    if any(g in parsed["integrations"] for g in ["google_docs", "google_sheets", "gmail"]):
        token_files = [
            ("token_docs.json", "token_docs.json"),  # Google Docs token
            ("token_docs.json", "token.json"),  # Also as token.json for some scripts
            ("token_gmail.json", "token_gmail.json"),
            ("credentials.json", "credentials.json"),
            ("token.pickle", "token.pickle"),  # Some scripts use pickle format
        ]
        token_lines = []
        for local_name, remote_name in token_files:
            token_file = PROJECT_ROOT / local_name
            if token_file.exists():
                token_lines.append(f'    .add_local_file("{token_file}", remote_path="/app/{remote_name}")')
        google_token_code = "\n".join(token_lines) + "\n" if token_lines else ""
    # Generate build version for cache busting
    from datetime import datetime as dt
    build_version = dt.now().strftime('%Y%m%d_%H%M%S')
    
    # Build the Modal app template
    app_code = f'''#!/usr/bin/env python3
"""
Modal App: {directive_name}
Auto-generated by deploy_to_modal.py
Build: {build_version}

Description: {parsed["description"]}

Deploy: modal deploy execution/modal_apps/{directive_name}_modal.py
Logs:   modal logs {directive_name}
"""

import modal
import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

app = modal.App("{directive_name}")

# Build image with required packages (Build: {build_version})
image = (
    modal.Image.debian_slim(python_version="3.11")
    .run_commands("echo 'Build: {build_version}'")
    .pip_install({pip_install})
    .add_local_dir("{EXECUTION_DIR}", remote_path="/app/execution")
    .add_local_dir("{DIRECTIVES_DIR}", remote_path="/app/directives")
    .add_local_file("{PROJECT_ROOT}/.env", remote_path="/app/.env")
{google_token_code}{skill_files_code})

secrets = [
    {secrets_code}
]


def slack_notify(message: str):
    """Send notification to Slack if configured."""
    import requests
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return
    try:
        requests.post(webhook_url, json={{"text": message}}, timeout=5)
    except Exception:
        pass


def run_script(script_name: str, args: list = None) -> dict:
    """Run an execution script and return output."""
    script_path = f"/app/execution/{{script_name}}.py"
    if not Path(script_path).exists():
        return {{"error": f"Script not found: {{script_name}}"}}
    
    cmd = ["python3", script_path] + (args or [])
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
            cwd="/app",
            env={{**os.environ, "PYTHONPATH": "/app"}}
        )
        return {{
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0
        }}
    except subprocess.TimeoutExpired:
        return {{"error": "Script timed out after 10 minutes"}}
    except Exception as e:
        return {{"error": str(e)}}


@app.function(image=image, secrets=secrets, timeout=900)
@modal.fastapi_endpoint(method="POST")
def webhook(payload: dict = None):
    """
    Webhook endpoint for {directive_name}
    
    POST /webhook
    Body: {{"data": {{...}}}}
    """
    payload = payload or {{}}
    input_data = payload.get("data", payload)
    
    slack_notify(f"🚀 *{{'{directive_name}'}}* triggered\\n```{{json.dumps(input_data, indent=2)[:500]}}```")
    
    try:
        # Build command args from input data
        args = []
        for key, value in input_data.items():
            if value is not None and value != "":
                # Keep original key format (scripts may use underscores or hyphens)
                args.extend([f"--{{key}}", str(value)])
        
        # Run the main execution script
        result = run_script("{scripts_to_include[0] if scripts_to_include else directive_name.replace('-', '_')}", args)
        
        if result.get("success"):
            slack_notify(f"✅ *{{'{directive_name}'}}* completed successfully")
        else:
            slack_notify(f"❌ *{{'{directive_name}'}}* failed:\\n```{{result.get('stderr', result.get('error', 'Unknown error'))[:500]}}```")
        
        return {{
            "status": "success" if result.get("success") else "error",
            "directive": "{directive_name}",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }}
        
    except Exception as e:
        slack_notify(f"💥 *{{'{directive_name}'}}* error: {{str(e)}}")
        return {{"status": "error", "error": str(e)}}


@app.function(image=image, secrets=secrets, timeout=30)
@modal.fastapi_endpoint(method="GET")
def health():
    """Health check endpoint."""
    return {{
        "status": "healthy",
        "app": "{directive_name}",
        "timestamp": datetime.utcnow().isoformat()
    }}


@app.function(image=image, secrets=secrets, timeout=30)
@modal.fastapi_endpoint(method="GET")
def info():
    """Get info about this workflow."""
    return {{
        "name": "{directive_name}",
        "description": "{parsed['description']}",
        "integrations": {parsed['integrations']},
        "scripts": {scripts_to_include},
        "inputs": {parsed['inputs']}
    }}
'''
    
    return app_code


def deploy_to_modal(app_file: Path) -> tuple[bool, str]:
    """Deploy the Modal app and return success status and URL."""
    try:
        result = subprocess.run(
            ["modal", "deploy", str(app_file)],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            return False, f"Deployment failed: {result.stderr}"
        
        # Parse URL from output
        url_match = re.search(r"https://[^\s]+\.modal\.run", result.stdout)
        url = url_match.group(0) if url_match else "URL not found in output"
        
        return True, url
        
    except subprocess.TimeoutExpired:
        return False, "Deployment timed out"
    except FileNotFoundError:
        return False, "Modal CLI not found. Run: pip install modal && python3 -m modal setup"
    except Exception as e:
        return False, str(e)


def ensure_modal_installed() -> bool:
    """Check if Modal is installed, install if missing."""
    try:
        subprocess.run(["modal", "--version"], capture_output=True, timeout=10)
        return True
    except FileNotFoundError:
        print("Installing Modal CLI...")
        result = subprocess.run(
            ["pip", "install", "modal"],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0


def auto_setup_secrets() -> list[str]:
    """Auto-create Modal secrets from .env file. Returns list of created secrets."""
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return []
    
    env_vars = {}
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            env_vars[key.strip()] = value.strip().strip('"').strip("'")
    
    secrets_to_create = [
        ("anthropic-secret", ["ANTHROPIC_API_KEY"]),
        ("openrouter-secret", ["OPENROUTER_API_KEY"]),
        ("slack-webhook", ["SLACK_WEBHOOK_URL"]),
    ]
    
    created = []
    for secret_name, keys in secrets_to_create:
        key_values = []
        for key in keys:
            if key in env_vars and env_vars[key]:
                key_values.append(f"{key}={env_vars[key]}")
        
        if key_values:
            cmd = ["modal", "secret", "create", secret_name] + key_values
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 or "already exists" in result.stderr:
                created.append(secret_name)
    
    return created


def main():
    parser = argparse.ArgumentParser(description="Deploy workflow to Modal AI")
    parser.add_argument("--directive", "-d", help="Directive name to deploy")
    parser.add_argument("--app-name", "-n", help="Custom Modal app name")
    parser.add_argument("--list", "-l", action="store_true", help="List available directives")
    parser.add_argument("--dry-run", action="store_true", help="Generate without deploying")
    parser.add_argument("--info", "-i", help="Show parsed info for a directive")
    parser.add_argument("--setup-secrets", action="store_true", help="Create Modal secrets from .env file")
    parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation prompts")
    parser.add_argument("--auto", "-a", action="store_true", help="Fully automated mode: auto-setup secrets, no prompts, JSON output")
    
    args = parser.parse_args()
    
    # Ensure modal_apps directory exists
    MODAL_APPS_DIR.mkdir(parents=True, exist_ok=True)
    
    # AUTO MODE: Fully automated deployment with JSON output
    if args.auto and args.directive:
        directive_name = args.directive.replace(".md", "")
        app_name = args.app_name or directive_name
        
        # Step 1: Ensure Modal is installed
        if not ensure_modal_installed():
            print(json.dumps({"status": "error", "error": "Failed to install Modal CLI"}))
            return 1
        
        # Step 2: Auto-setup secrets from .env
        auto_setup_secrets()
        
        # Step 3: Load and parse directive
        try:
            content = load_directive(directive_name)
        except FileNotFoundError:
            print(json.dumps({
                "status": "error",
                "error": f"Directive not found: {directive_name}",
                "available": list_directives()[:20]
            }))
            return 1
        
        parsed = parse_directive(content)
        required_secrets = get_required_secrets(parsed)
        existing, _ = check_modal_secrets(required_secrets)
        
        # Step 4: Generate and deploy
        app_code = generate_modal_app(app_name, parsed, available_secrets=existing if existing else None)
        app_file = MODAL_APPS_DIR / f"{app_name}_modal.py"
        app_file.write_text(app_code)
        
        success, result = deploy_to_modal(app_file)
        
        if success:
            # Parse workspace from URL
            base_url = result.replace("-webhook.modal.run", "")
            output = {
                "status": "success",
                "directive": directive_name,
                "description": parsed["description"],
                "endpoints": {
                    "webhook": result,
                    "health": f"{base_url}-health.modal.run",
                    "info": f"{base_url}-info.modal.run"
                },
                "example_curl": f'curl -X POST "{result}" -H "Content-Type: application/json" -d \'{{"data": {{}}}}\''
            }
            print(json.dumps(output, indent=2))
            return 0
        else:
            print(json.dumps({"status": "error", "error": result}))
            return 1
    
    if args.setup_secrets:
        print("\n🔐 Setting up Modal secrets from .env file...\n")
        env_file = PROJECT_ROOT / ".env"
        if not env_file.exists():
            print("❌ .env file not found")
            return 1
        
        # Parse .env file
        env_vars = {}
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
        
        # Create secrets
        secrets_to_create = [
            ("anthropic-secret", ["ANTHROPIC_API_KEY"]),
            ("openrouter-secret", ["OPENROUTER_API_KEY"]),
            ("slack-webhook", ["SLACK_WEBHOOK_URL"]),
        ]
        
        for secret_name, keys in secrets_to_create:
            key_values = []
            for key in keys:
                if key in env_vars and env_vars[key]:
                    key_values.append(f"{key}={env_vars[key]}")
            
            if key_values:
                cmd = ["modal", "secret", "create", secret_name] + key_values
                print(f"   Creating {secret_name}...")
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ {secret_name} created")
                elif "already exists" in result.stderr:
                    print(f"   ⏭️  {secret_name} already exists")
                else:
                    print(f"   ❌ {secret_name} failed: {result.stderr[:100]}")
            else:
                print(f"   ⏭️  {secret_name} - no keys found in .env")
        
        print("\n✅ Secret setup complete")
        return 0
    
    if args.list:
        print("\n📋 Available Directives:\n")
        for d in list_directives():
            print(f"  - {d}")
        print(f"\n  Total: {len(list_directives())} directives")
        print("\nUsage: python3 execution/deploy_to_modal.py --directive <name>")
        return 0
    
    if args.info:
        try:
            content = load_directive(args.info)
            parsed = parse_directive(content)
            print(f"\n📋 Directive: {args.info}\n")
            print(f"Description: {parsed['description']}")
            print(f"Scripts: {parsed['execution_scripts']}")
            print(f"Integrations: {parsed['integrations']}")
            print(f"Has LLM: {parsed['has_llm']}")
            print(f"Skill Bibles: {parsed.get('skill_bibles', [])}")
            print(f"Inputs: {json.dumps(parsed['inputs'], indent=2)}")
            print(f"Required Secrets: {get_required_secrets(parsed)}")
            return 0
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return 1
    
    if not args.directive:
        parser.print_help()
        print("\n❌ Error: --directive is required")
        return 1
    
    directive_name = args.directive.replace(".md", "")
    app_name = args.app_name or directive_name
    
    print(f"\n🚀 Deploying: {directive_name}")
    print(f"   App name: {app_name}")
    
    # Load and parse directive
    try:
        content = load_directive(directive_name)
    except FileNotFoundError:
        print(f"\n❌ Directive not found: {directive_name}")
        print("\nAvailable directives:")
        for d in list_directives()[:10]:
            print(f"  - {d}")
        if len(list_directives()) > 10:
            print(f"  ... and {len(list_directives()) - 10} more")
        return 1
    
    parsed = parse_directive(content)
    required_secrets = get_required_secrets(parsed)
    print(f"   Description: {parsed['description'][:60]}...")
    print(f"   Scripts: {parsed['execution_scripts'] or ['(auto-detect)']}")
    print(f"   Integrations: {parsed['integrations']}")
    print(f"   Secrets: {required_secrets}")
    
    # Check for missing secrets
    existing, missing = check_modal_secrets(required_secrets)
    if missing:
        print(f"\n⚠️  Missing Modal secrets: {missing}")
        print("\n   Create them at https://modal.com/secrets or run:")
        for secret in missing:
            if secret == "anthropic-secret":
                print(f'   modal secret create {secret} ANTHROPIC_API_KEY=<your-key>')
            elif secret == "openrouter-secret":
                print(f'   modal secret create {secret} OPENROUTER_API_KEY=<your-key>')
            elif secret == "slack-webhook":
                print(f'   modal secret create {secret} SLACK_WEBHOOK_URL=<your-url>')
            elif secret == "google-token":
                print(f'   modal secret create {secret} GOOGLE_TOKEN_JSON=<your-json>')
            else:
                print(f'   modal secret create {secret} <KEY>=<value>')
        
        if not args.dry_run and not args.force:
            try:
                response = input("\n   Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    print("   Aborted. Create secrets and try again.")
                    return 1
            except EOFError:
                print("\n   Use --force to skip this prompt")
                return 1
    
    # Generate Modal app (pass existing secrets to filter)
    app_code = generate_modal_app(app_name, parsed, available_secrets=existing)
    app_file = MODAL_APPS_DIR / f"{app_name}_modal.py"
    app_file.write_text(app_code)
    print(f"\n✅ Generated: {app_file}")
    
    if args.dry_run:
        print("\n🔍 Dry run - skipping deployment")
        print(f"\nTo deploy manually:")
        print(f"  modal deploy {app_file}")
        return 0
    
    # Deploy
    print("\n📦 Deploying to Modal...")
    success, result = deploy_to_modal(app_file)
    
    if success:
        print(f"\n✅ Deployment successful!")
        print(f"   Webhook URL: {result}")
        print(f"\n   Test with:")
        print(f'   curl -X POST "{result}" -H "Content-Type: application/json" -d \'{{"data": {{}}}}\' ')
    else:
        print(f"\n❌ Deployment failed: {result}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
