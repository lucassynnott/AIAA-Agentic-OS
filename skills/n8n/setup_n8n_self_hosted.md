# Setup N8N Self-Hosted - Complete Infrastructure Guide

## Purpose
This skill enables you to set up a complete, production-ready N8N self-hosted instance with cost optimization, focusing on Railway.app deployment. This is critical for agencies that need unlimited workflow executions without the per-execution pricing of N8N Cloud.

## When to Use This Skill
- When you need unlimited workflow executions without per-execution costs
- When you have more than 50-100 workflows running regularly
- When you need full control over your automation infrastructure
- When you want to minimize monthly costs while scaling operations
- When you need to connect multiple Google accounts without restrictions

## Prerequisites
### Required Accounts
1. **Railway.app account** (Primary hosting platform)
   - Sign up at railway.app
   - Add payment method (required even for free tier)
   - Free tier: $5/month credit included

2. **GitHub account** (for deployment)
   - Required for Railway deployment
   - Enables version control integration

3. **Email account** (for N8N admin access)
   - Used for initial N8N setup
   - Can be any email provider

### Required Knowledge
- Basic understanding of environment variables
- Ability to copy/paste and follow instructions precisely
- Understanding of DNS (if using custom domain)

### Cost Breakdown
**Railway.app Hosting:**
- Estimated cost: $5-15/month for typical agency use
- Scales based on usage (CPU, RAM, bandwidth)
- $5/month free credits applied automatically
- Estimated costs for different scales:
  - Small agency (10-20 workflows): ~$5-8/month
  - Medium agency (50-100 workflows): ~$10-15/month
  - Large agency (200+ workflows): ~$20-30/month

**vs N8N Cloud Costs:**
- N8N Cloud: Starts at $20/month for 2,500 executions
- Next tier: $50/month for 10,000 executions
- Self-hosted breaks even at ~50-100 workflows running regularly

## Architecture Overview
```
Railway.app (Hosting)
    ↓
N8N Instance (Docker Container)
    ↓
PostgreSQL Database (Persistent Storage)
    ↓
Your Workflows & Credentials
```

## Step-by-Step Execution Instructions

### Phase 1: Railway.app Account Setup (5 minutes)

#### Step 1.1: Create Railway Account
1. Navigate to https://railway.app
2. Click "Start a New Project" or "Sign Up"
3. Choose "Login with GitHub" (RECOMMENDED)
   - This enables seamless deployment
   - Provides version control integration
4. Authorize Railway to access your GitHub account
5. Complete the signup process

#### Step 1.2: Add Payment Method
1. Go to Account Settings (top right corner)
2. Click "Billing" tab
3. Click "Add Payment Method"
4. Enter credit/debit card details
5. Verify $5/month free credit is active
   - This appears as "$5.00 credit" in your billing section
   - Renews monthly
   - Applied automatically to your bill

**CRITICAL NOTE:** Railway requires a payment method even for free tier. Your first month will likely be free with the $5 credit.

### Phase 2: Deploy N8N on Railway (10 minutes)

#### Step 2.1: Create New Project
1. From Railway dashboard, click "New Project"
2. Select "Deploy from Template" option
3. In search bar, type "n8n"
4. Select the official "n8n" template
   - Look for the one with N8N logo
   - Should show "Self-Hostable Workflow Automation"

#### Step 2.2: Configure Template Deployment
1. Click "Deploy" on the N8N template
2. Railway will present configuration options
3. **DO NOT CHANGE** the following defaults:
   - Docker image: `n8nio/n8n:latest`
   - Port: `5678`
   - Database: PostgreSQL (automatically added)

#### Step 2.3: Set Essential Environment Variables
Railway will auto-generate some variables. You need to configure these critical ones:

**Required Variables:**
1. **N8N_BASIC_AUTH_ACTIVE**
   - Value: `true`
   - Purpose: Enables login protection
   - Security: Essential for public deployment

2. **N8N_BASIC_AUTH_USER**
   - Value: Your desired username (e.g., `admin`)
   - Purpose: Your login username
   - Note: Remember this - you'll need it to access N8N

3. **N8N_BASIC_AUTH_PASSWORD**
   - Value: Strong password (12+ characters, mixed case, numbers, symbols)
   - Example: `MyN8N2024!Secure`
   - Purpose: Your login password
   - SECURITY CRITICAL: Use a strong, unique password

4. **N8N_HOST**
   - Value: Will be your Railway domain (comes after deployment)
   - Format: `your-project-name.up.railway.app`
   - Purpose: Tells N8N what domain it's running on
   - NOTE: Set this AFTER initial deployment

5. **WEBHOOK_URL**
   - Value: Same as N8N_HOST with https://
   - Format: `https://your-project-name.up.railway.app`
   - Purpose: Enables webhook functionality
   - NOTE: Set this AFTER initial deployment

6. **N8N_ENCRYPTION_KEY**
   - Value: Random 32-character string
   - Example: Generate with: `openssl rand -base64 32`
   - Purpose: Encrypts credentials in database
   - CRITICAL: Never change this after initial setup or you'll lose access to credentials

