@echo off
echo 🚀 FitLoop Git Setup for Deployment
echo ===================================
echo.

cd /d "C:\Users\LARED\source\repos\terraform-logiapp-demo\fitloop"

echo Initializing Git repository...
git init
git add .
git commit -m "FitLoop - TCS AI Hackathon Submission"
git branch -M main

echo.
echo ✅ Git repository initialized!
echo.
echo 📋 Next steps:
echo 1. Create GitHub repository: https://github.com/new
echo 2. Name it: fitloop
echo 3. Run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/fitloop.git
echo    git push -u origin main
echo.
echo 🚀 Then deploy to:
echo - Backend: https://railway.app (connect GitHub repo)
echo - Frontend: https://vercel.com (connect GitHub repo, set root to 'frontend')
echo.
echo 🎯 Your app will be live in 5 minutes!
pause