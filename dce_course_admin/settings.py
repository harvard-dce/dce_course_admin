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

ADMINS = ((env('DJANGO_ADMIN_NAME'), env('DJANGO_ADMIN_EMAIL')),)

# depends on DATABASE_URL being set in your env. See https://github.com/kennethreitz/dj-database-url
# you can also set DJANGO_DATABASE_DEFAULT_ENGINE if you want to override the
# default engine, e.g., using https://github.com/kennethreitz/django-postgrespool/
DATABASES = {
    'default': dj_database_url.config(engine=env('DJANGO_DATABASE_DEFAULT_ENGINE', None))
}

LTI_OAUTH_CREDENTIALS = {
    env('LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY'): env('LTI_OAUTH_COURSE_ADMIN_CONSUMER_SECRET')
}

LTI_APP_DEVELOPER_KEYS = {
    # These values must be obtained by registering the LTI app with the canvas instance
    # See: <instance_base_url>/developer_keys
    env('LTI_OAUTH_COURSE_ADMIN_CONSUMER_KEY'): {
        'client_id': env('CANVAS_DEVELOPER_KEY_CLIENT_ID'),
        'client_secret': env('CANVAS_DEVELOPER_KEY_CLIENT_SECRET')
    }
}

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
        'console':{
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
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
