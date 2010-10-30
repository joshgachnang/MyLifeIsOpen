import sys
import os

sys.path.append('/var/www/mylifeisgeek.com/dev/MyLifeIsOpen')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

 
