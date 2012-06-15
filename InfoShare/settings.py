# -*- coding: utf-8 -*-
# Django settings for InfoShare project

import os.path
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SERVE_MEDIA = DEBUG

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = False

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("user", "user@host.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "postgresql_psycopg2", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "social",                       # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}


TIME_ZONE = "US/Eastern"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = False


MEDIA_ROOT = os.path.join(PROJECT_ROOT,"site_media","media")
STATIC_ROOT = ""

MEDIA_URL = "/media/"
STATIC_URL = "/static/"


# Additional directories which hold static files
STATICFILES_DIRS = [
   os.path.join(PROJECT_ROOT, "site_media","static"),
   os.path.join(PROJECT_ROOT, "site_media", "media"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = "cache"

# Make this unique, and don't share it with anybody.
SECRET_KEY = "tw4@z^*-ugnf@2vob4vtqbb)k9k!b1=5hm7n-7!wo66w#+!z&d"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "django.middleware.csrf.CsrfResponseMiddleware",
]

ROOT_URLCONF = "InfoShare.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.static",

    "pinax.core.context_processors.pinax_settings",
    "pinax.apps.account.context_processors.account",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",    
    "pinax.templatetags",
    
      
    # external
    "notification",
    "compressor",
    "debug_toolbar",
    "mailer",
    "django_openid",
    "timezones",
    "emailconfirmation",
    "announcements",
    "pagination",
    "idios",
    "metron",
    "django_forms_bootstrap", 
   
    # Pinax
    "pinax.apps.account",
    "pinax.apps.signup_codes",
    
    
    # project
    "profiles",
    "userpage",
    "friends",
    "messages",
    "avatar",
    "avatar_crop",
]

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

ABSOLUTE_URL_OVERRIDES = {                                                                                                                                                                   
     "auth.user": lambda o: "/profiles/profile/%s/" % o.username,                                                                                                                            
}                                                                                                                                                                                            
                                                                                                                                                                                             
AUTH_PROFILE_MODULE = "profiles.Profile"                                                                                                                                                     
NOTIFICATION_LANGUAGE_MODULE = "account.Account"  

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_BACKEND = "mailer.backend.DbBackend"

#AVATAR_STORAGE_DIR = os.path.join(PROJECT_ROOT, "site_media", "media","avatars")
FRIENDS_USE_NOTIFICATION_APP = True
SHOW_FRIENDS_OF_FRIEND = True
NOTIFY_ABOUT_NEW_FRIENDS_OF_FRIEND = True
NOTIFY_ABOUT_FRIENDS_REMOVAL = True
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = True
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = True

AUTHENTICATION_BACKENDS = [
    "pinax.apps.account.auth_backends.AuthenticationBackend",
]

LOGIN_URL = "/account/login/" 
LOGIN_REDIRECT_URLNAME = "home"
LOGOUT_REDIRECT_URLNAME = "home"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'informationsocialnetwork@gmail.com'
EMAIL_HOST_PASSWORD = '#password#'
EMAIL_PORT = 587


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
