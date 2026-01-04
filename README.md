# player_roster

[日本語 README](README_JP.md)

## Overview

This project is a RESTful Web API developed using Django REST Framework (DRF),
featuring user authentication and role-based authorization.

Users can post and view comments on players.
Available API operations and response contents are controlled
based on the user role (admin / general).

The API is designed with JWT-based authentication,
role-based access control, and a resource-oriented approach,
with an emphasis on testability.

## Features

-   User authentication using JWT
-   Role-based API access control (admin / general)
-   Role-based response content control
-   List and retrieve users, teams, players, and comments
-   Create and view users, teams, players, and comments
-   Conditional resource retrieval (filtering, searching, ordering)
-   API request rate limiting (Throttling)
-   Soft delete mechanism for data visibility control

## Design Decisions

### User Registration and Authentication

Users can freely register accounts.
Only `username`, `email`, and `password` are required at registration.

Since email addresses are considered personal information,
they are excluded from API responses to expose only the minimum necessary data.

All newly registered users are assigned the `general` role.
Administrator users (`admin`) cannot be created via the API
and are expected to be registered directly from the command line
by the system administrator.

This design prevents privilege escalation and improves security.

### Role-Based Access Control

Creation and update operations for teams and players
are restricted to administrator users (`admin`)
to maintain data consistency.

On the other hand, list and retrieve operations
are available to general users (`general`),
clearly separating read and write responsibilities.

### Response Content Control

Even for the same endpoint,
response contents are controlled based on the user role
(`general` / `admin`).

This allows administrative information and publicly accessible data
to be clearly separated.

### Soft Delete

Instead of physically deleting records,
a soft delete approach using `deleted_at` is adopted.

This enables recovery from accidental deletions
and supports basic data history management.

Soft-deleted records are hidden from general users,
while administrators can access them when necessary.

### API Rate Limiting

To ensure API stability,
request rate limiting (Throttling) is applied
based on the user type.

This helps prevent excessive requests and abuse.

## Tech Stack

### Backend

-   Python
-   Django
-   Django REST Framework

### Authentication / Authorization

-   JWT (djangorestframework-simplejwt)

### Database

-   SQLite (development environment)
-   PostgreSQL (intended for production)

### API Features

-   django-filter (Filtering)
-   Ordering / SearchFilter (Django REST Framework)

### Testing

-   pytest
-   pytest-django

### Environment Management

-   django-environ

## Testing

Test targets are separated by responsibility.

-   **Models**  
    Verify model attributes and method behavior.

-   **Serializers**  
    Verify serialization, deserialization,
    and validation logic.

-   **Views**  
    Verify authentication, authorization,
    and response behavior through actual HTTP requests.

Detailed test cases are available in [documents/tests](documents/tests/).

## Authentication

This project uses JWT-based authentication.

By using access tokens and refresh tokens,
a balance between security and usability is achieved.

## Setup (Local Development)

```bash
git clone https://github.com/kikutan-day65/player_roster.git
cd player_roster

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## Notes

-   This project is intended for learning and design exploration.
-   No frontend is implemented; the API is designed to be used standalone.
