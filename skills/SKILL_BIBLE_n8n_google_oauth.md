# SKILL BIBLE: N8N Google OAuth Integration & Authentication Setup

## Executive Summary

This skill bible provides comprehensive guidance for setting up Google OAuth authentication in self-hosted N8N instances, enabling seamless integration with Gmail, Google Sheets, Google Docs, Google Drive, Google Calendar, and other Google Workspace services. Unlike N8N Cloud which comes with pre-configured Google OAuth, self-hosted installations require manual configuration of Google Cloud Console projects, API enablement, OAuth consent screens, and credential management.

The process involves creating a Google Cloud project, enabling necessary APIs, configuring OAuth consent screens, creating OAuth credentials, and properly linking them to N8N. This setup is critical for any automation workflows that interact with Google services and represents one of the most technically challenging but essential aspects of self-hosting N8N. Proper implementation ensures reliable, long-term authentication without token expiration issues.

This skill transforms a complex, multi-platform configuration process into a systematic, repeatable procedure that prevents common pitfalls like redirect URI mismatches, API enablement oversights, and OAuth app publishing failures that can cause authentication to break after 7 days.

## Source
- **Type:** Internal SOP/Skill Document  
- **Category:** n8n
- **Original File:** setup_n8n_google_oauth.md

## Core Principles

### 1. **Self-Hosted OAuth Ownership Principle**
Self-hosted N8N requires you to own and manage your OAuth credentials, unlike cloud versions where OAuth is pre-configured. This means creating your own Google Cloud project, managing API access, and maintaining OAuth credentials independently. Understanding this fundamental difference prevents confusion about why Google integrations don't "just work" out of the box.

### 2. **OAuth Flow Architecture Understanding**
The OAuth flow involves multiple redirects between N8N, Google's authorization servers, and back to N8N. Each step must be precisely configured: N8N redirects to Google with your Client ID, Google shows consent screen, user authorizes, Google redirects back to N8N with authorization code, N8N exchanges code for access token. Any misconfiguration breaks this chain.

### 3. **Domain and Redirect URI Precision**
Redirect URI configuration is the most critical and error-prone aspect. The URI in Google Cloud Console must match N8N's OAuth callback URL exactly - including protocol (HTTPS), domain, path, and absence of trailing characters. Even minor discrepancies cause "redirect_uri_mismatch" errors that prevent authorization.

### 4. **API Enablement Before Usage**
Google APIs must be explicitly enabled in Google Cloud Console before N8N can access them. Attempting to use services like Gmail or Google Sheets without enabling their respective APIs results in "API not enabled" errors. Enable all APIs you plan to use during initial setup to avoid workflow failures.

### 5. **OAuth App Publishing Requirement**
OAuth apps default to "Testing" mode with 7-day token expiration. Publishing the app to "Production" mode eliminates token expiration and warning screens for test users. Failing to publish causes authentication to break after one week, requiring re-authorization.

### 6. **Test User Management Strategy**
In testing/development mode, only explicitly listed test users can authorize the OAuth app. Any Google account not in the test user list receives "Access blocked" errors. Maintain an accurate test user list including all accounts that need N8N access.

### 7. **Scope and Permission Alignment**
OAuth scopes determine what permissions N8N requests from Google. Insufficient scopes cause "permission denied" errors even after successful authorization. Configure comprehensive scopes during initial setup rather than adding them incrementally, as scope changes require re-authorization.

### 8. **Multi-Account Credential Management**
Each Google account requires a separate N8N credential, but all can use the same OAuth Client ID and Secret. Proper naming conventions and organization prevent confusion when managing multiple Google accounts within N8N workflows.

## Step-by-Step Process

### Phase 1: Google Cloud Console Access and Project Creation (15 minutes)

