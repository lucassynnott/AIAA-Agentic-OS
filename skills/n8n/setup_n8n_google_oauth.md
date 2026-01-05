# Setup N8N Google OAuth - Complete Google Services Integration

## Purpose
This skill provides step-by-step instructions for setting up Google OAuth authentication in self-hosted N8N, enabling integration with Gmail, Google Sheets, Google Docs, Google Drive, Google Calendar, and other Google Workspace services. This is one of the most important but potentially confusing aspects of self-hosting N8N.

## When to Use This Skill
- When setting up self-hosted N8N for the first time
- When you need to connect Google services (Gmail, Sheets, Docs, Drive, Calendar)
- When OAuth connections fail with "redirect URI mismatch" errors
- When connecting multiple Google accounts to N8N
- Before building workflows that rely on Google services
- When migrating from N8N Cloud to self-hosted (Google credentials need reconfiguration)

## Prerequisites

### Required Accounts
- **Google Account** - The account you want to connect to N8N
- **Google Cloud Console Access** - Same or different Google account (for creating OAuth app)
- **Self-Hosted N8N Instance** - Running on Railway, DigitalOcean, or other host
- **Public Domain** - Your N8N must be accessible via public URL (not localhost)

### Required Knowledge
- Basic N8N workflow understanding
- Understanding of OAuth2 authentication flow (helpful but not critical)
- Ability to follow multi-step technical instructions precisely

### Why This is Necessary for Self-Hosted N8N

**N8N Cloud vs Self-Hosted:**
```yaml
N8N Cloud:
  - Google OAuth pre-configured
  - Click "Sign in with Google" and it works
  - Uses N8N's OAuth credentials
  - No setup required

Self-Hosted N8N:
  - You must create your own OAuth app in Google Cloud Console
  - Configure redirect URLs manually
  - Enable APIs manually
  - Manage credentials yourself
  - This skill teaches you how
```

---

## Architecture Overview

### OAuth Flow for Google Services

```
User Action in N8N:
  ↓
1. User clicks "Sign in with Google" in credential setup
  ↓
2. N8N redirects to Google with OAuth Client ID
  ↓
3. Google shows consent screen (asks user to authorize)
  ↓
4. User clicks "Allow"
  ↓
5. Google redirects back to N8N with authorization code
  ↓
6. N8N exchanges code for access token
  ↓
7. N8N stores token securely
  ↓
8. Workflows can now use Google services
```

