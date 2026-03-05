# Transaction Risk Assessment Service

A simple FastAPI backend with one endpoint (`POST /assess-risk`) to validate incoming transaction data, calculate a risk level, and store each request in SQLite.

## Features

- Input validation with Pydantic
- SQLite persistence with SQLAlchemy
- Basic risk rules:
  - `transaction_amount > 10000` -> `HIGH`
  - `country` not in `CA`, `US`, `UK` -> `MEDIUM`
  - Otherwise -> `LOW`
- Meaningful status codes and structured JSON responses

## Project Structure

```text
app/
  api/
    routes.py
  services/
    risk_service.py
  database.py
  main.py
  models.py
  schemas.py
requirements.txt
README.md
```

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```windows powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs will be available at:
- `http://127.0.0.1:8000/docs`

## API

### `POST /assess-risk`

Request body:

```json
{
  "transaction_id": "txn-1001",
  "transaction_amount": 12500.50,
  "country": "US"
}
```

Success response (`201 Created`):

```json
{
  "assessment_id": 1,
  "transaction_id": "txn-1001",
  "transaction_amount": 12500.50,
  "country": "US",
  "risk_level": "HIGH",
  "risk_reason": "transaction_amount is greater than 10000",
  "created_at": "2026-03-05T12:00:00"
}
```

Validation errors return `422 Unprocessable Entity`.
Unexpected server/database errors return `500 Internal Server Error`.

## Test Script

Run the API test script (uses FastAPI `TestClient`, no running server required):

```bash
python scripts/test_assess_risk.py
```

The script validates:
- `HIGH` risk for amount above threshold
- `MEDIUM` risk for disallowed countries
- `LOW` risk for allowed countries with low amount
- `422` responses for invalid input

## Database

SQLite database file is created automatically at:
- `risk_assessment.db`
