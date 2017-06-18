# PMS - Printing Management System
The PMS is a web-based software which provides easy management of both 2d and 3d printing orders.

## Quickstart
1. Create virtual environment with Python 3 and don't forget to activate the environment.
2. Install requirements: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python3 manage.py runserver 8000`

## Development Notes
* Regenerate translation files: `django-admin makemessages -l de`
* Recompile translation files: `django-admin.py compilemessages`
