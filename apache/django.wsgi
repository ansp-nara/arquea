import os
import sys

paths = ['/var/lib', '/var/lib/sistema']
#paths = ['/var/lib/sistema']

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema.settings'
os.environ['APP_ENV'] = 'prod'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

