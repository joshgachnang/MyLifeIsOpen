from settings import *

DEBUG = TEMPLATE_DEBUG = False

# Custom Tags
POSTS_PER_PAGE = 25
AKISMET_API_KEY = 'your-key-here'

# These will rename the like and dislike buttons on each post/comment.
RENAME_LIKE_DISLIKE = 'l33t', 'n00b'

# For django-registration
ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_PORT = 587

SITE_TITLE = 'My Life Is Geek'

GOOGLE_ANALYTICS_KEY='ua-0000000-0'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
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
