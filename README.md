# Compiler Stage Explorer

This project now includes a React UI plus a Python API that exposes each compiler stage:

- Lexemes / Tokens
- Parse Tree
- Symbol Table
- Abstract Syntax Tree (AST)
- Optimized AST
- Generated Code
- Execution Output

## Architecture (MVC-style)

### Backend (Python + Flask)

- `backend/models`: request/response models
- `backend/services`: compiler business logic wrapper
- `backend/controllers`: API routes
- `compiler_pipeline.py`: shared pipeline used by both API and CLI

### Frontend (React + Vite)

- `frontend/src/models`: API access layer
- `frontend/src/controllers`: UI logic/state management
- `frontend/src/views`: page and presentational components

## Run Backend

From the project root:

```powershell
pip install -r requirements.txt
python -m backend.app
```

Backend runs on `http://127.0.0.1:5000`.

## Run Frontend

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:5173` and proxies `/api` to the backend.

## CLI Still Works

```powershell
python main.py
```

The CLI now reuses `compiler_pipeline.py` for consistent behavior with the UI.