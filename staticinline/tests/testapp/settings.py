import logging.config
import os

DEBUG = True

SECRET_KEY = "super-secret-staticinline-testing-key"

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

INSTALLED_APPS = [
    'staticinline.tests.testapp.apps.CustomizedStaticInlineAppConfig',
    'staticinline.tests.testapp',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',)
MIDDLEWARE = MIDDLEWARE_CLASSES

STATIC_ROOT = '/tmp/test-staticinline-static-root/'
STATIC_URL = '/static/'
# ROOT_URLCONF = 'staticinline.tests.testapp.urls'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            }
        },
        'loggers': {
            '': {
                'level': os.environ.get('LOG_LEVEL', 'ERROR').upper(),
                'handlers': ['console'],
            }
        },
    }
)
