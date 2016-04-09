"""
WSGI config for kimeo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
#import IHM.src.main as ihm
import subprocess

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kimeo.settings")

application = get_wsgi_application()


proc = subprocess.Popen('./../IHM/src/main.py', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
#ihm.launch();