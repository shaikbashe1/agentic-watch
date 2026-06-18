@echo off
cd backend
if not exist "venv\Scripts\activate.bat" (
    python -m venv venv
)
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
