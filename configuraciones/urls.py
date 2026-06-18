"""
URL configuration for configuraciones project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from apps.cuentas.views.login import login_view
from apps.cuentas.views.director_dashboard import director_dashboard
from apps.cuentas.views_dev import dev_404

urlpatterns = [
    # === Núcleo / Autenticación ===
    path("", login_view, name="home"),
    path("login/", login_view, name="login"),
    path("dashboard/director/", director_dashboard, name="director_dashboard"),
    path("admin/", admin.site.urls),

    # === API Global ===
    path("api/v1/", include("apps.api.urls")),

    # === Módulos del Sistema (Apps locales) ===
    path("auditoria/", include("apps.auditoria.urls", namespace="auditoria")),
    path("citaciones/", include("apps.citaciones.urls", namespace="citaciones")),
    path("cuentas/", include("apps.cuentas.urls", namespace="cuentas")),
    path("cursos/", include("apps.cursos.urls")),
    path("estudiantes/", include("apps.estudiantes.urls")),
    path("notifs/", include("apps.notificaciones.urls", namespace="notificaciones")),

    # === Entorno de Desarrollo ===
    path("dev/404/", dev_404, name="dev_404"),
]

# === Rutas de Debugging para WebSockets ===
if settings.DEBUG:
    from apps.citaciones.views_debug import ping_notifs, ping_cola, ping_dashboard
    
    urlpatterns += [
        path("debug/ws/notifs/", ping_notifs),
        path("debug/ws/cola/", ping_cola),
        path("debug/ws/dashboard/", ping_dashboard),
    ]

# === Manejadores de Errores Globales ===
handler403 = "apps.cuentas.views.errors.error_403"
handler404 = "apps.cuentas.handlers.error_404"