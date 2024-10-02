
# Inventory Management System

## Table of Contents
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Conventions](#conventions)
  - [Class-Based Views](#class-based-views)
  - [Selectors and Services](#selectors-and-services)
- [Special Features](#special-features)
  - [Custom Exception Handler](#custom-exception-handler)
  - [Logging](#logging)
- [Running Tests](#running-tests)
- [Dockerization](#dockerization)

## Introduction
This Inventory Management System is a robust web application built with Django and Django Rest Framework (DRF). It provides APIs for managing inventory items with authentication using JWT tokens.

## Project Structure
```
inventory_management/
├── inventory_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│
├── inventory/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── selectors.py
│   ├── services.py
│   ├── api.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Technologies Used
- Django
- Django Rest Framework
- PostgreSQL
- Redis
- Docker
- Gunicorn
- JWT (JSON Web Tokens) for authentication

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### Environment Variables
Create a `.env` file in the project root with the following content:
```env
DEBUG=1
SECRET_KEY=your_secret_key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Database
DB_NAME=yourdbname
DB_USER=yourdbuser
DB_PASSWORD=yourdbpassword
DB_HOST=db
DB_PORT=5432

# Redis
CACHE_URL=redis://redis:6379/1
```

### Running the Project
1. **Build and run the Docker containers:**
   ```sh
   docker-compose up --build
   ```

2. **Apply the migrations:**
   ```sh
   docker-compose exec web python manage.py migrate
   ```

3. **Create a superuser (optional):**
   ```sh
   docker-compose exec web python manage.py createsuperuser
   ```

4. Open your browser and go to `http://localhost:8000` to see the application running.

## API Endpoints

### Authentication
- **Register**: `POST /auth/register/`
  - Request Body: `{"username": "user", "password": "pass"}`
- **Login**: `POST /auth/login/`
  - Request Body: `{"username": "user", "password": "pass"}`
- **Token Retrieve**: `POST /auth/token/`
  - Request Body: `{"username": "user", "password": "pass"}`
- **Token Refresh**: `POST /auth/token/refresh/`
  - Request Body: `{"refresh": "refresh_token"}`

### Items
- **Create Item**: `POST /items/`
  - Request Body: `{"name": "item", "description": "desc", "quantity": 10, "price": 99.99}`
- **Get, Update, Delete Item**: `GET, PUT, DELETE /item/<int:item_id>/`

## Conventions

### Class-Based Views
We use Django's class-based views for better code organization and reuse.

### Selectors and Services
- **Selectors**: Handle data retrieval logic.
- **Services**: Handle business logic and operations (create, update, delete).

## Special Features

### Custom Exception Handler
We have a custom exception handler for better error handling. It provides specific error messages and descriptions using custom exceptions like `NotFoundException` and `AlreadyExistsException`.

### Logging
Operations along with user actions are logged to provide a clear audit trail. Logs include details of the request made and the result obtained.

## Running Tests
To run tests, execute:
```sh
docker-compose exec web python manage.py test
```

## Dockerization
The project is fully Dockerized. It includes services for the Django application, PostgreSQL database, and Redis.

### Dockerfile
Defines the setup for the Django application.

### docker-compose.yml
Defines the multi-container setup for the project.

---