**Step 1.1: Access Google Cloud Console**
1. Navigate to https://console.cloud.google.com in Chrome browser
2. Sign in with Google account (can be any Google account, doesn't need to match N8N connection accounts)
3. Accept terms of service if prompted
4. Familiarize yourself with console layout: hamburger menu (☰) on left, project selector in top bar

**Step 1.2: Create Dedicated Google Cloud Project**
1. Click project selector in top bar (shows current project or "Select a project")
2. Click "New Project" in top-right of modal
3. Configure project details:
   - Project Name: "N8N Automation" (or similar descriptive name)
   - Organization: Leave default (usually your email domain)
   - Location: Leave default unless you have organizational requirements
4. Click "Create" and wait 10-30 seconds for project creation
5. Verify project appears in project selector and is currently selected
6. Note project ID for future reference (appears under project name)

### Phase 2: Google API Enablement (20 minutes)

**Step 2.1: Access API Library**
1. Click hamburger menu (☰) → "APIs & Services" → "Library"
2. Understand that APIs must be explicitly enabled before N8N can access them
3. Plan to enable all APIs you'll use now to avoid future workflow failures

**Step 2.2: Enable Core APIs (Repeat for Each)**
1. **Google Drive API** (CRITICAL - Enable First):
   - Search "Google Drive API" in library search bar
   - Click on "Google Drive API" result card
   - Click blue "Enable" button
   - Wait for "API enabled" confirmation (5-10 seconds)
   - Verify you see green checkmark and API dashboard

2. **Google Sheets API**:
   - Return to API Library (back button or navigate via menu)
   - Search "Google Sheets API"
   - Enable following same process
   - Note: Requires Drive API also enabled

3. **Gmail API**:
   - Search "Gmail API"
   - Enable for email automation capabilities
   - Provides send, read, and manage email functionality

4. **Google Docs API**:
   - Search "Google Docs API"  
   - Enable for document creation and editing
   - Also requires Drive API for file access

5. **Google Calendar API**:
   - Search "Google Calendar API"
   - Enable for calendar event management
   - Provides create, read, update, delete event capabilities

**Step 2.3: Verify API Enablement**
1. Navigate to "APIs & Services" → "Dashboard"
2. Confirm "Enabled APIs" section shows count of enabled APIs
3. Click "View all" to see complete list
4. Verify all intended APIs appear with "Enabled" status

### Phase 3: OAuth Consent Screen Configuration (25 minutes)

**Step 3.1: Initialize OAuth Consent Screen**
1. Navigate to "APIs & Services" → "OAuth consent screen"
2. Choose user type:
   - **External**: For any Google account (recommended for self-hosted N8N)
   - **Internal**: Only for Google Workspace organization users (requires paid Workspace)
3. Select "External" and click "Create"

**Step 3.2: Configure OAuth Consent Screen (Page 1)**
1. **App Information**:
   - App Name: "N8N Automation" (users see this during authorization)
   - User Support Email: Select your Google account from dropdown
   - App Logo: Optional 120x120px image (can skip)

2. **App Domain Configuration** (Optional for internal use):
   - Application Home Page: Your company website (optional)
   - Privacy Policy: Privacy policy URL (optional)
   - Terms of Service: Terms URL (optional)

3. **Authorized Domains** (CRITICAL):
   - Click "Add Domain"
   - Enter your N8N domain (just domain, not full URL):
     - Railway: `railway.app`
     - Custom domain: `yourdomain.com`
     - DigitalOcean: `yourdomain.com`
   - Press Enter to add domain
   - Verify domain appears in list below

4. **Developer Contact Information**:
   - Add at least one email address for Google notifications
   - Click "Add Another Email" for multiple contacts

5. Click "Save and Continue"

**Step 3.3: Configure Scopes (Page 2)**
1. Click "Add or Remove Scopes"
2. Use search functionality to find and select these scopes:

   **Google Drive Scopes**:
   - `https://www.googleapis.com/auth/drive` (Full Drive access)
   - `https://www.googleapis.com/auth/drive.file` (File-specific access)

   **Google Sheets Scopes**:
   - `https://www.googleapis.com/auth/spreadsheets` (Read/write spreadsheets)

   **Gmail Scopes**:
   - `https://www.googleapis.com/auth/gmail.modify` (Read, write, send email)
   - `https://www.googleapis.com/auth/gmail.compose` (Create and send messages)
   - `https://www.googleapis.com/auth/gmail.send` (Send email on behalf of user)

   **Google Docs Scopes**:
   - `https://www.googleapis.com/auth/documents` (Read/write documents)

   **Google Calendar Scopes**:
   - `https://www.googleapis.com/auth/calendar` (Manage calendars)
   - `https://www.googleapis.com/auth/calendar.events` (Create/edit events)

3. Click "Update" to save scope selection
4. Verify selected scopes appear in summary list
5. Click "Save and Continue"

**Step 3.4: Configure Test Users (Page 3)**
1. Click "Add Users"
2. Enter Google account email addresses that will connect to N8N:
   - Your primary Google account
   - Team member accounts
   - Client accounts requiring N8N access
   - Up to 100 test users allowed
3. Press Enter after each email address
4. Click "Add" to save test users
5. Verify all users appear in test users list
6. Click "Save and Continue"

**Step 3.5: Review and Complete (Page 4)**
1. Review all configuration sections for completeness
2. Verify all sections show green checkmarks
3. Click "Back to Dashboard"
4. Note current status shows "Testing" (will change this in next phase)

### Phase 4: OAuth App Publishing (CRITICAL - 5 minutes)

**Step 4.1: Understand Publishing Necessity**
- Testing Mode: Only test users can authorize, tokens expire every 7 days
- Published Mode: No token expiration, production-ready authentication
- Publishing is essential for reliable long-term operation

**Step 4.2: Publish OAuth Application**
1. Navigate to "OAuth consent screen" if not already there
2. Locate "Publishing status" section showing "Testing"
3. Click "Publish App" button (location varies in Google's UI)
4. Confirm publishing in modal dialog by clicking "Confirm" or "Publish"
5. Verify status changes to "In production" or "Published"
6. Look for green indicator or confirmation message

### Phase 5: OAuth Credentials Creation (15 minutes)

**Step 5.1: Create OAuth Client ID**
1. Navigate to "APIs & Services" → "Credentials"
2. Click "Create Credentials" in top bar
3. Select "OAuth client ID" from dropdown
4. Choose "Web application" as application type
5. Name your OAuth client: "N8N OAuth Client" (for reference only)

**Step 5.2: Configure Authorized Redirect URIs**
1. **Obtain N8N OAuth Redirect URL**:
   - Open N8N instance in new browser tab
   - Create new workflow or open existing
   - Add Google service node (Gmail, Sheets, etc.)
   - Click node → Credential dropdown → "Create New Credential"
   - Select "Google OAuth2 API"
   - Copy OAuth Redirect URL from top of form:
     `https://your-n8n-domain.up.railway.app/rest/oauth2-credential/callback`

2. **Add Redirect URI to Google Cloud Console**:
   - Return to Google Cloud Console credentials creation
   - Find "Authorized redirect URIs" section
   - Click "Add URI"
   - Paste N8N OAuth redirect URL exactly (no modifications)
   - Verify URL includes:
     - `https://` protocol
     - Correct domain name
     - `/rest/oauth2-credential/callback` path
     - No trailing slash or extra characters
   - Press Enter to add URI

3. **Handle Multiple N8N Instances** (if applicable):
   - Add separate redirect URI for each N8N instance
   - Development, staging, and production environments each need unique URIs

**Step 5.3: Save OAuth Client and Retrieve Credentials**
1. Click "Create" to save OAuth client
2. Modal appears with OAuth client credentials
3. **CRITICAL**: Copy and securely store both values:
   - **Client ID**: Long string ending in `.apps.googleusercontent.com`
   - **Client Secret**: String beginning with `GOCSPX-`
4. Save credentials in password manager or secure temporary location
5. Click "OK" to close modal

### Phase 6: N8N Credential Configuration (10 minutes)

**Step 6.1: Create N8N Google Credential**
1. Return to N8N browser tab with Google node open
2. In credential creation form, enter:
   - **Name**: Descriptive name like "Google Account - [Account Name]"
   - **Client ID**: Paste from Google Cloud Console
   - **Client Secret**: Paste from Google Cloud Console
3. Verify no extra spaces or truncation in pasted values

**Step 6.2: Authorize Google Account**
1. Click "Sign in with Google" button
2. New window opens to Google authorization
3. Select Google account to connect (must be in test users list)
4. **Handle Security Warning** (if appears):
   - "Google hasn't verified this app" is normal for self-hosted apps
   - Click "Advanced" → "Go to N8N Automation (unsafe)"
   - This is safe - it's your own OAuth application
5. **Review Authorization Screen**:
   - Shows requested permissions (scopes configured earlier)
   - Lists specific access being granted
   - Scroll through all permissions
6. Click "Allow" or "Continue" to authorize
7. Window closes or shows "You can close this window"
8. Return to N8N shows "Successfully connected!" message

**Step 6.3: Test Credential Functionality**
1. In Google service node, select newly created credential
2. Configure basic node operation:
   - Gmail: Resource "Message", Operation "Get All"
   - Sheets: Resource "Spreadsheet", Operation "Get All"
   - Drive: Resource "File", Operation "Get All"
3. Click "Execute Node" to test
4. Verify node returns data without errors
5. Green checkmark indicates successful authentication and API access

### Phase 7: Multiple Account Configuration (Optional - 10 minutes per account)

**Step 7.1: Prepare Additional Accounts**
1. Ensure additional Google accounts are added to test users list in Google Cloud Console
2. Navigate to "OAuth consent screen" → "Test users"
3. Add any additional Google accounts that will connect to N8N
4. Save changes

**Step 7.2: Create Additional N8N Credentials**
1. In N8N, create new credential for each additional Google account
2. Use same Client ID and Client Secret for all credentials
3. Use descriptive naming convention:
   - "Google - Personal ([email])"
   - "Google - Work ([email])"
   - "Google - Client A ([email])"
4. Follow same authorization process for each account
5. Select appropriate Google account during authorization

**Step 7.3: Organize Multiple Credentials**
1. Test each credential with appropriate Google service nodes
2. Document which credential connects to which Google account
3. Establish workflow conventions for credential selection
4. Consider access patterns and data segregation requirements

## Frameworks & Templates

### OAuth Configuration Checklist Framework
```
Pre-Configuration Phase:
☐ Self-hosted N8N instance running with public URL
☐ Google account for Google Cloud Console access
☐ List of Google services needed (Gmail, Sheets, Docs, Drive, Calendar)
☐ List of Google accounts that will connect to N8N

Google Cloud Console Configuration:
☐ Project created with descriptive name
☐ All required APIs enabled (Drive, Sheets, Gmail, Docs, Calendar)
☐ OAuth consent screen configured with external user type
☐ Authorized domain added (matches N8N domain)
☐ Comprehensive scopes selected for all needed services
☐ Test users added for all connecting Google accounts
☐ OAuth app published (not in testing mode)
☐ OAuth client ID created as web application
☐ Redirect URI matches N8N OAuth callback exactly
☐ Client ID and Secret securely stored

N8N Configuration:
☐ Google OAuth2 API credential created
☐ Client ID and Secret entered correctly
☐ Authorization completed successfully
☐ Test node execution successful
☐ Multiple accounts configured if needed
☐ Credentials named descriptively

Validation:
☐ No "redirect_uri_mismatch" errors
☐ No "API not enabled" errors  
☐ No token expiration after 7 days
☐ All team members can authorize successfully
☐ Production workflows using Google services function reliably
```

### Google API Scope Selection Template
```yaml
Gmail Integration Scopes:
  Basic Email Access:
    - gmail.readonly (read-only access)
  Full Email Management:
    - gmail.modify (read, write, send)
    - gmail.compose (create messages)
    - gmail.send (send on behalf)

Google Sheets Integration Scopes:
  Read/Write Spreadsheets:
    - spreadsheets (full access)
  Drive Access (Required):
    - drive.file (files created by app)
    - drive (full Drive access)

Google Docs Integration Scopes:
  Document Management:
    - documents (read/write docs)
  Drive Access (Required):
    - drive.file (files created by app)
    - drive (full Drive access)

Google Calendar Integration Scopes:
  Calendar Management:
    - calendar (manage calendars)
    - calendar.events (manage events)
  Read-Only Calendar:
    - calendar.readonly (read-only access)

Google Drive Integration Scopes:
  File Management:
    - drive (full Drive access)
    - drive.file (app-created files only)
  Metadata Only:
    - drive.metadata.readonly (file info only)
```

### Multi-Account Credential Naming Convention
```
Template: "Google - [Account Type] ([Email/Identifier])"

Examples:
- "Google - Personal (john@gmail.com)"
- "Google - Work (john@company.com)"  
- "Google - Client A (contact@clienta.com)"
- "Google - Marketing (marketing@company.com)"
- "Google - Support (support@company.com)"

Benefits:
- Clear identification in credential dropdown
- Easy workflow credential selection
- Simplified troubleshooting
- Organized credential management
```

### OAuth Redirect URI Validation Template
```
Correct Format:
https://[n8n-domain]/rest/oauth2-credential/callback

Examples:
✓ https://n8n-prod.railway.app/rest/oauth2-credential/callback
✓ https://automation.company.com/rest/oauth2-credential/callback
✓ https://n8n.example.com/rest/oauth2-credential/callback

Common Mistakes:
✗ http://n8n-prod.railway.app/rest/oauth2-credential/callback (HTTP not HTTPS)
✗ https://n8n-prod.railway.app/rest/oauth2-credential/callback/ (trailing slash)
✗ https://n8n-prod.railway.app/oauth2-credential/callback (missing /rest/)
✗ https://localhost:5678/rest/oauth2-credential/callback (localhost not accessible)
```

## Best Practices

### Security and Access Management
**Principle of Least Privilege**: Only enable APIs and scopes that you actually need. Start with minimal permissions and add more as requirements become clear. This reduces security exposure and simplifies troubleshooting.

**Dedicated Google Cloud Project**: Create a separate Google Cloud project specifically for N8N OAuth rather than mixing with other projects. This provides clear separation, easier management, and simplified billing/usage tracking.

**Test User Management**: Maintain an accurate list of test users and review periodically. Remove users who no longer need access and add new team members promptly to prevent access issues.

**Credential Naming Conventions**: Use descriptive, consistent naming for N8N credentials that clearly identifies which Google account each credential represents. This prevents confusion in workflows and troubleshooting.

### Configuration Management
**Document OAuth Settings**: Maintain documentation of your OAuth configuration including Client ID (not secret), enabled APIs, authorized domains, and test users. This facilitates troubleshooting and team knowledge sharing.

**Version Control OAuth Consent Screen**: Take screenshots or export configuration of your OAuth consent screen setup. Google's UI changes frequently, and having reference documentation helps with future modifications.

**Backup Client Credentials**: Store Client ID and Client Secret in secure password manager or encrypted documentation. While retrievable from Google Cloud Console, having backup access speeds up troubleshooting and new environment setup.

### Operational Excellence
**Publish OAuth App Immediately**: Don't operate in testing mode longer than necessary. Publish the OAuth app as soon as initial testing is complete to prevent token expiration issues.

**Test All Integrations**: After OAuth setup, test each Google service integration (Gmail, Sheets, Docs, etc.) with simple operations to verify full functionality before building complex workflows.

**Monitor Token Health**: Periodically verify that OAuth tokens remain valid by testing Google service nodes. Set up monitoring workflows that alert if Google integrations fail.

**Plan for Scale**: If you anticipate multiple N8N instances (development, staging, production), configure redirect URIs for all environments during initial setup rather than adding them later.

### Troubleshooting Preparation
**Enable Comprehensive Logging**: Configure N8N logging to capture OAuth and API errors for troubleshooting. Understanding error patterns helps identify configuration issues quickly.

**Maintain Test Workflows**: Create simple test workflows for each Google service that can be executed to verify OAuth functionality. These serve as health checks and troubleshooting tools.

**Document Common Error Resolutions**: Keep a record of OAuth errors encountered and their solutions. This builds institutional knowledge and speeds up future troubleshooting.

## Common Mistakes to Avoid

### Critical Configuration Errors

**Mistake: Not Publishing OAuth App**
- **Symptom**: OAuth works initially but breaks after exactly 7 days with "invalid grant" or "token expired" errors
- **Root Cause**: OAuth app remains in "Testing" mode with automatic token expiration
- **Impact**: All Google integrations stop working, requiring re-authorization
- **Prevention**: Always publish OAuth app to production mode immediately after initial testing
- **Recovery**: Publish app, delete N8N credentials, recreate and re-authorize

**Mistake: Redirect URI Mismatch**
- **Symptom**: "redirect_uri_mismatch" error during Google authorization
- **Root Cause**: URI in Google Cloud Console doesn't exactly match N8N's OAuth callback URL
- **Common Variations**: Missing HTTPS, extra trailing slash, typo in domain, missing path components
- **Prevention**: Copy redirect URI directly from N8N credential form, verify character-by-character
- **Recovery**: Edit OAuth client in Google Cloud Console, correct redirect URI, save changes

**Mistake: Forgetting to Enable APIs**
- **Symptom**: Authorization succeeds but node execution fails with "API has not been used" or "API not enabled" errors
- **Root Cause**: Google APIs must be explicitly enabled before use
- **Impact**: Workflows fail despite successful OAuth setup
- **Prevention**: Enable all required APIs during initial setup phase
- **Recovery**: Enable missing API in Google Cloud Console, wait 1-2 minutes, retry operation

### Access and Permission Errors

**Mistake: Insufficient OAuth Scopes**
- **Symptom**: Authorization succeeds but operations fail with "insufficient permissions" or "access denied" errors
- **Root Cause**: OAuth scopes don't include permissions needed for specific operations
- **Impact**: Limited functionality despite successful connection
- **Prevention**: Configure comprehensive scopes during initial setup
- **Recovery**: Add required scopes to OAuth consent screen, delete and recreate N8N credential

**Mistake: Not Adding Test Users**
- **Symptom**: "Access blocked: This app's request is invalid" error during authorization
- **Root Cause**: Google account attempting authorization not listed in test users
- **Impact**: Users cannot connect their Google accounts to N8N
- **Prevention**: Add all connecting Google accounts to test users list
- **Recovery**: Add user to test users in OAuth consent screen, save, retry authorization

**Mistake: Wrong Credential Type Selection**
- **Symptom**: No "Sign in with Google" button appears in N8N credential form
- **Root Cause**: Selected "Google Service Account" or other credential type instead of "Google OAuth2 API"
- **Impact**: Cannot complete OAuth flow
- **Prevention**: Always select "Google OAuth2 API" for user account connections
- **Recovery