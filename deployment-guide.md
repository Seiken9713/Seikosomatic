# Discord Bot CI/CD Deployment Guide

This guide will help you set up automated deployments for your Discord bot using GitHub Actions and Replit.

## Prerequisites

1. **GitHub Repository**: Your bot code should be in a GitHub repository
2. **Replit Account**: Your bot should be hosted on Replit
3. **Discord Webhook** (optional): For deployment notifications

## Setup Instructions

### 1. GitHub Repository Setup

1. Push your bot code to a GitHub repository
2. Ensure your main branch is named `main` or `master`

### 2. Replit Integration

#### Get Replit Token:
1. Go to https://replit.com/account
2. Navigate to "API Tokens"
3. Generate a new token and copy it

#### Get Repl ID:
1. Open your Replit project
2. Look at the URL: `https://replit.com/@username/repl-name`
3. Your Repl ID is in the format: `@username/repl-name`

### 3. GitHub Secrets Configuration

In your GitHub repository, go to Settings > Secrets and variables > Actions.

Add these secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `REPLIT_TOKEN` | Your Replit API token | `1234567890abcdef` |
| `REPLIT_REPL_ID` | Your Replit project ID | `@yourusername/discord-bot` |
| `DISCORD_WEBHOOK` | Discord webhook URL for notifications | `https://discord.com/api/webhooks/...` |

### 4. Discord Webhook Setup (Optional)

For deployment notifications:

1. In your Discord server, go to Server Settings > Integrations > Webhooks
2. Create a new webhook
3. Copy the webhook URL
4. Add it as `DISCORD_WEBHOOK` secret in GitHub

## Workflow Features

### Main Deployment Workflow (`deploy.yml`)

**Triggers:**
- Push to main/master branch
- Pull requests to main/master

**What it does:**
1. **Code Quality Checks:**
   - Python syntax validation
   - Corruption scan using your existing scripts
   - Duplicate command detection

2. **Automated Deployment:**
   - Deploys to Replit on successful tests
   - Only runs on main branch pushes

3. **Notifications:**
   - Sends Discord notifications about deployment status
   - Includes commit info and deployment result

### Pull Request Checks (`pr-check.yml`)

**Triggers:**
- Pull requests to main/master

**What it does:**
1. **Code Quality:**
   - Black code formatting check
   - Import sorting with isort
   - Linting with flake8

2. **Security:**
   - Security vulnerability scanning
   - Configuration validation

3. **Bot-Specific Checks:**
   - Command audit
   - Duplicate function detection

## Manual Deployment

You can also trigger deployments manually:

1. Go to your GitHub repository
2. Click "Actions" tab
3. Select "Discord Bot CI/CD" workflow
4. Click "Run workflow"

## Monitoring Deployments

### GitHub Actions Dashboard
- Go to your repository > Actions tab
- View deployment history and logs
- Check for any failed deployments

### Discord Notifications
If you set up the Discord webhook, you'll receive:
- ✅ Success notifications with commit details
- ❌ Failure notifications with links to logs

## Troubleshooting

### Common Issues:

1. **Replit Token Issues:**
   - Ensure token has proper permissions
   - Regenerate token if needed

2. **Deployment Failures:**
   - Check GitHub Actions logs
   - Verify Replit project is accessible
   - Ensure dependencies are properly listed

3. **Code Quality Failures:**
   - Run `black .` locally to fix formatting
   - Run `isort .` to fix import order
   - Fix any syntax errors before pushing

### Local Testing Before Push:

```bash
# Install development dependencies
pip install black isort flake8 bandit

# Format code
black .
isort .

# Run linting
flake8 .

# Run security scan
bandit -r .

# Test bot syntax
python debug_corruption_scan.py
python command_audit.py
```

## Advanced Configuration

### Custom Deployment Conditions

You can modify the workflow to deploy only on specific conditions:

```yaml
deploy-to-replit:
  if: github.ref == 'refs/heads/main' && contains(github.event.head_commit.message, '[deploy]')
```

This will only deploy when commit message contains `[deploy]`.

### Environment-Specific Deployments

For staging and production environments:

1. Create separate Replit projects
2. Add environment-specific secrets:
   - `REPLIT_TOKEN_STAGING`
   - `REPLIT_TOKEN_PRODUCTION`
3. Modify workflow to deploy to different environments based on branch

### Rollback Strategy

If deployment fails:

1. GitHub Actions will prevent deployment
2. Your previous Replit deployment remains active
3. Fix issues and push again
4. Monitor Discord notifications for status

## Security Best Practices

1. **Never commit secrets** to your repository
2. **Use GitHub secrets** for all sensitive data
3. **Regular token rotation** - regenerate Replit tokens periodically
4. **Review pull requests** before merging to main
5. **Monitor deployment notifications** for unauthorized changes

## Cost Considerations

- GitHub Actions provides 2,000 free minutes/month for public repos
- Unlimited minutes for public repositories
- Private repos have usage limits based on plan

## Support

If you encounter issues:

1. Check GitHub Actions logs for detailed error messages
2. Verify all secrets are properly configured
3. Ensure Replit project permissions are correct
4. Test deployments with small changes first

This CI/CD setup will help you maintain code quality and deploy your Discord bot reliably!