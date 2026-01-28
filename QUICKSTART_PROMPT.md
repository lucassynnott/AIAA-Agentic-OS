# AIAA Agentic OS - Interactive Setup Guide

**Version 2.3** | **139 Workflows** | **Complete Agency Operating System**

Paste this entire prompt into Claude Code to get a fully interactive setup experience. Claude will clone the system, configure your APIs, set up your agency profile, **deploy your dashboard to Railway automatically**, and walk you through everything step by step.

---

## Prerequisites

**Good news: Claude will automatically install any missing tools for you!**

You just need TWO things before starting:

### Required Accounts (Create These First)
1. **GitHub Account** - To clone the repository
   - Go to https://github.com and sign up if you don't have one
2. **Railway Account** - For deploying the dashboard
   - Go to https://railway.app
   - Click "Sign Up"
   - Connect with GitHub (recommended) or use email
   - Verify your email if needed

### Tools (Auto-Installed)
Claude will automatically check for and install these if missing:
- **Homebrew** (macOS only) - Package manager for easy installs
- **Python 3.8+** - Programming language
- **Git** - Version control
- **Node.js & npm** - JavaScript runtime
- **Railway CLI** - Deploy to Railway from terminal
- **Railway Skill** - Enhanced Railway integration for Claude

### Optional Accounts (Can set up during installation)
- **Google Account** - For Google Docs/Sheets integration
- **OpenRouter Account** - For AI model access (you'll create this during setup)
- **Perplexity Account** - For research features
- **Slack Workspace** - For notifications

**That's it!** Just have your GitHub and Railway accounts ready, then paste the prompt below. Claude handles everything else!

---

## The Prompt (Copy Everything Below)

```
I want to set up AIAA Agentic OS v2.3. Please help me through the entire process interactively, asking me ONE question at a time and waiting for my response before moving on.

## Prerequisites Check (Do This FIRST)

Before we begin Step 1, say:

"Before we get started, let me check if you have the required tools installed. I'll automatically install anything that's missing - you don't need to do anything!"

### Step 0a: Check for Homebrew (macOS only)

First, RUN this command to check the operating system:

uname -s

If macOS (Darwin), check if Homebrew is installed by RUNNING:

which brew

If Homebrew is NOT installed (command not found), say "I need to install Homebrew first - this is a package manager that makes installing other tools easy..." and RUN:

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

After Homebrew installs, RUN these commands to add it to the PATH:

echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

### Step 0b: Check and Auto-Install Required Tools

Now check each required tool and AUTOMATICALLY install any that are missing:

**Check Python:**
RUN: python3 --version

If Python is NOT installed, say "Installing Python..." and RUN:
- On macOS: brew install python3
- On Linux: sudo apt-get install -y python3 python3-pip

**Check Git:**
RUN: git --version

If Git is NOT installed, say "Installing Git..." and RUN:
- On macOS: brew install git
- On Linux: sudo apt-get install -y git

**Check npm/Node.js:**
RUN: npm --version

If npm is NOT installed, say "Installing Node.js (includes npm)..." and RUN:
- On macOS: brew install node
- On Linux: curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs

### Step 0c: Install Railway CLI and Railway Skill

After all tools are installed, say "Now I'll install the Railway CLI and Railway skill for easier deployments..."

RUN these commands:

npm install -g @railway/cli
npx add-skill mshumer/claude-skill-railway

### Step 0d: Verify Everything is Ready

RUN these commands to confirm everything is installed:

python3 --version
git --version
npm --version
railway --version

If all 4 commands succeed, say: "All required tools are installed and ready!"

Then ask: "Do you have a Railway account? If not, please:
1. Go to https://railway.app
2. Click 'Sign Up'
3. Connect with GitHub (recommended) or use email
4. Verify your email

Reply 'yes' when you have a Railway account and we'll proceed to Step 1!"

Wait for my response before continuing.

## Step 1: Clone & Install

Say: "Great! Let me download and install AIAA Agentic OS for you..."

Then RUN these commands automatically:

git clone https://github.com/stopmoclay/AIAA-Agentic-OS.git
cd AIAA-Agentic-OS
pip install -r requirements.txt

After running them, tell me if they completed successfully or if there were any errors.

## Step 2: Configure API Keys (.env file)

Create my .env file with API keys. Ask me for each one individually, and walk me through getting each key with detailed instructions:

---

### OPENROUTER_API_KEY (REQUIRED - Powers all AI features)

**What it does:** Routes requests to Claude, GPT-4, and other AI models. This is the only required key.

**How to get it:**
1. Go to https://openrouter.ai
2. Click "Sign Up" (top right) - use Google or email
3. Once logged in, click your profile icon → "Keys"
4. Click "Create Key"
5. Name it "AIAA" and click "Create"
6. Copy the key (starts with `sk-or-`)

**Cost:** Pay-as-you-go. Most workflows cost $0.01-0.10. Add $5-10 credits to start.

---

### PERPLEXITY_API_KEY (Recommended - Deep research & prospect intel)

**What it does:** Powers all research workflows - company research, market analysis, prospect intelligence, competitor monitoring.

**How to get it:**
1. Go to https://perplexity.ai
2. Sign up or log in
3. Click your profile icon (bottom left) → "Settings"
4. Click "API" in the left sidebar
5. Click "Generate" to create a new API key
6. Copy the key (starts with `pplx-`)

**Cost:** $5/month for 1000 requests, or pay-as-you-go at ~$0.005 per request.

---

### SLACK_WEBHOOK_URL (Recommended - Notifications & alerts)

**What it does:** Sends notifications when workflows complete, meetings are booked, leads are found, etc.

**How to get it:**
1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name it "AIAA Notifications" and select your workspace
4. Click "Create App"
5. In the left sidebar, click "Incoming Webhooks"
6. Toggle "Activate Incoming Webhooks" to ON
7. Click "Add New Webhook to Workspace"
8. Select the channel for notifications (e.g., #aiaa-alerts)
9. Click "Allow"
10. Copy the Webhook URL (starts with `https://hooks.slack.com/services/`)

**Cost:** Free

---

### ANTHROPIC_API_KEY (Optional - Direct Claude access, faster)

**What it does:** Direct access to Claude without going through OpenRouter. Slightly faster responses.

**How to get it:**
1. Go to https://console.anthropic.com
2. Sign up with email
3. Verify your email and complete setup
4. Click "Get API Keys" in the dashboard
5. Click "Create Key"
6. Name it "AIAA" and copy the key (starts with `sk-ant-`)

**Cost:** Pay-as-you-go, similar pricing to OpenRouter.

---

### FAL_KEY (Optional - AI image generation)

**What it does:** Generates ad creatives, thumbnails, and marketing images using Nano Banana Pro model.

**How to get it:**
1. Go to https://fal.ai
2. Click "Sign Up" → use Google or GitHub
3. Once logged in, click your profile → "Dashboard"
4. Click "Keys" in the left sidebar
5. Click "Create Key"
6. Copy the key

**Cost:** Pay-as-you-go. ~$0.02-0.05 per image.

---

### APIFY_API_TOKEN (Optional - Lead scraping)

**What it does:** Scrapes Google Maps for local businesses, LinkedIn for prospects, and other lead generation tasks.

**How to get it:**
1. Go to https://console.apify.com
2. Sign up with email or Google
3. Once logged in, click "Settings" (gear icon, bottom left)
4. Click "Integrations" in the left sidebar
5. Your API token is displayed - click to copy

**Cost:** Free tier includes $5/month credits. Most scraping tasks cost $0.25-2.00.

---

For each key, ask me: "Do you have [KEY_NAME]? If yes, paste it. If no, I'll help you get it."

## Step 3: Google Drive, Docs & Sheets Setup (Recommended)

This enables automatic document creation, lead exports to Sheets, and file management. Walk me through the complete setup:

---

### Why This Matters

Google integration powers these workflows:
- **Auto-create Google Docs** from generated content (VSL scripts, sales pages, emails)
- **Export leads to Sheets** from scraping workflows
- **Meeting prep documents** created automatically from Calendly webhooks
- **Client deliverables** formatted and shared via Google Drive

---

### Step 3a: Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Click the project dropdown (top left, next to "Google Cloud")
3. Click "NEW PROJECT" (top right of popup)
4. Name it "AIAA Agentic OS" 
5. Click "CREATE"
6. Wait for project creation (takes 10-30 seconds)
7. Make sure the new project is selected in the dropdown

---

### Step 3b: Enable Required APIs

1. In the left sidebar, click "APIs & Services" → "Library"
2. Search for and enable EACH of these APIs (click each one, then click "ENABLE"):

**Required APIs:**
- **Google Docs API** - For creating/editing documents
- **Google Sheets API** - For spreadsheet exports
- **Google Drive API** - For file management and sharing

For each API:
1. Search the name in the API Library
2. Click on the API
3. Click the blue "ENABLE" button
4. Wait for it to enable, then go back and enable the next one

---

### Step 3c: Create OAuth 2.0 Credentials

1. In the left sidebar, click "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" (top of page)
3. Select "OAuth client ID"

**If you see "Configure Consent Screen" warning:**
1. Click "CONFIGURE CONSENT SCREEN"
2. Select "External" (unless you have Google Workspace, then "Internal")
3. Click "CREATE"
4. Fill in required fields:
   - App name: "AIAA Agentic OS"
   - User support email: Your email
   - Developer contact: Your email
5. Click "SAVE AND CONTINUE"
6. On Scopes page, click "SAVE AND CONTINUE" (no changes needed)
7. On Test Users page, click "ADD USERS"
8. Add your Gmail address
9. Click "SAVE AND CONTINUE"
10. Click "BACK TO DASHBOARD"
11. Go back to Credentials and create OAuth client ID again

**Create the OAuth Client:**
1. Click "+ CREATE CREDENTIALS" → "OAuth client ID"
2. Application type: Select "Desktop app"
3. Name: "AIAA Desktop Client"
4. Click "CREATE"

---

### Step 3d: Download and Place Credentials

1. After creating, you'll see a popup with your Client ID
2. Click "DOWNLOAD JSON" button
3. Rename the downloaded file to exactly: `credentials.json`
4. Move it to your AIAA project root folder:
   ```
   AIAA-Agentic-OS/
   ├── credentials.json    ← Place it here
   ├── directives/
   ├── execution/
   └── ...
   ```

---

### Step 3e: Test the Integration

Say: "Now let me test the Google integration..."

Then RUN this command:

python3 execution/create_google_doc.py --test

Tell me: "A browser window should open asking you to sign in to Google. Please:
1. Select your Google account
2. If you see 'Google hasn't verified this app' - click 'Continue' (it's your own app)
3. Grant permissions for Docs, Sheets, and Drive
4. You'll see 'The authentication flow has completed'

