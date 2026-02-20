# Deployment Guide for Render

## Prerequisites

Before deploying, you'll need:

1. **GitHub Account** - To host your code
2. **Render Account** - Free account at [render.com](https://render.com)
3. **Gemini API Key** - From [Google AI Studio](https://makersuite.google.com/app/apikey)

## Step 1: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (starts with `AIza...`)
5. **Important**: Keep this key secure - don't share it or commit to git

## Step 2: Push to GitHub

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

### 3. Add Environment Variable

In the **Environment** section, add this variable:

| Key | Value |
|-----|-------|
| `GOOGLE_API_KEY` | Your Gemini API key (from Step 1) |

**Example**: `AIzaSyDLYn6mPglg7-3_w4SAdnGIxW4pdr2dNpk`

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
- Verify `GOOGLE_API_KEY` is valid
- Review logs for authentication errors

### Chat Not Working

- Verify API key is correct
- Check API key has Gemini API access
- Review logs for API errors
- Ensure you're using a valid Gemini API key

### Slow Performance

- Free tier has limited resources
- Consider upgrading for better performance
- Optimize code and queries

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Gemini API key | `AIzaSyDLYn6mPglg7-3_w4SAdnGIxW4pdr2dNpk` |
| `PORT` | Server port | `10000` |

## Security Notes

1. **Never commit API keys** to git (they're in `.gitignore`)
2. **Use environment variables** for sensitive data
3. **Rotate API keys** regularly
4. **Monitor usage** to detect unauthorized access
5. **Keep API keys secret** - don't share them

## Cost Management

### Free Tier Limits

- Render Free: 750 hours/month
- Gemini API: Free tier available
- Check current pricing at Google AI

### To Reduce Costs

1. Use free tiers where available
2. Monitor API usage
3. Implement caching
4. Optimize queries

## Support

If you encounter issues:

1. Check Render status page
2. Review deployment logs
3. Verify API key in Google AI Studio
4. Check API key permissions

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