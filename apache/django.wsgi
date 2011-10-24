import os
import sys

paths = ['/var/lib', '/var/lib/sistema']

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

