@echo off
echo Building FitLoop for production deployment...

echo Building frontend...
cd frontend
call npm install
call npm run build
cd ..

echo Frontend built successfully!
echo.
echo Deployment Instructions:
echo =======================
echo.
echo BACKEND DEPLOYMENT (Railway):
echo 1. Go to https://railway.app/
echo 2. Sign in with GitHub
echo 3. Click 'New Project' -^> 'Deploy from GitHub repo'
echo 4. Select your fitloop repository
echo 5. Choose the 'fitloop' folder as root directory
echo 6. Railway will auto-detect Python and deploy
echo 7. Set environment variables:
echo    - AUTH_TOKEN=fitloop2024
echo    - OPENAI_API_KEY=your_openai_key (optional)
echo.
echo FRONTEND DEPLOYMENT (Vercel):
echo 1. Go to https://vercel.com/
echo 2. Sign in with GitHub  
echo 3. Click 'New Project'
echo 4. Select your repository
echo 5. Set root directory to 'fitloop/frontend'
echo 6. Update VITE_API_BASE_URL to your Railway URL
echo 7. Deploy!
echo.
echo Build completed! Check fitloop/frontend/dist for production files.
pause