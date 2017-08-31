# PMS - Printing Management System
The PMS is a web-based software which provides easy management of both 2d and 3d printing orders.

## Quickstart
1. Create virtual environment with Python 3.6 and don't forget to activate the environment.
2. Install requirements: `pip install -r requirements.txt`
3. Copy `local_settings.py.sample` to `local_settings.py` and adjust the configuration (see `pms/settings/`)
4. Apply migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Install ImageMagick and Ghostscript (if you want pdf preview to work)
 https://www.ghostscript.com/download/gsdnld.html
 http://www.imagemagick.org/script/download.php (NOTE:!! VERSION MUST BE SMALLER THAN 7.0.0!!)
7. Run server: `python3 manage.py runserver 8000`

## Development Notes
* Regenerate translation files: `django-admin makemessages -l de`
* Recompile translation files: `django-admin.py compilemessages`
