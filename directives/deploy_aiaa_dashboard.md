# Deploy AIAA Agentic OS Dashboard

## What This Workflow Does
Deploys a complete management dashboard for the AIAA Agentic OS to Railway. The dashboard provides:

1. **Password-Protected Access** - Secure login with username/password
2. **Workflow Management** - View all 130+ workflows with descriptions
3. **Environment Variable Tracking** - See which API keys are configured
4. **Webhook Endpoints** - Monitor and manage webhook integrations
5. **Real-Time Event Logs** - Track all system activity
6. **Claude-Style Dark Theme** - Beautiful slate grey + orange UI

## Prerequisites

### Required Tools
- Railway CLI installed: `brew install railway`
- Railway account and logged in: `railway login`

### Optional Environment Variables
These will be auto-loaded from `.env` if present:
- `OPENROUTER_API_KEY`
- `PERPLEXITY_API_KEY`
- `SLACK_WEBHOOK_URL`
- `CALENDLY_API_KEY`

## How to Run

### Option 1: Automated Deployment
```bash
python3 execution/deploy_aiaa_dashboard.py --username admin --password yoursecurepassword
```

### Option 2: Interactive Mode
```bash
python3 execution/deploy_aiaa_dashboard.py --interactive
```

### Option 3: With Existing Railway Project
```bash
python3 execution/deploy_aiaa_dashboard.py --project-id your-project-id --password yourpassword
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | No | Login username (default: admin) |
| password | string | Yes | Login password (will be securely hashed) |
| project-id | string | No | Existing Railway project ID |
| project-name | string | No | Name for new project (default: aiaa-dashboard) |

## Process

### Step 1: Prerequisites Check
- Verifies Railway CLI is installed
- Confirms user is logged into Railway
- Locates dashboard source files

### Step 2: Project Setup
- Creates new Railway project OR links to existing one
- Initializes project configuration

### Step 3: Environment Configuration
- Sets `DASHBOARD_USERNAME` and hashed password
- Generates secure `FLASK_SECRET_KEY`
- Copies relevant API keys from local `.env`

### Step 4: Deployment
- Uploads dashboard app to Railway
- Waits for build completion
- Generates public domain

### Step 5: Verification
- Confirms deployment successful
- Returns dashboard URL and login credentials

## Output

### Console Output
```
============================================================
  AIAA Dashboard Deployed Successfully!
============================================================

  URL: https://aiaa-dashboard-production.up.railway.app

  Login Credentials:
    Username: admin
    Password: your-secure-password

  Save these credentials - the password cannot be recovered!
============================================================
```

### Dashboard Features

**Overview Page:**
- System status indicator
- Workflow count, event stats, error tracking
- Environment variable status at a glance
- Recent events timeline
- Quick access to top workflows

**Workflows Page:**
- Searchable list of all 130+ workflows
- Description and script availability
- Filter and search functionality

**Environment Page:**
- All tracked API keys
- Set/unset status with masked previews
- Instructions for adding new variables

**Webhooks Page:**
- List of all registered endpoints
- Method badges (GET/POST)
- Base URL for API calls

**Logs Page:**
- Real-time event log
- Timestamp, type, source, status
- Auto-refresh every 30 seconds

## Quality Gates

- [ ] Railway CLI installed and authenticated
- [ ] Dashboard source files exist
- [ ] Password provided or generated
- [ ] Environment variables set successfully
- [ ] Deployment completes without errors
- [ ] Public domain generated
- [ ] Login works with provided credentials

## Security Notes

1. **Password Hashing**: Passwords are hashed with SHA-256 before storage
2. **Session Security**: Flask sessions use secure random secret key
3. **No Password Recovery**: Lost passwords require re-deployment
4. **HTTPS Only**: Railway provides automatic SSL/TLS

## Troubleshooting

### "Railway CLI not installed"
```bash
brew install railway
```

### "Not logged into Railway"
```bash
railway login
```

### "Deployment failed"
Check Railway logs:
```bash
cd railway_apps/aiaa_dashboard && railway logs
```

### "Cannot access dashboard"
1. Wait 30 seconds for deployment to propagate
2. Clear browser cache
3. Check Railway dashboard for deployment status

## Related Files
- `railway_apps/aiaa_dashboard/app.py` - Main Flask application
- `railway_apps/aiaa_dashboard/requirements.txt` - Python dependencies
- `railway_apps/aiaa_dashboard/railway.json` - Railway configuration
- `execution/deploy_aiaa_dashboard.py` - Deployment automation script

## Self-Annealing Notes

### 2026-01-09 - Initial Creation
- Created complete dashboard with Claude-style dark theme
- Hardcoded 90+ workflows since Railway deployment can't read local files
- Added password authentication with SHA-256 hashing
- Implemented sidebar navigation pattern for better UX
- Added searchable workflows page
- Railway CLI requires `railway link -p <project-id> -s <service>` to link after init
- Must deploy first before setting variables (creates the service)
- Generate domain after deployment with `railway domain`

### Key Learnings
1. **Railway Non-Interactive Mode**: CLI prompts fail in scripts; use explicit `-p` and `-s` flags
2. **Service Linking**: Must link project AND service after `railway init`
3. **Variable Order**: Deploy first, then set variables, then redeploy
4. **Workflow Data**: Cannot read files at runtime on Railway; hardcode workflow metadata
5. **Session Security**: Generate `FLASK_SECRET_KEY` at deployment time, not in code

### 2026-01-09 - v2.0 Update
- Added light/dark mode toggle with localStorage persistence
- Theme uses CSS custom properties for instant switching
- Added environment variable management UI (set from dashboard)
- Runtime env vars stored in memory + os.environ
- Added workflow detail pages with full descriptions
- 90+ workflows with rich descriptions, inputs, outputs
- Sidebar navigation with active state indicators
- All templates updated with unified BASE_CSS
- API authentication enforced on all sensitive endpoints
- Version bumped to 2.0.0

### v2.0 Features
1. **Theme Toggle**: Sun/moon icon in sidebar, persists via localStorage
2. **Env Var Management**: Dropdown selector + password field to set API keys
3. **Workflow Details**: Click any workflow to see full description, inputs, outputs
4. **Unified Styling**: Single BASE_CSS variable with light/dark variants
5. **Responsive**: Works on mobile with sidebar hidden
