# Deployment Guide

## GitHub Actions Setup

This project uses GitHub Actions for CI/CD. You need to configure secrets in your GitHub repository.

## Required GitHub Secrets

Go to your GitHub repository: **Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets:

### 1. SUPABASE_URL
Your Supabase project URL
```
https://vyadvnjnwpwzysqhbplz.supabase.co
```

### 2. SUPABASE_KEY
Your Supabase anon/public key
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ5YWR2bmpud3B3enlzcWhicGx6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA0NzYzNTEsImV4cCI6MjA3NjA1MjM1MX0.rN8MrMxpF_kPfki4citELFnXx_H1Um1D1ECRRSwBUQI
```

### 3. OPENROUTER_API_KEY
Your OpenRouter API key
```
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
```

### 4. OPENROUTER_BASE_URL (optional, has default)
```
https://openrouter.ai/api/v1
```

### 5. LLM_MODEL (optional, has default)
```
openai/gpt-3.5-turbo
```

## GitHub Actions Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)
Runs on every push and pull request:
- Sets up Python environment
- Installs dependencies
- Runs linting (ruff)
- Runs type checking (mypy)
- Runs tests
- Checks code formatting (black)

### 2. Deploy Workflow (`.github/workflows/deploy.yml`)
Runs on push to main branch:
- Builds the application
- Runs tests
- Deploys migrations to Supabase
- Can be triggered manually via "workflow_dispatch"

## Deployment to Production

### Option 1: Deploy to Cloud Run (Google Cloud)

```bash
# Build Docker image
docker build -t gcr.io/PROJECT_ID/supabase-chatbot .

# Push to Container Registry
docker push gcr.io/PROJECT_ID/supabase-chatbot

# Deploy to Cloud Run
gcloud run deploy supabase-chatbot \
  --image gcr.io/PROJECT_ID/supabase-chatbot \
  --platform managed \
  --region us-central1 \
  --set-env-vars SUPABASE_URL=xxx,SUPABASE_KEY=xxx,OPENROUTER_API_KEY=xxx
```

### Option 2: Deploy to Railway

1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Railway will auto-deploy on push to main

### Option 3: Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn src.chatbot.presentation.api.app:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Option 4: Deploy to Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Launch app
fly launch

# Set secrets
fly secrets set SUPABASE_URL=xxx
fly secrets set SUPABASE_KEY=xxx
fly secrets set OPENROUTER_API_KEY=xxx

# Deploy
fly deploy
```

## Applying Migrations

Migrations need to be applied manually through the Supabase Dashboard:

1. Go to Supabase Dashboard → SQL Editor
2. Run each migration file in order:
   - `migrations/001_create_conversations_table.sql`
   - `migrations/002_create_messages_table.sql`
   - `migrations/003_create_functions.sql`

Alternatively, use Supabase CLI for automated migrations:

```bash
# Install Supabase CLI
npm install -g supabase

# Link to your project
supabase link --project-ref vyadvnjnwpwzysqhbplz

# Apply migrations
supabase db push
```

## Monitoring and Logs

- **GitHub Actions**: Check workflow runs in the Actions tab
- **Application Logs**: Use your hosting platform's logging
- **Supabase Logs**: Available in Supabase Dashboard → Logs

## Rollback

If deployment fails:
1. Revert the commit in GitHub
2. The deploy workflow will run with the previous version
3. Check Supabase logs for any database issues

## Security Best Practices

1. ✅ Never commit `.env` file to Git
2. ✅ Use GitHub Secrets for sensitive data
3. ✅ Enable RLS (Row Level Security) in Supabase
4. ✅ Use service role key only in secure backend environments
5. ✅ Rotate API keys regularly
6. ✅ Use HTTPS for all API endpoints
7. ✅ Implement rate limiting in production

## Troubleshooting

### Deployment fails
- Check GitHub Actions logs
- Verify all secrets are set correctly
- Ensure migrations are applied

### Can't connect to Supabase
- Verify SUPABASE_URL and SUPABASE_KEY
- Check network connectivity
- Verify RLS policies

### LangChain errors
- Verify OPENROUTER_API_KEY is valid
- Check API quota/credits
- Verify model name is correct
