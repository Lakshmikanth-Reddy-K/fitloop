#!/bin/bash

# Auto-deployment script for Railway/Vercel
echo "🚀 FitLoop Auto-Deployment Helper"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial FitLoop platform submission"
    git branch -M main
    echo "✅ Git repository initialized"
    echo ""
    echo "🔗 Next steps:"
    echo "1. Create GitHub repository: https://github.com/new"
    echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/fitloop.git"
    echo "3. Run: git push -u origin main"
else
    echo "📁 Git repository exists, adding latest changes..."
    git add .
    git commit -m "Updated FitLoop for deployment - $(date)"
    echo "✅ Changes committed"
fi

echo ""
echo "🎯 Deployment URLs:"
echo "==================="
echo "Backend (Railway): https://railway.app/new"
echo "Frontend (Vercel): https://vercel.com/new"
echo ""
echo "📋 Environment Variables Needed:"
echo "================================"
echo "Backend (Railway):"
echo "  AUTH_TOKEN=fitloop2024"
echo "  OPENAI_API_KEY=your_key_here"
echo ""
echo "Frontend (Vercel):"
echo "  VITE_API_BASE_URL=https://your-railway-app.railway.app"
echo "  VITE_AUTH_TOKEN=fitloop2024"
echo ""
echo "🎉 Ready for deployment!"