# 🚀 GitHub Setup & Deployment Guide

This guide will help you push your IBKR Dashboard to GitHub and deploy it for free on Streamlit Cloud.

## Step 1: Initialize Git Repository

Open Terminal and navigate to your project:

```bash
cd /Users/kelvin/Documents/Visual_studio/ibkr_dashboard
```

Initialize git:

```bash
git init
```

Add all files:

```bash
git add .
```

Create initial commit:

```bash
git commit -m "Initial commit: IBKR Performance Dashboard"
```

## Step 2: Create GitHub Repository

1. Go to [github.com](https://github.com) and log in (create account if needed)
2. Click the **+** icon in the top right corner
3. Select **New repository**
4. Name it: `ibkr_dashboard`
5. Add description: "Interactive Brokers Performance Dashboard with Money-Weighted Returns"
6. Keep it **Public** (so others can use it)
7. Click **Create repository**

## Step 3: Connect Local Repo to GitHub

After creating the repo, GitHub will show you commands. Run:

```bash
git branch -M main
git remote add origin https://github.com/akelvin88/IBKR_dashboard.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

## Step 4: Deploy to Streamlit Cloud (Free)

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account (or create free account)
3. Click **New app** button
4. Select:
   - Repository: `ibkr_dashboard`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **Deploy**

Streamlit will build and deploy your app. You'll get a public URL like:
```
https://ibkr-dashboard-YOUR-USERNAME.streamlit.app
```

## Step 5: Share Your App

- **Share the URL** with anyone - they can use it without installing anything
- Users can:
  1. Visit your app URL
  2. Upload their own IBKR CSV file
  3. View their performance dashboard

## Updating Your App

After making changes:

```bash
cd /Users/kelvin/Documents/Visual_studio/ibkr_dashboard

# Make your changes to files...

git add .
git commit -m "Describe your changes here"
git push origin main
```

Streamlit Cloud will automatically redeploy within seconds!

## Optional: Add Local Data Files

If you want to include sample data:

1. Keep CSV files in the `data/` folder
2. Users can either:
   - Upload their own file, OR
   - Select a pre-loaded sample file

The `data/` folder is already included and ready!

## Troubleshooting

### Git not found?
```bash
# On Mac, install with:
brew install git
```

### Authentication error?
Create a GitHub Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when prompted

### Streamlit not deploying?
- Check that all required packages are in `requirements.txt`
- Ensure `app.py` exists in root directory
- Check the "Deploy" logs for errors

## Next Steps

1. **Share URL** with colleagues, friends, or team
2. **Add to your portfolio** - this is a great demo project!
3. **Customize** - add your branding, modify colors, etc.
4. **Monitor usage** - Streamlit Cloud shows analytics

---

**Questions?** 
- Streamlit docs: https://docs.streamlit.io
- GitHub help: https://docs.github.com
