#!/bin/bash

# AI Bioinformatics Assistant - Startup Script
# This script starts both FastAPI backend and Streamlit frontend

echo "========================================"
echo "🧬 AI Bioinformatics Assistant"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo "✅ .env created. Please edit it and add your OPENROUTER_API_KEY"
    else
        echo "❌ .env.example not found!"
        exit 1
    fi
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo "Checking Python installation..."
python3 --version

echo ""
echo "Checking required packages..."

# Check if requirements are installed
packages=("fastapi" "uvicorn" "streamlit" "requests" "python-dotenv")
missing=()

for pkg in "${packages[@]}"; do
    if python3 -c "import ${pkg//-/_}" 2>/dev/null; then
        echo "✅ $pkg"
    else
        echo "❌ $pkg"
        missing+=("$pkg")
    fi
done

if [ ${#missing[@]} -gt 0 ]; then
    echo ""
    echo "Installing missing packages..."
    pip install -r requirements.txt
fi

echo ""
echo "========================================"
echo "Starting services..."
echo "========================================"
echo ""

echo "📡 Backend URL: http://localhost:8000"
echo "🖥️  Frontend URL: http://localhost:8501"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""

echo "Starting FastAPI backend..."
python3 backend/main.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

echo "Waiting for backend to start..."
sleep 3

echo "Starting Streamlit frontend..."
streamlit run frontend/app.py &
FRONTEND_PID=$!

echo ""
echo "✅ Services started!"
echo "Frontend will open in your browser shortly..."
echo ""
echo "To stop services, press Ctrl+C"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
