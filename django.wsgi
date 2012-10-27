#!/home/tools/python/bin/python
import os
import sys

path = '/home/tools/releases/ATM'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ATM.settings'
os.environ['MPLCONFIGDIR'] = '/tmp'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()