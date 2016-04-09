"""
WSGI config for kimeo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import subprocess

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kimeo.settings")

application = get_wsgi_application()


#proc = subprocess.Popen('python /home/pi/Desktop/Kimeo/kimeo/kimeo/src/main.py', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
proc = subprocess.call(['python', '/home/pi/Desktop/Kimeo/kimeo/kimeo/src/main.py'])
#ihm.launch();