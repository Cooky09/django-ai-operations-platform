# Django AI Operations Platform

A production-oriented backend platform for managing support tickets and processing AI-powered operations asynchronously using **Django REST Framework, PostgreSQL, Redis, Celery, Docker, and automated CI**.

The project demonstrates how to build a reliable backend system where API requests, database persistence, asynchronous background processing, and AI services are separated into clear components.

---

## 🚀 Overview

The platform provides a REST API for creating and managing support tickets.

When a ticket is created:

1. The API validates and stores the ticket in PostgreSQL.
2. An `AIJob` record is created to track processing.
3. A Celery task is queued through Redis.
4. A background worker processes the ticket.
5. The AI processing service classifies the ticket and generates a short summary.
6. The ticket and AI job are updated with the results.
7. The API exposes the ticket and processing status to clients.

This architecture demonstrates a common pattern for production AI applications:

```text
                    ┌─────────────────────┐
                    │      REST Client    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Django REST API     │
                    │                     │
                    │ Ticket ViewSets     │
                    │ Serializers         │
                    │ Validation          │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │   PostgreSQL    │        │      Redis      │
        │                 │        │                 │
        │ Tickets         │        │ Celery Broker   │
        │ AI Jobs         │        │                 │
        └─────────────────┘        └────────┬────────┘
                                            │
                                            ▼
                                  ┌─────────────────────┐
                                  │   Celery Worker     │
                                  │                     │
                                  │ Background AI Task  │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │    AI Service       │
                                  │                     │
                                  │ Classification      │
                                  │ Summarisation       │
                                  └─────────────────────┘
```

---

## ✨ Features

* RESTful API built with Django REST Framework
* PostgreSQL persistence
* Asynchronous background processing with Celery
* Redis message broker
* AI job tracking and processing status
* Ticket classification
* Automatic ticket summarisation
* Dockerized development environment
* Docker Compose orchestration
* Automated database migrations
* API and service-level tests with Pytest
* Django system checks
* Ruff linting and formatting
* GitHub Actions CI pipeline
* Environment-based configuration
* Separation of API, business logic, and background tasks

---

## 🛠️ Technology Stack

| Technology                | Purpose                     |
| ------------------------- | --------------------------- |
| **Python 3.12**           | Application language        |
| **Django**                | Backend web framework       |
| **Django REST Framework** | REST API                    |
| **PostgreSQL**            | Relational database         |
| **Redis**                 | Message broker              |
| **Celery**                | Background task processing  |
| **Docker**                | Containerisation            |
| **Docker Compose**        | Local service orchestration |
| **Pytest**                | Automated testing           |
| **pytest-django**         | Django testing integration  |
| **Ruff**                  | Linting and code quality    |
| **Gunicorn**              | Production WSGI server      |
| **GitHub Actions**        | Continuous integration      |

---

# 📁 Project Structure

```text
django-ai-operations-platform/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── config/
│   ├── __init__.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── tickets/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   │
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tasks.py
│   ├── urls.py
│   └── views.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── manage.py
├── pytest.ini
├── requirements.txt
├── ruff.toml
└── README.md
```

---

# 🧠 Architecture

The application separates responsibilities between several components.

### Django API

Django and Django REST Framework handle:

* HTTP requests
* API routing
* request validation
* serializers
* database operations
* API responses

### PostgreSQL

PostgreSQL stores:

* support tickets
* ticket status
* AI-generated summaries
* ticket classifications
* AI processing jobs
* processing errors
* timestamps

### Redis

Redis acts as the message broker between the Django application and Celery workers.

```text
Django API
    │
    │ enqueue task
    ▼
  Redis
    │
    │ task message
    ▼
Celery Worker
```

### Celery

Celery handles work that should not block the API request.

For example:

```text
POST /api/tickets/

        │
        ▼

Create Ticket
        │
        ▼
Create AIJob
        │
        ▼
Queue Celery Task
        │
        ▼
Return API Response
```

The actual AI processing happens asynchronously.

---

# 🎫 Ticket Processing Flow

A typical ticket lifecycle looks like:

```text
OPEN
 │
 │ ticket created
 ▼
PROCESSING
 │
 │ Celery worker
 ▼
AI PROCESSING
 │
 ├── classify ticket
 ├── generate summary
 │
 ▼
RESOLVED
```

If processing fails:

```text
PROCESSING
      │
      ▼
   FAILED
```

The corresponding `AIJob` records the error so that processing failures can be inspected separately from the ticket itself.

---

# 📊 Data Model

## Ticket

A ticket contains:

* ID
* title
* description
* priority
* status
* AI-generated summary
* AI-generated category
* creation timestamp
* update timestamp

Example:

```json
{
  "id": 1,
  "title": "Unable to access account",
  "description": "I cannot log into my account after resetting my password.",
  "priority": "high",
  "status": "resolved",
  "ai_summary": "I cannot log into my account after resetting my password.",
  "ai_category": "account",
  "created_at": "...",
  "updated_at": "..."
}
```

## AIJob

Each background processing operation is tracked independently.

The job records:

* ticket
* processing status
* error information
* creation timestamp
* completion timestamp

This provides visibility into asynchronous processing rather than treating AI processing as a black box.

---

# 🔌 API Endpoints

## Tickets

### List tickets

```http
GET /api/tickets/
```

### Create a ticket

```http
POST /api/tickets/
```

Example request:

```json
{
  "title": "Unable to access account",
  "description": "I cannot log into my account after resetting my password.",
  "priority": "high"
}
```

### Retrieve a ticket

```http
GET /api/tickets/{id}/
```

### Update a ticket

