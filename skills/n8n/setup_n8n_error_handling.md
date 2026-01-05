# Setup N8N Error Handling - Comprehensive Error Management Guide

## Purpose
This skill teaches you how to implement production-ready error handling in N8N workflows, ensuring failures are caught, logged, and resolved automatically where possible. This is CRITICAL for client-facing automations that must run reliably 24/7.

## When to Use This Skill
- Before deploying ANY workflow to production
- When workflows fail silently and you don't know why
- When you need to ensure client deliverables are reliable
- When you want to be notified immediately of workflow failures
- When building critical business automations

## Prerequisites
- N8N instance set up and running
- Basic understanding of N8N workflows (see build_n8n_workflow.md)
- At least one workflow already built
- Notification channel ready (Slack, email, or Telegram)

## Error Handling Architecture

### The Three Layers of Error Handling
```
Layer 1: Node-Level Error Handling
    ↓ (if error)
Layer 2: Workflow-Level Error Handling
    ↓ (if critical error)
Layer 3: Global Error Workflow
```

**Layer 1:** Individual nodes have "On Error" settings
**Layer 2:** Workflow settings define what happens on failures
**Layer 3:** Separate "Error Workflow" handles all errors globally

## Step-by-Step Implementation

### Phase 1: Node-Level Error Handling (15 minutes)

#### Step 1.1: Configure "Continue on Fail" for Individual Nodes

Every node in N8N has error handling options. Access them:

1. Double-click any node to open configuration
2. Click "Settings" tab (at top of node panel)
3. Find "On Error" section
4. Configure based on node importance

**Option A: Continue On Fail**
- **When to use:** Non-critical nodes where workflow should continue even if this fails
- **Example:** Sending a notification to Slack - if Slack is down, main workflow should still complete
- **Configuration:**
  1. Toggle "Continue on Fail" to ON
  2. Workflow will continue to next node even if this fails
  3. Failed node shows red warning but doesn't stop execution

**Example Use Case:**
```
Get Order from Database (CRITICAL - don't continue on fail)
    ↓
Process Payment (CRITICAL - don't continue on fail)
    ↓
Send Confirmation Email (Continue on fail = ON)
    ↓
Post to Slack (Continue on fail = ON)
```

**Implementation:**
1. Open workflow
2. For each notification node (Slack, Email notifications):
   - Double-click node
   - Settings tab
   - Enable "Continue on Fail"
3. For each critical node (API calls, database operations):
   - LEAVE "Continue on Fail" OFF
   - These should stop workflow if they fail

#### Step 1.2: Use "Retry on Fail" for Flaky APIs

Some APIs fail temporarily (rate limits, network issues). Retry automatically:

**Configuration:**
1. Double-click node
2. Settings tab → "Retry on Fail" section
3. Set:
   - **Number of Retries:** 3 (recommended)
   - **Time Between Retries (ms):** 1000 (1 second)
4. N8N will automatically retry failed requests

**Best for:**
- HTTP Request nodes calling external APIs
- Database operations that might timeout
- File download/upload operations

**Example:**
```
HTTP Request Node (Call External API)
Settings:
  Continue on Fail: OFF
  Retry on Fail: ON
    Number of Retries: 3
    Time Between Retries: 1000ms
```

**Advanced: Exponential Backoff**
For APIs with strict rate limits:
- Retry 1: Wait 1 second
- Retry 2: Wait 2 seconds
- Retry 3: Wait 4 seconds

N8N doesn't have built-in exponential backoff. Implement with multiple HTTP nodes:
```
HTTP Request (Attempt 1)
    ↓ (on error)
Wait (2 seconds)
    ↓
HTTP Request (Attempt 2)
    ↓ (on error)
Wait (4 seconds)
    ↓
HTTP Request (Attempt 3)
```

#### Step 1.3: Implement Try-Catch in Code Nodes

ALWAYS wrap Code node logic in try-catch:

**Basic Pattern:**
```javascript
try {
  // Your main logic
  const result = processData($json);

  return [{
    json: {
      success: true,
      data: result
    }
  }];
} catch (error) {
  // Error handling
  return [{
    json: {
      success: false,
      error: error.message,
      stackTrace: error.stack,
      originalData: $json
    }
  }];
}
```

