# SlotFlow

REST API for appointment booking with specialists. Built for cosmetology clinics, legal offices, medical centers — any service business.

## Stack
FastAPI · SQLAlchemy (async) · PostgreSQL · JWT · Docker · pytest

## Architecture
Service layer — routers handle HTTP, services handle business logic.

## Quick Start

```bash
git clone https://github.com/kit-kosatka/SlotFlow.git
cd SlotFlow
docker-compose up --build
```

## API

| Method | Endpoint | Access |
|--------|----------|--------|
| POST | `/auth/register` | Public |
| POST | `/auth/login` | Public |
| GET | `/specialists/` | Public |
| GET | `/specialists/{id}` | Public |
| POST | `/specialists/` | Admin |
| GET | `/slots/` | Public |
| POST | `/slots/` | Specialist |
| DELETE | `/slots/{id}` | Specialist |
| POST | `/appointments/` | Client |
| GET | `/appointments/my` | Authenticated |
| DELETE | `/appointments/{id}` | Admin |

## Testing

```bash
pytest -v
```