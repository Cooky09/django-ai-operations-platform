# Django AI Operations Platform

A small production-shaped backend demonstrating **Django, Django REST Framework, PostgreSQL, Redis, Celery, Docker and automated testing/CI**.

The application models an AI-assisted support-ticket workflow. When a ticket is created, a Celery background job classifies it and creates a short summary. The AI service is intentionally local/deterministic so the project runs without an external API key.

## Architecture

```text
Client
  |
  v
Django REST API
  |
  +----> PostgreSQL
  |
  +----> Redis ----> Celery Worker ----> AI Service
```

## Features

- RESTful ticket CRUD API with Django REST Framework
- PostgreSQL persistence
- Redis message broker
- Celery asynchronous AI processing
- Job status tracking
- Ticket classification and summarisation service
- Docker Compose development environment
- Pytest API tests
- Ruff linting
- GitHub Actions CI
- Clear separation between API, models, background tasks and AI service logic

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/tickets/` | List tickets |
| POST | `/api/tickets/` | Create a ticket and queue AI processing |
| GET | `/api/tickets/{id}/` | Retrieve a ticket |
| POST | `/api/tickets/{id}/process/` | Re-run AI processing |
| GET | `/api/tickets/{id}/jobs/` | View processing jobs |
| GET | `/api/jobs/` | List background jobs |
| GET | `/api/jobs/health/` | Simple API health endpoint |

### Example

```bash
curl -X POST http://localhost:8000/api/tickets/   -H "Content-Type: application/json"   -d '{
    "title": "Payment failed",
    "description": "My card was charged but the invoice shows an error.",
    "priority": "high"
  }'
```

The ticket is stored immediately and a Celery job is queued. Once the worker completes, the ticket contains:

```json
{
  "ai_category": "billing",
  "ai_summary": "My card was charged but the invoice shows an error."
}
```

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

API:

`http://localhost:8000/api/tickets/`

Run tests:

```bash
docker compose exec web pytest
```

## Run locally

Start PostgreSQL and Redis, then:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python manage.py migrate
python manage.py runserver
```

In another terminal:

```bash
celery -A config worker --loglevel=INFO
```

Run tests:

```bash
pytest
```

## Why this project?

This project is intentionally small, but demonstrates the architecture used in larger backend/AI systems:

- synchronous API requests are separated from long-running work
- background jobs are persisted and observable
- relational data is stored in PostgreSQL
- Redis acts as the queue/broker
- business/AI logic is separated from API views
- tests cover API behaviour
- CI automatically runs linting, Django checks, migrations and tests

## Future extensions

- JWT authentication and role-based access control
- real LLM provider behind `tickets/services.py`
- OpenTelemetry tracing
- Prometheus metrics
- API rate limiting
- Azure deployment
- Terraform infrastructure
