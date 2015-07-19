"""
Global settings for Numbles.
"""

# Determine the directory this file resides in so that an absolute path can be
# specified for the static files and templates
import os.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Numbles uses the Jinja2 template engine, which is similar to Django templates
# but offers more flexibility - but we still need Django templates for the admin
TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': (os.path.join(PROJECT_ROOT, 'jinja2'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'numbles.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ),
        },
    },
)

# Include site-wide static files
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)

# Enable timezones (each user can specify a timezone)
USE_TZ = True
TIME_ZONE = 'UTC'

ROOT_URLCONF = 'numbles.urls'
WSGI_APPLICATION = 'numbles.wsgi.application'

# After login, redirect to the home page
LOGIN_REDIRECT_URL = 'home'

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
