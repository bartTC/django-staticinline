DEBUG = True

SECRET_KEY = "super-secret-staticinline-testing-key"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
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
            ],
        },
    },
]

INSTALLED_APPS = [
    'staticinline',
    'staticinline.tests.testapp',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)
MIDDLEWARE = MIDDLEWARE_CLASSES

STATIC_ROOT = '/tmp/test-staticinline-static-root/'
STATIC_URL = '/static/'
ROOT_URLCONF = 'staticinline.tests.testapp.urls'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

