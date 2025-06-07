# Koden Backend

This is the backend service for Koden, built with FastAPI.

## Setup

1. Install PDM if you haven't already:
```bash
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
```

2. Install dependencies:
```bash
pdm install
```

## Running the Service

To run the development server:

```bash
pdm run dev
```

This will start the server with hot-reload enabled at `http://localhost:8000`

Alternatively, you can run it directly with uvicorn:
```bash
pdm run uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/analyze/
Accepts a zip file containing a repository and returns its file structure.

Request:
- Content-Type: multipart/form-data
- Body: zip file

Response:
```json
{
    "files": ["path/to/file1.txt", "path/to/file2.py", ...]
}
``` 