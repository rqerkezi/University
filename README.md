# University Project

This project contains a Django REST backend and a simple React frontend.

## Backend

- Install dependencies: `pip install -r requirements.txt` (create requirements with django, djangorestframework, djangorestframework-authtoken, corsheaders, etc.)
- Apply migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Run server: `python manage.py runserver`

API endpoints of note:
- `POST /api/register/` - register user (fields: username, password, role: 'professor'|'student'|'administrator', faculty_id, title/year if needed)
- `POST /api-token-auth/` - obtain token (username, password)
- `GET /api/faculties/` - list faculties
- `GET /api/subjects/` - list subjects
- `GET /api/student/` `GET /api/professor/` `GET /api/admin/` - role-specific dashboards (authenticated + correct role)

CORS is configured in `backend/settings.py` to allow `http://localhost:3000`.

## Frontend

- Change directory to `frontend/`
- Install: `npm install`
- Start: `npm start`

Login stores the token in `localStorage` and navigates to a simple dashboard page.

## Tests

Run `python manage.py test` to execute Django tests.

## Deployment to PythonAnywhere (Free Tier)

1. Create a new PythonAnywhere account and log in.
2. Upload the project files or push via Git to your PythonAnywhere account.
3. Create a virtualenv on PythonAnywhere and install requirements: `pip install -r requirements.txt`.
4. In the Web tab, create a new web app and point it to the WSGI file in `backend/wsgi.py`.
5. Set environment variables in the PythonAnywhere Web app configuration page:
   - `ALLOWED_HOSTS` to your domain (e.g. `yourusername.pythonanywhere.com`)
   - `CORS_ALLOWED_ORIGINS` to your frontend origin(s). For example: `https://yourusername.pythonanywhere.com` or `https://yourfrontend.example.com`
   - Optionally `CSRF_TRUSTED_ORIGINS` to the same domain(s)
6. Run migrations on PythonAnywhere: `python manage.py migrate` (this will create the sample data and faculties)
7. Collect static files: `python manage.py collectstatic --noinput` and map the static files folder (`staticfiles`) in the PythonAnywhere Static files section.
8. Restart the web app in the PythonAnywhere Web tab.

Notes:
- Token authentication endpoints remain available at `/api-token-auth/`.
- Ensure you add your frontend domain to `CORS_ALLOWED_ORIGINS` either via environment variables or directly in settings before deploying.

