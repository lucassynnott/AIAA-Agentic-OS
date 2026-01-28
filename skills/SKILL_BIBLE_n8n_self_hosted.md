# SKILL BIBLE: N8N Self-Hosted Infrastructure Deployment

## Executive Summary

This skill bible provides a comprehensive guide for deploying a production-ready, self-hosted N8N automation platform using Railway.app as the hosting infrastructure. N8N is a powerful workflow automation tool that allows businesses to connect different services and automate repetitive tasks. While N8N offers a cloud service, self-hosting provides unlimited workflow executions without per-execution costs, making it ideal for agencies and businesses with high automation volumes.

The self-hosted approach becomes cost-effective when running more than 50-100 workflows regularly, as N8N Cloud charges per execution (starting at $20/month for 2,500 executions). A self-hosted instance on Railway.app typically costs $5-15/month for unlimited executions, providing significant cost savings for automation-heavy operations. This skill covers the complete infrastructure setup, from initial deployment to production optimization, security configuration, monitoring, and backup strategies.

Railway.app was chosen as the hosting platform due to its simplicity, automatic SSL certificates, integrated PostgreSQL database, and developer-friendly deployment process. The platform offers $5/month in free credits and scales automatically based on usage, making it ideal for both small agencies and growing businesses.

## Source
- **Type:** Internal SOP/Skill Document
- **Category:** n8n
- **Original File:** setup_n8n_self_hosted.md

## Core Principles

### 1. Cost Optimization Through Self-Hosting
Self-hosting N8N eliminates per-execution costs that can quickly escalate with N8N Cloud. The break-even point occurs around 50-100 active workflows, where the fixed hosting cost ($5-15/month) becomes significantly cheaper than execution-based pricing ($20-150/month depending on volume).

### 2. Infrastructure as Code Mentality
All configuration should be managed through environment variables, making the deployment reproducible and maintainable. This approach ensures that the entire N8N instance can be recreated from configuration alone, supporting disaster recovery and scaling scenarios.

### 3. Security-First Deployment
Every self-hosted instance must implement multiple security layers: basic authentication for initial access control, HTTPS encryption for all communications, strong password policies, and proper credential encryption. Security cannot be an afterthought in automation infrastructure.

### 4. Database Persistence and Backup Strategy
N8N workflows and execution history represent critical business assets. Proper database configuration with automated backups ensures business continuity. Execution data pruning prevents database bloat while maintaining necessary audit trails.

### 5. Monitoring and Observability
Production automation infrastructure requires continuous monitoring of resource usage, execution success rates, and cost metrics. Early warning systems prevent outages and cost overruns before they impact business operations.

### 6. Scalability Through Resource Management
Railway.app's resource allocation should match actual usage patterns. Over-provisioning wastes money, while under-provisioning causes execution failures. Proper resource monitoring enables optimal cost-performance balance.

### 7. Environment Separation and Testing
Production automation infrastructure requires thorough testing before deployment. Test workflows verify functionality, while monitoring workflows provide ongoing health checks. This prevents production issues that could disrupt client operations.

### 8. Documentation and Knowledge Transfer
Self-hosted infrastructure requires comprehensive documentation for team access, troubleshooting, and knowledge transfer. This includes credential management, backup procedures, and escalation processes.

## Step-by-Step Process

### Phase 1: Foundation Setup (15 minutes)

#### Step 1: Railway.app Account Creation
1. **Navigate to Railway.app Platform**
   - Visit https://railway.app in your browser
   - Review the platform overview and pricing structure
   - Note the $5/month free credit allocation

2. **Account Registration Process**
   - Click "Start a New Project" or "Sign Up"
   - Select "Login with GitHub" (strongly recommended)
   - This choice enables automatic deployment from repositories
   - Authorize Railway to access your GitHub account
   - Complete the email verification process

