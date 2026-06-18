import os
from django.core.asgi import get_asgi_application
from django.urls import path

# 1. Configurar la variable de entorno antes de inicializar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuraciones.settings")

# 2. Inicializar la aplicación ASGI de Django (carga modelos y apps)
django_asgi_app = get_asgi_application()

# 3. Importaciones diferidas (Debe ir después de get_asgi_application)
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402

from apps.citaciones.ws import ColaConsumer, DashboardConsumer  # noqa: E402
from apps.notificaciones.ws import NotifConsumer  # noqa: E402

# 4. Enrutamiento de WebSockets (Mantenlo limpio metiéndolo en una variable)
websocket_urlpatterns = [
    path("ws/notifs/", NotifConsumer.as_asgi()),
    path("ws/cola/", ColaConsumer.as_asgi()),
    path("ws/dashboard/", DashboardConsumer.as_asgi()),
]

# 5. Aplicación principal ASGI
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(websocket_urlpatterns),
})   