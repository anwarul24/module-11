# Property Rental & Management System

A Django-based rental platform where **Property Owners** can list properties and manage
rental requests, and **Tenants** can search properties, send rental requests, and leave
reviews after a request is accepted.

Built with Django 5.1, PostgreSQL, and Bootstrap 5.3.

---

## Features

- **Authentication** — register (choose Owner or Tenant role), login, logout, profile update
- **Role-based authorization** — enforced both in views and via a custom
  `RoleBasedAccessMiddleware` (`accounts/middleware.py`)
- **Property CRUD** — owners can add/edit/delete only their own listings
- **Search & Filter** — by location, property type, min/max rent, with pagination
- **Rental Requests** — send / accept / reject / cancel, with these rules enforced:
  - a tenant can't request their own property
  - a tenant can't have two *pending* requests for the same property
    (enforced at the database level with a `UniqueConstraint`)
  - only the owner of a property can accept/reject its requests
- **Reviews & Ratings** — a tenant can review a property only after their request was
  accepted, and only once per property
- **Owner Dashboard** — total/available properties, total/pending/accepted requests
- **Tenant Dashboard** — total/pending/accepted/rejected requests
- **Django Admin** — Users, Properties, Rental Requests, Reviews all registered
- **Bonus features included**: pagination, favorite properties, email notifications
  (printed to console by default) for new requests and status changes

---

## Project Structure

```
property_rental_system/
├── accounts/       # Custom User model, auth views, role middleware
├── properties/     # Property model, CRUD, search/filter, favorites
├── rentals/        # RentalRequest model, send/accept/reject/cancel
├── reviews/        # Review model & submission
├── dashboard/      # Owner & Tenant dashboards
├── templates/      # Shared base.html, home.html
├── static/         # CSS
└── property_rental_system/   # Project settings & root urls
```

## Requirements

- Python 3.10+
- PostgreSQL 13+

## Setup

1. **Clone & enter the project, create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create the PostgreSQL database**
   ```bash
   psql -U postgres -c "CREATE DATABASE property_rental_db;"
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set `SECRET_KEY` and the `DB_*` values (and email settings if you
   want real emails instead of console output). Example:
   ```
   DB_NAME=property_rental_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create an admin account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/`.

## Roles

When registering, choose **Property Owner** or **Tenant**. What each role sees:

| | Owner | Tenant |
|---|---|---|
| Add/edit/delete properties | ✅ | ❌ |
| Browse & search properties | ✅ | ✅ |
| Send rental requests | ❌ | ✅ |
| Accept/reject requests | ✅ | ❌ |
| Cancel own pending requests | ❌ | ✅ |
| Leave reviews | ❌ | ✅ (after acceptance) |
| Dashboard | Owner stats | Tenant stats |

## Notes on Design Decisions

- Image uploads (`Property.image`, `User.profile_photo`) are stored under `MEDIA_ROOT`
  (`/media/`) — served by Django only in `DEBUG` mode; use a real file/object storage
  (e.g. S3) in production.
- Email notifications use Django's console backend by default so you can see them in
  the terminal without configuring SMTP. Set `EMAIL_BACKEND` /`EMAIL_HOST*` in `.env`
  to send real emails (e.g. via Gmail SMTP).
- Once a rental request is **accepted**, the property is automatically marked
  unavailable (`is_available = False`).

## What's not included (left as an exercise)

- REST API (Django REST Framework)
- Map/location integration
- Property image galleries (multiple images per property)

---

*This project was built to satisfy a Django assignment covering CRUD, Forms, Templates,
Authentication, Middleware, Model Relationships, and User Permissions.*
