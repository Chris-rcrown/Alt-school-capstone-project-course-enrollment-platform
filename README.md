# Course Enrollment Platform API

A FastAPI backend for a course enrollment platform with JWT authentication, role-based access control, and relational database persistence.

## Features
- User registration and login with JWT authentication
- Role-based authorization for `student` and `admin`
- Public course listing and course details
- Admin-only course creation and updates
- Student enrollment and deregistration from courses
- Admin oversight on enrollments
- SQLAlchemy ORM and Alembic migrations
- Automated tests covering all endpoints

## Setup
1. Clone the repository.
2. Create a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and update the values.

```bash
copy .env.example .env
```

5. Set a secure `SECRET_KEY` and a PostgreSQL `DATABASE_URL` in `.env`.

## Run locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://127.0.0.1:8000/api/v1`.

## Migrations

Initialize and run migrations with Alembic:

```bash
alembic upgrade head
```

If you change models, generate a new migration with:

```bash
alembic revision --autogenerate -m "your message"
```

## Tests

Run tests with:

```bash
pytest
```

## API Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me`
- `GET /api/v1/courses`
- `GET /api/v1/courses/{course_id}`
- `POST /api/v1/courses` (admin)
- `PUT /api/v1/courses/{course_id}` (admin)
- `POST /api/v1/enrollments/{course_id}` (student)
- `DELETE /api/v1/enrollments/{course_id}` (student)
- `GET /api/v1/enrollments` (admin)
- `GET /api/v1/enrollments/course/{course_id}` (admin)
- `DELETE /api/v1/enrollments/{course_id}/users/{user_id}` (admin)