Let me know when you've completed the authentication, or if you see any errors!"

Wait for my response. If successful, confirm the test document was created.

---

### Troubleshooting Google Setup

**"credentials.json not found"**
- Make sure the file is named exactly `credentials.json` (not `credentials (1).json`)
- Make sure it's in the project root, not a subfolder

**"Access blocked" or "App not verified"**
- Click "Advanced" → "Go to AIAA Agentic OS (unsafe)"
- This is safe - it's your own app

**"Token has been expired or revoked"**
- Delete `token.pickle` and `token_docs.json` files
- Run the test command again to re-authenticate

**"API not enabled"**
- Go back to Google Cloud Console → APIs & Services → Library
- Make sure all 3 APIs are enabled (Docs, Sheets, Drive)

---

## Step 4: Agency Profile Setup

Ask me questions one at a time and create my agency profile:

Questions to ask:
1. What's your agency name?
2. What's your website URL?
3. What services do you offer? (list them)
4. Who is your ideal client/target audience?
5. What makes you different from competitors?
6. Describe your brand voice (professional, casual, bold, friendly, authoritative, etc.)
7. Who is the owner/founder? (name and background)

Save to these files:
- context/agency.md - Agency overview
- context/brand_voice.md - Tone and style guide
- context/services.md - Service offerings
- context/owner.md - Founder info

