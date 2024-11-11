#!/bin/bash

# Wait for the database to be ready
echo "Waiting for the database..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "Database is ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Run initial data-loading scripts
echo "Running initial data-loading scripts..."
python app/scripts/load_data.py
python app/scripts/load_photos.py

# Start the FastAPI application
echo "Starting FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
