from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


with open('/etc/project_var.txt') as f:
    var_list = f.read().split('\n')
    DSN_KEY = var_list[0].strip() 
    SECRET_KEY = var_list[1].strip()
    DB_NAME = var_list[3].strip()
    DB_USER = var_list[4].strip()
    DB_PASS = var_list[5].strip()
    HOST = var_list[2].strip()
    DJANGO_SETTINGS_MODULE = var_list[6].strip()
    EMAIL_USER = var_list[7].strip()
    EMAIL_PASSWORD = var_list[8].strip()

sentry_sdk.init(
    dsn=DSN_KEY,
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

DEBUG = False
ALLOWED_HOSTS = [HOST,]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': 'localhost',
        'PORT': '5432',
 	'OPTIONS': {
	    'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    }
}

EMAIL_HOST_USER = EMAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
SERVER_EMAIL = EMAIL_USER
