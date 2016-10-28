"""
Global settings for Numbles.
"""

import os

# Determine if the application is running in DEBUG mode - assume it isn't
DEBUG = bool(os.environ.get('DEBUG', False))

#################
# Core Settings #
#################

# A secret key MUST be provided when not running in debug mode. The blank
# default below will trigger a runtime error
SECRET_KEY = os.environ.get('SECRET_KEY', 'DEBUG' if DEBUG else '')

# Retrieve the domain name for the site
SITE_DOMAIN = os.environ.get('SITE_DOMAIN', 'numbles')

# Ensure that the correct host is used
ALLOWED_HOSTS = [SITE_DOMAIN]
USE_X_FORWARDED_HOST = True

ROOT_URLCONF = 'numbles.urls'
WSGI_APPLICATION = 'numbles.wsgi.application'
LOGIN_REDIRECT_URL = 'home'

# Enable timezone-aware datetimes
USE_TZ = True
TIME_ZONE = 'UTC'  # the One True Timezone :)

################
# Applications #
################

INSTALLED_APPS = (
    # Core Django applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django helper applications
    'django_archive',
    # Numbles applications
    'numbles.accounts',
    'numbles.ledger',
)

################################
# Project and Data Directories #
################################

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# When running in debug mode, the data directory is one level up from this
# directory and when in production, it is /data.
if DEBUG:
    DATA_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), 'data')
else:
    DATA_ROOT = '/data'

# Ensure it exists
try:
    os.makedirs(DATA_ROOT)
except OSError as e:
    from errno import EEXIST
    if e.errno != EEXIST:
        raise

############
# Database #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('NUMBLES_DB_NAME', 'postgres'),
        'USER': os.environ.get('NUMBLES_DB_USER', 'postgres'),
        'HOST': os.environ.get('NUMBLES_DB_HOST', 'postgres'),
    },
}

#########
# Email #
#########

DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'Numbles <donotreply@%s>' % SITE_DOMAIN

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'pyhectane.django.HectaneBackend'
    HECTANE_HOST = os.environ.get('NUMBLES_EMAIL_HOST', 'hectane')

# Error messages
ADMIN_EMAIL = os.environ.get('SITE_ADMIN', None)
if ADMIN_EMAIL is not None:
    ADMINS = (
        ('Admin', 'nathan.osman@gmail.com'),
    )

#############
# Templates #
#############

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': (os.path.join(PROJECT_ROOT, 'jinja2'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'numbles.jinja2.environment',
            'extensions': ('jinja2.ext.do',),
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            os.path.join(PROJECT_ROOT, 'templates'),
        ),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            )
        },
    },
)

##########################
# Media (Uploaded Files) #
##########################

MEDIA_ROOT = os.path.join(DATA_ROOT, 'media')
MEDIA_URL = '/media/'

################
# Static Files #
################

# Provide an additional location to search for the static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATIC_ROOT = os.path.join(DATA_ROOT, 'static')
STATIC_URL = '/static/'

#######################
# Additional Settings #
#######################

# The list of middleware needs to be customized in order to activate timezones
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'numbles.middleware.TimezoneMiddleware',
)
