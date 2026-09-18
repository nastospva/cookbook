cd cookbook/backend
source venv/Scripts/activate # Windows Git Bash

# или: source venv/bin/activate # macOS/Linux

uvicorn app.main:app --reload --port 8000
