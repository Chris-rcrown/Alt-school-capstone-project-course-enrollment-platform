# Course Enrollment Platform API

## Project Summary
The Course Enrollment Platform is a RESTful backend API built with FastAPI for managing users, courses, and student enrollments.

It provides:
- JWT-based authentication
- Role-based access control (`admin` and `student`)
- Course management for admins
- Course enrollment workflows for students
- Relational persistence with SQLAlchemy ORM
- Database migrations with Alembic
- Automated test coverage for key API flows

## Tech Stack
- Python 3.x
- FastAPI
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- JWT (`python-jose`)
- Password hashing (`passlib` with `sha256_crypt`)
- Pytest + FastAPI TestClient
- Uvicorn

## High-Level Architecture
The codebase follows a layered architecture:

- API Layer (`app/api/...`): route definitions, request handling, dependencies
- Service Layer (`app/services/...`): business logic and rule enforcement
- CRUD Layer (`app/crud/...`): database query and mutation operations
- Models (`app/models/...`): SQLAlchemy ORM entities
- Schemas (`app/schemas/...`): Pydantic input/output contracts
- Core (`app/core/...`): settings and security utilities
- DB (`app/db/...`): engine/session setup and base metadata

```mermaid
flowchart LR
		Client --> Router[FastAPI Routers]
		Router --> Deps[Auth/Role Dependencies]
		Router --> Services[Service Layer]
		Services --> CRUD[CRUD Layer]
		CRUD --> DB[(Database)]
		Router --> Schemas[Pydantic Schemas]
		Services --> Security[JWT + Password Hashing]
```

## Core Features and Rules

### 1. Authentication and Authorization
- User registration with hashed password storage
- OAuth2 password flow login (`username` = email)
- Bearer JWT access tokens
- Active-user check before protected operations
- Role guards:
	- `admin` required for course management and enrollment oversight
	- `student` required for self-enrollment endpoints

### 2. User Management
- Register users with role selection (`student` or `admin`)
- Retrieve current user profile via authenticated endpoint

### 3. Course Management
- Public read access to active courses
- Admin-only create/update operations
- Business rules:
	- Course code must be unique
	- Capacity must be greater than zero
	- Inactive courses are hidden from public course detail endpoint

### 4. Enrollment Management
- Students can enroll in active courses
- Students can deregister from enrolled courses
- Admins can:
	- list all enrollments
	- list enrollments by course
	- remove any student enrollment
- Business rules:
	- No duplicate enrollment for same user+course
	- Enrollment blocked when course is full
	- Enrollment blocked when course is inactive/unavailable

## Data Model

### User
- `id` (PK)
- `name`
- `email` (unique)
- `hashed_password`
- `role` (`student` or `admin`)
- `is_active`

### Course
- `id` (PK)
- `title`
- `code` (unique)
- `capacity`
- `is_active`

### Enrollment
- `id` (PK)
- `user_id` (FK -> users.id)
- `course_id` (FK -> courses.id)
- `created_at`
- Unique constraint: `(user_id, course_id)`

```mermaid

![ERD](image2.png)

erDiagram
		USERS ||--o{ ENROLLMENTS : has
		COURSES ||--o{ ENROLLMENTS : has

		USERS {
				int id PK
				string name
				string email UNIQUE
				string hashed_password
				string role
				bool is_active
		}

		COURSES {
				int id PK
				string title
				string code UNIQUE
				int capacity
				bool is_active
		}

		ENROLLMENTS {
				int id PK
				int user_id FK
				int course_id FK
				datetime created_at
		}
```

## Database and Migrations
- Alembic migration `0001_initial` creates `users`, `courses`, and `enrollments`
- Foreign keys use `ON DELETE CASCADE`
- Runtime database is configured via `DATABASE_URL`
- Default fallback database in settings: `sqlite:///./app.db`

Run migrations:

```bash
alembic upgrade head
```

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe_change"
```

## Environment Variables
Configuration is loaded from `.env` (if present).

Supported settings:
- `PROJECT_NAME` (default: `Course Enrollment Platform`)
- `SECRET_KEY` (default: `change-me-in-production`)
- `ALGORITHM` (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `60`)
- `DATABASE_URL` (default: `sqlite:///./app.db`)

Recommended `.env` template:

```env
PROJECT_NAME=Course Enrollment Platform
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./app.db
```

For production (example):

