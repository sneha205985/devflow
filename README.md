# DevFlow

> Enterprise-grade project management backend inspired by Jira and Linear.

DevFlow is a backend platform for managing software projects, teams, and organizations — the kind of system that tools like Jira, Linear, and Azure DevOps provide. It is built with **FastAPI** following a clean, layered architecture, and ships with **JWT authentication**, **role-based access control (RBAC)**, **PostgreSQL**, **Redis**, **Celery**, and **Docker** out of the box.

The project is designed to be production-shaped from day one: async SQLAlchemy, Alembic migrations, background workers, rate limiting, OAuth, and a full Swagger/OpenAPI specification. Authentication, organization management, team management, and RBAC are fully implemented; the remaining modules (projects, issues, notifications, and more) are scaffolded with a documented development roadmap.

---

## Features

- ✅ JWT Authentication
- ✅ Refresh Tokens
- ✅ Email Verification
- ✅ Google OAuth (OAuth2 / OpenID Connect)
- ✅ Organization Management
- ✅ Team Management
- ✅ Role-Based Access Control (RBAC)
- ✅ PostgreSQL (async)
- ✅ Redis (caching + Celery broker)
- ✅ Celery Background Workers
- ✅ Docker & Docker Compose
- ✅ Alembic Migrations
- ✅ Swagger / OpenAPI Documentation
- ✅ Async SQLAlchemy 2.0
- ✅ Rate Limiting & CORS
- ✅ Health Check API

---

## Tech Stack

**Backend**
- FastAPI
- Python 3.12
- SQLAlchemy (async, 2.0 style)
- Pydantic v2

**Database**
- PostgreSQL 16
- Alembic

**Authentication**
- JWT
- OAuth2
- Google OAuth

**Infrastructure**
- Docker
- Docker Compose
- Redis
- Celery

**Testing**
- Pytest
- pytest-asyncio

**Deployment**
- Uvicorn (ASGI server)

---

## Architecture Overview

DevFlow uses a **layered architecture** that keeps HTTP concerns, business logic, and data access cleanly separated. Each request flows through well-defined layers, which makes the codebase easy to test, extend, and reason about.

```
endpoint (HTTP)  ->  crud (DB queries)  ->  model (SQLAlchemy)
     |                                          ^
   schema (Pydantic in/out)                  Base + mixins
     |
   deps (auth + RBAC injected via Depends)
```

**Endpoints** are the HTTP boundary. They parse and validate requests, delegate work to the CRUD and service layers, and shape the response — they contain no database logic of their own. **CRUD** modules own all database access: every query, insert, update, and delete lives here as a reusable async function, so endpoints never touch the session directly. **Models** are the SQLAlchemy ORM definitions that map to database tables, using shared `Base` and mixins (UUID primary keys, timestamps) for consistency across every table.

**Schemas** are Pydantic models that define the shape of data entering and leaving the API. They enforce validation on input and serialization on output, and keep the public API contract decoupled from the internal database models. **Dependencies** (`deps.py`) provide cross-cutting concerns via FastAPI's `Depends` system — most importantly `get_current_user` for authentication and `require_role(...)` for org-scoped RBAC, both injected declaratively into any endpoint that needs them.

**Services** hold reusable business logic that spans multiple modules — for example notification dispatch, activity logging, and email orchestration — so that logic is written once and called from anywhere. This separation means a new module is always added the same way: model → schema → CRUD → endpoint → router → migration → test.

---

## Project Structure

```
app/
├── api/          # HTTP layer: route definitions, dependencies, versioned endpoints
│   ├── deps.py   # Auth + RBAC dependencies (get_current_user, require_role)
│   └── v1/       # Versioned API (router + endpoints)
├── core/         # Config, security (JWT/hashing), Redis client, rate limiter
├── crud/         # Database query functions (one module per resource)
├── db/           # SQLAlchemy Base, mixins, async session/engine
├── models/       # ORM models + shared enums (Role, IssueStatus, etc.)
├── schemas/      # Pydantic request/response models
├── services/     # Cross-cutting business logic (notifications, activity, email)
├── workers/      # Celery app + background tasks
└── main.py       # FastAPI app factory, middleware, router registration
tests/            # Pytest suite (async fixtures, in-memory SQLite)
alembic/          # Migration environment and versions
```

| Folder | Responsibility |
|---|---|
| `app/api` | HTTP routing, request/response handling, dependency injection |
| `app/core` | Configuration, JWT/password security, Redis, rate limiting |
| `app/crud` | All database read/write operations |
| `app/db` | ORM base classes, mixins, async session management |
| `app/models` | SQLAlchemy table definitions and enums |
| `app/schemas` | Pydantic validation and serialization models |
| `app/services` | Reusable business logic shared across modules |
| `app/workers` | Celery worker app and asynchronous tasks |
| `tests` | Automated test suite |
| `alembic` | Database migration scripts and environment |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/devflow.git
cd devflow
```

### 2. Create your environment file

```bash
cp .env.example .env
```

Then edit `.env` and set at minimum a strong `SECRET_KEY` (and your Google OAuth credentials if you want OAuth login).

### 3. Start the stack with Docker

```bash
docker compose up --build
```

This starts the API, PostgreSQL, Redis, and the Celery worker together.

### 4. Apply database migrations

```bash
docker compose exec api alembic upgrade head
```

### 5. Open the API docs

Navigate to **http://localhost:8000/docs** for the interactive Swagger UI.

---

## Environment Variables

Configuration is supplied via a `.env` file (see `.env.example`). Do not commit real secrets.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Secret used to sign JWT access and refresh tokens |
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_HOST` | Database host (`db` when running via Docker Compose) |
| `POSTGRES_PORT` | Database port (default `5432`) |
| `REDIS_URL` | Redis connection URL (cache) |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `MAIL_USERNAME` | SMTP username for outbound email |
| `MAIL_PASSWORD` | SMTP password for outbound email |

