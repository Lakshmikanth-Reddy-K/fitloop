#!/bin/bash

# FitLoop Simple Deployment Script
echo "🚀 Starting FitLoop deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install fastapi uvicorn python-multipart sqlalchemy requests python-dotenv openai

# Set environment variables
export AUTH_TOKEN="fitloop2024"
export PORT=8000

# Start the application
echo "🎯 Starting FitLoop on port $PORT..."
uvicorn main:app --host 0.0.0.0 --port $PORT