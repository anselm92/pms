from pms.settings.celery import app as cel_app
from pms.settings.local_settings import *
import os

# Note: do not remove this, it makes sure the import is not deleted and thus celery starts
cel_app

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = '%s/../' % os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'pms',
    'printing',
    'printing_2d',
    'printing_3d',
    'bootstrap3',
    'captcha',
    'rest_framework',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'pms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pms.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'de-DE'

from django.utils.translation import ugettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('de', _('German')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

INTERNAL_IPS = ['127.0.0.1']

LOGIN_REDIRECT_URL = '/'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

RECAPTCHA_PUBLIC_KEY = '6Lc_mS8UAAAAAEcdteSObFe2tMDxHI5wWE8kBMJZ'
RECAPTCHA_PRIVATE_KEY = '6Lc_mS8UAAAAACDQD4g5mtvByRoUHQbXXL-aBiNe'
NOCAPTCHA = True
RECAPTCHA_TESTING = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = 'mail.bwk-technik.de'
# Port for sending e-mail.
EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = 'PMS <test@bwk-technik.de>'

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'testbwk@bwk-technik.de'
EMAIL_HOST_PASSWORD = '3jfk6dCCGT75fHVFdd9987'  # remove last letter
EMAIL_USE_TLS = True

SITE = "localhost:8000"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}