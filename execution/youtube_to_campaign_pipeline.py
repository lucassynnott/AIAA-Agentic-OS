#!/usr/bin/env python3
"""
YouTube to Campaign Pipeline - Complete Automation System

This is the MASTER orchestrator that:
1. Mines knowledge from YouTube (best practices)
2. Creates skill bibles for each campaign phase
3. Runs full campaign pipeline with learned best practices

Phases covered:
- Client Research
- Meta Ads Setup
- Ad Copy Generation
- Ad Image Generation
- Landing Page Generation
- Landing Page Images
- CRM Lead Flow
- Follow-up Sequences

Usage:
    python3 execution/youtube_to_campaign_pipeline.py \
        --client "Acme Corp" \
        --website "https://acmecorp.com" \
        --offer "AI Lead Generation" \
        --learn-from-youtube \
        --deploy-agents 10

Follows directive: directives/youtube_to_campaign_pipeline.md
"""

import os
import sys
import json
import argparse
import time
import subprocess
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

# Campaign phases and their YouTube research topics
CAMPAIGN_PHASES = {
    "client_research": {
        "name": "Client Research",
        "keywords": ["B2B market research", "customer avatar", "ideal client profile"],
        "skill_bible": "SKILL_BIBLE_client_research.md"
    },
    "meta_ads_setup": {
        "name": "Meta Ads Setup",
        "keywords": ["Facebook ads structure", "Meta ads campaign setup", "Facebook ad targeting"],
        "skill_bible": "SKILL_BIBLE_meta_ads_setup.md"
    },
    "ad_copy": {
        "name": "Ad Copy Writing",
        "keywords": ["Facebook ad copywriting", "direct response ad copy", "high converting ad copy"],
        "skill_bible": "SKILL_BIBLE_ad_copywriting.md"
    },
    "ad_creative": {
        "name": "Ad Creative/Images",
        "keywords": ["Facebook ad creative", "ad design best practices", "scroll stopping ads"],
        "skill_bible": "SKILL_BIBLE_ad_creative.md"
    },
    "landing_pages": {
        "name": "Landing Page Creation",
        "keywords": ["high converting landing pages", "landing page copywriting", "sales page structure"],
        "skill_bible": "SKILL_BIBLE_landing_pages.md"
    },
    "crm_automation": {
        "name": "CRM & Automation",
        "keywords": ["CRM automation", "sales pipeline setup", "lead nurturing automation"],
        "skill_bible": "SKILL_BIBLE_crm_automation.md"
    },
    "email_sequences": {
        "name": "Email Follow-up Sequences",
        "keywords": ["email nurture sequences", "sales email sequences", "follow up email strategy"],
        "skill_bible": "SKILL_BIBLE_email_sequences.md"
    }
}


