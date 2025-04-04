#!/bin/bash

# Predefined port number
PORT=8000  # Change this if needed

## Activate virtual environment
#echo "Activating virtual environment..."
#source venv/bin/activate  # macOS/Linux

# Run FastAPI with Uvicorn
echo "Starting FastAPI server on port $PORT..."
uvicorn main:app --host 127.0.0.1 --port $PORT --reload