# Agentic Watch - Backend

This is the backend for the Agentic Watch platform, built with FastAPI.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
cd backend
uvicorn app.main:app --reload
```

## API Documentation
Once the application is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
