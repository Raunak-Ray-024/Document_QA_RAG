#!/bin/bash
# start.sh - Ensures the app binds to the correct port

# Log the startup
echo "Starting FastAPI application on port ${PORT:-10000}..."

# Run uvicorn with the port from Render's environment or default to 10000
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}