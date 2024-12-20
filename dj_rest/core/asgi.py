import os
from django.core.asgi import get_asgi_application
from fastapi.middleware.wsgi import WSGIMiddleware
from fst_api.fst_api import app as fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_asgi_app = get_asgi_application()

application = WSGIMiddleware(django_asgi_app)
application.mount("/api", fastapi_app)
