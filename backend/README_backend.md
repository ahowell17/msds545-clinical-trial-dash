# Clinical Trial Dashboard Backend

FastAPI + SQLite backend for the Clinical Trial Data Dashboard project.

## Features

- JWT-based authentication
- Two roles: `uploader`, `viewer`
- CSV upload endpoint that validates and stores trial records
- Data summary endpoint for demographics
- SQLite database via SQLAlchemy
- Basic test suite with pytest

## Quick Start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database and seed default users
python init_db.py

# Run dev server
uvicorn app.main:app --reload --port 8000