3. **Payment Method Configuration**
   - Access Account Settings from the top-right user menu
   - Navigate to the "Billing" tab
   - Click "Add Payment Method"
   - Enter valid credit/debit card information
   - Verify the $5/month free credit appears in your billing summary
   - Note: Payment method is required even for free tier usage

#### Step 2: Project Initialization
1. **Create New Railway Project**
   - From the Railway dashboard, click "New Project"
   - Select "Deploy from Template" option
   - This approach uses pre-configured N8N templates

2. **Template Selection**
   - In the template search bar, type "n8n"
   - Locate the official N8N template with the N8N logo
   - Verify the description shows "Self-Hostable Workflow Automation"
   - Click on the template to review its components

3. **Template Deployment Initiation**
   - Click "Deploy" on the selected N8N template
   - Railway will display the deployment configuration screen
   - Review the included services: N8N application and PostgreSQL database
   - Confirm the deployment will create both services automatically

### Phase 2: Core Configuration (20 minutes)

#### Step 3: Essential Environment Variables
Environment variables control N8N's behavior and security. Each variable serves a specific purpose in the deployment architecture.

1. **Authentication Configuration**
   ```
   N8N_BASIC_AUTH_ACTIVE=true
   ```
   - Purpose: Enables basic authentication layer
   - Security: Essential for public internet deployment
   - Impact: Adds login prompt before N8N interface access

   ```
   N8N_BASIC_AUTH_USER=admin
   ```
   - Purpose: Defines the basic authentication username
   - Recommendation: Use "admin" or your organization name
   - Note: This is separate from the N8N owner account

   ```
   N8N_BASIC_AUTH_PASSWORD=MyN8N2024!Secure
   ```
   - Purpose: Sets the basic authentication password
   - Requirements: Minimum 12 characters, mixed case, numbers, symbols
   - Security Critical: Use a password manager for generation

2. **Domain and URL Configuration**
   ```
   N8N_HOST=your-project-name.up.railway.app
   ```
   - Purpose: Tells N8N its public domain name
   - Format: Domain only, no protocol prefix
   - Timing: Set after initial deployment when domain is known

   ```
   WEBHOOK_URL=https://your-project-name.up.railway.app
   ```
   - Purpose: Enables webhook functionality for external integrations
   - Format: Full URL with HTTPS protocol
   - Critical: Must match N8N_HOST with https:// prefix

3. **Security and Encryption**
   ```
   N8N_ENCRYPTION_KEY=[32-character random string]
   ```
   - Purpose: Encrypts stored credentials in the database
   - Generation: Use `openssl rand -base64 32` command
   - Critical Warning: Never change after initial setup or lose all credentials

4. **Timezone Configuration**
   ```
   TZ=America/New_York
   ```
   - Purpose: Ensures scheduled workflows run at correct local times
   - Format: Use tz database timezone names
   - Examples: Europe/London, Australia/Sydney, Asia/Tokyo

5. **Data Management Settings**
   ```
   EXECUTIONS_DATA_PRUNE=true
   EXECUTIONS_DATA_MAX_AGE=168
   EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000
   ```
   - Purpose: Automatically manages execution history to prevent database bloat
   - MAX_AGE: Hours to retain execution data (168 = 7 days)
   - MAX_COUNT: Maximum number of executions to retain

#### Step 4: Variable Configuration Process
1. **Access Variable Configuration**
   - In Railway dashboard, click on the N8N service
   - Navigate to the "Variables" tab
   - This interface manages all environment variables

2. **Variable Entry Method**
   - Click "New Variable" for each configuration item
   - Enter the variable name exactly as specified (case-sensitive)
   - Enter the corresponding value
   - Press Enter or click outside the field to save
   - Repeat for each required variable

3. **Deployment Trigger**
   - Railway automatically redeploys after variable changes
   - Wait for deployment completion (indicated by green status)
   - Monitor the deployment logs for any error messages

### Phase 3: Database Integration (10 minutes)

