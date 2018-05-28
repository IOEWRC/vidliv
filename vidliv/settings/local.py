import os

from decouple import config, Csv

from django.conf import settings

DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {  # set ENV `DATABASE_NAME' to `postgresql' to use otherwise it will use default sqllite3
    # replace with your own database credential
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
    } if config('DATABASE_NAME') == 'postgresql' else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(settings.BASE_DIR, 'db.sqlite3'),
    }
}

# EMAIL backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# for media files
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

SECRET_KEY = config('SECRET_KEY')
