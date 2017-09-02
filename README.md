# PMS - Printing Management System
The PMS is a web-based software which provides easy management of both 2d and 3d printing orders.

## Quickstart
1. Create virtual environment with Python 3.6 and don't forget to activate the environment.
2. Install requirements: `pip install -r requirements.txt`
3. Prepare settings
  * Copy `local_settings.py.sample` to `local_settings.py` (see `pms/settings/`)
  * Set local file directory, create directory and set folder permissions
4. Apply migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Install necessary software dependencies (for PDF previews)
  * ImageMagick: http://www.imagemagick.org/script/download.php (**Note**: Version must be **smaller** than 7.0.0!)
  * Ghostscript: https://www.ghostscript.com/download/gsdnld.html
7. Run server: `python3 manage.py runserver 8000`

## Development Notes
* Regenerate translation files: `django-admin makemessages -l de`
* Recompile translation files: `django-admin.py compilemessages`
