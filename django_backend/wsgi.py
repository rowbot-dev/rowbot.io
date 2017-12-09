"""
WSGI config for rowbot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import config

# get settings from config
settings_path = config.data['path'] if config.data is not None else 'settings.common' # default value

# setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_path)
application = get_wsgi_application()