---

## Running with Docker

The entire stack is orchestrated by `docker-compose.yml`:

```bash
docker compose up --build
```

Services started:

| Service | Description |
|---|---|
| `api` | FastAPI application served by Uvicorn |
| `db` | PostgreSQL 16 database |
| `redis` | Redis (cache + Celery broker/result backend) |
| `worker` | Celery worker for background tasks (e.g. email) |

Once running:

- **API:** http://localhost:8000
- **Swagger:** http://localhost:8000/docs

---

## Database Migrations

Database schema is managed with **Alembic**.

**For users running the project:** apply the existing migrations only.

```bash
docker compose exec api alembic upgrade head
```

**For developers modifying the database models:** generate a new revision after changing any model, then apply it.

```bash
docker compose exec api alembic revision --autogenerate -m "describe your change"
docker compose exec api alembic upgrade head
```

> Creating a revision is only required when you change `app/models`. Regular users never need `--autogenerate`.

---

## Running Tests

The test suite uses **Pytest** with async fixtures and an in-memory SQLite database.

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run a specific directory
pytest tests/
```

---

## API Documentation

DevFlow automatically generates interactive API documentation from the FastAPI route definitions:

- **Swagger UI:** http://localhost:8000/docs
- **OpenAPI schema:** http://localhost:8000/api/v1/openapi.json

The Swagger UI lets you explore every endpoint, view request/response schemas, and execute calls directly from the browser.

---

## Current Implemented Features

### Authentication
- `POST /api/v1/auth/register` — register a new user
- `POST /api/v1/auth/login` — obtain access + refresh tokens
- `POST /api/v1/auth/refresh` — rotate tokens using a refresh token
- `GET /api/v1/auth/verify-email` — verify email via signed token
- `GET /api/v1/auth/me` — current authenticated user
- `GET /api/v1/auth/google/login` + `/callback` — Google OAuth flow

### Organizations
- `POST /api/v1/organizations` — create an organization
- `GET /api/v1/organizations` — list organizations
- Add members with assigned roles
- Org-scoped RBAC guard via `require_role(Role.admin, ...)`

### Teams
- Create teams within an organization
- List teams within an organization

### Infrastructure
- Celery worker for background tasks (email dispatch)
- Redis caching and Celery broker
- Rate limiting and CORS middleware
- Health check endpoint

---

## Project Roadmap

- [x] Authentication
- [x] Organizations
- [x] Teams
- [x] RBAC
- [ ] Projects
- [ ] Issues
- [ ] Comments
- [ ] Notifications
- [ ] Analytics
- [ ] Search
- [ ] Activity Logs
- [ ] Admin Dashboard

---

## Development Roadmap

A detailed, file-by-file guide for implementing each remaining module. Follow the **auth/orgs pattern** every time: model → schema → crud → endpoint → register in router → migration → test.

### 1. Projects
- `app/models/project.py` — Project(id, name, org_id FK, team_id FK?, is_archived, created_by). + project_members assoc.
- `app/schemas/project.py` — ProjectCreate / ProjectOut / ProjectUpdate
- `app/crud/project.py` — create, list_by_org, archive, get
- `app/api/v1/endpoints/projects.py` — replace stub; guard with require_role
- Add to `app/models/__init__.py`

### 2. Issues (the core)
- `app/models/issue.py` — Issue(id, project_id FK, title, description, status[Enum], priority[Enum], assignee_id FK, reporter_id FK, due_date, sprint_id FK?). + Label, IssueLabel assoc, Attachment(issue_id, file_url).
- `app/models/sprint.py` — Sprint(id, project_id, name, start, end)
- `app/schemas/issue.py` — IssueCreate / Out / Update / StatusUpdate (for Kanban drag-drop)
- `app/crud/issue.py` — CRUD + move_status + filter(status, assignee, label)
- `app/api/v1/endpoints/issues.py` — CRUD + PATCH /{id}/status (Kanban)
- On every mutation: call `log_activity(...)` (module 7) + `create_notification(...)` (module 4)

### 3. Comments
- `app/models/comment.py` — Comment(id, issue_id FK, author_id FK, body)
- Parse `@username` in body -> create mention notifications
- schema + crud + endpoint (nested under /issues/{id}/comments)

### 4. Notifications (real-time)
- `app/models/notification.py` — Notification(id, user_id, type, payload JSON, is_read)
- `app/api/v1/endpoints/notifications.py` — list, mark-read
- `app/api/v1/ws.py` — **WebSocket** `/ws/notifications`; maintain `dict[user_id, set[WebSocket]]` connection manager in `app/services/ws_manager.py`
- `app/services/notify.py` — create_notification() -> save + push via ws_manager + queue email task
- Register WS route in `app/main.py`

### 5. Search
- `app/api/v1/endpoints/search.py` — GET /search?q=&status=&assignee=&label=
- `app/crud/search.py` — Postgres `ILIKE` across title/description; later upgrade to `tsvector` full-text or Meilisearch
- Cache hot queries in Redis (`app/core/redis.py`)

### 6. Analyticsa
- `app/crud/analytics.py` — aggregate queries: tasks_completed, avg_completion_time, productivity_per_dev, project_completion_pct, sprint_burndown
- `app/api/v1/endpoints/analytics.py` — return JSON for frontend charts
- Cache results in Redis with TTL

### 7. Activity Log
- `app/models/activity.py` — ActivityLog(id, org_id, actor_id, action, target_type, target_id, meta JSON)
- `app/services/activity.py` — `async def log_activity(db, actor, action, target)` — call from every mutation
- endpoint: GET /activity?org_id=

### 8. Invitations
- `app/models/invitation.py` — Invitation(id, org_id, email, role, token, status[Enum], expires_at)
- `app/crud/invitation.py` + endpoint: POST /organizations/{id}/invite, GET /invitations/accept?token=
- Email task in `app/workers/tasks.py`

### 9. Admin dashboard
- `app/api/v1/endpoints/admin.py` — guard with `get_current_user` + `is_superuser` check
- list/manage users, orgs, projects; system health (DB ping, Redis ping, worker count)

### 10. Background workers (expand)
- `app/workers/tasks.py` — real SMTP send, periodic sprint-digest (Celery beat), analytics precompute

---

## Production Deployment

The project is structured for a standard cloud deployment. Recommended components:

| Component | Purpose |
|---|---|
| **GitHub Actions** | CI pipeline — lint (ruff), run Pytest, and build the Docker image on every push (`.github/workflows/ci.yml`). |
| **Docker** | Package the application into a reproducible image for any environment. |
| **AWS ECS / Fargate** | Run the containerized API and worker as managed, scalable services. |
| **AWS RDS** | Managed PostgreSQL database for durable, backed-up storage. |
| **Redis (ElastiCache)** | Managed Redis for caching and the Celery message broker. |
| **Environment Variables** | Inject secrets and config at runtime via AWS SSM Parameter Store / Secrets Manager. |
| **Prometheus** | Scrape application metrics from a `/metrics` endpoint. |
| **Grafana** | Visualize metrics and build operational dashboards. |
| **Sentry** | Capture and alert on application errors and exceptions. |
| **Structured Logging** | Emit JSON logs (`app/core/logging.py`) for searchable, aggregatable observability. |

---

## Database Schema / Tables

DevFlow targets **25+ tables** for full feature coverage.

| Table | Purpose |
|---|---|
| `users` | Registered user accounts and credentials |
| `organizations` | Top-level tenant entities |
| `organization_members` | User ↔ organization membership with roles |
| `teams` | Teams within an organization |
| `team_members` | User ↔ team membership |
| `projects` | Projects belonging to an organization |
| `project_members` | User ↔ project membership |
| `issues` | Tasks/bugs with status, priority, assignee |
| `labels` | Labels/tags for categorizing issues |
| `issue_labels` | Issue ↔ label association |
| `attachments` | Files attached to issues |
| `comments` | Discussion threads on issues |
| `sprints` | Time-boxed iterations within a project |
| `notifications` | In-app notifications per user |
| `activity_logs` | Audit trail of every action |
| `invitations` | Pending organization invitations |
| `refresh_tokens` | Persisted refresh tokens (optional) |
| `roles` / `permissions` | Dynamic RBAC definitions (optional) |
| `saved_searches` | Stored user search filters |
| `webhooks` | Outbound integration webhooks (optional) |

---

## Future Improvements

- **Projects** — full project lifecycle, archiving, and per-project analytics
- **Issues** — Kanban board, sprints, labels, attachments, and filtering
- **Notifications** — real-time delivery over WebSockets plus email
- **Analytics** — productivity, completion-time, and sprint burndown dashboards
- **Search** — global full-text search across issues and projects
- **Admin Dashboard** — user, organization, and system-health management
- **Monitoring** — Prometheus metrics, Grafana dashboards, and Sentry error tracking
- **Deployment** — CI/CD via GitHub Actions and managed AWS infrastructure

---

## Contributing

Contributions are welcome. To propose a change:

1. **Fork** the repository.
2. **Create a branch** for your feature or fix (`git checkout -b feature/my-feature`).
3. **Commit** your changes (`git commit -m "Add my feature"`).
4. **Push** to your fork (`git push origin feature/my-feature`).
5. **Open a Pull Request** describing your changes.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## Author

**Sneha Gupta**