## Step 5: First Client Profile (Optional)

Ask if I want to set up a client profile. If yes, create clients/{client_name}/ with:
- profile.md - Company info, industry, audience
- rules.md - Content guidelines
- preferences.md - Style preferences

## Step 6: Deploy AIAA Dashboard to Railway (IMPORTANT - AUTOMATE THIS)

This is the key step. Deploy my monitoring dashboard to Railway. Handle as much as possible automatically.

### Step 6a: Check Prerequisites

Say: "Let me check if Railway CLI is installed..."

Then RUN this command:

railway --version

If not installed, say "I need to install Railway CLI for you..." and RUN:

npm install -g @railway/cli

Then RUN this command to check if you're logged in:

railway whoami

If not logged in, tell me: "Please run 'railway login' in your terminal and complete the browser authentication, then let me know when done!"

Wait for my response before continuing.

### Step 6b: Ask for Dashboard Credentials
Ask me TWO questions (one at a time):
1. "What username do you want for your dashboard? (default: admin)"
2. "What password do you want for your dashboard?"

After I provide the password, say "Let me generate the secure password hash..."

Then RUN this command to generate the hash (using heredoc to avoid escape issues):

python3 << 'PYHASH'
import hashlib
password = "THE_PASSWORD_I_GAVE_YOU"
print(hashlib.sha256(password.encode()).hexdigest())
PYHASH

Save the username and hash - you'll need them for environment variables.

### Step 6c: Create Railway Project and Deploy

Say: "Now let me deploy your dashboard to Railway..."

Then RUN these commands:

