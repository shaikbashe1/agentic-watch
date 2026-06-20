#!/bin/bash
set -e

# Run the database initialization
echo "Initializing database..."
python init_db.py

# Start the application
echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
