"""
WSGI config for webmodels project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import posixpath

fweb_path = posixpath.split(os.path.abspath(__file__))[0]
fweb_uppath = posixpath.abspath(posixpath.join(fweb_path, '..'))

sys.path.append(fweb_path)
sys.path.append(fweb_uppath)

os.chdir(fweb_uppath)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webmodels.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
