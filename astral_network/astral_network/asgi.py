"""
ASGI config for astral_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astral_network.settings')

import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from messenger.routing import websocket_urlpatterns


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    'http': ASGIStaticFilesHandler(django_asgi_app),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})