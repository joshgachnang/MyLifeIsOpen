import sys
import os

sys.path.append('/var/www/example.com/MyLifeIsOpen/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings-production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

 