**Advanced Pattern with Logging:**
```javascript
try {
  console.log('[Start] Processing item:', $json.id);

  // Validate input
  if (!$json.required_field) {
    throw new Error('Missing required field: required_field');
  }

  // Process
  const result = complexOperation($json);
  console.log('[Success] Processed item:', $json.id);

  return [{
    json: {
      success: true,
      itemId: $json.id,
      result: result,
      timestamp: new Date().toISOString()
    }
  }];

} catch (error) {
  console.error('[Error] Failed to process item:', $json.id, error);

  // Return error details
  return [{
    json: {
      success: false,
      error: error.message,
      stack: error.stack,
      itemId: $json.id,
      originalData: $json,
      timestamp: new Date().toISOString()
    }
  }];
}
```

**Why This Matters:**
- Without try-catch: Workflow stops completely on error
- With try-catch: Error is captured, can be handled downstream
- Allows for partial success (some items process, some fail)

### Phase 2: Workflow-Level Error Handling (20 minutes)

#### Step 2.1: Configure Workflow Settings

1. Open workflow
2. Click "Workflow Settings" (gear icon, bottom-left)
3. Go to "Error Workflow" section

**Key Settings:**

**A. Error Workflow**
- Select a dedicated error handling workflow
- Any error in THIS workflow triggers THAT workflow
- See Phase 3 for creating error workflow

**B. Timeout After (seconds)**
- Default: No timeout
- Recommended: Set based on workflow purpose
  - Quick workflows: 60 seconds
  - API-heavy workflows: 300 seconds (5 min)
  - Data processing: 600 seconds (10 min)
- **Why:** Prevents runaway workflows that consume resources

**C. Save Data on Error**
- Default: Save Manually
- Recommended: Always Save
- **Why:** Allows debugging - you can see exactly what data caused the error

**D. Save Data on Success**
- Default: Save Manually
- Production workflows: Always Save
- Development workflows: Save Manually (reduces database size)

#### Step 2.2: Add Error Handling Branch

For critical workflows, add explicit error handling:

**Pattern: IF Node Error Check**
```
HTTP Request (API Call)
    ↓
IF Node: {{ $json.error }} exists
    ↓                      ↓
  TRUE                   FALSE
(Error occurred)     (Success)
    ↓                      ↓
Error Handler          Continue Normal Flow
```

**Implementation:**
1. After critical node, add IF node
2. Configure IF:
   - Condition: `{{ $json.success }}` equals `false`
   - OR: `{{ $json.error }}` is not empty
3. TRUE branch:
   - Log error
   - Send notification
   - Attempt recovery or fallback action
4. FALSE branch:
   - Continue normal workflow

**Example:**
```
Code Node (Process Payment)
    ↓
IF: {{ $json.success }} equals false
    ↓                           ↓
  TRUE                        FALSE
    ↓                           ↓
Send Email:                 Send Receipt
"Payment failed"            Update Database
Log to Database             Mark Order Complete
Retry Logic
```

#### Step 2.3: Implement Fallback Actions

When primary action fails, have backup:

**Pattern: Try Primary, Fall Back to Secondary**
```
HTTP Request (Primary API)
Settings: Continue on Fail = ON
    ↓
IF: {{ $json.error }} exists
    ↓              ↓
  TRUE           FALSE
    ↓              ↓
HTTP Request    Continue
(Backup API)
```

**Real Example: Send Email with Fallback**
```
Gmail (Try Gmail first)
Settings: Continue on Fail = ON
    ↓
IF: {{ $json.error }} exists
    ↓                       ↓
  TRUE                    FALSE
    ↓                       ↓
SendGrid                Stop
(Fallback email service)
```

### Phase 3: Global Error Workflow (30 minutes)

Create ONE workflow that handles errors from ALL your workflows.

#### Step 3.1: Create Error Workflow

1. Create new workflow
2. Name it: "🚨 Global Error Handler"
3. Add "Error Trigger" node (this is special trigger type)
4. Save workflow

