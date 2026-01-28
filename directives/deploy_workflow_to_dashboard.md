# Deploy Workflow to Dashboard

## What This Workflow Is

Complete, error-free deployment of any AIAA workflow to the Railway dashboard. This directive captures all learnings from debugging deployment issues and ensures zero-error deployments.

## Trigger Phrases

- "deploy this workflow to my dashboard"
- "publish this workflow"
- "add this to the dashboard"
- "deploy [workflow_name] to Railway"

## Prerequisites

Before starting, ensure:
- [ ] Railway CLI installed and authenticated (`railway login`)
- [ ] Railway project exists with dashboard deployed
- [ ] Local `.env` file has all required API keys
- [ ] `token.pickle` exists if workflow uses Google APIs

## Step-by-Step Deployment Process

### Phase 1: Pre-Deployment Checks

```bash
# 1. Verify Railway CLI is authenticated
railway whoami

# 2. Get project and service IDs (save these!)
railway status

# 3. Check what services exist
TOKEN=$(cat ~/.railway/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('user', {}).get('token', ''))")
curl -s -X POST "https://backboard.railway.app/graphql/v2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { me { projects { edges { node { id name services { edges { node { id name } } } } } } } }"}' | python3 -m json.tool
```

### Phase 2: Identify Workflow Requirements

```bash
# 1. Check what API keys the workflow needs
grep -E "os\.getenv|os\.environ" railway_apps/<workflow_name>/*.py

# 2. Check if workflow uses Google APIs
grep -l "google" railway_apps/<workflow_name>/*.py && echo "NEEDS GOOGLE_OAUTH_TOKEN_PICKLE"

# 3. Check if workflow has a cron schedule
grep -i "cron" railway_apps/<workflow_name>/*.py
grep -i "schedule" railway_apps/<workflow_name>/railway.toml 2>/dev/null
```

### Phase 3: Deploy the Workflow Service

```bash
cd railway_apps/<workflow_name>

# Deploy to Railway (creates new service if doesn't exist)
railway up --service <workflow_name>

# Wait for deployment to complete
sleep 60

# Verify deployment succeeded
TOKEN=$(cat ~/.railway/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('user', {}).get('token', ''))")
curl -s -X POST "https://backboard.railway.app/graphql/v2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { service(id: \"SERVICE_ID\") { name deployments(first: 1) { edges { node { status } } } } }"}' | python3 -m json.tool
```

### Phase 4: Set Environment Variables

**CRITICAL: Set ALL required variables. Missing any will cause silent failures.**

```bash
cd railway_apps/<workflow_name>

# Core API keys (check which ones your workflow needs)
railway variables set OPENROUTER_API_KEY="$(grep OPENROUTER_API_KEY ../../.env | cut -d'=' -f2)"
railway variables set SLACK_WEBHOOK_URL="$(grep SLACK_WEBHOOK_URL ../../.env | cut -d'=' -f2)"
railway variables set ANTHROPIC_API_KEY="$(grep ANTHROPIC_API_KEY ../../.env | cut -d'=' -f2)"
railway variables set PERPLEXITY_API_KEY="$(grep PERPLEXITY_API_KEY ../../.env | cut -d'=' -f2)"

# For Google API workflows ONLY
GOOGLE_TOKEN=$(python3 -c "import base64; print(base64.b64encode(open('../../token.pickle','rb').read()).decode())")
railway variables set GOOGLE_OAUTH_TOKEN_PICKLE="$GOOGLE_TOKEN"

# Verify all variables are set
railway variables --json | python3 -c "import json,sys; d=json.load(sys.stdin); print('\n'.join(d.keys()))"
```

### Phase 5: Get Service and Environment IDs

```bash
# Get the service ID and environment ID (needed for dashboard)
TOKEN=$(cat ~/.railway/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('user', {}).get('token', ''))")

# Query for the new service
curl -s -X POST "https://backboard.railway.app/graphql/v2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { service(id: \"SERVICE_ID\") { id name projectId serviceInstances { edges { node { environmentId cronSchedule } } } } }"}' | python3 -m json.tool

# Save these values:
# - service_id: The service ID
# - project_id: The project ID
# - environment_id: The environment ID (for API calls)
# - cron_schedule: The cron expression if it's a cron job
```