```env
DATABASE_URL=postgresql+psycopg2://username:password@host:5432/dbname
```

## Local Setup and Run Guide

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env`, then set secure values.

```bash
copy .env.example .env
```

If you are using macOS/Linux:

```bash
cp .env.example .env
```

5. Run database migrations:

```bash
alembic upgrade head
```

6. Start the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Base API URL:
- `http://127.0.0.1:8000/api/v1`

Interactive docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoint Reference

### Auth

#### Register User
- Method: `POST`
- Path: `/api/v1/auth/register`
- Request body (JSON):

```json
{
	"name": "Jane Student",
	"email": "jane@example.com",
	"password": "password123",
	"role": "student"
}
```

- Success response: `201 Created`

#### Login
- Method: `POST`
- Path: `/api/v1/auth/login`
- Content type: `application/x-www-form-urlencoded`
- Form fields:
	- `username` (user email)
	- `password`

- Success response: `200 OK`

```json
{
	"access_token": "<jwt_token>",
	"token_type": "bearer"
}
```

### Users

#### Get Current User
- Method: `GET`
- Path: `/api/v1/users/me`
- Auth: Bearer token required
- Success response: `200 OK`

### Courses

#### List Active Courses (Public)
- Method: `GET`
- Path: `/api/v1/courses`
- Success response: `200 OK`

#### Get Course by ID (Public, Active Only)
- Method: `GET`
- Path: `/api/v1/courses/{course_id}`
- Success response: `200 OK`
- Not found/inactive: `404 Not Found`

#### Create Course (Admin)
- Method: `POST`
- Path: `/api/v1/courses`
- Auth: Admin token required
- Request body example:

```json
{
	"title": "Intro to Python",
	"code": "CS101",
	"capacity": 30
}
```

- Success response: `200 OK`

#### Update Course (Admin)
- Method: `PUT`
- Path: `/api/v1/courses/{course_id}`
- Auth: Admin token required
- Request body fields are optional (`title`, `code`, `capacity`, `is_active`)
- Success response: `200 OK`

### Enrollments

#### Enroll in Course (Student)
- Method: `POST`
- Path: `/api/v1/enrollments/{course_id}`
- Auth: Student token required
- Success response: `200 OK`

#### Deregister from Course (Student)
- Method: `DELETE`
- Path: `/api/v1/enrollments/{course_id}`
- Auth: Student token required
- Success response: `200 OK`

#### List All Enrollments (Admin)
- Method: `GET`
- Path: `/api/v1/enrollments`
- Auth: Admin token required
- Success response: `200 OK`

#### List Enrollments by Course (Admin)
- Method: `GET`
- Path: `/api/v1/enrollments/course/{course_id}`
- Auth: Admin token required
- Success response: `200 OK`

#### Remove Student from Course (Admin)
- Method: `DELETE`
- Path: `/api/v1/enrollments/{course_id}/users/{user_id}`
- Auth: Admin token required
- Success response: `200 OK`

## Common Error Responses
- `400 Bad Request`
	- email already registered
	- invalid/inactive enrollment target
	- course full
	- duplicate enrollment
	- invalid capacity
- `401 Unauthorized`
	- invalid token
	- bad login credentials
- `403 Forbidden`
	- role mismatch (admin-only or student-only route)
- `404 Not Found`
	- course not found
	- enrollment not found

## Testing
The project includes automated tests for:
- authentication flow
- profile retrieval
- admin course lifecycle operations
- student enrollment/deregistration
- admin enrollment oversight and removal

Run tests:

```bash
pytest
```

Testing strategy:
- Uses SQLite test database (`test.db`)
- Overrides application DB dependency
- Per-test transaction rollback for isolation

## Deployment Notes
The provided `Procfile` defines:
- release phase: `alembic upgrade head`
- web process: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
![API Docs](image.png)

This supports platforms that honor Procfile-based deployment workflows.

## Security Considerations
- Replace the default `SECRET_KEY` in all non-local environments
- Use HTTPS in production
- Restrict CORS origins in production (current config allows all origins)
- Use strong password policies and consider account verification/rate limiting

## Submission Checklist
- [x] REST API with authentication
- [x] Role-based authorization
- [x] Course management endpoints
- [x] Enrollment workflow endpoints
- [x] Database models + migration
- [x] Automated tests
- [x] Deployment process definition

## Author Notes
This documentation is aligned with the current implementation in this repository and can be used directly for capstone project submission.
