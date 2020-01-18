"""
Django project settings.
"""

import os
import sys


def gettext(s):
    return s


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))

BACKEND_DIR = os.path.realpath(os.path.join(BASE_DIR, 'backend'))
FRONTEND_DIR = os.path.realpath(os.path.join(BASE_DIR, 'frontend'))

APPS_DIR = os.path.realpath(os.path.join(BACKEND_DIR, 'apps'))
sys.path.append(APPS_DIR)

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# By default, do not include the debug toolbar (True in development settings)
DEBUG_TOOLBAR = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'


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


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BACKEND_DIR, 'db.sqlite3'),
    }
}


# Password validation

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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Translations

LANGUAGES = (
    # Customize this
    ('en', gettext('English')),
)

# Logging

LOGS_ROOT = os.path.realpath(os.path.join(BACKEND_DIR, 'logs'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_format': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file_format': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_format',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_ROOT, 'django.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15 MB
            'backupCount': 10,
            'formatter': 'file_format',
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'apps': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'werkzeug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# Static files (CSS, JavaScript, Images)

STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')

# Prefix added to static resources (the first '/' is important to allow the development server to build correct url)
STATIC_URL = STATIC_HOST + '/static/'

# Directory where Django static files are collected
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# List of directory were to find static assets
STATICFILES_DIRS = [
    os.path.join(BACKEND_DIR, 'build'),
    os.path.join(FRONTEND_DIR, 'build', 'static'),
]

# Webpack output location containing Vue index.html file (outputDir)
# Adds the Webpack build directory to Django's template paths so Django
# can find the production index.html Vue template
TEMPLATES[0]['DIRS'] += [
    os.path.join(STATIC_ROOT, 'frontend'),
]
