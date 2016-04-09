"""
WSGI config for kimeo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import kimeo.IHM.src.main as kimeo

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kimeo.settings")

application = get_wsgi_application()

kimeo.launch();