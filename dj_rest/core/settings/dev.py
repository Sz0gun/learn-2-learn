# dj_rest/core/settings/dev.py
from .base import *
from shared.settings import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.PSQL_DB_DEV,
        'USER': config.PSQL_USER_DEV,
        'PASSWORD': config.PSQL_PASSWORD_DEV,
        'HOST': config.PSQL_HOST_DEV,
        'PORT': config.PSQL_PORT_DEV,
        'TEST': {
            'NAME': 'test_l2l_db',
        }
    }
}


