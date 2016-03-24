"""
Django settings for dce_course_admin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from getenv import env

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djrill',
    'canvas_api_token',
    'course_admin'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_auth_lti.middleware.LTIAuthMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'dce_course_admin.urls'

WSGI_APPLICATION = 'dce_course_admin.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django_auth_lti.backends.LTIAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = 'static_root'
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'course_admin/static'), )

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'course_admin/templates'),
)

LTI_APPS = {
    'course_admin': {
        'id': 'course_admin',
        'name': 'DCE Course Admin',
        'menu_title': 'DCE Course Admin',
        'extensions_provider': 'canvas.instructure.com',
        'description': "Provides account course listing with additional information and adminstrative controls.",
        'privacy_level': 'public'
    }
}

SECRET_KEY = env('DJANGO_SECRET_KEY', required=True)

# this tells django who to send app error emails to
ADMINS = ((env('DJANGO_ADMIN_NAME'), env('DJANGO_ADMIN_EMAIL')),)

# From: addr of the app error emails
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', 'root@localhost')

# use sparkpost to send app error emails
EMAIL_HOST = 'smtp.sparkpostmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'SMTP_Injection'
EMAIL_HOST_PASSWORD = env('SPARKPOST_API_KEY')
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# depends on DATABASE_URL being set in your env. See https://github.com/kennethreitz/dj-database-url
# you can also set DJANGO_DATABASE_DEFAULT_ENGINE if you want to override the
# default engine, e.g., using https://github.com/kennethreitz/django-postgrespool/
DATABASES = {
    'default': dj_database_url.config(
        engine=env('DJANGO_DATABASE_DEFAULT_ENGINE', None))
}

REDIS_URL = env('REDIS_URL')

LTI_REQUEST_VALIDATOR = 'course_admin.validator.LTIRequestValidator'

LTI_OAUTH_CREDENTIALS = {
    env('LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY'): env(
        'LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET')
}

CURRENT_TERM_ID = env('CURRENT_TERM_ID')

# env() will automatically eval the env string value into native python
ENROLLMENT_TERMS = env('ENROLLMENT_TERMS', required=True)
if not isinstance(ENROLLMENT_TERMS, list):
    raise ImproperlyConfigured("eval of ENROLLMENT_TERMS failed; check syntax.")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'null': {
            "class": 'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console'],
            'level': "DEBUG",
        },
    }
}

