@echo off
echo 🚀 Setting up FitLoop development environment...

REM Backend setup
echo 📦 Setting up backend...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Environment setup
if not exist .env (
    copy .env.sample .env
    echo ✅ Created .env file - please configure your settings
) else (
    echo ✅ .env file already exists
)

REM Frontend setup
echo 🎨 Setting up frontend...
cd frontend
npm install
cd ..

echo 🎉 Setup complete!
echo.
echo To start development:
echo 1. Backend: uvicorn main:app --reload
echo 2. Frontend: cd frontend && npm run dev
echo.
echo Don't forget to configure your .env file with AUTH_TOKEN and optionally OPENAI_API_KEY
pause