#### Step 5: PostgreSQL Database Verification
Railway automatically provisions a PostgreSQL database with the N8N template. Verification ensures proper integration.

1. **Service Verification**
   - Confirm two services appear in your Railway project:
     - `n8n` (the application service)
     - `postgres` (the database service)
   - Both should show "Active" status with green indicators

2. **Database Connection Variables**
   - Click on the `postgres` service
   - Navigate to "Variables" tab
   - Verify these auto-generated variables exist:
     - `POSTGRES_DB`: Database name
     - `POSTGRES_USER`: Database username
     - `POSTGRES_PASSWORD`: Database password
     - `DATABASE_URL`: Complete connection string

3. **N8N Database Integration**
   - Railway typically auto-configures database connection
   - If manual configuration needed, add these variables to N8N service:
     ```
     DB_TYPE=postgresdb
     DB_POSTGRESDB_DATABASE=[value from postgres POSTGRES_DB]
     DB_POSTGRESDB_HOST=[postgres service host]
     DB_POSTGRESDB_PORT=5432
     DB_POSTGRESDB_USER=[value from postgres POSTGRES_USER]
     DB_POSTGRESDB_PASSWORD=[value from postgres POSTGRES_PASSWORD]
     ```

### Phase 4: Domain and Access Configuration (15 minutes)

#### Step 6: Domain Acquisition and Configuration
1. **Railway Domain Retrieval**
   - In Railway dashboard, click on N8N service
   - Navigate to "Settings" tab
   - Scroll to "Domains" section
   - Copy the auto-generated domain (format: project-name.up.railway.app)

2. **Domain Variable Updates**
   - Return to N8N service "Variables" tab
   - Update or add these variables with your specific domain:
     ```
     N8N_HOST=your-actual-domain.up.railway.app
     WEBHOOK_URL=https://your-actual-domain.up.railway.app
     ```
   - Save changes and wait for automatic redeployment

#### Step 7: Initial Access and Setup
1. **First Access Attempt**
   - Navigate to your Railway domain in a web browser
   - Expect to see N8N basic authentication prompt
   - Enter credentials from N8N_BASIC_AUTH_USER and N8N_BASIC_AUTH_PASSWORD

2. **N8N Owner Account Creation**
   - After basic auth, N8N presents owner account setup
   - This creates your primary N8N user account (separate from basic auth)
   - Enter email address and strong password
   - Complete the initial setup wizard

3. **Access Verification**
   - Confirm you can access the N8N workflow canvas
   - Verify "Create Workflow" button is visible and functional
   - Check that user icon appears in top-right corner

### Phase 5: Security Hardening (15 minutes)

#### Step 8: HTTPS and SSL Configuration
1. **SSL Certificate Verification**
   - Railway automatically provisions SSL certificates
   - Verify browser shows padlock icon when accessing N8N
   - Click padlock to confirm "Connection is secure"
   - Allow 5-10 minutes for certificate provisioning if not immediate

2. **Protocol Enforcement**
   - Add these variables to enforce HTTPS:
     ```
     N8N_PROTOCOL=https
     N8N_PORT=443
     ```
   - These settings ensure N8N generates correct URLs for webhooks and redirects

#### Step 9: Access Control Configuration
1. **Password Strength Verification**
   - Ensure N8N_BASIC_AUTH_PASSWORD meets security requirements:
     - Minimum 12 characters
     - Contains uppercase and lowercase letters
     - Includes numbers and special characters
     - Not based on dictionary words or personal information

2. **Additional Security Measures**
   - Document all passwords in a secure password manager
   - Enable two-factor authentication on email account used for N8N owner account
   - Consider IP whitelisting if Railway Pro plan is available

### Phase 6: Performance Optimization (10 minutes)

#### Step 10: Resource Allocation
1. **Initial Resource Assessment**
   - Railway dashboard → N8N service → Settings
   - Navigate to "Resources" section
   - Review current allocation (typically 512MB RAM default)

