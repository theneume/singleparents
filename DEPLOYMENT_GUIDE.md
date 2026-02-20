# Deployment Guide for Render

## Prerequisites

Before deploying, you'll need:

1. **GitHub Account** - To host your code
2. **Render Account** - Free account at [render.com](https://render.com)
3. **Google Cloud Project** - With Vertex AI enabled
4. **Service Account Key** - For Google Cloud authentication

## Step 1: Push to GitHub

### Option A: Create New Repository

1. Go to [github.com/new](https://github.com/new)
2. Create a new repository (e.g., `adelaide-single-parents-connect`)
3. Copy the repository URL
4. Run these commands:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Option B: Use Existing Repository

If you already have a repository:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 2: Configure Google Cloud

### 1. Enable Vertex AI API

```bash
gcloud services enable aiplatform.googleapis.com --project=YOUR_PROJECT_ID
```

### 2. Create Service Account

```bash
gcloud iam service-accounts create vertex-ai-service \
  --display-name="Vertex AI Service" \
  --project=YOUR_PROJECT_ID
```

### 3. Grant Permissions

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:vertex-ai-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### 4. Create and Download Service Account Key

```bash
gcloud iam service-accounts keys create vertex-ai-key.json \
  --iam-account=vertex-ai-service@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --project=YOUR_PROJECT_ID
```

Open the `vertex-ai-key.json` file and copy its contents. You'll need this for Render.

## Step 3: Deploy to Render

### 1. Create New Web Service

1. Log in to [render.com](https://render.com)
2. Click **"New +"** in the top right
3. Select **"Web Service"**

### 2. Connect GitHub Repository

1. Click **"Connect"** next to your repository
2. Render will automatically detect `render.yaml`
3. Review the configuration:
   - **Name**: `adelaide-single-parents-connect`
   - **Region**: Oregon (or your preference)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT vertex_api_server:app`

### 3. Add Environment Variables

In the **Environment** section, add these variables:

| Key | Value |
|-----|-------|
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud Project ID |
| `GOOGLE_CLOUD_LOCATION` | `us-central1` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Paste the entire contents of `vertex-ai-key.json` (including `{}`) |
| `PORT` | `10000` |

**Important**: For `GOOGLE_APPLICATION_CREDENTIALS`, paste the entire JSON file content as a single string. It should look like:

```
{"type": "service_account", "project_id": "your-project", ...}
```

### 4. Deploy

1. Click **"Create Web Service"**
2. Wait for deployment to complete (usually 2-5 minutes)
3. You'll see a live URL when ready

## Step 4: Verify Deployment

1. Click on your service URL
2. Check that:
   - The page loads correctly
   - Navigation works
   - AI chat responds (may take a few seconds on first load)
   - Donate button links to Stripe
   - Contact button opens email client

## Step 5: Monitor and Maintain

### View Logs

1. Go to your service dashboard
2. Click **"Logs"**
3. Monitor for any errors

### Update Deployment

To update the application:

```bash
git add .
git commit -m "Your commit message"
git push
```

Render will automatically redeploy on push.

## Troubleshooting

### Build Failures

- Check that `requirements.txt` is correct
- Verify Python version compatibility
- Review build logs for specific errors

### Runtime Errors

- Check environment variables are set correctly
- Verify `GOOGLE_APPLICATION_CREDENTIALS` is valid JSON
- Ensure service account has correct permissions

### Chat Not Working

- Verify Vertex AI API is enabled
- Check service account has `aiplatform.user` role
- Review logs for authentication errors

### Slow Performance

- Free tier has limited resources
- Consider upgrading for better performance
- Optimize code and database queries

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_CLOUD_PROJECT` | Google Cloud Project ID | `realtime-chats` |
| `GOOGLE_CLOUD_LOCATION` | Region for Vertex AI | `us-central1` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account JSON | `{"type": "service_account", ...}` |
| `PORT` | Server port | `10000` |

## Security Notes

1. **Never commit credentials** to git (they're in `.gitignore`)
2. **Use environment variables** for sensitive data
3. **Rotate service account keys** regularly
4. **Limit service account permissions** to only what's needed
5. **Monitor usage** to detect unauthorized access

## Cost Management

### Free Tier Limits

- Render Free: 750 hours/month
- Vertex AI: Free tier available
- Google Cloud: Check current pricing

### To Reduce Costs

1. Use free tiers where available
2. Monitor API usage
3. Implement caching
4. Optimize queries

## Support

If you encounter issues:

1. Check Render status page
2. Review deployment logs
3. Verify Google Cloud console
4. Check service account permissions

For application-specific issues, contact: deepsyketech@proton.me

## Next Steps

After successful deployment:

1. Set up custom domain (optional)
2. Configure SSL certificates (automatic on Render)
3. Set up monitoring and alerts
4. Create backup strategies
5. Document any custom configurations

---

**Congratulations! Your application is now live!** 🎉

Access your deployed application at the URL provided by Render.