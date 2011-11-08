import os
import sys

sys.path.append('/var/lib')
sys.path.append('/var/lib/nara')

os.environ['DJANGO_SETTINGS_MODULE'] = 'nara.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