**Error Trigger Node:**
- Automatically receives error data from any workflow that fails
- Error data includes:
  - `$json.execution.error` - Error message
  - `$json.execution.mode` - How workflow was triggered
  - `$json.execution.id` - Execution ID for debugging
  - `$json.workflow.name` - Which workflow failed
  - `$json.workflow.id` - Workflow ID

#### Step 3.2: Build Error Handling Logic

**Complete Error Handler Template:**

```
[Error Trigger]
    ↓
[Set: Format Error Details]
Fields:
  workflowName: {{ $json.workflow.name }}
  errorMessage: {{ $json.execution.error }}
  executionId: {{ $json.execution.id }}
  timestamp: {{ $now.toFormat('yyyy-MM-dd HH:mm:ss') }}
  executionUrl: {{ $env.WEBHOOK_URL }}/execution/{{ $json.execution.id }}
    ↓
[Slack: Notify Team]
Channel: #workflow-errors
Message:
⚠️ WORKFLOW ERROR ⚠️
Workflow: {{ $json.workflowName }}
Error: {{ $json.errorMessage }}
Time: {{ $json.timestamp }}
View Execution: {{ $json.executionUrl }}
@channel
    ↓
[Google Sheets: Log Error]
Append Row:
  Column A: {{ $json.timestamp }}
  Column B: {{ $json.workflowName }}
  Column C: {{ $json.errorMessage }}
  Column D: {{ $json.executionId }}
  Column E: Pending
    ↓
[IF: Critical Workflow?]
Condition: {{ $json.workflowName }} contains "Production"
    ↓                      ↓
  TRUE                   FALSE
(Critical)             (Non-critical)
    ↓                      ↓
[Send Email:           [Stop]
Emergency Alert]
To: manager@company.com
Subject: CRITICAL WORKFLOW FAILURE
Body: Immediate attention required...
```

#### Step 3.3: Assign Error Workflow to All Workflows

For EACH production workflow:

1. Open workflow
2. Workflow Settings (gear icon, bottom-left)
3. "Error Workflow" section
4. Select: "🚨 Global Error Handler"
5. Save workflow

**Efficiency Tip:** Do this for all workflows at once
- Open each workflow
- Change settings
- Save
- Repeat for all

#### Step 3.4: Create Error Dashboard

Track all errors in one place:

**Option A: Google Sheets Dashboard**
1. Create sheet: "Workflow Errors"
2. Columns:
   - Timestamp
   - Workflow Name
   - Error Message
   - Execution ID
   - Status (Pending, Investigating, Resolved)
   - Notes
3. Error workflow appends to this sheet
4. Team reviews and updates status

**Option B: Notion Database**
1. Create Notion database with same columns
2. Use Notion API in error workflow
3. Benefit: Better collaboration features

**Option C: Custom Dashboard**
1. Use Airtable, Monday.com, or similar
2. Error workflow posts to API
3. Benefit: Visual dashboards, automations

### Phase 4: Error Recovery Strategies (20 minutes)

#### Strategy 1: Automatic Retry with Delay

For transient errors (network issues, rate limits):

```
[Main Workflow Node]
Settings: Continue on Fail = ON
    ↓
[IF: Check Success]
{{ $json.success }} equals false
    ↓              ↓
  TRUE           FALSE
(Failed)      (Success - Continue)
    ↓
[Wait: 30 seconds]
    ↓
[Retry Same Operation]
    ↓
[IF: Check Success Again]
    ↓              ↓
  TRUE           FALSE
(Failed)      (Success - Continue)
    ↓
[Log to Errors]
[Notify Team]
```

#### Strategy 2: Queue Failed Items for Manual Review

When automatic recovery isn't possible:

```
[Error Trigger]
    ↓
[Set: Prepare Failed Item]
Fields:
  originalData: {{ $json.execution.data }}
  errorMessage: {{ $json.execution.error }}
  workflowId: {{ $json.workflow.id }}
    ↓
[Google Sheets: Queue for Review]
Sheet: Failed Items Queue
Append:
  Timestamp, Workflow Name, Error, Data, Status: "Pending Review"
    ↓
[Slack: Notify Team]
Message: New item in Failed Items Queue requires manual review
```

