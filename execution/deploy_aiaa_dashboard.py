#!/usr/bin/env python3
"""
Deploy AIAA Dashboard to Railway

This script automates the deployment of the AIAA Agentic OS Dashboard to Railway.
It handles:
- Creating a new Railway project (or using existing)
- Setting up environment variables
- Creating secure password-protected authentication
- Deploying the dashboard app
- Configuring the public domain

Usage:
    python3 execution/deploy_aiaa_dashboard.py --username admin --password mysecret
    python3 execution/deploy_aiaa_dashboard.py --project-id existing-project-id
    python3 execution/deploy_aiaa_dashboard.py --interactive

Requirements:
    - Railway CLI installed and authenticated (brew install railway && railway login)
    - RAILWAY_TOKEN environment variable (optional, for non-interactive)
"""

import argparse
import hashlib
import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DASHBOARD_DIR = PROJECT_ROOT / "railway_apps" / "aiaa_dashboard"


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def run_command(cmd: list, cwd: str = None, capture: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            cwd=cwd,
            timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def check_railway_cli() -> bool:
    """Check if Railway CLI is installed and authenticated."""
    code, stdout, stderr = run_command(["railway", "--version"])
    if code != 0:
        print("ERROR: Railway CLI not installed. Run: brew install railway")
        return False
    
    # Check if logged in
    code, stdout, stderr = run_command(["railway", "whoami"])
    if code != 0:
        print("ERROR: Not logged into Railway. Run: railway login")
        return False
    
    print(f"  Railway CLI: OK")
    return True


def get_env_vars_from_dotenv() -> dict:
    """Load environment variables from .env file."""
    env_file = PROJECT_ROOT / ".env"
    env_vars = {}
    
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value:
                    env_vars[key] = value
    
    return env_vars


def create_railway_project(name: str = "aiaa-dashboard") -> str:
    """Create a new Railway project and return project ID."""
    print(f"\n  Creating Railway project: {name}")
    
    code, stdout, stderr = run_command(["railway", "init", "--name", name], cwd=str(DASHBOARD_DIR))
    
    if code != 0:
        # Project might already exist, try to link
        print(f"  Project creation returned: {stderr}")
        return None
    
    # Get project ID
    code, stdout, stderr = run_command(["railway", "status", "--json"], cwd=str(DASHBOARD_DIR))
    if code == 0:
        try:
            status = json.loads(stdout)
            return status.get("project", {}).get("id")
        except:
            pass
    
    return None


def link_railway_project(project_id: str) -> bool:
    """Link to an existing Railway project."""
    print(f"\n  Linking to Railway project: {project_id}")
    
    code, stdout, stderr = run_command(
        ["railway", "link", project_id],
        cwd=str(DASHBOARD_DIR)
    )
    
    return code == 0


def set_railway_variables(variables: dict) -> bool:
    """Set environment variables in Railway."""
    print(f"\n  Setting {len(variables)} environment variables...")
    
    for key, value in variables.items():
        # Use railway variables --set
        code, stdout, stderr = run_command(
            ["railway", "variables", "--set", f"{key}={value}"],
            cwd=str(DASHBOARD_DIR)
        )
        if code != 0:
            print(f"    WARNING: Failed to set {key}: {stderr}")
        else:
            masked = f"{value[:4]}...{value[-4:]}" if len(value) > 10 else "***"
            print(f"    Set {key} = {masked}")
    
    return True


def deploy_to_railway() -> tuple[bool, str]:
    """Deploy the dashboard to Railway."""
    print("\n  Deploying to Railway...")
    
    code, stdout, stderr = run_command(
        ["railway", "up", "--detach"],
        cwd=str(DASHBOARD_DIR),
        capture=False  # Show output in real-time
    )
    
    if code != 0:
        return False, stderr
    
    # Wait for deployment
    print("\n  Waiting for deployment to complete...")
    time.sleep(10)
    
    # Get the domain
    code, stdout, stderr = run_command(
        ["railway", "domain"],
        cwd=str(DASHBOARD_DIR)
    )
    
    domain = stdout.strip() if code == 0 else None
    
    if not domain:
        # Try to generate domain
        code, stdout, stderr = run_command(
            ["railway", "domain", "--generate"],
            cwd=str(DASHBOARD_DIR)
        )
        domain = stdout.strip() if code == 0 else "Unable to get domain"
    
    return True, domain


def main():
    parser = argparse.ArgumentParser(description="Deploy AIAA Dashboard to Railway")
    parser.add_argument("--username", "-u", default="admin", help="Dashboard login username")
    parser.add_argument("--password", "-p", help="Dashboard login password (will be hashed)")
    parser.add_argument("--project-id", help="Existing Railway project ID to use")
    parser.add_argument("--project-name", default="aiaa-dashboard", help="Name for new Railway project")
    parser.add_argument("--interactive", "-i", action="store_true", help="Prompt for missing values")
    parser.add_argument("--skip-env", action="store_true", help="Skip setting environment variables from .env")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without doing it")
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("  AIAA Dashboard Deployment")
    print("=" * 60)
    
    # Check prerequisites
    print("\n[1/5] Checking prerequisites...")
    if not check_railway_cli():
        return 1
    
    if not DASHBOARD_DIR.exists():
        print(f"ERROR: Dashboard directory not found: {DASHBOARD_DIR}")
        return 1
    print(f"  Dashboard source: {DASHBOARD_DIR}")
    
    # Get password
    password = args.password
    if not password:
        if args.interactive:
            import getpass
            password = getpass.getpass("Enter dashboard password: ")
        else:
            # Generate random password
            password = secrets.token_urlsafe(12)
            print(f"\n  Generated password: {password}")
    
    password_hash = hash_password(password)
    print(f"  Password hash generated: {password_hash[:16]}...")
    
    if args.dry_run:
        print("\n[DRY RUN] Would deploy with:")
        print(f"  Username: {args.username}")
        print(f"  Password: {password}")
        print(f"  Password Hash: {password_hash}")
        return 0
    
    # Setup Railway project
    print("\n[2/5] Setting up Railway project...")
    
    if args.project_id:
        if not link_railway_project(args.project_id):
            print("ERROR: Failed to link to Railway project")
            return 1
    else:
        # Create new project or link existing
        project_id = create_railway_project(args.project_name)
        if not project_id:
            print("  Note: Using existing linked project or will create on deploy")
    
    # Set environment variables
    print("\n[3/5] Configuring environment variables...")
    
    variables = {
        "DASHBOARD_USERNAME": args.username,
        "DASHBOARD_PASSWORD_HASH": password_hash,
        "FLASK_SECRET_KEY": secrets.token_hex(32),
    }
    
    # Load from .env if not skipped
    if not args.skip_env:
        env_vars = get_env_vars_from_dotenv()
        
        # Only include relevant API keys
        keys_to_include = [
            "OPENROUTER_API_KEY",
            "PERPLEXITY_API_KEY",
            "SLACK_WEBHOOK_URL",
            "CALENDLY_API_KEY",
            "GOOGLE_OAUTH_TOKEN_JSON",
            "ANTHROPIC_API_KEY",
        ]
        
        for key in keys_to_include:
            if key in env_vars:
                variables[key] = env_vars[key]
    
    set_railway_variables(variables)
    
    # Deploy
    print("\n[4/5] Deploying dashboard...")
    success, result = deploy_to_railway()
    
    if not success:
        print(f"ERROR: Deployment failed: {result}")
        return 1
    
    # Summary
    print("\n[5/5] Deployment complete!")
    print("\n" + "=" * 60)
    print("  AIAA Dashboard Deployed Successfully!")
    print("=" * 60)
    print(f"\n  URL: https://{result}")
    print(f"\n  Login Credentials:")
    print(f"    Username: {args.username}")
    print(f"    Password: {password}")
    print("\n  Save these credentials - the password cannot be recovered!")
    print("=" * 60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
