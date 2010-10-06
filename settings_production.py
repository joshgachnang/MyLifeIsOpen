# -*- coding: utf-8 -*-
from settings import *

DEBUG = TEMPLATE_DEBUG = False

POSTS_PER_PAGE = 25
AKISMET_API_KEY = 'your-key-here'

# These will rename the like and dislike buttons on each post/comment.
RENAME_LIKE = 'l33t'
RENAME_DISLIKE = 'n00b'

# For django-registration
ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

ADMINS = (
    ('YourName', 'YourEmailAddress'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/josh/programming/MyLifeIsOpen/sqlite3.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Chicago'

SECRET_KEY = 'idu7lmt&6y&em!*khslyb7s+xy*y6t34%8ml9(gk^f67*wl1dg'

SEND_BROKEN_LINK_EMAILS = True