**Complementary Workflow: Manual Retry**
```
[Schedule Trigger: Check Queue Hourly]
    ↓
[Google Sheets: Read Failed Items]
Filter: Status = "Pending Review"
    ↓
[For Each Item]
    ↓
[Attempt to Reprocess]
    ↓
[IF: Success]
    ↓                      ↓
  TRUE                   FALSE
    ↓                      ↓
[Update Sheet:         [Leave as Pending]
Status = "Resolved"]
```

#### Strategy 3: Graceful Degradation

When service unavailable, use simplified fallback:

**Example: Notification System**
```
[Try Slack Notification]
Continue on Fail: ON
    ↓
[IF: Slack Failed]
    ↓
[Try Email Notification]
Continue on Fail: ON
    ↓
[IF: Email Failed]
    ↓
[Try SMS (Twilio)]
Continue on Fail: ON
    ↓
[IF: All Failed]
    ↓
[Log to Database]
(At minimum, error is recorded)
```

#### Strategy 4: Circuit Breaker Pattern

Prevent repeated failures from overwhelming system:

```
[Check Failure Count in Last Hour]
Query Database: Count errors for this workflow in last 60 minutes
    ↓
[IF: Count > 10]
    ↓                          ↓
  TRUE                       FALSE
(Too many failures)      (Normal operation)
    ↓                          ↓
[Stop Workflow]            [Continue]
[Send Alert:              [Execute as normal]
"Circuit breaker tripped"]
[Disable Workflow]
```

### Phase 5: Error Monitoring & Alerting (15 minutes)

#### Step 5.1: Set Up Slack Alerts

**Create Slack Channel:**
1. Create channel: #workflow-errors
2. Add team members who should be notified
3. Create Slack app and get webhook URL (or use Slack node with OAuth)

**Error Alert Template:**
```
Slack Node Configuration:
Channel: #workflow-errors
Message:
🚨 *WORKFLOW ERROR* 🚨

*Workflow:* {{ $json.workflowName }}
*Error:* {{ $json.errorMessage }}
*Time:* {{ $json.timestamp }}
*Severity:* {{ $json.severity }}

*Details:*
• Execution ID: {{ $json.executionId }}
• Workflow ID: {{ $json.workflowId }}
• <{{ $json.executionUrl }}|View Execution>

@channel
```

**Severity Levels:**
Implement in error workflow:
```javascript
// In Set node or Code node
let severity = 'Low';

if ($json.workflowName.includes('Production')) {
  severity = 'Critical';
} else if ($json.workflowName.includes('Client')) {
  severity = 'High';
} else if ($json.workflowName.includes('Internal')) {
  severity = 'Medium';
}

return [{
  json: {
    ...$json,
    severity: severity,
    notifyImmediate: severity === 'Critical'
  }
}];
```

#### Step 5.2: Set Up Email Alerts for Critical Errors

```
[Error Trigger]
    ↓
[Set: Categorize Error]
    ↓
[IF: {{ $json.severity }} equals "Critical"]
    ↓                              ↓
  TRUE                           FALSE
    ↓                              ↓
[Gmail: Send to Manager]       [Slack Only]
To: manager@company.com
Subject: 🚨 CRITICAL WORKFLOW FAILURE
Priority: High
Body:
A critical workflow has failed and requires immediate attention.

Workflow: {{ $json.workflowName }}
Error: {{ $json.errorMessage }}
Time: {{ $json.timestamp }}
Execution: {{ $json.executionUrl }}

This is a production-critical system. Please investigate immediately.
```

#### Step 5.3: Create Error Summary Report

Daily digest of all errors:

```
[Schedule Trigger: Daily at 9 AM]
    ↓
[Google Sheets: Read Yesterday's Errors]
Range: Error Log
Filter: Date = {{ $now.minus({ days: 1 }).toFormat('yyyy-MM-dd') }}
    ↓
[Code: Generate Summary]
```javascript
const errors = $input.all();

// Group by workflow
const byWorkflow = {};
errors.forEach(error => {
  const name = error.json.workflowName;
  if (!byWorkflow[name]) {
    byWorkflow[name] = [];
  }
  byWorkflow[name].push(error.json);
});