7. **TZ**
   - Value: Your timezone (e.g., `America/New_York`, `Europe/London`, `Australia/Sydney`)
   - Purpose: Ensures scheduled workflows run at correct times
   - Find your timezone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

**Optional but Recommended Variables:**

8. **N8N_METRICS**
   - Value: `false` (set to `true` only if you need Prometheus metrics)
   - Purpose: Enables performance monitoring

9. **EXECUTIONS_DATA_PRUNE**
   - Value: `true`
   - Purpose: Automatically deletes old execution data to save database space

10. **EXECUTIONS_DATA_MAX_AGE**
    - Value: `168` (hours = 7 days)
    - Purpose: How long to keep execution history
    - Adjust based on your needs (168 hours = 1 week)

11. **EXECUTIONS_DATA_PRUNE_MAX_COUNT**
    - Value: `10000`
    - Purpose: Maximum number of executions to keep
    - Prevents database from growing infinitely

#### Step 2.4: How to Set Environment Variables in Railway
1. Click on your N8N service in Railway dashboard
2. Go to "Variables" tab
3. Click "New Variable"
4. Enter variable name (e.g., `N8N_BASIC_AUTH_ACTIVE`)
5. Enter value (e.g., `true`)
6. Click outside the field or press Enter to save
7. Repeat for each variable above

**IMPORTANT:** After adding variables, Railway will automatically redeploy. Wait for deployment to complete (usually 1-2 minutes).

### Phase 3: Access Your N8N Instance (5 minutes)

#### Step 3.1: Get Your Railway Domain
1. In Railway dashboard, click on your N8N service
2. Go to "Settings" tab
3. Scroll to "Domains" section
4. You'll see a domain like: `your-project-name.up.railway.app`
5. Click the domain to open N8N in new tab
6. **COPY THIS DOMAIN** - you need it for next steps

#### Step 3.2: Update Domain Variables
Now that you have your domain, update these variables:

