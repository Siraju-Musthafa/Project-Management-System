Project Management System API

A backend system for managing users, projects, and tasks with authentication and role-based access control.

Built using FastAPI, PostgreSQL, and JWT Authentication.

Features

. JWT Authentication (Login)
. User Management (Admin & Developer roles)
. Project Management
. Task Management
. Task Assignment
. Status Tracking (todo, in_progress, done, blocked)
. Role-based Authorization (Admin-only actions)
. Auto API Docs (Swagger UI)

Tech Stack

. Backend: FastAPI (Python)
. Database: PostgreSQL
. ORM: SQLAlchemy
. Authentication: JWT (python-jose)
. Validation: Pydantic
. Server: Uvicorn

Project Structure

project-management-system/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── projects.py
│   │       └── tasks.py
│   ├── alembic/
│   ├── requirements.txt
│   ├── .env.example
│   
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── .env.local.example
│   
│
├── screenshots/
├── postman_collection.json
└── README.md

Setup Instructions
1. Clone Repository
git clone https://github.com/your-username/project-management-system.git
cd project-management-system
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install Dependencies
pip install -r requirements.txt
4. Setup Environment Variables

Create a .env file:

DATABASE_URL=postgresql://admin:admin%40123@localhost:5432/project_management_system
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
5. Run Server
uvicorn app.main:app --reload
API Documentation

Once server is running:

. Swagger UI: http://localhost:8000/docs

. ReDoc: http://localhost:8000/redoc

Authentication Flow

. Login via POST /auth/login
. Get JWT token
. Use token in headers

Authorization: Bearer <your_token>

API Endpoints
Auth
. POST /auth/login → Login user

Users
. POST /users/ → Create user (admin only)
. GET /users/ → List users (admin only)
. GET /users/me → Get current logged-in user

Projects
. POST /projects/ → Create project (admin only)
. GET /projects/ → List projects
. PUT /projects/{project_id} → Update project
. DELETE /projects/{project_id} → Delete project

Tasks
.POST /tasks/ → Create task (admin only)
. GET /tasks/ → List tasks with filtering and pagination
. GET /tasks/{task_id} → Get task by id
. PUT /tasks/{task_id} → Update task
. PATCH /tasks/{task_id}/status → Update task status
. DELETE /tasks/{task_id} → Delete task

Task Status Values
Allowed values:

. todo
. in_progress
. done
. blocked

Testing

. Use Postman or Swagger UI
. Set Content-Type: application/json
. Add Authorization header for protected routes

Role-Based Access Control
Admin
--Create users
--View all users
--Create projects
--Create tasks
--View all tasks
--Update status of any task

Developer

--Login to the system
--View assigned projects
--View assigned tasks
--Update status of own assigned tasks only

Common Issues and Fixes
422 Unprocessable Entity

. Ensure request body is JSON
. Set Content-Type: application/json

401 Unauthorized

. Missing or invalid JWT token

500 ResponseValidationError

. Status mismatch
. Use valid enum values

Future Improvements

. Frontend (React / Next.js Dashboard)
. Pagination and filtering
. Email notifications
. Docker support
. CI/CD pipeline

ER Diagram

Users
-----
id (PK)
name
email
password
role

Projects
--------
id (PK)
name
description
created_by (FK -> users.id)

Tasks
-----
id (PK)
title
description
status
project_id (FK -> projects.id)
assigned_to (FK -> users.id)
due_date
