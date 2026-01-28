# YouTube to Campaign Pipeline (Master Orchestrator)

## What This Workflow Is

The MASTER orchestrator that combines YouTube knowledge mining with full campaign generation. Learns best practices from top YouTube experts, creates skill bibles, and deploys multiple AI agents to execute campaigns with learned knowledge.

## What It Does

1. **Learn from YouTube** - Mine knowledge for each campaign phase
2. **Create Skill Bibles** - Generate comprehensive guides from expert content
3. **Run Campaign Pipeline** - Execute full campaign with learned best practices
4. **Deploy Agents** - Spin up specialized agents for parallel work

## Campaign Phases Covered

| Phase | YouTube Topics | Output |
|-------|---------------|--------|
| Client Research | Market research, customer avatar | SKILL_BIBLE_client_research.md |
| Meta Ads Setup | Facebook ads structure, targeting | SKILL_BIBLE_meta_ads_setup.md |
| Ad Copy | Direct response copywriting | SKILL_BIBLE_ad_copywriting.md |
| Ad Creative | Ad design, scroll-stopping | SKILL_BIBLE_ad_creative.md |
| Landing Pages | Sales page copywriting | SKILL_BIBLE_landing_pages.md |
| CRM Automation | Pipeline setup, nurturing | SKILL_BIBLE_crm_automation.md |
| Email Sequences | Follow-up strategy | SKILL_BIBLE_email_sequences.md |

## Prerequisites

**Required API Keys:**
- `OPENROUTER_API_KEY` - For Claude
- `OPENAI_API_KEY` - For Whisper transcription
- YouTube Data API enabled

**Optional:**
- `PERPLEXITY_API_KEY` - For research
- `GOOGLE_API_KEY` - For Gemini (cheaper)

**Installation:**
```bash
pip install google-api-python-client google-auth google-auth-oauthlib openai requests yt-dlp python-dotenv
```

## How to Run

### Full Pipeline (Learn + Campaign + Deploy Agents)
```bash
python3 execution/youtube_to_campaign_pipeline.py \
  --client "Acme Corp" \
  --website "https://acmecorp.com" \
  --offer "AI Lead Generation" \
  --learn-from-youtube \
  --deploy-agents 10
```

### Learn Only (No Campaign)
```bash
python3 execution/youtube_to_campaign_pipeline.py \
  --learn-from-youtube \
  --phases client_research meta_ads_setup ad_copy \
  --skip-campaign
```

### Campaign Only (Use Existing Skills)
```bash
python3 execution/youtube_to_campaign_pipeline.py \
  --client "Acme Corp" \
  --website "https://acmecorp.com" \
  --offer "AI Lead Generation" \
  --deploy-agents 10
```

### Specific Phases
```bash
python3 execution/youtube_to_campaign_pipeline.py \
  --learn-from-youtube \
  --phases landing_pages email_sequences \
  --client "Coaching Pro" \
  --website "https://coachingpro.com" \
  --offer "Executive Coaching"
```

## Inputs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--client` | string | * | - | Client/company name |
| `--website` | string | * | - | Client website |
| `--offer` | string | * | - | Main offer/product |
| `--budget` | float | No | 5000 | Monthly ad budget |
| `--learn-from-youtube` | flag | No | False | Mine YouTube first |
| `--phases` | list | No | all | Specific phases to learn |
| `--deploy-agents` | int | No | 0 | Number of agents to deploy |
| `--skip-campaign` | flag | No | False | Only learn, no campaign |
| `--output-dir` | string | No | .tmp/youtube_campaign_pipeline | Output directory |
| `--parallel` | int | No | 3 | Parallel processing level |

*Required unless `--skip-campaign` is set

## Process

### Step 1: Load Existing Skills
Check `skills/` directory for existing skill bibles to avoid re-mining.

### Step 2: YouTube Knowledge Mining
For each campaign phase (can run in parallel):
1. Search for top channels in niche
2. Get best-performing videos
3. Download and transcribe audio
4. Convert to how-to manuals
5. Rate and filter quality content
6. Generate comprehensive skill bible

### Step 3: Campaign Generation
Run full 8-phase campaign pipeline:
1. Client research
2. Meta ads setup
3. Ad copy generation
4. Ad image generation
5. Landing page creation
6. Landing page images
7. CRM pipeline setup
8. Follow-up sequences

### Step 4: Agent Deployment
Deploy specialized agents:
- Research Agents (2)
- Ad Copy Agents (2)
- Creative Agent (1)
- Landing Page Agents (2)
- CRM Agent (1)
- Email Sequence Agents (2)

## Outputs

```
.tmp/youtube_campaign_pipeline/
├── pipeline_results.json      # Master results
├── deployed_agents.json       # Agent configurations
│
├── knowledge/                 # YouTube mining outputs
│   ├── client_research/
│   │   ├── channels.json
│   │   ├── videos.json
│   │   ├── manuals/
│   │   └── SKILL_BIBLE_client_research.md
│   ├── meta_ads_setup/
│   ├── ad_copy/
│   └── ...
│
└── campaigns/                 # Campaign outputs
    └── acme_corp/
        ├── 01_research.json
        ├── 02_meta_ads_setup.md
        ├── 03_ad_copy.md
        ├── 04_ad_images.md
        ├── 05_landing_page.md
        ├── 06_landing_page_images.md
        ├── 07_crm_setup.md
        ├── 08_followup_sequences.md
        └── images/
```

## Agent Roles

| Agent | Count | Responsibility |
|-------|-------|----------------|
| Research Agent | 2 | Client research, market analysis |
| Ad Copy Agent | 2 | Ad copy variations, headlines |
| Creative Agent | 1 | Image prompts, visual concepts |
| Landing Page Agent | 2 | Page copy, structure |
| CRM Agent | 1 | Pipeline, automations |
| Email Agent | 2 | Sequences, follow-ups |

## Time & Cost Estimates

### Learning Phase (per topic)
- Channels: 5 x 3 videos = 15 videos
- ~$4-6 per topic
- ~$30-40 total for all 7 phases
- Time: 30-60 minutes

### Campaign Phase
- 8 phases x $0.10 = $0.80
- Images (optional): $0.30
- Time: 10-15 minutes

### Total for Full Pipeline
- **Cost:** ~$35-45
- **Time:** 45-75 minutes

## Quality Gates

- [ ] At least 5/7 skill bibles generated
- [ ] All 8 campaign phases complete
- [ ] 10 agents deployed successfully
- [ ] All output files saved

## Example Use Cases

### 1. Starting a New Niche
```bash
# Learn everything about SaaS marketing
python3 execution/youtube_to_campaign_pipeline.py \
  --learn-from-youtube \
  --skip-campaign
```

### 2. Client Campaign with Learning
```bash
# Learn + Generate for new client
python3 execution/youtube_to_campaign_pipeline.py \
  --client "TechStartup" \
  --website "https://techstartup.io" \
  --offer "AI Analytics Platform" \
  --budget 10000 \
  --learn-from-youtube \
  --deploy-agents 10
```

### 3. Quick Campaign (Use Existing Skills)
```bash
# Fast campaign using existing knowledge
python3 execution/youtube_to_campaign_pipeline.py \
  --client "ConsultingFirm" \
  --website "https://consultingfirm.com" \
  --offer "Strategy Consulting" \
  --deploy-agents 5
```

## Related Workflows

- `youtube_knowledge_miner.md` - Knowledge mining only
- `full_campaign_pipeline.md` - Campaign generation only
- `youtube_channel_finder.md` - Channel discovery only
