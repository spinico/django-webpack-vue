from .base import *

# SECURITY WARNING: don't run with debug turned on in production
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

# During testing Django forces DEBUG = False, DEBUG_TOOLBAR overrides it
DEBUG_TOOLBAR = DEBUG

# SECURITY WARNING: keep the secret key used in production secret
with open(BACKEND_DIR + '/settings/development.key') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# Because we are in development, we do not have our email set up, and so we cannot
# test the form. Luckily, Django provides a file-based email back end designed specifically
# for the purpose of assisting developers test emails without having to configure an email
# server first.
#
# You don’t need to create the maildump folder; Django will do that for you the first
# time you try to send an email. When you do try to send email, you will find this folder
# contains files named something like 20151009-100625-98201520.log. Inside this log
# file will be your complete message, including any mail headers and error messages. Very
# handy for testing.
#
# To get our email back end running, add the following to the end of your settings.py:
EMAIL_FILE_PATH = '../maildump'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# https://data-flair.training/blogs/django-caching/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

if DEBUG_TOOLBAR:
    # Debug Toolbar is shown only if your IP address is listed in the INTERNAL_IPS setting
    INTERNAL_IPS = ['127.0.0.1', '::1']
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += [
        # Debug Toolbar middleware must come after any other middleware that
        # encodes the response’s content, such as GZipMiddleware.
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
    # Tells the debug toolbar not to adjust your settings automatically
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_COLLAPSED': True,
        # To show/hide debug toolbar in development
        'SHOW_TOOLBAR_CALLBACK': lambda r: True,
    }

INSTALLED_APPS = [
    # 'livereload' and 'whitenoise.runserver_nostatic' must be set before 'django.contrib.staticfiles'
    'livereload',
    'whitenoise.runserver_nostatic',
] + INSTALLED_APPS + [
    'django_extensions',
]

MIDDLEWARE += [
    # Inject the livereload.js script into your webpages if DEBUG setting is on. (add at end of MIDDLEWARE)
    'livereload.middleware.LiveReloadScript',
]

try:
    from .local import *
except ImportError:
    pass
