#!/bin/bash

# FitLoop Development Setup Script

echo "🚀 Setting up FitLoop development environment..."

# Backend setup
echo "📦 Setting up backend..."
python -m venv venv

# Activate virtual environment (platform specific)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt

# Environment setup
if [ ! -f .env ]; then
    cp .env.sample .env
    echo "✅ Created .env file - please configure your settings"
else
    echo "✅ .env file already exists"
fi

# Frontend setup
echo "🎨 Setting up frontend..."
cd frontend
npm install
cd ..

echo "🎉 Setup complete!"
echo ""
echo "To start development:"
echo "1. Backend: uvicorn main:app --reload"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Don't forget to configure your .env file with AUTH_TOKEN and optionally OPENAI_API_KEY"