// Calculate stats
const summary = {
  date: $now.minus({ days: 1 }).toFormat('yyyy-MM-dd'),
  totalErrors: errors.length,
  uniqueWorkflows: Object.keys(byWorkflow).length,
  byWorkflow: Object.entries(byWorkflow).map(([name, errs]) => ({
    workflowName: name,
    errorCount: errs.length,
    errors: errs.map(e => ({
      time: e.timestamp,
      message: e.errorMessage
    }))
  }))
};

return [{ json: summary }];
```
    ↓
[Gmail: Send Daily Report]
To: team@company.com
Subject: N8N Error Report - {{ $json.date }}
Body HTML:
```html
<h2>Daily Error Report - {{ $json.date }}</h2>
<p><strong>Total Errors:</strong> {{ $json.totalErrors }}</p>
<p><strong>Workflows Affected:</strong> {{ $json.uniqueWorkflows }}</p>

<h3>Breakdown by Workflow:</h3>
{{ #each $json.byWorkflow }}
<h4>{{ this.workflowName }} ({{ this.errorCount }} errors)</h4>
<ul>
  {{ #each this.errors }}
  <li>{{ this.time }}: {{ this.message }}</li>
  {{ /each }}
</ul>
{{ /each }}
```
```

### Phase 6: Testing Error Handling (15 minutes)

#### Test 1: Force Node Failure

Create test workflow:
```
[Manual Trigger]
    ↓
[HTTP Request: Invalid URL]
URL: https://this-does-not-exist-error-test.com/fail
Method: GET
Settings: Continue on Fail = OFF
    ↓
(This will fail and trigger error workflow)
```

**Verify:**
- Error workflow executes
- Slack notification received
- Error logged to spreadsheet
- Email sent if configured

#### Test 2: Code Node Error

```
[Manual Trigger]
    ↓
[Code: Throw Error]
```javascript
throw new Error('Test error - this is intentional for testing error handling');
```
```

**Verify:** Same as Test 1

#### Test 3: Timeout Test

```
[Manual Trigger]
    ↓
[Code: Infinite Loop]
```javascript
while(true) {
  // This will run until timeout
}
```

Workflow Settings:
- Timeout After: 10 seconds
```

**Verify:**
- Workflow stops after 10 seconds
- Error workflow triggered with timeout message

#### Test 4: Partial Failure with Continue on Fail

```
[Manual Trigger]
    ↓
[Set: Create Test Data]
data: "test"
    ↓
[HTTP Request: Will Fail]
URL: https://invalid-url.com
Continue on Fail: ON
    ↓
[Set: This Should Still Execute]
result: "completed"
```

**Verify:**
- HTTP Request fails (red X on node)
- But workflow continues
- Final Set node executes successfully
- Execution shows as "Success" (not "Error")

## Common Mistakes to Avoid

### Mistake 1: Not Enabling "Continue on Fail" for Non-Critical Nodes
**Problem:** Slack notification fails, entire workflow stops, critical data not saved
**Solution:** Enable "Continue on Fail" for all notification/logging nodes

### Mistake 2: No Error Workflow Configured
**Problem:** Errors happen silently, team doesn't know workflows are failing
**Solution:** Create global error workflow, assign to ALL production workflows

### Mistake 3: No Try-Catch in Code Nodes
**Problem:** Single malformed item crashes entire workflow
**Solution:** ALWAYS wrap Code node logic in try-catch

### Mistake 4: Not Logging Enough Context
**Problem:** Error message says "Failed" but no idea what data caused it
**Solution:** Include original data, timestamp, execution ID in error logs

### Mistake 5: Only Email Alerts
**Problem:** Emails get lost in inbox, critical errors not noticed for hours
**Solution:** Multi-channel alerts - Slack + Email for critical errors

### Mistake 6: Testing Only Success Cases
**Problem:** Error handling looks good but doesn't actually work
**Solution:** Actively test error scenarios (see Phase 6)

### Mistake 7: No Retry Logic for Flaky APIs
**Problem:** Workflow fails due to temporary API issue
**Solution:** Enable "Retry on Fail" for external API calls

### Mistake 8: Alert Fatigue
**Problem:** Every minor error sends urgent alert, team starts ignoring
**Solution:** Implement severity levels, only @channel for Critical

### Mistake 9: No Error Dashboard
**Problem:** Errors scattered across Slack, email, hard to track what's resolved
**Solution:** Centralized error tracking in Google Sheets/Notion/Airtable

### Mistake 10: Forgetting to Assign Error Workflow to New Workflows
**Problem:** New production workflow has no error handling
**Solution:** Make error workflow assignment part of deployment checklist

## Troubleshooting

### Issue: Error Workflow Not Triggering
**Diagnosis:**
1. Check workflow settings: Is error workflow selected?
2. Is error workflow active?
3. Check error workflow execution history

**Solutions:**
- Workflow Settings → Error Workflow → Select your error handler
- Toggle error workflow to "Active"
- Test with intentional error (see Phase 6)

### Issue: Too Many Error Alerts
**Diagnosis:** Same error repeating every minute

**Solutions:**
1. Disable problematic workflow immediately:
   - Open workflow → Toggle to "Inactive"
2. Add alert throttling to error workflow:
   ```javascript
   // In error workflow Code node
   const workflowName = $json.workflow.name;
   const lastAlertKey = `lastAlert_${workflowName}`;

   // Check last alert time (store in environment or database)
   const lastAlert = $env[lastAlertKey];
   const now = Date.now();
   const oneHourAgo = now - (60 * 60 * 1000);

   if (lastAlert && lastAlert > oneHourAgo) {
     // Don't alert, was alerted recently
     return [];
   }

   // Store alert time, send alert
   // (Requires persistent storage setup)
   return $input.all();
   ```

### Issue: Error Message Not Descriptive
**Diagnosis:** Error says "Failed" with no context

**Solutions:**
- In Code nodes, throw descriptive errors:
  ```javascript
  if (!$json.email) {
    throw new Error(`Missing email field for item ID: ${$json.id}`);
  }
  ```
- Add logging before operations:
  ```javascript
  console.log('Processing payment for order:', $json.orderId, 'amount:', $json.amount);
  ```

### Issue: Can't Find Which Node Failed
**Diagnosis:** Error workflow triggered but unclear which node in original workflow failed

**Solutions:**
- Name nodes descriptively (not "Set1", "Set2" - use "Format Customer Data", "Calculate Total")
- In error workflow, log node name:
  ```
  Node Name: {{ $json.execution.lastNodeExecuted }}
  ```

## Success Metrics
- ✅ Zero silent failures (all errors are detected and logged)
- ✅ Team notified of critical errors within 1 minute
- ✅ Error resolution time under 2 hours for critical workflows
- ✅ Less than 5% of workflows fail in production (month average)
- ✅ All production workflows have error workflow assigned
- ✅ Error dashboard reviewed daily by team
- ✅ Failed items automatically queued for retry or manual review

## Error Handling Checklist

Before deploying workflow to production:

- [ ] All critical nodes have "Retry on Fail" enabled (if appropriate)
- [ ] Non-critical nodes (notifications) have "Continue on Fail" enabled
- [ ] All Code nodes wrapped in try-catch
- [ ] Error workflow assigned in workflow settings
- [ ] Workflow timeout configured appropriately
- [ ] Save data on error: Always Save
- [ ] Error handling tested with forced failures
- [ ] Slack channel #workflow-errors created and configured
- [ ] Team members added to error notifications
- [ ] Error dashboard (Google Sheets/Notion) created
- [ ] Documentation updated with workflow purpose and error contacts

## Related Skills
- **build_n8n_workflow.md** - Build workflows with error handling from the start
- **setup_n8n_self_hosted.md** - Monitor infrastructure errors in self-hosted setup
- **import_modify_n8n_workflows.md** - Add error handling when importing templates

---

**Skill Version:** 1.0
**Last Updated:** 2024
**Estimated Execution Time:** 60-90 minutes to set up complete error handling system
**Difficulty:** Intermediate
**Prerequisites:** At least one N8N workflow built, notification channel ready
