import os

from celery.schedules import crontab

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
SECRET_KEY = 'c+34d(_=o-^q!8u(+1glra2b)re*9v6rys85#8trgt$w28akui'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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

    'debug_toolbar',
    'django_extensions',

    'rate',
]

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
            ],
        },
    },
]

WSGI_APPLICATION = 'currency.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Celery
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_BEAT_SCHEDULE = {
    'parse1': {
        'task': 'rate.tasks.parse_privatbank',
        'schedule': crontab(minute='*/1'),
    },
    'parse2': {
        'task': 'rate.tasks.parse_monobank',
        'schedule': crontab(minute='*/1'),
    },
    'parse3': {
        'task': 'rate.tasks.parse_vkurse',
        'schedule': crontab(minute='*/1'),
    },
    'parse4': {
        'task': 'rate.tasks.parse_fixer',
        'schedule': crontab(minute='*/45'),  # free version hes a limit of 1000 request per manth
    },
    'parse5': {
        'task': 'rate.tasks.parse_oschadbank',
        'schedule': crontab(minute='*/1'),
    },
    'parse6': {
        'task': 'rate.tasks.parse_prostobank',
        'schedule': crontab(minute='*/1'),
    },
    'parse7': {
        'task': 'rate.tasks.parse_minfin',
        'schedule': crontab(minute='*/1'),
    },
    'parse8': {
        'task': 'rate.tasks.parse_ukrgasbank',
        'schedule': crontab(minute='*/1'),
    },
    'parse9': {
        'task': 'rate.tasks.parse_pumb',
        'schedule': crontab(minute='*/1'),
    },
    'parse10': {
        'task': 'rate.tasks.parse_pravex',
        'schedule': crontab(minute='*/1'),
    },
    'parse11': {
        'task': 'rate.tasks.parse_alpha',
        'schedule': crontab(minute='*/1'),
    },
}
