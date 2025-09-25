#!/bin/bash

# Simple production server
echo "🚀 Starting FitLoop Production Server"

# Install production dependencies
pip install uvicorn[standard] fastapi sqlalchemy openai python-dotenv requests python-multipart

# Start the server
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}