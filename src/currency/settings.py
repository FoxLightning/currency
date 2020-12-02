import os

from celery.schedules import crontab


if os.environ.get('CACHE_APP', 'memcached') == 'memcached':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'memcached:11211',
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
            "KEY_PREFIX": "example"
        }
    }

SITE_ID = 1

# EMAIL SETTINGS
EMAIL_HOST_USER = 'battlefieldblo@gmail.com'
EMAIL_HOST_PASSWORD = '7494496asdfAA1'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('SERVER', 'dev') == 'dev'

ALLOWED_HOSTS = ['*']


# Application definition

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # extensions
    # dev
    'debug_toolbar',
    'django_extensions',
    # prodaction
    'crispy_forms',
    'rest_framework',
    'drf_yasg',

    # extension registration
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',

    # apps
    'account',
    'rate',
]

LOGIN_REDIRECT_URL = '/'

# for extension authentification
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'currency.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

# for extension authentification
# Provider specific settings
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': '654'
#         }
#     }
# }

WSGI_APPLICATION = 'currency.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# SQLite database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ['POSTGRES_DB'],
#         'USER': os.environ['POSTGRES_USER'],
#         'PASSWORD': os.environ['POSTGRES_PASSWORD'],
#         'HOST': 'postgres',
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_content')


# STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static_content', 'static')
STATIC_ROOT = os.path.join('/tmp', 'static_content', 'static')


AUTH_USER_MODEL = 'account.User'

# django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Celery
CELERY_BROKER_URL = 'amqp://{0}:{1}@rabbitmq:5672//'.format(
    os.environ.get('RABBITMQ_DEFAULT_USER', 'guest'),
    os.environ.get('RABBITMQ_DEFAULT_PASS', 'guest'),
)

PERIOD = '*/15'
CELERY_BEAT_SCHEDULE = {
    'parse1': {
        'task': 'rate.tasks.parse_privatbank',
        'schedule': crontab(minute=PERIOD),
    },
    'parse2': {
        'task': 'rate.tasks.parse_monobank',
        'schedule': crontab(minute=PERIOD),
    },
    'parse3': {
        'task': 'rate.tasks.parse_vkurse',
        'schedule': crontab(minute=PERIOD),
    },
    # 'parse4': {
    #     'task': 'rate.tasks.parse_fixer',
    #     'schedule': crontab(minute='*/45'),  # free version hes a limit of 1000 request per manth
    # },
    'parse5': {
        'task': 'rate.tasks.parse_oschadbank',
        'schedule': crontab(minute=PERIOD),
    },
    'parse6': {
        'task': 'rate.tasks.parse_prostobank',
        'schedule': crontab(minute=PERIOD),
    },
    'parse7': {
        'task': 'rate.tasks.parse_minfin',
        'schedule': crontab(minute=PERIOD),
    },
    'parse8': {
        'task': 'rate.tasks.parse_ukrgasbank',
        'schedule': crontab(minute=PERIOD),
    },
    'parse9': {
        'task': 'rate.tasks.parse_pumb',
        'schedule': crontab(minute=PERIOD),
    },
    'parse10': {
        'task': 'rate.tasks.parse_pravex',
        'schedule': crontab(minute=PERIOD),
    },
    'parse11': {
        'task': 'rate.tasks.parse_alpha',
        'schedule': crontab(minute=PERIOD),
    },
    'send_xml_to_all_async': {
        'task': 'rate.tasks.send_xml_to_all_async',
        'schedule': crontab(minute=PERIOD)
    }
}


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'example@ex.com'
    DOMAIN = 'http://localhost:8000'

    # debug tool_bar
    import socket
    DEBUG_TOOLBAR_PATCH_SETTINGS = True
    INTERNAL_IPS = ['127.0.0.1']

    # tricks to have debug toolbar when developing with docker
    ip = socket.gethostbyname(socket.gethostname())
    ip = '.'.join(ip.split('.')[:-1])
    ip = f'{ip}.1'
    INTERNAL_IPS.append(ip)
else:
    # for rabitmq in pytest
    CELERY_TASK_ALWAYS_EAGER = True


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