cd railway_apps/aiaa_dashboard
railway init

Tell me: "When prompted, please select 'Empty Project' and give it a name like 'aiaa-dashboard'. Let me know when that's done!"

Wait for my response.

Then say "Deploying the dashboard code to Railway..." and RUN:

railway up

Tell me when the deployment completes.

### Step 6d: Set Environment Variables

Say: "Now I'll configure the environment variables..."

First, generate the FLASK_SECRET_KEY by RUNNING:

python3 -c "import secrets; print(secrets.token_hex(32))"

Then RUN these commands with the username and hash you saved earlier:

railway variables set DASHBOARD_USERNAME="[USERNAME_I_CHOSE]"
railway variables set DASHBOARD_PASSWORD_HASH="[THE_HASH_YOU_GENERATED]"
railway variables set FLASK_SECRET_KEY="[THE_SECRET_KEY_YOU_JUST_GENERATED]"

If I provided API keys in Step 2, also RUN:

railway variables set OPENROUTER_API_KEY="[MY_KEY_FROM_STEP_2]"
railway variables set PERPLEXITY_API_KEY="[MY_KEY_FROM_STEP_2]"
railway variables set SLACK_WEBHOOK_URL="[MY_WEBHOOK_FROM_STEP_2]"

Tell me when all variables are set.

### Step 6e: Generate Public Domain

Say: "Let me generate a public URL for your dashboard..."

Then RUN:

railway domain