2. **Recommended Resource Settings**
   - **Memory**: 1GB minimum for production use
   - **CPU**: Shared tier sufficient for most agencies
   - **Scaling**: Enable automatic scaling based on demand

3. **Cost-Performance Balance**
   - Start with 1GB RAM allocation
   - Monitor usage for first week
   - Increase only if consistently using >80% of allocated resources
   - Each resource increase impacts monthly cost

#### Step 11: Execution Optimization
1. **Database Pruning Configuration**
   - Verify these variables are set (add if missing):
     ```
     EXECUTIONS_DATA_PRUNE=true
     EXECUTIONS_DATA_MAX_AGE=168
     EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000
     ```

2. **Performance Monitoring Setup**
   - Access Railway metrics: N8N service → Metrics tab
   - Monitor CPU usage, memory consumption, and restart frequency
   - Set up alerts for resource threshold breaches

### Phase 7: Backup and Recovery (20 minutes)

#### Step 12: Automated Backup Configuration
1. **Railway Native Backups**
   - Check if Railway offers database backup features
   - Enable if available: Postgres service → Settings → Backups
   - Configure daily backups with 7-day retention minimum

2. **Manual Backup System Setup**
   - Install PostgreSQL client tools locally
   - Create backup script with database credentials from Railway
   - Test backup creation and restoration process

3. **Backup Script Implementation**
   ```bash
   #!/bin/bash
   # N8N Database Backup Script
   
   # Database credentials from Railway Postgres service
   DB_HOST="your-postgres-host.railway.app"
   DB_PORT="5432"
   DB_NAME="railway"
   DB_USER="postgres"
   DB_PASSWORD="your-postgres-password"
   
   # Backup configuration
   BACKUP_DIR="$HOME/n8n-backups"
   mkdir -p $BACKUP_DIR
   
   # Create timestamped backup
   TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
   BACKUP_FILE="$BACKUP_DIR/n8n_backup_$TIMESTAMP.sql"
   
   # Execute backup
   PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > $BACKUP_FILE
   
   # Compress and cleanup
   gzip $BACKUP_FILE
   find $BACKUP_DIR -name "n8n_backup_*.sql.gz" -mtime +30 -delete
   
   echo "Backup completed: $BACKUP_FILE.gz"
   ```

4. **Backup Automation**
   - Schedule weekly backups using cron (Unix/Linux/Mac)
   - Test restoration process with non-production database
   - Document recovery procedures for team access

### Phase 8: Monitoring and Alerting (15 minutes)

#### Step 13: Infrastructure Monitoring
1. **Railway Usage Monitoring**
   - Set up budget alerts in Railway dashboard
   - Configure warnings at $10 and critical alerts at $20
   - Monitor resource utilization trends weekly

2. **Application Health Monitoring**
   - Create N8N workflow for health checking
   - Schedule hourly HTTP requests to `/healthz` endpoint
   - Configure alerts for health check failures

3. **Performance Baseline Establishment**
   - Document initial performance metrics
   - Record typical execution times for standard workflows
   - Establish normal resource usage patterns

#### Step 14: Operational Alerting
1. **Cost Monitoring**
   - Railway project settings → Usage alerts
   - Email notifications for budget thresholds
   - Weekly cost review process

2. **Uptime Monitoring**
   - External monitoring service (optional)
   - Internal N8N health check workflows
   - Team notification procedures for outages

### Phase 9: Testing and Validation (20 minutes)

#### Step 15: Functional Testing
1. **Basic Workflow Testing**
   - Create test workflow with schedule trigger
   - Add simple data processing nodes
   - Verify execution success and data persistence

2. **Webhook Functionality Testing**
   - Create webhook-triggered workflow
   - Test external webhook calls using curl or Postman
   - Verify response handling and data processing

3. **Credential Storage Testing**
   - Add test credential (non-production)
   - Verify encryption and storage functionality
   - Test credential retrieval in workflows

