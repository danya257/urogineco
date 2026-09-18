"""
Passenger WSGI entry for urogineco on Beget.
Beget's PassengerAppRoot points to public_html/HelloDjango/HelloDjango/
sys.path adds the parent HelloDjango/ so 'urogineco' and 'core' are importable.
"""

import os
import sys

SITE_ROOT = '/home/d/drgvozkc/drgvozkc.beget.tech/public_html'
PROJECT_DIR = SITE_ROOT + '/HelloDjango'
VENV_PACKAGES = SITE_ROOT + '/venv/lib/python3.11/site-packages'

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)
if VENV_PACKAGES not in sys.path:
    sys.path.insert(1, VENV_PACKAGES)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urogineco.settings')

from django.core.wsgi import get_wsgi_application  # noqa: E402
application = get_wsgi_application()