Save the generated URL (it will look like: https://aiaa-dashboard-production.up.railway.app)

### Step 6f: Verify Deployment

Say: "Testing that your dashboard is live..."

Then RUN (using the domain from Step 6e):

curl -s "https://[THE_GENERATED_DOMAIN]/health"

Check if it returns: {"status": "ok", "version": "2.3.0", "workflows": 139}

If successful, tell me "Dashboard is live!" If it fails, wait 30 seconds and try again (deployment may still be starting).

### Step 6g: Provide Login Details
Once everything is deployed, give me:
- Dashboard URL
- Username
- Password (the one I chose)
- Remind me to bookmark it!

Tell me: "Your AIAA Dashboard is now live! You can monitor all 139 workflows, manage environment variables, and track webhook events."

## Step 7: Test the System

Say: "Let's test the system with a quick workflow!"

Ask me: "What type of agency/business are you? (marketing/content/design/other)"

Based on my answer, RUN one of these test commands:
- If marketing: `python3 execution/write_cold_emails.py --sender "Test" --company "TestCo" --offer "Marketing services" --target "Small businesses"`
- If content: `python3 execution/generate_blog_post.py --topic "Getting started with AI" --length 500`
- If design: Ask for a sample project to research
- If other: `python3 execution/research_company_offer.py --company "Apple" --website "https://apple.com"`

Show me the output file location and tell me if it was successful.

## Step 8: Show What's Available

Give me a quick tour of the 139 workflows:

**Content Creation (25+ workflows):**
- Blog posts, LinkedIn posts, Twitter threads
- YouTube scripts, Instagram Reels
- Email newsletters, Content calendars

**Sales & Funnels (30+ workflows):**
- VSL scripts, Sales pages, Landing pages
- Cold email sequences, Follow-up automation
- Webinar funnels, Lead magnets

**Research & Intelligence (20+ workflows):**
- Company research, Competitor monitoring
- Prospect research, Market analysis
- Niche validation, Pricing strategy

**Lead Generation (15+ workflows):**
- Google Maps scraping, LinkedIn scraping
- Email enrichment, Lead scoring
- CRM automation, Prospecting pipelines

**Paid Advertising (15+ workflows):**
- Meta ad campaigns, Google Ads
- Ad creative generation, FB Ad Library analysis
- Video ad scripts, Static ad generation

**Client Management (20+ workflows):**
- Onboarding automation, QBR generation
- Churn risk alerts, Health scores
- Invoice generation, Testimonial requests

## Important Instructions for Claude

- Ask me ONE question at a time
- Wait for my response before continuing
- **RUN ALL COMMANDS AUTOMATICALLY** - Don't ask me to run them manually
- When you see "RUN this command" or "Run these commands", execute them using your Bash tool
- If I don't know something, help me or skip it
- Save files as we complete each section
- Be encouraging and explain why each step matters
- If errors occur, help me debug them
- For the Railway deployment, DO AS MUCH AUTOMATICALLY AS POSSIBLE
- Generate hashes, secrets, and execute all commands for me
- Only ask me for input when you absolutely need it (username, password, API keys, confirming interactive prompts)
- Save any important values (URLs, hashes, passwords) so you can reuse them later in the setup

## CRITICAL: Publishing Workflows After Setup

When I ask you to publish, deploy, or schedule ANY workflow after initial setup, you MUST:

### 1. Deploy to the SAME Railway Project as Dashboard
NEVER create a new Railway project. Always deploy workflow services to the same project where the dashboard was installed:
```bash
cd railway_apps/aiaa_dashboard
railway status  # Get the project ID
cd ../new_workflow
railway link -p <DASHBOARD_PROJECT_ID>
railway up
```

### 2. Upload ALL Required API Keys
Every workflow deployment MUST include setting all environment variables from `.env`:
```bash
# Read keys from .env and set in Railway
railway variables set OPENROUTER_API_KEY="<value>"
railway variables set SLACK_WEBHOOK_URL="<value>"
railway variables set PERPLEXITY_API_KEY="<value>"
# Check directive for required keys
```

### 3. Update Dashboard Active Workflows Section
After deploying a scheduled workflow, ALWAYS update `railway_apps/aiaa_dashboard/app.py`:
- Find the `workflow_page()` function
- Add the new workflow to the `active_workflows` list
- Redeploy the dashboard with `railway up`

### Publishing Checklist (Complete ALL Steps Every Time)
- [ ] Deploy to SAME Railway project as dashboard
- [ ] Set ALL required environment variables
- [ ] Add workflow to dashboard's Active Workflows UI
- [ ] Redeploy dashboard
- [ ] Verify workflow appears in dashboard

Let's start! Begin with the Prerequisites Check.
```

---

## What This Does

When you paste this prompt, Claude Code becomes your personal setup assistant:

1. **Downloads & installs** - Clones repo and installs dependencies
2. **Configures API keys** - One-by-one walkthrough with instructions
3. **Sets up Google OAuth** - Optional Docs/Sheets integration
4. **Creates agency profile** - Your brand voice and services
5. **Sets up clients** - Optional client profiles
6. **Deploys dashboard to Railway** - **Fully automated deployment**
   - Creates Railway project
   - Deploys dashboard code
   - Sets all environment variables
   - Generates public domain
   - Verifies deployment
   - Provides login credentials
7. **Tests the system** - Verifies everything works
8. **Shows capabilities** - Tour of all 139 workflows

**Time to complete:** 15-30 minutes depending on options chosen

---

## Dashboard Features (v2.3)

Once deployed, your dashboard includes:

| Feature | Description |
|---------|-------------|
| **139 Workflows** | Full documentation with prerequisites, how-to-run, and process steps |
| **Light/Dark Mode** | Toggle with localStorage persistence |
| **Environment Variables** | View and set API keys from the UI |
| **Webhook Monitoring** | Track incoming webhooks and events |
| **Real-time Logs** | See all workflow executions |
| **Mobile Responsive** | Works on phones and tablets |
| **Password Protected** | Secure SHA-256 hashed login |

---

## Manual Dashboard Deployment (Alternative)

If you prefer to deploy manually instead of using the interactive prompt:

### Prerequisites
```bash
npm install -g @railway/cli
railway login
```

### Deploy
```bash
cd railway_apps/aiaa_dashboard
railway init
railway up
```

### Configure
```bash
# Generate password hash (use heredoc to avoid escape sequence issues)
python3 << 'PYHASH'
import hashlib
password = "your-password"
print(hashlib.sha256(password.encode()).hexdigest())
PYHASH

# Set variables
railway variables set DASHBOARD_USERNAME="admin"
railway variables set DASHBOARD_PASSWORD_HASH="your-hash-here"
railway variables set FLASK_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"

# Generate domain
railway domain
```

### Verify
```bash
curl https://your-domain.up.railway.app/health
```

---

## Troubleshooting

### "railway: command not found"
```bash
npm install -g @railway/cli
```

### "Not logged in"
```bash
railway login
```
Complete browser authentication.

### "No project linked"
```bash
railway init
```
Select "Empty Project" when prompted.

### Dashboard shows "Invalid credentials"
Regenerate password hash using heredoc (avoids escape sequence issues with special characters):
```bash
python3 << 'PYHASH'
import hashlib
password = "your-password"
print(hashlib.sha256(password.encode()).hexdigest())
PYHASH

railway variables set DASHBOARD_PASSWORD_HASH="new-hash"
```

### Health check fails
Wait 1-2 minutes for deployment to complete, then retry:
```bash
railway logs
```

---

## Support

- **GitHub Issues:** https://github.com/stopmoclay/AIAA-Agentic-OS/issues
- **Documentation:** See `CLAUDE.md` for full system documentation
- **Workflows:** Browse all 139 in your deployed dashboard