```http
PUT /api/tickets/{id}/
```

### Partially update a ticket

```http
PATCH /api/tickets/{id}/
```

### Delete a ticket

```http
DELETE /api/tickets/{id}/
```

---

## Process a Ticket

```http
POST /api/tickets/{id}/process/
```

This queues the asynchronous AI processing task.

---

## AI Jobs

### List AI jobs

```http
GET /api/jobs/
```

### Retrieve an AI job

```http
GET /api/jobs/{id}/
```

### AI service health

```http
GET /api/jobs/health/
```

---

# 🐳 Running with Docker

Docker Compose is the recommended way to run the complete application.

## Prerequisites

Install:

* Docker Desktop
* Git

Clone the repository:

```bash
git clone https://github.com/Cooky09/django-ai-operations-platform.git
cd django-ai-operations-platform
```

Create the environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Start the application:

```bash
docker compose up --build
```

The following services will start:

```text
web       → Django API
worker    → Celery worker
db        → PostgreSQL
redis     → Redis
```

The API will be available at:

```text
http://localhost:8000/
```

API endpoint:

```text
http://localhost:8000/api/tickets/
```

---

# 🧪 Running Tests

Because PostgreSQL runs inside Docker, the recommended way to run the test suite is from the `web` container.

Start the services:

```bash
docker compose up -d
```

Run tests:

```bash
docker compose exec web pytest
```

Run Django system checks:

```bash
docker compose exec web python manage.py check
```

Expected result:

```text
System check identified no issues
```

---

# 🔍 Code Quality

Ruff is used for linting and import organisation.

Run:

```bash
ruff check .
```

Automatically fix supported issues:

```bash
ruff check . --fix
```

Format the project:

```bash
ruff format .
```

Then verify:

```bash
ruff check .
```

---

# 🔄 Continuous Integration

GitHub Actions automatically validates the project.

The CI pipeline performs checks including:

1. Python environment setup
2. Dependency installation
3. Ruff linting
4. Django system checks
5. Database migrations
6. Automated tests

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

This ensures that changes pushed to the repository are validated automatically.

---

# ⚙️ Environment Variables

Configuration is provided through environment variables.

Example:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=1

POSTGRES_DB=aiops
POSTGRES_USER=aiops
POSTGRES_PASSWORD=aiops
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
```

Do not commit `.env` files containing real credentials.

Use `.env.example` as the template for local configuration.

---

# 🧩 Local Development Without Docker

A Python virtual environment can also be used for development.

Create the environment:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run Django checks:

```powershell
python manage.py check
```

Run tests:

```powershell
pytest
```

> The Docker-based setup is recommended for the complete application because PostgreSQL and Redis are included as services.

---

# 🧪 Example API Request

Using PowerShell:

```powershell
$body = @{
    title = "Payment failed"
    description = "My payment was declined when trying to renew my subscription."
    priority = "high"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:8000/api/tickets/" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

The API creates the ticket and queues background processing.

You can then inspect:

```text
GET http://localhost:8000/api/tickets/
```

and:

```text
GET http://localhost:8000/api/jobs/
```

---

# 🧱 Design Principles

The project intentionally separates different responsibilities.

### API Layer

Responsible for:

* HTTP
* validation
* serialization
* routing
* responses

### Service Layer

Responsible for:

* ticket classification
* summarisation
* business logic

### Task Layer

Responsible for:

* asynchronous processing
* job state management
* error handling

### Data Layer

Responsible for:

* ticket persistence
* AI job persistence
* relationships
* database state

This separation makes the system easier to test and provides a foundation for replacing the current AI service with a production LLM or ML model.

---

# 🔮 Future Improvements

The current implementation provides the foundation for a larger AI operations platform.

Potential future improvements include:

### Authentication & Authorization

* JWT authentication
* user accounts
* role-based permissions
* API access controls

### Production AI Integration

Replace the current deterministic AI service with:

* OpenAI API
* Azure OpenAI
* locally hosted transformer models
* structured LLM outputs
* prompt/version management

### Observability

Add:

* structured logging
* request IDs
* Celery task metrics
* processing latency
* failure rates
* AI evaluation metrics

### API Documentation

Add:

* OpenAPI schema
* Swagger UI
* ReDoc

### Deployment

Deploy the application to Azure using services such as:

```text
Azure App Service / Container Apps
        │
        ├── Django API
        │
        ├── Celery Worker
        │
        ├── PostgreSQL
        │
        └── Redis
```

### AI Evaluation

Introduce automated evaluation for:

* classification accuracy
* summary quality
* response consistency
* latency
* failure rates

---

# 📈 Engineering Skills Demonstrated

This project demonstrates practical experience with:

* Python backend development
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* asynchronous architecture
* REST API design
* database modelling
* background job processing
* Docker
* Docker Compose
* automated testing
* Pytest
* code quality tooling
* CI/CD with GitHub Actions
* environment-based configuration
* AI service integration patterns

---

# 🎯 Why This Project Exists

The goal of this project is to demonstrate how an AI-enabled backend can be designed as a **maintainable and testable software system**, rather than simply calling an AI API from a web endpoint.

The architecture separates:

```text
API
 ↓
Business Logic
 ↓
Asynchronous Processing
 ↓
AI Service
 ↓
Persistent Results
```

This pattern can be extended to production use cases such as customer support automation, document processing, AI-assisted operations, and intelligent workflow systems.

---

# 📄 License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for details.

---

## 👩‍💻 Author

**Mahua Mukhopadhyay**

Software Engineer · Applied AI · Backend Development · QA/UAT

GitHub: [@Cooky09](https://github.com/Cooky09)