class YouTubeToCampaignPipeline:
    """Master orchestrator for the complete pipeline."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir = Path(__file__).parent.parent / "skills"
        self.skill_bibles = {}
        
    def log(self, message: str, level: str = "info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"info": "  ", "success": "✓ ", "error": "✗ ", "phase": "\n▶ "}
        print(f"[{timestamp}] {prefix.get(level, '  ')}{message}")
    
    def run_youtube_knowledge_miner(self, keywords: list, phase_name: str, max_channels: int = 5, videos_per_channel: int = 3) -> Path:
        """Run the YouTube knowledge miner for a specific phase."""
        self.log(f"Mining YouTube for: {phase_name}", "phase")
        
        output_subdir = self.output_dir / "knowledge" / phase_name.lower().replace(" ", "_")
        
        cmd = [
            "python3",
            str(Path(__file__).parent / "youtube_knowledge_miner.py"),
            "--niche"] + keywords + [
            "--max-channels", str(max_channels),
            "--videos-per-channel", str(videos_per_channel),
            "--min-subscribers", "10000",
            "--min-views", "5000",
            "--min-skill-rating", "6",
            "--output-dir", str(output_subdir),
            "--parallel", "2"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            if result.returncode == 0:
                self.log(f"Knowledge mining complete for {phase_name}", "success")
                
                # Look for any SKILL_BIBLE file in the output directory
                for f in output_subdir.glob("SKILL_BIBLE_*.md"):
                    return f
                
                # Check skills directory for recently created files
                for f in sorted(self.skills_dir.glob("SKILL_BIBLE_*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
                    # Check if file was created in last 30 minutes and matches phase
                    import time
                    if (time.time() - f.stat().st_mtime) < 1800:
                        return f
            else:
                self.log(f"Mining failed for {phase_name}: {result.stderr[:200]}", "error")
        except subprocess.TimeoutExpired:
            self.log(f"Mining timed out for {phase_name}", "error")
        except Exception as e:
            self.log(f"Mining error for {phase_name}: {e}", "error")
        
        return None
    
    def learn_from_youtube(self, phases: list = None, parallel: int = 3) -> dict:
        """Learn best practices from YouTube for all campaign phases."""
        self.log("=" * 60)
        self.log("PHASE 1: LEARNING FROM YOUTUBE")
        self.log("=" * 60)
        
        if phases is None:
            phases = list(CAMPAIGN_PHASES.keys())
        
        results = {}
        
        # Run knowledge mining for each phase (can be parallelized)
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {}
            
            for phase_key in phases:
                phase = CAMPAIGN_PHASES[phase_key]
                future = executor.submit(
                    self.run_youtube_knowledge_miner,
                    phase["keywords"],
                    phase["name"],
                    max_channels=5,
                    videos_per_channel=3
                )
                futures[future] = phase_key
            
            for future in as_completed(futures):
                phase_key = futures[future]
                try:
                    skill_bible_path = future.result()
                    if skill_bible_path:
                        self.skill_bibles[phase_key] = skill_bible_path
                        results[phase_key] = {"status": "success", "skill_bible": str(skill_bible_path)}
                    else:
                        results[phase_key] = {"status": "failed"}
                except Exception as e:
                    results[phase_key] = {"status": "error", "error": str(e)}
        
        self.log(f"Learned from YouTube for {len(self.skill_bibles)}/{len(phases)} phases", "success")
        return results
    
    def load_existing_skill_bibles(self) -> dict:
        """Load any existing skill bibles from the skills directory."""
        self.log("Loading existing skill bibles...")
        
        for phase_key, phase in CAMPAIGN_PHASES.items():
            skill_file = self.skills_dir / phase["skill_bible"]
            if skill_file.exists():
                self.skill_bibles[phase_key] = skill_file
                self.log(f"  Found: {phase['skill_bible']}")
        
        return self.skill_bibles
    
    def run_campaign_pipeline(self, client: str, website: str, offer: str, budget: float = 5000) -> dict:
        """Run the full campaign pipeline with learned knowledge."""
        self.log("=" * 60)
        self.log("PHASE 2: RUNNING CAMPAIGN PIPELINE")
        self.log("=" * 60)
        
        from full_campaign_pipeline import CampaignPipeline
        
        campaign_dir = self.output_dir / "campaigns" / client.lower().replace(" ", "_")[:30]
        
        pipeline = CampaignPipeline(
            client_name=client,
            website=website,
            offer=offer,
            output_dir=campaign_dir
        )
        
        results = pipeline.run(budget=budget)
        
        return {
            "status": "success",
            "output_dir": str(campaign_dir),
            "files": [str(f) for f in campaign_dir.glob("*.md")]
        }
    
    def deploy_agents(self, num_agents: int = 10) -> dict:
        """Deploy multiple agents to work on different parts of the pipeline."""
        self.log("=" * 60)
        self.log(f"PHASE 3: DEPLOYING {num_agents} AGENTS")
        self.log("=" * 60)
        
        # Define agent roles
        agent_roles = [
            {"name": "Research Agent", "task": "client_research", "count": 2},
            {"name": "Ad Copy Agent", "task": "ad_copy", "count": 2},
            {"name": "Creative Agent", "task": "ad_creative", "count": 1},
            {"name": "Landing Page Agent", "task": "landing_pages", "count": 2},
            {"name": "CRM Agent", "task": "crm_automation", "count": 1},
            {"name": "Email Sequence Agent", "task": "email_sequences", "count": 2},
        ]
        
        deployed = []
        
        for role in agent_roles:
            for i in range(role["count"]):
                agent_id = f"{role['name'].lower().replace(' ', '_')}_{i+1}"
                
                # Create agent configuration
                agent_config = {
                    "id": agent_id,
                    "name": f"{role['name']} #{i+1}",
                    "task": role["task"],
                    "skill_bible": str(self.skill_bibles.get(role["task"], "")),
                    "status": "deployed",
                    "deployed_at": datetime.now().isoformat()
                }
                
                deployed.append(agent_config)
                self.log(f"Deployed: {agent_config['name']}", "success")
                
                if len(deployed) >= num_agents:
                    break
            
            if len(deployed) >= num_agents:
                break
        
        # Save agent configurations
        agents_file = self.output_dir / "deployed_agents.json"
        with open(agents_file, "w") as f:
            json.dump(deployed, f, indent=2)
        
        self.log(f"Deployed {len(deployed)} agents", "success")
        return {"agents": deployed, "config_file": str(agents_file)}


def main():
    parser = argparse.ArgumentParser(
        description="YouTube to Campaign Pipeline - Complete Automation"
    )
    
    # Client info (required for campaign generation)
    parser.add_argument("--client", help="Client/company name")
    parser.add_argument("--website", help="Client website")
    parser.add_argument("--offer", help="Main offer/product")
    parser.add_argument("--budget", type=float, default=5000, help="Monthly ad budget")
    
    # Options
    parser.add_argument("--learn-from-youtube", action="store_true", 
                        help="Mine YouTube for best practices first")
    parser.add_argument("--phases", nargs="+", 
                        choices=list(CAMPAIGN_PHASES.keys()),
                        help="Specific phases to learn (default: all)")
    parser.add_argument("--deploy-agents", type=int, default=0,
                        help="Number of agents to deploy")
    parser.add_argument("--skip-campaign", action="store_true",
                        help="Skip campaign generation (only learn)")
    parser.add_argument("--output-dir", default=".tmp/youtube_campaign_pipeline",
                        help="Output directory")
    parser.add_argument("--parallel", type=int, default=3,
                        help="Parallel processing level")
    
    args = parser.parse_args()
    
    # Validate
    if not args.skip_campaign and not (args.client and args.website and args.offer):
        if not args.learn_from_youtube:
            parser.error("Either --learn-from-youtube or (--client, --website, --offer) required")
    
    print("=" * 70)
    print("YOUTUBE TO CAMPAIGN PIPELINE")
    print("=" * 70)
    print(f"Output: {args.output_dir}")
    print(f"Learn from YouTube: {args.learn_from_youtube}")
    if args.client:
        print(f"Client: {args.client}")
        print(f"Website: {args.website}")
        print(f"Offer: {args.offer}")
    print("=" * 70)
    
    start_time = time.time()
    
    pipeline = YouTubeToCampaignPipeline(output_dir=args.output_dir)
    
    results = {}
    
    # Load existing skill bibles
    pipeline.load_existing_skill_bibles()
    
    # Phase 1: Learn from YouTube
    if args.learn_from_youtube:
        results["learning"] = pipeline.learn_from_youtube(
            phases=args.phases,
            parallel=args.parallel
        )
    
    # Phase 2: Run campaign pipeline
    if args.client and not args.skip_campaign:
        results["campaign"] = pipeline.run_campaign_pipeline(
            client=args.client,
            website=args.website,
            offer=args.offer,
            budget=args.budget
        )
    
    # Phase 3: Deploy agents
    if args.deploy_agents > 0:
        results["agents"] = pipeline.deploy_agents(num_agents=args.deploy_agents)
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)
    print(f"Total time: {elapsed/60:.1f} minutes")
    print(f"Results saved to: {args.output_dir}")
    
    if "campaign" in results:
        print(f"\nCampaign files:")
        for f in results["campaign"].get("files", []):
            print(f"  - {Path(f).name}")
    
    if "agents" in results:
        print(f"\nAgents deployed: {len(results['agents']['agents'])}")
    
    print("=" * 70)
    
    # Save final results
    results_file = Path(args.output_dir) / "pipeline_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": elapsed,
            "results": results
        }, f, indent=2, default=str)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
