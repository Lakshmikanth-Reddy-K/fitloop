# 🔑 Personal GitHub Authentication Guide

## Quick Setup for Personal GitHub Account

### Option 1: Personal Access Token (Recommended)

1. **Create Personal Access Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: "FitLoop Hackathon"
   - Expiration: 30 days
   - Scopes: Check "repo" (full repository access)
   - Click "Generate token"
   - **COPY THE TOKEN** (you won't see it again!)

2. **Push with Token**:
   ```bash
   git push -u origin main
   # When prompted for password, paste your TOKEN (not your GitHub password)
   ```

### Option 2: GitHub CLI (Alternative)
```bash
# Install GitHub CLI if not installed
gh auth login
# Follow prompts to authenticate with your personal account
git push -u origin main
```

### Option 3: SSH Key (Most Secure)
1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "reddylucky1500@gmail.com"
   ```
2. Add to GitHub: https://github.com/settings/ssh/new
3. Update remote:
   ```bash
   git remote set-url origin git@github.com:Lakshmikanth-Reddy-K/fitloop.git
   git push -u origin main
   ```

## 🚨 Important Notes:
- Use your **personal email**: reddylucky1500@gmail.com
- Use your **personal GitHub token/credentials**
- This won't affect your org VS Code setup
- Repository-specific configuration only

## Next Steps After Push:
1. ✅ Code pushed to GitHub
2. 🚀 Deploy Backend: https://railway.app
3. 🎨 Deploy Frontend: https://vercel.com
4. 🎉 Get public URLs for hackathon!