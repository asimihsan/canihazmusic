# Django settings for canihazmusic project.

import os

#   File path constants.
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# -----------------------------------------------------------------------------
#   Development and Heroku production databases.
# -----------------------------------------------------------------------------
DATABASES = {"default": {}}
if bool(os.environ.get('CANIHAZMUSIC_DEVELOPMENT', False)):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(PROJECT_DIR, "database.sqlite3"),  # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
# -----------------------------------------------------------------------------

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, "staticfiles")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kl9*y-&amp;s)knf&amp;uyf-bw95li3z_e=ne&amp;@-w^x1f*#py@y9id8)#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.utilities.middleware.CommonVariablesMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'canihazmusic.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'canihazmusic.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # My apps.
    'apps.landing',
    'apps.updates',
    'apps.search',
    'apps.settings',

    # Third party apps
    'gunicorn',
    'debug_toolbar',
    'south',
    'kombu.transport.django',
    'djcelery',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s - %(asctime)s - %(module)s - %(process)d - %(thread)d - %(message)s',
        },
        'simple': {
            'format': '%(asctime)s - %(name)s - %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
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
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    },
}

# ---------------------------------------------------------------------------
#   django-debug-toolbar settings.
# ---------------------------------------------------------------------------
INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
#   celery settings.
# ---------------------------------------------------------------------------
import djcelery
djcelery.setup_loader()

# Broker settings
BROKER_URL = os.environ.get("CLOUDAMQP_URL", "")

# List of modules to import when celery starts.
CELERY_IMPORTS = ("apps.search.tasks", )

# Use the database to store task state and results.
# CELERY_RESULT_DBURI = r"sqlite://database.sqlite3"
# CELERY_RESULT_DBRI = r"postgresql://username:password@localhost/mydatabase"

# CELERY_ANNOTATIONS = {"tasks.add": {"rate_limit": "10/s"}}

# Annotate all tasks
# CELERY_ANNOTATIONS = {"*": {"rate_limit": "10/s"}}

# AMQP settings.
CELERY_RESULT_BACKEND = "amqp"
CELERY_RESULT_EXCHANGE = "celeryresults"
CELERY_RESULT_EXCHANGE_TYPE = "direct"
CELERY_RESULT_PERSISTENT = True
CELERY_TASK_RESULT_EXPIRES = 18000 # 5 hours
CELERY_MESSAGE_COMPRESSION = "bzip2"
# ---------------------------------------------------------------------------

