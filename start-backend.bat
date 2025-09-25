@echo off
cd /d "C:\Users\LARED\source\repos\terraform-logiapp-demo\fitloop"
echo Starting FitLoop Backend...
".\venv\Scripts\python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause