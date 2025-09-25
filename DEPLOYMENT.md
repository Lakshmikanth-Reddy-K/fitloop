# 🚀 FitLoop Deployment Guide

## Quick Deployment to Free Platforms

Your FitLoop app is ready for deployment! Follow these steps to get your public URLs.

### 🔧 Prerequisites
- GitHub account (to store your code)
- Railway account (for backend) - https://railway.app  
- Vercel account (for frontend) - https://vercel.com

Both platforms offer generous free tiers perfect for hackathons!

---

## 📦 Step 1: Push to GitHub

First, push your code to a GitHub repository:

```bash
cd C:\Users\LARED\source\repos\terraform-logiapp-demo\fitloop
git init
git add .
git commit -m "Initial FitLoop hackathon submission"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fitloop.git
git push -u origin main
```

---

## 🚄 Step 2: Deploy Backend (Railway)

1. **Go to Railway**: https://railway.app/
2. **Sign up/Login** with GitHub
3. **Create New Project**:
   - Click "Deploy from GitHub repo"
   - Select your `fitloop` repository
   - **Root Directory**: Set to `/` (Railway will detect the Python app)
4. **Environment Variables** (in Railway dashboard):
   ```
   AUTH_TOKEN=hackathon2024
   OPENAI_API_KEY=your_key_here (optional - has fallback)
   ```
5. **Deploy** - Railway auto-detects Python and uses your `requirements.txt`

**Your backend URL will be**: `https://your-app-name.railway.app`

---

## ⚡ Step 3: Deploy Frontend (Vercel)

1. **Go to Vercel**: https://vercel.com/
2. **Sign up/Login** with GitHub  
3. **Create New Project**:
   - Select your `fitloop` repository
   - **Root Directory**: Set to `frontend/`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
4. **Environment Variables**:
   ```
   VITE_API_BASE_URL=https://your-railway-app.railway.app
   VITE_AUTH_TOKEN=hackathon2024
   ```
5. **Deploy** - Vercel builds and deploys automatically

**Your frontend URL will be**: `https://your-app-name.vercel.app`

---

## 🧪 Step 4: Test Your Production App

1. **Visit your Vercel frontend URL**
2. **Upload sample CSVs** (in `sample_data/` folder):
   - `reviews_sample.csv`
   - `returns_sample.csv`  
3. **Click "Process Data"** - should see AI processing results
4. **View Dashboard** - should show 4 products with risk scores
5. **Check Product Details** - click any product for insights

---

## 📊 Sample Data Included

Your app includes production-ready sample data:
- **18 customer reviews** across 5 products
- **8 return records** with reasons and conditions
- **Expected output**: 4 products with risk scores 0.5-0.6

---

## 🔑 Authentication

- **Token**: `hackathon2024` (set in environment variables)
- **Frontend automatically includes** the token in requests
- **No manual login required** - ready for demo!

---

## 🏆 Hackathon Submission URLs

After deployment, you'll have:

✅ **Frontend (Demo)**: `https://your-app.vercel.app`  
✅ **Backend (API)**: `https://your-app.railway.app`  
✅ **GitHub Repo**: `https://github.com/your-username/fitloop`

---

## 🎯 Key Features to Demo

1. **CSV Upload** - Drag & drop reviews/returns data
2. **AI Processing** - Extracts issues, calculates risk scores  
3. **Product Dashboard** - Visual risk assessment
4. **Product Details** - Detailed insights per product
5. **Markdown Export** - Copy generation for product descriptions

---

## 💡 Pro Tips

- **Demo Flow**: Upload → Process → Dashboard → Product Details → Export
- **Sample Story**: "FitLoop identified that Product P1003 has a 'runs_large' issue affecting 60% of customers"
- **AI Highlight**: Automatically extracts issues like sizing, color fading, shrinkage from text feedback
- **Business Value**: Converts messy feedback into actionable product insights

---

## 🔧 Troubleshooting

**Backend not starting?**
- Check Railway logs for dependency issues
- Ensure `requirements.txt` has correct versions

**Frontend can't reach backend?**  
- Verify `VITE_API_BASE_URL` points to your Railway URL
- Check CORS settings allow your Vercel domain

**Need help?** Check the `TESTING.md` for detailed testing procedures.

---

**🎉 Happy Hacking! Your FitLoop app is production-ready!**