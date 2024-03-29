DEBUG = True

SECRET_KEY = "super-secret-staticinline-testing-key"  # noqa: S105 Possible hardcoded password:

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

USE_TZ = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

INSTALLED_APPS = [
    "staticinline.tests.testapp.apps.CustomizedStaticInlineAppConfig",
    "staticinline.tests.testapp",
    "django.contrib.staticfiles",
]

MIDDLEWARE_CLASSES = ("django.middleware.common.CommonMiddleware",)
MIDDLEWARE = MIDDLEWARE_CLASSES

STATIC_ROOT = "/tmp/test-staticinline-static-root/"  # noqa: S108 Probable insecure usage of temporary file
STATIC_URL = "/static/"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
