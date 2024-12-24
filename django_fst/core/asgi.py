# dj_rest/core/asgi.py
import os
from django.core.asgi import get_asgi_application
from fastapi.middleware.wsgi import WSGIMiddleware
from fst_on_demand import fst_app as fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')

django_asgi_app = get_asgi_application()

# Combine Django and FastAPI
application = WSGIMiddleware(django_asgi_app)
application.mount("/api", fastapi_app)