**What We're Configuring:**
- Step 2: OAuth Client ID (we create this)
- Step 3: Consent screen (we configure this)
- Step 5: Redirect URL (must match N8N's URL exactly)
- API Access: Which Google services N8N can use

---

## Phase 1: Access Google Cloud Console (5 minutes)

### Step 1.1: Navigate to Google Cloud Console

1. Open browser (Chrome recommended)
2. Go to: **https://console.cloud.google.com**
3. Sign in with your Google account
   - This can be any Google account
   - Doesn't have to be the account you'll connect to N8N
   - Recommend using your company/admin Google account

### Step 1.2: Understand Console Layout

**First Time Access:**
```
You'll see:
- Welcome screen
- "Select a project" dropdown (top bar)
- Or "Create Project" prompt

Don't worry if it looks different from screenshots - Google updates UI frequently
Key elements remain the same
```

**Main Navigation:**
```
Left Sidebar (☰ hamburger menu):
├── Home
├── APIs & Services
│   ├── Credentials (what we need)
│   ├── OAuth consent screen (what we need)
│   └── Library (what we need)
├── IAM & Admin
└── Other services
```

---

## Phase 2: Create Google Cloud Project (10 minutes)

### Step 2.1: Create New Project

**Why a Project?**
```
Google Cloud organizes everything into projects
- Project = Container for APIs, credentials, billing
- You can have multiple projects
- We'll create one specifically for N8N

Benefits:
- Keeps N8N OAuth separate from other Google projects
- Easy to manage/delete if needed
- Clear organization
```

**Creation Steps:**

1. **Click Project Selector**
   - Top bar, near Google Cloud logo
   - Shows current project or "Select a project"

2. **Click "New Project"**
   - Top right of project selector modal
   - Or if no projects exist, you'll see "Create Project" button

3. **Fill Project Details**
   ```yaml
   Project Name: N8N Automation
   Organization: (Leave as-is, usually your email)
   Location: (Leave default or select if you have an organization)
   ```

4. **Click "Create"**
   - Takes 10-30 seconds
   - Progress indicator shows at top

5. **Verify Project Created**
   - Notification appears: "Project created successfully"
   - Project selector now shows "N8N Automation"

**Important:** Make sure "N8N Automation" is selected in project selector before proceeding.

---

## Phase 3: Enable Required Google APIs (15 minutes)

### Step 3.1: Understand Which APIs to Enable

**Core APIs (Enable These First):**
```yaml
Google Drive API:
  - Required for: Drive, Docs, Sheets (they use Drive API)
  - Most important - enable this first

Google Sheets API:
  - For: Reading/writing Google Sheets
  - Requires Drive API also enabled

Gmail API:
  - For: Sending emails, reading inbox
  - Email automation

Google Calendar API:
  - For: Creating events, checking availability
  - Meeting scheduling automation
```

**How APIs Work:**
```
Enabled APIs = Services N8N can access
If API not enabled → N8N gets "API not enabled" error
Enable all APIs you plan to use now (can add more later)
```

### Step 3.2: Enable APIs One by One

**Process (Repeat for Each API):**

1. **Access API Library**
   - Click ☰ (hamburger menu)
   - Select "APIs & Services"
   - Click "Library" or "Enabled APIs & services" → "Library"

2. **Search for API**
   - Search bar at top: "Google Drive API"
   - Click on result (blue "Google Drive API" card)

3. **Enable API**
   - Click blue "Enable" button
   - Wait for "API enabled" confirmation (5-10 seconds)
   - Automatically redirects to API overview page

4. **Verify Enabled**
   - You'll see "API enabled" with green checkmark
   - Dashboard shows usage metrics (will be 0)

**Enable These APIs:**

**API 1: Google Drive API**
```
Search: "Google Drive API"
Enable: Yes (REQUIRED - enable first)
Why: Docs and Sheets need Drive API to function
```

**API 2: Google Sheets API**
```
Search: "Google Sheets API"
Enable: Yes (if using Sheets)
Why: Read/write spreadsheet data
```

**API 3: Gmail API**
```
Search: "Gmail API"
Enable: Yes (if using Gmail)
Why: Send emails, read inbox, manage labels
```

**API 4: Google Docs API**
```
Search: "Google Docs API"
Enable: Yes (if using Docs)
Why: Create/edit documents
```

**API 5: Google Calendar API**
```
Search: "Google Calendar API"
Enable: Yes (if using Calendar)
Why: Manage calendar events
```

**Verification:**
```
To verify all enabled:
1. ☰ Menu → APIs & Services → Dashboard
2. "Enabled APIs" section shows count
3. Click "View all" to see list
4. Should see: Drive, Sheets, Gmail, etc.
```

---

## Phase 4: Configure OAuth Consent Screen (20 minutes)

### Step 4.1: Understand OAuth Consent Screen

**What is it?**
```
The screen users see when connecting Google to N8N
Shows:
- App name (your choice)
- What permissions it's requesting
- Who created it
- Privacy policy (optional for internal use)
```

**Why Configure It?**
```
Required before creating OAuth credentials
Google needs to know:
- Who created this app
- What it does
- Who can use it (just you, or everyone)
```

### Step 4.2: Start OAuth Consent Screen Setup

1. **Navigate to OAuth Consent Screen**
   - ☰ Menu → APIs & Services
   - Click "OAuth consent screen" (left sidebar)

2. **Choose User Type**
   - You'll see two options:

   ```yaml
   Internal:
     - Only for Google Workspace organization users
     - Requires Google Workspace account (not free Gmail)
     - Not available if using personal Gmail
     - Skip this if using free Gmail account

   External:
     - For anyone with Google account
     - Works with free Gmail
     - Choose this for self-hosted N8N (recommended)
     - Allows you to connect any Google account
   ```

3. **Select "External"**
   - Click "External" radio button
   - Click "Create" button

### Step 4.3: Configure OAuth Consent Screen - Page 1

**OAuth Consent Screen Configuration:**

**App Information:**
```yaml
App Name: N8N Automation
  - Users see this when authorizing
  - Suggestion: "N8N" or "N8N Automation" or "Your Company N8N"

User Support Email: your-email@gmail.com
  - Select from dropdown (your Google account)
  - Users contact this if they have issues

App Logo: (Optional)
  - Upload 120x120px image
  - Can use N8N logo or skip
  - Not required for functionality
```

**App Domain (Optional - Can Skip):**
```yaml
Application Home Page: https://yourdomain.com (optional)
Application Privacy Policy: https://yourdomain.com/privacy (optional)
Application Terms of Service: https://yourdomain.com/terms (optional)

For internal agency use, these are not required
Only needed if making app public or for compliance
```

**Authorized Domains:**
```yaml
THIS IS CRITICAL - DO NOT SKIP

Add your N8N domain here:
- If Railway: railway.app
- If DigitalOcean: yourdomain.com
- If custom domain: yourdomain.com

Example: railway.app

Why this matters:
- Google only allows OAuth redirects to these domains
- If not added, you get "redirect URI mismatch" error

How to add:
1. Click "Add Domain" button
2. Type domain (just domain, not full URL)
   - Correct: railway.app
   - Wrong: https://your-app.railway.app
3. Press Enter
4. Domain appears in list below
```

**Developer Contact Information:**
```yaml
Email Addresses: your-email@gmail.com
  - Add at least one email
  - Google sends important notifications here
  - Click "Add Another Email" for multiple
```

**Click "Save and Continue"**

### Step 4.4: Configure Scopes - Page 2

**What are Scopes?**
```
Scopes = Permissions your app requests
Examples:
- Read Gmail messages
- Write to Google Sheets
- Create Google Docs

More scopes = More permissions = More things N8N can do
```

**For N8N, Add These Scopes:**

1. **Click "Add or Remove Scopes"**

2. **Filter scopes:** Type in search box to find

3. **Select these scopes:**

   ```yaml
   Google Drive:
   ☑ .../auth/drive - Full access to Drive
   ☑ .../auth/drive.file - Access to files created by app

   Google Sheets:
   ☑ .../auth/spreadsheets - Read/write spreadsheets

   Gmail:
   ☑ .../auth/gmail.modify - Read, write, send email
   ☑ .../auth/gmail.compose - Create and send messages
   ☑ .../auth/gmail.send - Send email on user's behalf

   Google Docs:
   ☑ .../auth/documents - Read/write documents

   Google Calendar:
   ☑ .../auth/calendar - Manage calendars
   ☑ .../auth/calendar.events - Create/edit events
   ```

4. **Click "Update" at bottom**

5. **Verify scopes added**
   - Should see list of selected scopes
   - Shows which APIs they're for
   - Shows as "Sensitive" or "Restricted" (normal)

6. **Click "Save and Continue"**

### Step 4.5: Test Users - Page 3

**What are Test Users?**
```
In development/testing mode, only listed users can authorize
Prevents random people from using your OAuth app
Required until you publish the app
```

**Add Test Users:**

1. **Click "Add Users"**

2. **Enter email addresses:**
   ```
   Add Google accounts that will connect to N8N:
   - Your main Google account
   - Any team member accounts
   - Client accounts (if they'll use N8N)

   Format: email@gmail.com (press Enter after each)

   You can add up to 100 test users
   ```

3. **Click "Add"**

4. **Verify users listed**

5. **Click "Save and Continue"**

**Important:** If a Google account isn't listed as a test user, they'll see "Access blocked: This app's request is invalid" when trying to authorize.

### Step 4.6: Summary - Page 4

**Review Configuration:**

1. **Check all sections are complete**
   ```
   ✓ OAuth consent screen
   ✓ Scopes
   ✓ Test users
   ```

2. **Click "Back to Dashboard"**

**Current Status:**
```
Publishing Status: Testing
- App in testing mode
- Only test users can authorize
- Good for initial setup and testing
```

---

## Phase 5: Publish OAuth App (CRITICAL STEP) (5 minutes)

### Step 5.1: Understand Publishing vs Testing Mode

**Testing Mode (Default):**
```
Limitations:
- Only test users (added in Step 4.5) can authorize
- Shows warning: "Google hasn't verified this app"
- OAuth tokens expire every 7 days
- Must manually re-authorize frequently

Result: Annoying for production use
```

**Published Mode:**
```
Benefits:
- Any Google account can authorize
- No expiration on tokens (stays authorized)
- No warning screens (for your test users)
- Production-ready

Caveat:
- Still shows "Google hasn't verified" to non-test users
- But test users won't see warnings
- Verification only needed if making app public (we're not)
```

### Step 5.2: Publish Your OAuth App

**Steps:**

1. **Navigate to OAuth Consent Screen**
   - ☰ Menu → APIs & Services → OAuth consent screen

2. **Find Publishing Status**
   - Top section shows: "Publishing status: Testing"
   - Or look for "Publish App" button

3. **Click "Publish App"**
   - Button location varies based on Google's UI updates
   - May be in top section or under "Publishing status"

4. **Confirm Publishing**
   - Modal appears: "Push to production?"
   - Click "Confirm" or "Publish"

5. **Verify Published**
   - Status changes to: "In production" or "Published"
   - Green checkmark or indicator

**CRITICAL:** If you skip this step, your N8N OAuth connections will break after 7 days!

---

## Phase 6: Create OAuth Credentials (15 minutes)

### Step 6.1: Navigate to Credentials

1. ☰ Menu → APIs & Services
2. Click "Credentials" (left sidebar)
3. You'll see credentials page (probably empty)

### Step 6.2: Create OAuth Client ID

1. **Click "Create Credentials" (top bar)**
   - Dropdown appears

2. **Select "OAuth client ID"**

3. **Application Type Selection**
   - Choose: **"Web application"**
   - (Desktop app, Mobile app are wrong for N8N)

4. **Name Your OAuth Client**
   ```yaml
   Name: N8N OAuth Client
   Or: N8N Automation
   Or: Your Company N8N

   This is just for your reference in Google Cloud Console
   ```

### Step 6.3: Configure Authorized Redirect URIs

**THIS IS THE MOST IMPORTANT STEP**

**Get Your N8N OAuth Redirect URL:**

1. **Open N8N in New Tab**
   - Keep Google Cloud Console open
   - Open your N8N instance: https://your-n8n-domain.up.railway.app

2. **Create Test Workflow**
   - Click "Create Workflow"

3. **Add Google Node**
   - Click "+" to add node
   - Search: "Gmail" (or Sheets, Docs, any Google service)
   - Click to add node

4. **Start Credential Creation**
   - Node opens → Credential dropdown
   - Click "Create New Credential"
   - Select "Google OAuth2 API" (not other options)

5. **Copy OAuth Redirect URL**
   - At top of credential form, you'll see:
   ```
   OAuth Redirect URL:
   https://your-n8n-domain.up.railway.app/rest/oauth2-credential/callback
   ```
   - Click copy icon or manually select and copy
   - **COPY THIS EXACTLY** - Every character matters

**Add Redirect URI to Google Cloud Console:**

1. **Back to Google Cloud Console**
   - Credentials page → Creating OAuth client ID

2. **Find "Authorized redirect URIs" section**

3. **Click "Add URI"**

4. **Paste N8N OAuth Redirect URL**
   ```
   Paste exactly:
   https://your-n8n-domain.up.railway.app/rest/oauth2-credential/callback

   Common mistakes to avoid:
   ✗ Missing https://
   ✗ Extra spaces at beginning or end
   ✗ Missing /rest/oauth2-credential/callback
   ✗ Typo in domain name
   ✗ Using localhost (won't work for self-hosted)
   ```

5. **Click "Add" or press Enter**
   - URI appears in list below

6. **Verify URI is correct**
   - Must match N8N's URL exactly
   - Check for typos

**Multiple N8N Instances?**
```
If you have multiple N8N instances (dev, staging, production):
1. Click "Add URI" again
2. Add redirect URL for each instance
3. Example:
   - https://n8n-dev.railway.app/rest/oauth2-credential/callback
   - https://n8n-staging.railway.app/rest/oauth2-credential/callback
   - https://n8n-prod.railway.app/rest/oauth2-credential/callback
```

### Step 6.4: Save OAuth Client

1. **Scroll to bottom**
2. **Click "Create"**
3. **Modal appears: "OAuth client created"**

**CRITICAL: Save These Credentials**

```yaml
Client ID:
  123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com

Client Secret:
  GOCSPX-AbCdEfGhIjKlMnOpQrStUvWxYz

COPY BOTH NOW
```

4. **Copy Client ID**
   - Click copy icon or select and copy
   - Save in secure location (password manager or notepad temporarily)

5. **Copy Client Secret**
   - Click copy icon or select and copy
   - Save in secure location

6. **Click "OK"**

**Important:** You can view these again later from Credentials page, but save them now for convenience.

---

## Phase 7: Configure N8N Credential (10 minutes)

### Step 7.1: Return to N8N

**Back to N8N tab:**
- Workflow with Gmail (or other Google node)
- Credential creation form open

### Step 7.2: Enter OAuth Credentials

**Fill in form:**

```yaml
Name: Google Account - Your Name
  (Or "Main Google Account" or "Company Google")
  Just for your reference in N8N

Client ID: [Paste from Google Cloud Console]
  The long string ending in .apps.googleusercontent.com

Client Secret: [Paste from Google Cloud Console]
  The string starting with GOCSPX-
```

**Verify:**
- No extra spaces
- Copied completely
- No truncation

### Step 7.3: Authorize Google Account

1. **Click "Sign in with Google"**
   - Button at bottom of credential form

2. **New window opens to Google**
   - Shows Google sign-in page

3. **Select Google Account**
   - Choose account to connect to N8N
   - Must be a test user (added in Phase 4.5)

4. **You May See Warning Screen**
   ```
   "Google hasn't verified this app"

   This is NORMAL for self-hosted apps
   It means Google hasn't reviewed your app (they only review public apps)

   Click "Advanced" (bottom left)
   Then: "Go to N8N Automation (unsafe)"
   ```

   **Is this actually unsafe?**
   ```
   No - it's your own app
   "Unsafe" just means Google hasn't verified it
   You control the app, you know it's safe
   Proceed with confidence
   ```

5. **Authorization Screen**
   - Shows permissions being requested (scopes from Phase 4.4)
   - Lists: "See, edit, create, and delete all your Google Drive files"
   - And other permissions based on scopes

6. **Review and Allow**
   - Review permissions (should match what you need)
   - Scroll to bottom
   - Click "Allow" or "Continue"

7. **Redirect Back to N8N**
   - Window closes automatically
   - Or shows "You can close this window"
   - Back to N8N credential form

8. **Success Confirmation**
   - N8N shows: "Successfully connected!"
   - Green checkmark appears
   - Credential is now active

### Step 7.4: Test Credential

1. **In your workflow node (Gmail, Sheets, etc.)**
   - Credential dropdown now shows your saved credential
   - Select it

2. **Configure node operation**
   - Gmail example: Resource: Message, Operation: Get All
   - Sheets example: Resource: Spreadsheet, Operation: Get All

3. **Click "Execute Node"**

4. **Verify it works**
   - Node shows green checkmark
   - Returns data (emails, sheets, etc.)
   - No error messages

**If it works: Success! Your Google OAuth is configured.**

---

## Phase 8: Configure Multiple Google Accounts (Optional) (10 minutes)

**Use Case:**
```
Connect multiple Google accounts to N8N:
- Personal and work Google accounts
- Multiple client Google accounts
- Different Google Workspace organizations
```

### Step 8.1: Ensure All Accounts Are Test Users

**Before adding new account:**

1. Go to Google Cloud Console
2. OAuth consent screen → Test users
3. Verify new Google account is in test users list
4. If not, click "Add Users", add it, save

### Step 8.2: Create Additional Credential in N8N

1. **In N8N workflow, add Google node (or open existing)**

2. **Credential dropdown → "Create New Credential"**
   - Select "Google OAuth2 API"

3. **Enter SAME Client ID and Secret**
   ```yaml
   Name: Google Account - Account Name (different name for organization)
   Client ID: [Same as first credential]
   Client Secret: [Same as first credential]
   ```

4. **Click "Sign in with Google"**

5. **Select DIFFERENT Google Account**
   - In Google sign-in, choose the other account
   - Or click "Use another account"

6. **Authorize**
   - Follow same authorization flow
   - Click "Allow"

7. **New Credential Created**
   - Now have two credentials in N8N
   - Each connects to different Google account
   - Can use either in workflows

**Managing Multiple Accounts:**
```
Name credentials clearly:
- "Google - Personal (john@gmail.com)"
- "Google - Work (john@company.com)"
- "Google - Client A (contact@clienta.com)"

When building workflows:
- Select appropriate credential for the task
- Can mix credentials in same workflow
  (e.g., read from one account, write to another)
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Publishing OAuth App
```
Symptom: OAuth works initially, breaks after 7 days
Error: "Invalid grant: token expired"
Cause: App still in "Testing" mode, not published

Solution:
1. Google Cloud Console → OAuth consent screen
2. Click "Publish App"
3. Confirm publishing
4. Re-authorize in N8N (may need to delete and recreate credential)
```

### Mistake 2: Redirect URI Mismatch
```
Symptom: Error during Google authorization: "redirect_uri_mismatch"
Cause: Redirect URI in Google Cloud doesn't match N8N's URL

Solution:
1. Check N8N OAuth redirect URL (in credential form)
2. Google Cloud Console → Credentials → Your OAuth client → Edit
3. Verify Authorized redirect URIs matches EXACTLY
4. Include https:// and full path: /rest/oauth2-credential/callback
5. Save changes in Google Cloud Console
6. Try authorization again in N8N
```

### Mistake 3: Forgetting to Add Domain
```
Symptom: Can't add redirect URI, Google shows error
Error: "Invalid redirect URI" or domain not authorized
Cause: Domain not added to "Authorized domains" in OAuth consent screen

Solution:
1. Google Cloud Console → OAuth consent screen → Edit app
2. Scroll to "Authorized domains"
3. Add your domain (e.g., railway.app)
4. Save
5. Go back to Credentials → Edit OAuth client
6. Now can add full redirect URI
```

### Mistake 4: Not Adding Test Users
```
Symptom: "Access blocked: This app's request is invalid"
Cause: Google account not listed in test users

Solution:
1. Google Cloud Console → OAuth consent screen → Test users
2. Add user's Google account email
3. Save
4. User can now authorize
```

### Mistake 5: Forgetting to Enable APIs
```
Symptom: Node executes but returns error: "API not enabled"
Error: "Gmail API has not been used in project... before or it is disabled"
Cause: Didn't enable required Google API

Solution:
1. Google Cloud Console → APIs & Services → Library
2. Search for the API mentioned in error (e.g., "Gmail API")
3. Click on it
4. Click "Enable"
5. Wait 1 minute for activation
6. Retry in N8N
```

### Mistake 6: Using Wrong Credential Type
```
Symptom: No "Sign in with Google" button in N8N
Cause: Selected wrong credential type (API Key instead of OAuth2)

Solution:
1. Delete incorrect credential in N8N
2. Create new credential
3. Choose "Google OAuth2 API" specifically
4. Not "Google Service Account" or other options
```

### Mistake 7: Credentials in Different Google Cloud Project
```
Symptom: OAuth works but node operations fail with 403 errors
Cause: OAuth client in one project, APIs enabled in different project

Solution:
1. Verify you're in correct Google Cloud project (check project selector)
2. Enable APIs in SAME project as OAuth credentials
3. Or recreate OAuth credentials in project where APIs are enabled
```

---

## Troubleshooting

### Issue 1: "Google hasn't verified this app" Warning Every Time
**Symptoms:** See warning screen every authorization, even after clicking "Advanced" → "Go to N8N"

**Solution:**
```
This happens when account isn't a test user:

1. Go to Google Cloud Console
2. OAuth consent screen → Test users
3. Add the Google account you're signing in with
4. Save
5. Try authorization again
6. Warning still appears, but won't for test users after
```

### Issue 2: OAuth Works But Node Fails with "Insufficient Permissions"
**Symptoms:** Authorization succeeds, but Gmail/Sheets node fails with permissions error

**Solution:**
```
Cause: Missing scopes

1. Google Cloud Console → OAuth consent screen → Edit app
2. Go to Scopes page
3. Add required scopes:
   - Gmail: .../auth/gmail.modify
   - Sheets: .../auth/spreadsheets
   - Drive: .../auth/drive
4. Save
5. In N8N, delete credential and recreate
6. Re-authorize (new scopes will be requested)
```

### Issue 3: "Redirect URI Mismatch" Despite Correct URI
**Symptoms:** URI in Google matches N8N but still get error

**Possible Causes:**

**Cause A: Trailing Slash**
```
Check for extra trailing slash:
Wrong: https://n8n.railway.app/rest/oauth2-credential/callback/
Right: https://n8n.railway.app/rest/oauth2-credential/callback
```

**Cause B: HTTP vs HTTPS**
```
Must use HTTPS:
Wrong: http://n8n.railway.app/rest/oauth2-credential/callback
Right: https://n8n.railway.app/rest/oauth2-credential/callback
```

**Cause C: Changes Not Saved**
```
1. Google Cloud Console → Credentials → OAuth client
2. Make sure you clicked "Save" after adding URI
3. Page should show "OAuth client updated" confirmation
```

**Cause D: Cached Old Settings**
```
1. In N8N, delete credential completely
2. Clear browser cache
3. Recreate credential with same Client ID and Secret
4. Try authorization again
```

### Issue 4: Authorization Succeeds But Token Expires Immediately
**Symptoms:** Can authorize but get "invalid token" error minutes later

**Cause: App Still in Testing Mode**

**Solution:**
```
1. Google Cloud Console → OAuth consent screen
2. Check "Publishing status"
3. If "Testing" → Click "Publish App"
4. In N8N, delete credential
5. Recreate and re-authorize
6. Token will now persist
```

### Issue 5: Multiple Google Accounts Get Confused
**Symptoms:** Trying to authorize Account B but keeps using Account A

**Solution:**
```
1. Open incognito/private browser window
2. Go to your N8N instance in incognito
3. Create credential and authorize
4. Sign in to correct Google account
5. Complete authorization
6. Credential created with correct account

Or:
1. Sign out of all Google accounts in browser
2. Then authorize in N8N
3. Sign in to specific account when prompted
```

### Issue 6: Can't Find "Publish App" Button
**Symptoms:** App status shows "Testing" but no publish button visible

**Solution:**
```
Google UI varies by account type:

Try these locations:
1. OAuth consent screen → Top section "Publishing status"
2. OAuth consent screen → Edit app → Last page
3. Look for "Push to production" link
4. Or "Make public" button

If truly can't find:
- App may already be published (check status text)
- Refresh page
- Or Google changed UI (search "publish oauth app google cloud")
```

---

## Success Metrics

### Immediate Success (Day 1)
- ✅ Google Cloud project created
- ✅ Required APIs enabled (Drive, Sheets, Gmail, etc.)
- ✅ OAuth consent screen configured
- ✅ OAuth client credentials created
- ✅ N8N credential authorized successfully
- ✅ Test node executes without errors

### Short-Term Success (Week 1)
- ✅ Multiple Google accounts connected if needed
- ✅ Gmail, Sheets, and other Google nodes working in production
- ✅ OAuth tokens not expiring (app is published)
- ✅ Team members can connect their Google accounts
- ✅ No "redirect URI mismatch" or authorization errors

### Long-Term Success (Month 1+)
- ✅ 10+ workflows using Google services running reliably
- ✅ No re-authorization required (tokens persist)
- ✅ Can connect new Google accounts without issues
- ✅ Can troubleshoot Google OAuth problems independently
- ✅ Team trained on Google integration setup

---

## Quick Reference

### Critical URLs
```
Google Cloud Console:
https://console.cloud.google.com

APIs & Services > Credentials:
https://console.cloud.google.com/apis/credentials

APIs & Services > OAuth Consent:
https://console.cloud.google.com/apis/credentials/consent

APIs & Services > Library:
https://console.cloud.google.com/apis/library
```

### Required OAuth Scopes for N8N
```
Google Drive:
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/drive.file

Google Sheets:
https://www.googleapis.com/auth/spreadsheets

Gmail:
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.compose
https://www.googleapis.com/auth/gmail.send

Google Docs:
https://www.googleapis.com/auth/documents

Google Calendar:
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/calendar.events
```

### Checklist: Is My Google OAuth Configured Correctly?
```
☐ Google Cloud project created
☐ APIs enabled: Drive, Sheets, Gmail, Docs, Calendar (as needed)
☐ OAuth consent screen configured
☐ App type: External
☐ Authorized domain added (e.g., railway.app)
☐ Scopes added for services you'll use
☐ Test users added (if not publishing publicly)
☐ OAuth app PUBLISHED (not in testing mode)
☐ OAuth client ID created (type: Web application)
☐ Redirect URI added and matches N8N exactly
☐ Client ID and Secret saved
☐ N8N credential created with correct Client ID and Secret
☐ Authorization completed successfully
☐ Test node executes without errors
☐ Token doesn't expire after 7 days
```

---

## Related Skills
- **setup_n8n_self_hosted.md** - Initial N8N setup (prerequisite)
- **build_n8n_workflow.md** - Using Google nodes in workflows
- **setup_n8n_gohighlevel_integration.md** - Similar OAuth setup process for GHL

---

**Skill Version:** 1.0
**Last Updated:** 2024
**Estimated Execution Time:** 45-60 minutes first time, 15-20 minutes after practice
**Difficulty:** Intermediate
**Prerequisites:** Self-hosted N8N instance running with public URL
