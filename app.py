import os
os.environ['AUTH_TOKEN'] = 'hackathon2024'

# Simple startup script for FitLoop
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)