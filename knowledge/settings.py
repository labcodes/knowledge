import os

import raven

from decouple import config

from django.urls import reverse_lazy

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config(
    'SECRET_KEY', cast=str, default='wmx4w0(boo)(ed9nm(9+%zhs$ixmzg@h(bwnpiid@#zn@n5m9-'
)

DEBUG = config('DEBUG', cast=bool, default=False)

LOGIN_REDIRECT_URL = reverse_lazy('links:list-links')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'links',
    'core',
    'api',

    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'raven.contrib.django.raven_compat',
    'tagging',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'knowledge.urls'

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

WSGI_APPLICATION = 'knowledge.wsgi.application'

DATABASE_URL = config('DATABASE_URL', cast=str, default='')

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=500)
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

LINKS_PER_PAGE = 20

# slack settings
SLACK_TOKEN = config('SLACK_TOKEN', cast=str)
SLACK_BOT_NAME = 'Cintia'
SLACK_CHANNEL_ID = '#links'
# end

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'knowledge@labcodes.com.br'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AUTHENTICATION_BACKENDS = ['core.backends.EmailBackend']

USE_SENTRY = config('USE_SENTRY', cast=bool, default=False)
if USE_SENTRY:
    RAVEN_CONFIG = {
        'dsn': config('SENTRY_DSN', cast=str),
        # If you are using git, you can also automatically configure the
        # release based on the git info.
        'release': raven.fetch_git_sha(BASE_DIR),
    }

# django_tagging settings
FORCE_LOWERCASE_TAGS = True
# end

# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
# end

# CORS HEADERS
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ORIGIN_ALLOW_ALL = True
# end

try:
    from .local_settings import * # noqa
except ImportError:
    pass


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        }
    }
}
