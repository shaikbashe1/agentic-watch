FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (needed for compiling some python packages like asyncpg, cryptography)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the schema and init script
COPY postgres_schema.sql .
COPY init_db.py .
COPY start.sh .
RUN chmod +x start.sh

# Copy the application code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Default command (can be overridden for Celery)
CMD ["./start.sh"]
