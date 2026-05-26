# SlotFlow

REST API for appointment booking with specialists — cosmetology clinics, legal offices, medical centers, and any other service business.

Specialists manage their availability, clients book appointments. Admins keep everything running smoothly.

## Stack
FastAPI · SQLAlchemy (async) · PostgreSQL · JWT · Docker · pytest

## Highlights
- Role-based access — admin, specialist, client
- Specialists linked to procedures via many-to-many
- Slot availability tracked automatically on booking and cancellation
- Service layer architecture
- Integration tests with isolated test database

## Quick Start
```bash
git clone https://github.com/kit-kosatka/SlotFlow.git
cd SlotFlow
docker-compose up --build
```

API docs available at `/docs`