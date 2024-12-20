# dj_rest/core/asgi.py

import os
from django.core.asgi import get_asgi_application
from fastapi.middleware.wsgi import WSGIMiddleware
from fa import fst_app as fa_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')

django_asgi_app = get_asgi_application()

application = WSGIMiddleware(django_asgi_app)
application.mount("/api", fa_app)
