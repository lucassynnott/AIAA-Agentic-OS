#!/usr/bin/env python3
"""
Deploy to Cloudflare Pages - Automated Deployment Script

Deploys static sites to Cloudflare Pages using either Wrangler CLI or direct API.

Usage:
    # Deploy a directory
    python3 execution/deploy_to_cloudflare.py \
        --directory .tmp/landing_pages/my_product \
        --project-name my-landing-page

    # Deploy and get live URL
    python3 execution/deploy_to_cloudflare.py \
        --directory ./dist \
        --project-name my-site \
        --production

    # List existing projects
    python3 execution/deploy_to_cloudflare.py --list

Environment Variables:
    CLOUDFLARE_API_TOKEN      - API token with Pages Edit permission
    CLOUDFLARE_ACCOUNT_ID     - Your Cloudflare account ID

Follows directive: directives/ai_landing_page_generator.md
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


class CloudflareDeployer:
    """Deploy static sites to Cloudflare Pages"""

    def __init__(self):
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/pages/projects"

    def log(self, message: str, level: str = "INFO"):
        """Log progress"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}.get(level, "")
        print(f"[{timestamp}] {prefix} {message}")

    def _get_headers(self) -> dict:
        """Get API headers"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def validate_credentials(self) -> bool:
        """Validate Cloudflare credentials"""
        if not self.api_token:
            self.log("CLOUDFLARE_API_TOKEN not set", "ERROR")
            self.log("Get token from: https://dash.cloudflare.com/profile/api-tokens", "INFO")
            return False

        if not self.account_id:
            self.log("CLOUDFLARE_ACCOUNT_ID not set", "ERROR")
            self.log("Find account ID in your Cloudflare dashboard URL", "INFO")
            return False

        # Test API connection
        try:
            response = requests.get(self.base_url, headers=self._get_headers(), timeout=10)
            if response.status_code == 200:
                self.log("Cloudflare credentials validated", "SUCCESS")
                return True
            else:
                self.log(f"API error: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Connection error: {e}", "ERROR")
            return False

    def list_projects(self) -> list:
        """List all Cloudflare Pages projects"""
        if not self.validate_credentials():
            return []

        try:
            response = requests.get(self.base_url, headers=self._get_headers(), timeout=30)
            if response.status_code == 200:
                projects = response.json().get("result", [])
                return projects
            else:
                self.log(f"Failed to list projects: {response.text}", "ERROR")
                return []
        except Exception as e:
            self.log(f"Error listing projects: {e}", "ERROR")
            return []

    def get_project(self, project_name: str) -> dict:
        """Get project details"""
        try:
            response = requests.get(
                f"{self.base_url}/{project_name}",
                headers=self._get_headers(),
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("result", {})
            return {}
        except Exception:
            return {}

    def create_project(self, project_name: str) -> bool:
        """Create a new Cloudflare Pages project"""
        self.log(f"Creating project: {project_name}", "INFO")

        try:
            response = requests.post(
                self.base_url,
                headers=self._get_headers(),
                json={
                    "name": project_name,
                    "production_branch": "main"
                },
                timeout=30
            )

            if response.status_code in [200, 201]:
                self.log(f"Project created: {project_name}", "SUCCESS")
                return True
            elif response.status_code == 409:
                self.log(f"Project already exists: {project_name}", "INFO")
                return True
            else:
                self.log(f"Failed to create project: {response.text}", "ERROR")
                return False

        except Exception as e:
            self.log(f"Error creating project: {e}", "ERROR")
            return False

    def deploy_with_wrangler(self, directory: str, project_name: str, production: bool = False) -> dict:
        """Deploy using Wrangler CLI (recommended method)"""
        self.log(f"Deploying with Wrangler to {project_name}...", "INFO")

        # Build command
        cmd = [
            "npx", "wrangler", "pages", "deploy",
            directory,
            "--project-name", project_name
        ]

        if production:
            cmd.append("--branch=main")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
                env={
                    **os.environ,
                    "CLOUDFLARE_API_TOKEN": self.api_token,
                    "CLOUDFLARE_ACCOUNT_ID": self.account_id
                }
            )

            output = result.stdout + result.stderr

            if result.returncode == 0:
                # Parse URL from output
                url_match = re.search(r'(https://[^\s]+\.pages\.dev)', output)
                live_url = url_match.group(1) if url_match else f"https://{project_name}.pages.dev"

                self.log(f"Deployment successful!", "SUCCESS")
                self.log(f"Live URL: {live_url}", "INFO")

                return {
                    "success": True,
                    "liveUrl": live_url,
                    "projectName": project_name,
                    "method": "wrangler",
                    "deployedAt": datetime.now().isoformat()
                }
            else:
                self.log(f"Wrangler deployment failed", "ERROR")
                self.log(f"Output: {output}", "ERROR")
                return {"success": False, "error": output}

        except FileNotFoundError:
            self.log("Wrangler not found. Install with: npm install -g wrangler", "ERROR")
            return {"success": False, "error": "Wrangler not installed"}

        except subprocess.TimeoutExpired:
            self.log("Deployment timed out", "ERROR")
            return {"success": False, "error": "Timeout"}

        except Exception as e:
            self.log(f"Deployment error: {e}", "ERROR")
            return {"success": False, "error": str(e)}

    def deploy(self, directory: str, project_name: str, production: bool = False) -> dict:
        """Deploy a directory to Cloudflare Pages"""
        self.log(f"Starting deployment to Cloudflare Pages", "INFO")
        self.log(f"   Directory: {directory}", "INFO")
        self.log(f"   Project: {project_name}", "INFO")

        # Validate inputs
        directory_path = Path(directory)
        if not directory_path.exists():
            self.log(f"Directory not found: {directory}", "ERROR")
            return {"success": False, "error": "Directory not found"}

        if not (directory_path / "index.html").exists():
            self.log("Warning: No index.html found in directory", "WARNING")

        # Validate credentials
        if not self.validate_credentials():
            return {"success": False, "error": "Invalid credentials"}

        # Ensure project exists
        existing_project = self.get_project(project_name)
        if not existing_project:
            if not self.create_project(project_name):
                return {"success": False, "error": "Failed to create project"}

        # Deploy using Wrangler
        return self.deploy_with_wrangler(directory, project_name, production)

    def get_deployments(self, project_name: str) -> list:
        """Get list of deployments for a project"""
        try:
            response = requests.get(
                f"{self.base_url}/{project_name}/deployments",
                headers=self._get_headers(),
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("result", [])
            return []
        except Exception:
            return []

    def delete_deployment(self, project_name: str, deployment_id: str) -> bool:
        """Delete a specific deployment"""
        try:
            response = requests.delete(
                f"{self.base_url}/{project_name}/deployments/{deployment_id}",
                headers=self._get_headers(),
                timeout=30
            )
            return response.status_code in [200, 204]
        except Exception:
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Deploy static sites to Cloudflare Pages"
    )

    parser.add_argument("--directory", "-d", help="Directory to deploy")
    parser.add_argument("--project-name", "-p", help="Cloudflare Pages project name")
    parser.add_argument("--production", action="store_true", help="Deploy to production branch")
    parser.add_argument("--list", "-l", action="store_true", help="List all projects")
    parser.add_argument("--info", "-i", help="Get info for a project")
    parser.add_argument("--deployments", help="List deployments for a project")

    args = parser.parse_args()

    deployer = CloudflareDeployer()

    # List projects
    if args.list:
        projects = deployer.list_projects()
        if projects:
            print("\n📁 Cloudflare Pages Projects:")
            print("-" * 50)
            for project in projects:
                subdomain = project.get("subdomain", "N/A")
                name = project.get("name", "Unknown")
                print(f"  • {name}")
                print(f"    URL: https://{subdomain}")
                if project.get("domains"):
                    for domain in project["domains"]:
                        print(f"    Custom: {domain}")
            print("-" * 50)
            print(f"Total: {len(projects)} projects")
        else:
            print("No projects found or error occurred")
        return 0

    # Get project info
    if args.info:
        project = deployer.get_project(args.info)
        if project:
            print(f"\n📋 Project: {project.get('name')}")
            print(f"   Subdomain: {project.get('subdomain')}")
            print(f"   Domains: {', '.join(project.get('domains', []))}")
            print(f"   Created: {project.get('created_on')}")
            latest = project.get("canonical_deployment", {})
            if latest:
                print(f"   Latest deployment: {latest.get('url')}")
        else:
            print(f"Project '{args.info}' not found")
        return 0

    # List deployments
    if args.deployments:
        deployments = deployer.get_deployments(args.deployments)
        if deployments:
            print(f"\n🚀 Deployments for {args.deployments}:")
            print("-" * 50)
            for dep in deployments[:10]:
                status = "✅" if dep.get("latest_stage", {}).get("status") == "success" else "⏳"
                print(f"  {status} {dep.get('id', 'N/A')[:8]}...")
                print(f"     URL: {dep.get('url', 'N/A')}")
                print(f"     Created: {dep.get('created_on', 'N/A')}")
            print(f"\nShowing {min(len(deployments), 10)} of {len(deployments)} deployments")
        else:
            print(f"No deployments found for '{args.deployments}'")
        return 0

    # Deploy
    if args.directory and args.project_name:
        result = deployer.deploy(
            directory=args.directory,
            project_name=args.project_name,
            production=args.production
        )

        if result["success"]:
            print(f"\n✅ Deployment successful!")
            print(f"   Live URL: {result.get('liveUrl')}")
            return 0
        else:
            print(f"\n❌ Deployment failed: {result.get('error')}")
            return 1

    # No valid action
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