#### Step 16: Performance Testing
1. **Load Testing**
   - Create workflow processing 100+ data items
   - Monitor execution time and resource usage
   - Verify system stability under typical load

2. **Concurrent Execution Testing**
   - Trigger multiple workflows simultaneously
   - Monitor system performance and response times
   - Verify no execution conflicts or data corruption

### Phase 10: Production Readiness (10 minutes)

#### Step 17: Documentation and Handover
1. **Access Documentation**
   - Document all login credentials securely
   - Create team access procedures
   - Establish password rotation schedule

2. **Operational Procedures**
   - Document backup and restoration processes
   - Create troubleshooting guide for common issues
   - Establish escalation procedures for outages

#### Step 18: Go-Live Checklist
1. **Pre-Production Verification**
   - All environment variables correctly set
   - SSL certificate active and valid
   - Database connectivity confirmed
   - Backup system tested and operational
   - Monitoring and alerting functional

2. **Production Cutover**
   - Migrate workflows from development/staging
   - Update external webhook URLs to production domain
   - Notify team of production availability
   - Begin normal operational monitoring

## Frameworks & Templates

### Environment Variables Framework
The N8N deployment relies on a structured approach to environment variable management. This framework ensures consistent, secure, and maintainable configuration across deployments.

#### Core Configuration Template
```
# Authentication Layer
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=[organization-specific-username]
N8N_BASIC_AUTH_PASSWORD=[strong-generated-password]

# Domain Configuration
N8N_HOST=[railway-domain-without-protocol]
WEBHOOK_URL=https://[railway-domain-with-protocol]

# Security Configuration
N8N_ENCRYPTION_KEY=[32-character-random-string]
N8N_PROTOCOL=https
N8N_PORT=443

# Operational Configuration
TZ=[organization-timezone]
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=168
EXECUTIONS_DATA_PRUNE_MAX_COUNT=10000

# Database Configuration (auto-configured by Railway)
DB_TYPE=postgresdb
```

### Cost Optimization Framework
This framework provides a systematic approach to managing and optimizing Railway.app hosting costs for N8N deployments.

#### Cost Analysis Template
```
Monthly Cost Breakdown:
- Base Railway Service: $5-8
- Additional RAM (if needed): $3-5 per GB
- Database Storage: $0.10 per GB
- Bandwidth: $0.10 per GB (typically minimal)

Cost Optimization Strategies:
1. Execution Pruning (30-50% database size reduction)
2. Workflow Consolidation (20-30% execution reduction)
3. Resource Right-sizing (10-20% cost reduction)
4. Efficient Node Usage (10-15% performance improvement)
```

### Security Configuration Framework
A layered security approach ensures N8N deployments meet enterprise security requirements while maintaining usability.

#### Security Layers Template
```
Layer 1: Network Security
- HTTPS enforcement (N8N_PROTOCOL=https)
- SSL certificate validation
- Domain-based access control

Layer 2: Authentication Security
- Basic authentication (N8N_BASIC_AUTH_*)
- Strong password policies (12+ characters, complexity)
- Owner account separation

Layer 3: Data Security
- Credential encryption (N8N_ENCRYPTION_KEY)
- Database access controls
- Backup encryption

Layer 4: Operational Security
- Regular security updates
- Access logging and monitoring
- Incident response procedures
```

### Monitoring and Alerting Framework
Comprehensive monitoring ensures reliable N8N operations and early problem detection.

#### Monitoring Template
```
Infrastructure Metrics:
- CPU Usage: Alert if >70% for 15+ minutes
- Memory Usage: Alert if >80% for 10+ minutes
- Disk Usage: Alert if >85% capacity
- Network Latency: Alert if >500ms average

Application Metrics:
- Workflow Execution Success Rate: Alert if <95%
- Average Execution Time: Alert if >2x baseline
- Webhook Response Time: Alert if >5 seconds
- Database Connection Errors: Alert on any occurrence

Cost Metrics:
- Daily Cost Trend: Alert if >150% of average
- Monthly Budget: Warning at 75%, critical at 90%
- Resource Utilization Efficiency: Review weekly
```

