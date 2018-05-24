import os

from decouple import config

from django.conf import settings

DEBUG = True
ALLOWED_HOSTS = []


DATABASES = {  # replace with your own database credential
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vidliv',
        'USER': 'forvidliv',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    } if config('DATABASE_POSTGRESQL') else {
        # set environment variable to `DATABASE_POSTGRESQL` to False
        # if you want to use default sqlite3
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(settings.BASE_DIR, 'db.sqlite3'),
    }
}

# EMAIL backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# for media files
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