### Phase 6: Add to Dashboard Active Workflows

Edit `railway_apps/aiaa_dashboard/app.py` and add to the `active_workflows` list:

```python
{
    "name": "Workflow Display Name",
    "description": "What this workflow does",
    "project_id": "PROJECT_ID_HERE",
    "service_id": "SERVICE_ID_HERE",
    "cron": "0 */3 * * *",  # Cron expression, or None if not a cron job
    "directive": "workflow_directive_name.md",
    "platform": "Railway Cron",  # or "Railway Service"
    "project_url": "https://railway.com/project/PROJECT_ID_HERE"
}
```

### Phase 7: Ensure Dashboard Has RAILWAY_API_TOKEN

**CRITICAL: Without this, cron toggle won't work.**

```bash
# Check if dashboard has the token
TOKEN=$(cat ~/.railway/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('user', {}).get('token', ''))")

curl -s -X POST "https://backboard.railway.app/graphql/v2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { variables(serviceId: \"DASHBOARD_SERVICE_ID\", environmentId: \"ENV_ID\") }"}' | python3 -c "import json,sys; d=json.load(sys.stdin); print('RAILWAY_API_TOKEN' in d.get('data', {}).get('variables', {}))"

# If False, set it:
curl -s -X POST "https://backboard.railway.app/graphql/v2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"mutation { variableUpsert(input: {projectId: \\\"PROJECT_ID\\\", serviceId: \\\"DASHBOARD_SERVICE_ID\\\", environmentId: \\\"ENV_ID\\\", name: \\\"RAILWAY_API_TOKEN\\\", value: \\\"$TOKEN\\\"}) }\"}"
```

### Phase 8: Redeploy Dashboard

```bash
cd railway_apps/aiaa_dashboard
railway up --service aiaa-dashboard

# Wait for deployment
sleep 60

# Verify dashboard is up
curl -s "https://aiaa-dashboard-production.up.railway.app/health"
```

### Phase 9: Verify Everything Works

```bash
# 1. Check workflow appears in dashboard UI
# Visit: https://aiaa-dashboard-production.up.railway.app

# 2. Check cron status via API (if cron workflow)
TOKEN=$(cat ~/.railway/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('user', {}).get('token', ''))")
curl -s -X POST "https://backboard.railway.app/graphql/v2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { service(id: \"NEW_SERVICE_ID\") { name deployments(first: 1) { edges { node { status } } } serviceInstances { edges { node { cronSchedule } } } } }"}' | python3 -m json.tool

# Expected output should show:
# - status: "SUCCESS"
# - cronSchedule: "0 */3 * * *" (or your schedule)

# 3. Test cron toggle in dashboard (click toggle off then on)

# 4. Manually trigger workflow to test
railway run python run.py
```

## Critical Gotchas (From Production Debugging)

### Railway GraphQL API
| Issue | Solution |
|-------|----------|
| `cronSchedule: ""` fails | Use `cronSchedule: null` to disable |
| `serviceInstanceRedeploy` fails | Use `railway up` CLI instead |
| Service shows "offline" after deployment removal | Must redeploy with `railway up` |
| `ServiceUpdateInput` missing cron | Use `ServiceInstanceUpdateInput` |

### Environment Variables
| Issue | Solution |
|-------|----------|
| Google Doc creation fails silently | Missing `GOOGLE_OAUTH_TOKEN_PICKLE` |
| API calls return 401 | Missing or expired API keys |
| Cron toggle doesn't work | Missing `RAILWAY_API_TOKEN` in dashboard |

### Deployment
| Issue | Solution |
|-------|----------|
| Workflow not in dashboard | Forgot to add to `active_workflows` list |
| Dashboard changes not showing | Forgot to redeploy dashboard |
| Cron not running | Check `cronSchedule` is set AND deployment exists |

## IDs Reference (AIAA Project)

```
Project ID: 3b96c81f-9518-4131-b2bc-bcd7a524a5ef
Environment ID: 951885c9-85a5-46f5-96a1-2151936b0314

Dashboard Service ID: 415686bb-d10c-40c5-b610-4c5e41bbe762
X-YouTube Service ID: 5fbf1961-5c49-41ec-a776-fb4c7723bf69
```