### Backup and Recovery Framework
Systematic backup procedures ensure business continuity and data protection for N8N deployments.

#### Backup Strategy Template
```
Backup Frequency:
- Database: Daily automated backups
- Configuration: Weekly environment variable export
- Workflows: Real-time through N8N export feature

Retention Policy:
- Daily backups: 30 days retention
- Weekly backups: 12 weeks retention
- Monthly backups: 12 months retention

Recovery Procedures:
1. Identify failure scope and impact
2. Assess backup availability and integrity
3. Execute recovery procedure based on failure type
4. Validate system functionality post-recovery
5. Document incident and lessons learned
```

## Best Practices

### Infrastructure Management Best Practices

#### 1. Environment Variable Security
- **Never expose sensitive variables in logs or documentation**
- Use Railway's secure variable storage exclusively
- Implement variable naming conventions for consistency
- Document variable purposes without exposing values
- Rotate encryption keys annually (requires credential re-entry)

#### 2. Resource Optimization
- **Start conservative, scale based on actual usage**
- Monitor resource utilization for minimum 1 week before adjustments
- Use execution pruning to prevent database bloat
- Implement workflow consolidation to reduce overhead
- Schedule resource-intensive workflows during off-peak hours

#### 3. Database Management
- **Enable execution pruning from day one**
- Set reasonable retention periods based on compliance requirements
- Monitor database size growth trends weekly
- Implement regular backup validation procedures
- Use database connection pooling for high-volume deployments

#### 4. Security Implementation
- **Implement defense-in-depth security strategy**
- Use strong, unique passwords for all authentication layers
- Enable HTTPS enforcement for all communications
- Implement regular security updates and patches
- Document all security configurations for audit purposes

### Operational Excellence Best Practices

#### 5. Monitoring and Alerting
- **Implement proactive monitoring before reactive troubleshooting**
- Set up multiple alert channels (email, Slack, SMS)
- Create escalation procedures for different severity levels
- Monitor both infrastructure and application metrics
- Establish baseline performance metrics for comparison

#### 6. Backup and Recovery
- **Test backup restoration procedures regularly**
- Automate backup processes to eliminate human error
- Store backups in geographically separate locations
- Document recovery procedures with step-by-step instructions
- Practice disaster recovery scenarios quarterly

#### 7. Cost Management
- **Monitor costs daily, optimize weekly, review monthly**
- Set up automated budget alerts at multiple thresholds
- Implement cost allocation tracking for different projects
- Regular review of resource utilization efficiency
- Document cost optimization decisions and results

#### 8. Team Collaboration
- **Maintain comprehensive documentation for knowledge sharing**
- Implement change management procedures for configuration updates
- Use version control for workflow and configuration changes
- Establish clear roles and responsibilities for system maintenance
- Create onboarding procedures for new team members

### Development and Deployment Best Practices

#### 9. Workflow Development
- **Test workflows in development environment before production deployment**
- Use descriptive naming conventions for workflows and nodes
- Implement error handling in all production workflows
- Document workflow purposes and dependencies
- Version control workflow exports for change tracking

#### 10. Integration Management
- **Use webhook authentication for external integrations**
- Implement rate limiting for high-volume integrations
- Monitor integration health and performance
- Document all external dependencies and their requirements
- Test integration failover scenarios

#### 11. Performance Optimization
- **Profile workflow execution times and optimize bottlenecks**
- Use efficient node types for data processing
- Implement data filtering early in workflow chains
- Cache frequently accessed data when appropriate
- Monitor and optimize database query performance

#### 12. Scalability Planning
- **Design workflows for horizontal scaling from the beginning**
- Implement queue-based processing for high-volume scenarios
-