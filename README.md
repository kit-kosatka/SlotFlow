# SlotFlow 📅

Booking system API for specialists (cosmetology, legal, medical, etc.)

## Tech Stack
- FastAPI
- SQLAlchemy (async)
- SQLite / PostgreSQL
- JWT Authentication
- pytest

## Features
- Role-based access (admin, specialist, client)
- Specialist profiles with procedures (many-to-many)
- Time slot management
- Appointment booking system
- 9 automated tests

## Installation
```bash
git clone https://github.com/kit-kosatka/SlotFlow.git
cd SlotFlow
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running
```bash
uvicorn app.main:app --reload
```

## API Endpoints
### Auth
- `POST /auth/register` — Register
- `POST /auth/login` — Login

### Specialists
- `GET /specialists/` — List specialists
- `GET /specialists/{id}` — Get specialist
- `POST /specialists/` — Create specialist (admin)

### Slots
- `GET /slots/` — Available slots
- `POST /slots/` — Create slot (specialist)
- `DELETE /slots/{id}` — Delete slot (specialist)

### Appointments
- `POST /appointments/` — Book appointment (client)
- `GET /appointments/my` — My appointments
- `DELETE /appointments/{id}` — Cancel appointment (admin)

## Testing
```bash
pytest -v
```