## Deployment Checklist

Before marking deployment complete, verify ALL items:

- [ ] Workflow deployed to Railway (`railway up` succeeded)
- [ ] Deployment status is SUCCESS (not BUILDING, not NO_DEPLOYMENT)
- [ ] ALL required environment variables set
- [ ] `GOOGLE_OAUTH_TOKEN_PICKLE` set (if uses Google APIs)
- [ ] Added to `active_workflows` in dashboard app.py
- [ ] Dashboard redeployed after app.py changes
- [ ] `RAILWAY_API_TOKEN` set in dashboard (for cron toggle)
- [ ] Workflow visible in dashboard UI
- [ ] Cron toggle works (if cron workflow)
- [ ] Manual test run succeeds
- [ ] Cron schedule is set correctly in Railway

## Self-Annealing Notes

### 2026-01-28: Initial Creation
- **Context**: Created after extensive debugging of cron toggle feature
- **Key Learning**: Railway GraphQL API has many undocumented quirks
- **cronSchedule gotcha**: Empty string `""` causes "Problem processing request" - must use `null`
- **Deployment gotcha**: After removing deployment, `serviceInstanceRedeploy` fails - must use CLI
- **Token gotcha**: Dashboard needs `RAILWAY_API_TOKEN` to make Railway API calls

### Railway API Mutations Reference
```graphql
# Modify cron schedule
serviceInstanceUpdate(serviceId, environmentId, input: {cronSchedule})

# Set environment variable
variableUpsert(input: {projectId, serviceId, environmentId, name, value})

# Get service info (includes service instance ID)
service(id) { name projectId serviceInstances { edges { node { id cronSchedule environmentId } } } }

# Trigger immediate cron execution (bypasses schedule)
# NOTE: Requires serviceInstanceId, not serviceId!
deploymentInstanceExecutionCreate(input: {serviceInstanceId: "INSTANCE_ID"})
```

### 2026-01-28: Run Now Button Implementation
- **Feature**: "Run Now" button triggers immediate cron execution
- **Mutation**: `deploymentInstanceExecutionCreate` with `serviceInstanceId`
- **Key Insight**: `serviceInstanceId` is different from `serviceId` - get it from `service.serviceInstances.edges[].node.id`
- **Behavior**: Runs the cron job immediately without waiting for the next scheduled time

### 2026-01-28: Schedule Editor Implementation
- **Feature**: Granular cron schedule editor replacing simple dropdown
- **UI Components**:
  - Interval input (1-24) for frequency
  - Unit selector ("hours" or "days")
  - Minute input (0-59) for timing
  - Save button to apply changes
  - Live cron expression display
- **Dynamic Schedule Text**: "Schedule:" display now updates dynamically:
  - On page load: parses cron and converts to human-readable text
  - On save: immediately updates to reflect new schedule
- **cronToText Conversion**: JavaScript function converts cron patterns:
  - `0 */3 * * *` → "Every 3 hours"
  - `30 * * * *` → "Every hour at :30"
  - `0 0 * * *` → "Daily at 00:00"

### 2026-01-28: RAILWAY_API_TOKEN Critical Fix
- **Issue**: Schedule updates from dashboard were silently failing
- **Root Cause**: `RAILWAY_API_TOKEN` was not set in dashboard environment
- **Symptom**: UI showed success toast but cron didn't actually change in Railway
- **Fix**: Set token via GraphQL API:
  ```bash
  TOKEN=$(cat ~/.railway/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('user', {}).get('token', ''))")
  curl -s -X POST "https://backboard.railway.app/graphql/v2" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"query": "mutation { variableUpsert(input: {projectId: \"PROJECT_ID\", serviceId: \"DASHBOARD_SERVICE_ID\", environmentId: \"ENV_ID\", name: \"RAILWAY_API_TOKEN\", value: \"TOKEN_VALUE\"}) }"}'
  ```
- **Learning**: Always verify `RAILWAY_API_TOKEN` is set when dashboard API calls fail silently
- **Verification**: Query variables to check: `variables(serviceId: "...", environmentId: "...")`