1. Go back to Railway dashboard
2. Click on N8N service → Variables tab
3. Add/Update these variables:
   - **N8N_HOST**: `your-project-name.up.railway.app` (NO https://)
   - **WEBHOOK_URL**: `https://your-project-name.up.railway.app` (WITH https://)
4. Save and wait for redeployment (1-2 minutes)

#### Step 3.3: First Login
1. Navigate to your Railway domain: `https://your-project-name.up.railway.app`
2. You'll see N8N login screen
3. Enter your credentials:
   - Username: Value you set in `N8N_BASIC_AUTH_USER`
   - Password: Value you set in `N8N_BASIC_AUTH_PASSWORD`
4. Click "Sign In"
5. **FIRST TIME SETUP:** N8N will ask you to:
   - Create an owner account (email + password)
   - This is SEPARATE from basic auth
   - This is your main N8N user account
6. Complete the setup wizard

#### Step 3.4: Verify Installation
1. Once logged in, you should see the N8N dashboard
2. Check top-right corner for your user icon
3. Click on "Settings" (gear icon bottom-left)
4. Verify under "About N8N":
   - Version number is displayed
   - You're running self-hosted
5. **SUCCESS INDICATOR:** If you can see the workflow canvas with a "Create Workflow" button, you're successfully deployed!

### Phase 4: Database Setup Verification (5 minutes)

Railway automatically creates a PostgreSQL database. Let's verify it's connected:

#### Step 4.1: Check Database Connection
1. In Railway dashboard, you should see two services:
   - `n8n` (your N8N instance)
   - `postgres` (your database)
2. Click on the `postgres` service
3. Go to "Variables" tab
4. You should see these auto-generated variables:
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `DATABASE_URL`

#### Step 4.2: Link Database to N8N
Railway usually does this automatically, but verify:

1. Click on `n8n` service → Variables
2. Look for `DATABASE_URL` or similar variable
3. If NOT present, add this variable:
   - Name: `DB_TYPE`
   - Value: `postgresdb`
4. Add these variables (get values from postgres service):
   - `DB_POSTGRESDB_DATABASE`: Value from postgres `POSTGRES_DB`
   - `DB_POSTGRESDB_HOST`: Value from postgres `HOST`
   - `DB_POSTGRESDB_PORT`: Value from postgres `PORT` (usually `5432`)
   - `DB_POSTGRESDB_USER`: Value from postgres `POSTGRES_USER`
   - `DB_POSTGRESDB_PASSWORD`: Value from postgres `POSTGRES_PASSWORD`

**SIMPLER METHOD:** Railway should auto-link these. If N8N is running and you can save workflows, your database is connected!

### Phase 5: Essential Security Configuration (10 minutes)

#### Step 5.1: Enable HTTPS (Automatic on Railway)
Railway automatically provides SSL certificates. Verify:
1. Navigate to your N8N domain
2. Check browser address bar for padlock icon
3. Click padlock → should show "Connection is secure"
4. If not showing HTTPS, wait 5-10 minutes for SSL certificate provisioning

#### Step 5.2: Configure Basic Auth Headers
This prevents unauthorized API access:

1. In Railway dashboard → N8N service → Variables
2. Add these variables:
   - `N8N_BASIC_AUTH_ACTIVE`: `true` (should already be set)
   - `N8N_PROTOCOL`: `https`
   - `N8N_PORT`: `443`

#### Step 5.3: Restrict Public Access (Optional but Recommended)
If you want to restrict who can access your N8N instance:

**Option A: IP Whitelist (Railway Pro only)**
1. Railway Pro required ($20/month)
2. In service settings → "Networking"
3. Add allowed IP addresses

**Option B: Use Strong Passwords (Free)**
1. Ensure `N8N_BASIC_AUTH_PASSWORD` is very strong
2. Use password manager to generate 20+ character password
3. Enable 2FA on your email account that owns the N8N owner account

### Phase 6: Custom Domain Setup (Optional, 15 minutes)

If you want to use your own domain (e.g., `automation.youragency.com`):

#### Step 6.1: Purchase/Configure Domain
1. You need access to domain DNS settings
2. Common providers: Namecheap, GoDaddy, Cloudflare

#### Step 6.2: Add Custom Domain in Railway
1. Railway dashboard → N8N service → Settings
2. Scroll to "Domains" section
3. Click "Add Domain"
4. Enter your custom domain: `automation.youragency.com`
5. Railway will provide DNS records to add

#### Step 6.3: Configure DNS
1. Go to your domain provider's DNS settings
2. Add a CNAME record:
   - Name: `automation` (or your subdomain)
   - Value: Your Railway domain (`your-project-name.up.railway.app`)
   - TTL: 300 (or Auto)
3. Save DNS changes
4. Wait 5-60 minutes for DNS propagation

#### Step 6.4: Update N8N Variables
1. Railway dashboard → N8N service → Variables
2. Update these variables to use your custom domain:
   - `N8N_HOST`: `automation.youragency.com` (NO https://)
   - `WEBHOOK_URL`: `https://automation.youragency.com` (WITH https://)
3. Save and wait for redeployment

#### Step 6.5: Verify Custom Domain
1. Navigate to `https://automation.youragency.com`
2. Should redirect to your N8N instance
3. Verify SSL certificate (padlock in browser)
4. Test login

### Phase 7: Performance Optimization (10 minutes)

#### Step 7.1: Increase Resource Allocation
Railway defaults may be too low for heavy workflows:

1. Railway dashboard → N8N service → Settings
2. Scroll to "Resources" section
3. Recommended settings:
   - **Memory**: 1GB minimum (2GB for heavy use)
   - **CPU**: Shared (default is fine for most)
4. Click "Update" if you make changes

**Cost Impact:** Increasing resources increases monthly cost. Monitor your usage first.

#### Step 7.2: Enable Execution Data Pruning
This prevents database bloat:

1. Railway dashboard → N8N service → Variables
2. Ensure these are set (add if missing):
   - `EXECUTIONS_DATA_PRUNE`: `true`
   - `EXECUTIONS_DATA_MAX_AGE`: `168` (7 days)
   - `EXECUTIONS_DATA_PRUNE_MAX_COUNT`: `10000`

#### Step 7.3: Configure Queue Mode (Optional - Advanced)
For high-volume workflows, enable queue mode:

1. Add these variables:
   - `QUEUE_BULL_REDIS_HOST`: (requires Redis - see Advanced Setup)
   - `EXECUTIONS_MODE`: `queue`

**Note:** Queue mode requires Redis setup, which adds complexity and cost. Only needed for 200+ workflows.

### Phase 8: Backup Configuration (15 minutes)

#### Step 8.1: Enable Automated Database Backups
Railway doesn't auto-backup. Set this up manually:

1. Railway dashboard → Postgres service → Settings
2. Look for "Backups" section
3. If available, enable automated backups
4. Set frequency: Daily
5. Retention: 7 days minimum

**Note:** Railway's native backup feature is limited. See manual backup method below.

#### Step 8.2: Manual Backup Method
Use this workflow to backup your N8N database weekly:

1. Install PostgreSQL client locally:
   ```bash
   # Mac
   brew install postgresql

   # Ubuntu/Debian
   sudo apt-get install postgresql-client

   # Windows
   # Download from postgresql.org
   ```

2. Get database credentials from Railway:
   - Go to Postgres service → Variables
   - Copy: `DATABASE_URL` value
   - Format: `postgresql://user:password@host:port/database`

3. Create backup script (`backup-n8n.sh`):
   ```bash
   #!/bin/bash
   # N8N Database Backup Script

   # Get these from Railway Postgres service variables
   DB_HOST="your-host.railway.app"
   DB_PORT="5432"
   DB_NAME="railway"
   DB_USER="postgres"
   DB_PASSWORD="your-password"

   # Backup location
   BACKUP_DIR="$HOME/n8n-backups"
   mkdir -p $BACKUP_DIR

   # Create backup with timestamp
   TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
   BACKUP_FILE="$BACKUP_DIR/n8n_backup_$TIMESTAMP.sql"

   # Export database
   PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > $BACKUP_FILE

   # Compress backup
   gzip $BACKUP_FILE

   # Delete backups older than 30 days
   find $BACKUP_DIR -name "n8n_backup_*.sql.gz" -mtime +30 -delete

   echo "Backup completed: $BACKUP_FILE.gz"
   ```

4. Make script executable:
   ```bash
   chmod +x backup-n8n.sh
   ```

5. Test backup:
   ```bash
   ./backup-n8n.sh
   ```

6. Schedule with cron (Mac/Linux):
   ```bash
   # Edit crontab
   crontab -e

   # Add this line for weekly backups (every Sunday at 2 AM)
   0 2 * * 0 /path/to/backup-n8n.sh
   ```

#### Step 8.3: Test Backup Restoration
**CRITICAL:** Always test your backups!

1. Download a backup file from your backup directory
2. Decompress it:
   ```bash
   gunzip n8n_backup_TIMESTAMP.sql.gz
   ```

3. Restore to test database (DON'T restore to production until verified):
   ```bash
   PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME < n8n_backup_TIMESTAMP.sql
   ```

4. Verify workflows are present in N8N after restoration

### Phase 9: Monitoring Setup (10 minutes)

#### Step 9.1: Monitor Railway Metrics
1. Railway dashboard → N8N service
2. Click "Metrics" tab
3. Monitor:
   - CPU usage (should be <70% average)
   - Memory usage (should be <80% of allocated)
   - Network traffic
   - Restart count (should be 0 or very low)

#### Step 9.2: Set Up Usage Alerts
1. Railway dashboard → Project Settings
2. Go to "Usage" section
3. Set budget alerts:
   - Warning at: $10
   - Critical at: $20
4. Add your email for notifications

#### Step 9.3: Monitor N8N Execution Health
Create a monitoring workflow in N8N:

1. New workflow: "System Health Monitor"
2. Add "Schedule" trigger: Every 1 hour
3. Add "HTTP Request" node:
   - Method: GET
   - URL: `{{ $env.WEBHOOK_URL }}/healthz`
4. Add "IF" node:
   - Condition: `{{ $json.status === "ok" }}`
5. On FALSE branch:
   - Add "Send Email" or "Slack" node
   - Message: "N8N health check failed!"
6. Save and activate workflow

### Phase 10: Final Testing (15 minutes)

#### Step 10.1: Create Test Workflow
1. Click "Create Workflow" in N8N
2. Add a "Schedule Trigger" node:
   - Trigger Interval: Every 5 minutes
3. Add a "Code" node after it:
   - JavaScript Code:
     ```javascript
     return [{
       json: {
         message: "Test workflow executed successfully",
         timestamp: new Date().toISOString(),
         hostname: $env.N8N_HOST
       }
     }];
     ```
4. Click "Save" (top-right)
5. Name it "Test Workflow"
6. Toggle workflow to "Active"

#### Step 10.2: Monitor Test Executions
1. Wait 5 minutes
2. Go to "Executions" (left sidebar)
3. Should see successful execution of "Test Workflow"
4. Click on execution to see details
5. Verify timestamp and data are correct

#### Step 10.3: Test Webhook Functionality
1. Create new workflow: "Webhook Test"
2. Add "Webhook" trigger node:
   - HTTP Method: POST
   - Path: `test-webhook`
3. Add "Respond to Webhook" node:
   - Response Code: 200
   - Response Body:
     ```json
     {
       "success": true,
       "message": "Webhook received!"
     }
     ```
4. Save and activate workflow
5. Copy webhook URL (shown in Webhook node)
6. Test with curl:
   ```bash
   curl -X POST https://your-domain.up.railway.app/webhook-test/test-webhook \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```
7. Should receive: `{"success": true, "message": "Webhook received!"}`

#### Step 10.4: Test Credentials Storage
1. Go to "Credentials" (left sidebar)
2. Click "Add Credential"
3. Search for "Gmail"
4. Click on "Gmail OAuth2 API"
5. Fill in test values (don't need to be real for this test)
6. Click "Save"
7. Verify credential appears in credentials list
8. This confirms database storage is working

#### Step 10.5: Performance Baseline Test
1. Create workflow: "Performance Test"
2. Add "Manual Trigger"
3. Add "Code" node with loop:
   ```javascript
   const items = [];
   for (let i = 0; i < 100; i++) {
     items.push({
       json: {
         id: i,
         data: `Test item ${i}`,
         timestamp: new Date().toISOString()
       }
     });
   }
   return items;
   ```
4. Execute workflow manually
5. Note execution time (should be <2 seconds for 100 items)
6. If slower, consider increasing Railway resources

## Common Mistakes to Avoid

### Mistake 1: Not Setting N8N_HOST Correctly
**Problem:** Workflows fail with "Invalid URL" or webhooks don't work
**Solution:**
- N8N_HOST should be JUST the domain: `your-project.up.railway.app`
- NO `https://` prefix
- NO trailing slash `/`

### Mistake 2: Changing Encryption Key After Setup
**Problem:** All credentials become inaccessible, encrypted with old key
**Solution:**
- NEVER change `N8N_ENCRYPTION_KEY` after initial setup
- If you must, export all workflows first, delete credentials, update key, re-add credentials
- This is a DESTRUCTIVE operation

### Mistake 3: Not Enabling Execution Pruning
**Problem:** Database grows infinitely, slowing down N8N and increasing costs
**Solution:**
- Always set `EXECUTIONS_DATA_PRUNE=true`
- Set reasonable `EXECUTIONS_DATA_MAX_AGE` (168 hours = 1 week is good default)
- Monitor database size in Railway

### Mistake 4: Using Weak Basic Auth Password
**Problem:** Unauthorized access to your N8N instance
**Solution:**
- Use password manager to generate 20+ character password
- Include uppercase, lowercase, numbers, symbols
- Never use common passwords like "password123"

### Mistake 5: Not Monitoring Railway Usage
**Problem:** Unexpected bill at end of month
**Solution:**
- Set up budget alerts in Railway
- Check usage weekly
- Optimize workflows if costs are high
- Consider execution pruning for cost reduction

### Mistake 6: Forgetting to Backup
**Problem:** Lost all workflows and data due to accidental deletion or corruption
**Solution:**
- Set up automated backups (see Phase 8)
- Test restoration at least once
- Store backups in separate location (not on Railway)

### Mistake 7: Not Setting Correct Timezone
**Problem:** Scheduled workflows run at wrong times
**Solution:**
- Set `TZ` environment variable to your timezone
- Use correct tz database format: `America/New_York`, not `EST`
- Verify in N8N by checking execution times

### Mistake 8: Deploying Without Testing
**Problem:** Workflows fail in production, affecting clients
**Solution:**
- Always create test workflows first
- Verify webhook functionality
- Test credential storage
- Monitor first 24 hours closely

### Mistake 9: Not Allocating Enough Resources
**Problem:** N8N crashes under load, workflows fail randomly
**Solution:**
- Start with 1GB RAM minimum
- Monitor Railway metrics
- Increase resources if CPU >70% or memory >80%
- Workflows processing large data need 2GB+ RAM

### Mistake 10: Ignoring Security Headers
**Problem:** Vulnerable to XSS, clickjacking attacks
**Solution:**
- Ensure `N8N_PROTOCOL=https`
- Use Railway's automatic SSL
- Keep N8N updated to latest version
- Enable basic auth for additional protection layer

## Troubleshooting

### Issue 1: N8N Won't Start
**Symptoms:** Railway shows service as "crashed" or continuously restarting

**Diagnosis Steps:**
1. Railway dashboard → N8N service → "Logs" tab
2. Look for error messages in logs
3. Common errors and solutions:

**Error: "Connection refused - Database"**
- **Cause:** Database not connected properly
- **Solution:**
  1. Check if Postgres service is running
  2. Verify DATABASE_URL variable exists
  3. Check database connection variables (see Phase 4.2)
  4. Restart N8N service

**Error: "Port 5678 already in use"**
- **Cause:** Incorrect port configuration
- **Solution:**
  1. Verify `PORT` environment variable is NOT set (Railway auto-assigns)
  2. Check N8N_PORT is set to `443` or not set at all
  3. Redeploy service

**Error: "N8N_ENCRYPTION_KEY must be set"**
- **Cause:** Missing encryption key variable
- **Solution:**
  1. Generate key: `openssl rand -base64 32`
  2. Add as `N8N_ENCRYPTION_KEY` variable
  3. Redeploy

### Issue 2: Can't Access N8N Domain
**Symptoms:** Domain shows "Application Error" or won't load

**Diagnosis Steps:**
1. Check Railway service status: Should be "Active" with green dot
2. Check domain is correctly set up in Railway settings
3. Wait 2-3 minutes after deployment for service to fully start

**Solutions:**
- If service is crashed, check logs for errors
- If domain shows 404, verify:
  - Service is deployed
  - Domain is correctly configured
  - SSL certificate has been issued (can take 5-10 minutes)
- Try hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Issue 3: Workflows Not Saving
**Symptoms:** "Error saving workflow" message, changes don't persist

**Diagnosis Steps:**
1. Check Railway Postgres service is running
2. Check database connection (see Phase 4)
3. Check Railway database storage hasn't hit limit

**Solutions:**
- Verify database connection variables are correct
- Check Postgres logs for errors
- Verify disk space: Railway dashboard → Postgres → Metrics
- If database is full:
  1. Enable execution pruning (see Phase 7.2)
  2. Manually delete old executions:
     - N8N → Executions → Select old executions → Delete
  3. Increase Railway database storage (may increase cost)

### Issue 4: Webhooks Not Working
**Symptoms:** Webhook triggers not firing, external services can't reach N8N

**Diagnosis Steps:**
1. Test webhook manually:
   ```bash
   curl -X POST https://your-domain.up.railway.app/webhook-test/test-path
   ```
2. Check N8N logs: Execution history for webhook workflow
3. Verify workflow is ACTIVE (toggle in top-right of workflow editor)

**Solutions:**
- Verify `WEBHOOK_URL` includes `https://` prefix
- Check `N8N_HOST` has NO `https://` prefix (common mistake)
- Ensure webhook workflow is activated
- Test with simple webhook first (see Phase 10.3)
- Check firewall settings if using IP whitelist
- Verify SSL certificate is valid (browser padlock icon)

### Issue 5: Scheduled Workflows Not Running
**Symptoms:** Schedule trigger workflows don't execute at expected times

**Diagnosis Steps:**
1. Check workflow is ACTIVE
2. Verify timezone setting: `TZ` environment variable
3. Check Railway service didn't crash during scheduled time
4. Review execution history for errors

**Solutions:**
- Set `TZ` variable to your timezone (see Phase 2.3)
- Verify schedule cron expression is correct
- Check service uptime in Railway metrics
- For testing, set schedule to "Every 5 minutes" temporarily
- Review logs during scheduled execution time
- If timezone is wrong:
  1. Update `TZ` variable
  2. Redeploy service
  3. Deactivate and reactivate workflow

### Issue 6: High Railway Costs
**Symptoms:** Monthly bill higher than expected

**Diagnosis Steps:**
1. Railway dashboard → Project → Usage
2. Check which service is consuming most resources
3. Review metrics: CPU, Memory, Bandwidth
4. Check execution count in N8N

**Solutions:**
- Enable execution pruning (reduces database size):
  - `EXECUTIONS_DATA_PRUNE=true`
  - `EXECUTIONS_DATA_MAX_AGE=168` (1 week)
- Optimize workflows:
  - Remove unnecessary nodes
  - Reduce polling frequency for trigger nodes
  - Use webhooks instead of polling where possible
- Delete old unused workflows
- Check for runaway workflows (executing too frequently)
- Reduce memory allocation if over-provisioned
- Consider upgrading to Railway Pro for better pricing (evaluate if processing 200+ workflows)

### Issue 7: Credentials Lost After Restart
**Symptoms:** All credentials show as invalid after Railway restarts service

**Diagnosis Steps:**
1. Check if `N8N_ENCRYPTION_KEY` was changed
2. Verify database connection is stable
3. Check Postgres service logs for errors

**Solutions:**
- If encryption key changed:
  - **CANNOT RECOVER** - credentials are permanently encrypted with old key
  - Must re-add all credentials manually
  - **PREVENTION:** Never change encryption key
- If database connection issue:
  - Verify DATABASE_URL or connection variables
  - Check Postgres service is running
  - Restart N8N service after fixing database
- If credentials genuinely lost:
  - Must re-authenticate all credentials manually
  - Check backup if you have one (restore database)

### Issue 8: N8N Running Slowly
**Symptoms:** Workflows take long time to execute, UI is sluggish

**Diagnosis Steps:**
1. Railway dashboard → N8N service → Metrics
2. Check resource usage:
   - CPU usage >80%: Need more CPU
   - Memory usage >80%: Need more RAM
   - High restart count: Crashing due to resource limits
3. Check database size: Postgres service → Metrics

**Solutions:**
- Increase Railway resources:
  - Go to Settings → Resources
  - Increase memory to 2GB (may increase cost)
- Enable execution pruning (reduce database bloat)
- Delete old execution history:
  - N8N → Executions → Delete old executions
- Optimize workflows:
  - Split large workflows into smaller ones
  - Use "Set" node instead of "Code" for simple operations
  - Limit data passed between nodes
- Check for infinite loops in workflows
- Restart service to clear memory

### Issue 9: OAuth Connections Failing (Google, etc.)
**Symptoms:** "Redirect URI mismatch" or OAuth authorization fails

**Diagnosis Steps:**
1. Check OAuth redirect URL configuration
2. Verify in Google Cloud Console (or relevant platform)
3. Check `N8N_HOST` and `WEBHOOK_URL` are correctly set

**Solutions:**
- For Google OAuth (see separate skill: setup_n8n_google_oauth.md)
  - Verify redirect URL in Google Cloud Console matches Railway domain
  - Must be: `https://your-domain.up.railway.app/rest/oauth2-credential/callback`
- For other OAuth providers:
  - Add Railway domain to allowed redirect URIs in provider settings
  - Ensure `WEBHOOK_URL` is set with https:// prefix
  - Check if custom domain is needed (some providers require non-.railway.app domains)
- Clear browser cache and try OAuth flow again

### Issue 10: Database Connection Errors
**Symptoms:** "Connection to database failed" in logs

**Diagnosis Steps:**
1. Check Postgres service status in Railway
2. Verify database connection variables
3. Check Postgres logs for errors
4. Test database connection manually

**Solutions:**
- Restart Postgres service:
  - Railway → Postgres service → Settings → Restart
- Verify connection variables match:
  - N8N variables: DB_POSTGRESDB_* should match Postgres service variables
- Check Railway service networking:
  - Both services should be in same project
  - Railway auto-configures internal networking
- If persistent, redeploy both services:
  - Deploy Postgres first
  - Then deploy N8N
  - Verify DATABASE_URL is auto-set

## Success Metrics

### Immediate Success (Day 1)
- ✅ N8N accessible via Railway domain
- ✅ Can log in with credentials
- ✅ Can create and save workflows
- ✅ Test workflow executes successfully
- ✅ Webhooks respond to external requests
- ✅ Credentials save without errors

### Short-term Success (Week 1)
- ✅ No service crashes or restarts
- ✅ Scheduled workflows run at correct times
- ✅ Railway cost is within expected range ($5-15)
- ✅ All workflows migrated from N8N Cloud (if migrating)
- ✅ Team members can access and use instance
- ✅ Backup system tested and working

### Long-term Success (Month 1+)
- ✅ Railway cost stable and predictable
- ✅ No execution failures due to infrastructure
- ✅ Database size stable (execution pruning working)
- ✅ Workflow execution time within acceptable limits
- ✅ Cost savings vs N8N Cloud realized (if applicable)
- ✅ System monitoring alerts functioning
- ✅ Disaster recovery plan tested

### Key Performance Indicators (KPIs)
- **Uptime:** >99.5% (check Railway metrics)
- **Average execution time:** <5 seconds for simple workflows
- **Monthly cost:** <$20 for typical agency use
- **Database growth rate:** <100MB/week with pruning enabled
- **Failed executions:** <1% of total executions
- **Backup success rate:** 100% of scheduled backups complete

## Cost Optimization Strategies

### Strategy 1: Execution Pruning
**Impact:** Reduces database size, lowers storage costs
**Implementation:**
1. Set `EXECUTIONS_DATA_PRUNE=true`
2. Set `EXECUTIONS_DATA_MAX_AGE=168` (adjust based on needs)
3. Set `EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000`
4. Monitor database size reduction over 1 week

**Expected Savings:** Can reduce database size by 50-80% over time

### Strategy 2: Optimize Workflow Execution Frequency
**Impact:** Reduces CPU usage, bandwidth, and overall costs
**Implementation:**
1. Review all schedule triggers
2. Ask: Does this need to run every 5 minutes or would every 15 work?
3. Reduce polling frequency for trigger nodes
4. Use webhooks instead of polling where possible (e.g., for form submissions)

**Expected Savings:** 30-50% reduction in execution count

### Strategy 3: Resource Right-Sizing
**Impact:** Don't over-provision resources you don't need
**Implementation:**
1. Start with 1GB RAM
2. Monitor for 1 week
3. Only increase if consistently using >80% resources
4. Don't allocate "just in case" resources

**Expected Savings:** $3-8/month compared to over-provisioning

### Strategy 4: Workflow Consolidation
**Impact:** Fewer workflows = less overhead
**Implementation:**
1. Look for similar workflows that could be combined
2. Use "Switch" node to route different inputs through same workflow
3. Consolidate multiple schedule triggers into one workflow with routing

**Example:**
- Instead of: 5 separate workflows checking different email inboxes
- Create: 1 workflow that checks all 5 inboxes sequentially

**Expected Savings:** Reduces execution count and overhead

### Strategy 5: Use Efficient Nodes
**Impact:** Faster execution, less resource usage
**Implementation:**
1. Replace "Code" node with "Set" node where possible
2. Use "Merge" node instead of multiple "Code" nodes for data combining
3. Use "Filter" node instead of "IF" node when just filtering data
4. Avoid unnecessary "HTTP Request" nodes (cache data if possible)

**Expected Savings:** 10-20% faster execution times

### Strategy 6: Lazy Load Data
**Impact:** Don't process data you don't need
**Implementation:**
1. Use "Limit" parameter in API calls
2. Filter data early in workflow (before heavy processing)
3. Use pagination wisely
4. Don't fetch all data if you only need recent items

**Example:**
```javascript
// Instead of fetching all 10,000 records
// Fetch only last 100 with API pagination
GET /api/records?limit=100&sort=created_desc
```

**Expected Savings:** Reduces bandwidth and processing time

### Strategy 7: Monitor and Alert on Unusual Usage
**Impact:** Catch cost spikes before they become expensive
**Implementation:**
1. Set Railway budget alerts at $10 and $20
2. Create N8N workflow to monitor daily execution count
3. Alert if executions spike >50% above normal
4. Investigate and optimize runaway workflows immediately

### Cost Comparison Example
**Scenario:** Agency with 75 active workflows, 50,000 executions/month

**N8N Cloud Cost:**
- Starter: $20/month = 2,500 executions (not enough)
- Pro: $50/month = 10,000 executions (not enough)
- Advanced: $150/month = 50,000 executions ✓

**Self-Hosted Cost:**
- Railway: ~$12/month (1GB RAM, typical usage)
- Total savings: $138/month = $1,656/year

**Break-even point:** After first month (setup time investment pays off immediately in cost savings)

## Related Skills
- **build_n8n_workflow.md** - How to build workflows once N8N is set up
- **setup_n8n_error_handling.md** - Add robust error handling to workflows
- **setup_n8n_google_oauth.md** - Connect Google services to self-hosted N8N
- **import_modify_n8n_workflows.md** - Import and customize existing workflow templates
- **setup_n8n_gohighlevel_integration.md** - Connect Go High Level to your N8N instance

## Advanced Topics (Future Skills)

### Queue Mode for High Volume
When you have 200+ active workflows, consider queue mode:
- Requires Redis instance (additional Railway service)
- Enables workflow queuing for better resource management
- Prevents execution bottlenecks
- See dedicated advanced skill when processing >100,000 executions/month

### Multi-Instance Scaling
For enterprise-level usage (500+ workflows):
- Deploy multiple N8N instances behind load balancer
- Shared PostgreSQL database
- Redis for queue management
- Requires Railway Pro plan

### Custom Docker Image
For specific version control or custom modules:
- Fork N8N repository
- Build custom Docker image
- Deploy to Railway from GitHub repository
- Enables custom node development

## Quick Reference Commands

### Generate Encryption Key
```bash
openssl rand -base64 32
```

### Backup Database
```bash
PGPASSWORD=$DB_PASSWORD pg_dump -h $HOST -p $PORT -U $USER -d $DB > backup.sql
```

### Restore Database
```bash
PGPASSWORD=$DB_PASSWORD psql -h $HOST -p $PORT -U $USER -d $DB < backup.sql
```

### Test Webhook
```bash
curl -X POST https://your-domain.up.railway.app/webhook-test/test-path \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Check N8N Health
```bash
curl https://your-domain.up.railway.app/healthz
```

## Essential Environment Variables Quick Reference

| Variable | Example Value | Required | Purpose |
|----------|---------------|----------|---------|
| N8N_BASIC_AUTH_ACTIVE | `true` | Yes | Enable basic authentication |
| N8N_BASIC_AUTH_USER | `admin` | Yes | Login username |
| N8N_BASIC_AUTH_PASSWORD | `MySecure2024!Pass` | Yes | Login password |
| N8N_HOST | `my-n8n.up.railway.app` | Yes | Domain (no https) |
| WEBHOOK_URL | `https://my-n8n.up.railway.app` | Yes | Full URL with https |
| N8N_ENCRYPTION_KEY | `[32 random chars]` | Yes | Credential encryption |
| TZ | `America/New_York` | Recommended | Timezone for schedules |
| EXECUTIONS_DATA_PRUNE | `true` | Recommended | Auto-delete old executions |
| EXECUTIONS_DATA_MAX_AGE | `168` | Recommended | Keep executions for 7 days |
| N8N_PROTOCOL | `https` | Recommended | Force HTTPS |
| DB_TYPE | `postgresdb` | Auto | Database type |

## Final Checklist

Before considering your N8N self-hosted setup complete, verify:

- [ ] N8N accessible via Railway domain
- [ ] Basic authentication working
- [ ] Owner account created and can log in
- [ ] PostgreSQL database connected and workflows saving
- [ ] Test workflow created and executed successfully
- [ ] Webhook test workflow created and responding
- [ ] Timezone set correctly (TZ variable)
- [ ] Execution pruning enabled
- [ ] Backup system configured and tested
- [ ] Railway budget alerts set up
- [ ] Monitoring workflow created and active
- [ ] SSL certificate active (https working)
- [ ] All environment variables set correctly
- [ ] Resource allocation appropriate for usage
- [ ] Team members have access credentials
- [ ] Documentation saved for team reference

## Support and Resources

### Official N8N Resources
- Documentation: https://docs.n8n.io
- Community Forum: https://community.n8n.io
- GitHub Issues: https://github.com/n8n-io/n8n/issues

### Railway Resources
- Documentation: https://docs.railway.app
- Discord Community: https://discord.gg/railway
- Status Page: https://status.railway.app

### Common Questions
1. **"How do I upgrade N8N version?"**
   - Railway auto-updates to latest if using `n8nio/n8n:latest` image
   - To pin version, change to `n8nio/n8n:0.235.0` (example version)

2. **"Can I migrate from N8N Cloud?"**
   - Yes! Export workflows from Cloud, import to self-hosted
   - Credentials must be re-added (can't export from Cloud)

3. **"What if Railway shuts down?"**
   - Export all workflows regularly
   - Keep database backups
   - Can migrate to any Docker-compatible host (DigitalOcean, AWS, etc.)

---

**Skill Version:** 1.0
**Last Updated:** 2024
**Estimated Execution Time:** 90-120 minutes first time, 30-45 minutes after practice
**Difficulty:** Intermediate
**Prerequisites:** Basic command line knowledge, ability to follow instructions precisely
