"""
Django settings for configuraciones project.
"""

import os
from pathlib import Path

# ==============================================================================
# 1. CONFIGURACIONES BASE Y ENTORNO
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DEBUG", "True") == "True"
SECRET_KEY = os.environ.get(
    "SECRET_KEY", 
    "django-insecure-if^n0ab85w_-8nsbz5!o^t=dk4%+ml^v&72vpez383d_ohdncf"
)

# ==============================================================================
# 2. SEGURIDAD Y RED
# ==============================================================================
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.0.14",
    "10.0.7.218",
]

# Si estás en Render, extraemos dinámicamente el dominio asignado
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Configuración CSRF segura para producción
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# Ajuste automático de cookies según el entorno (Seguras en producción)
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ==============================================================================
# 3. APLICACIONES E INFRAESTRUCTURA (Daphne / Channels)
# ==============================================================================
INSTALLED_APPS = [
    "daphne",  # Requerido arriba de todo para interceptar ASGI
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    # Apps de terceros
    "django_extensions",
    # Apps del proyecto (Agrupadas de manera limpia)
    "apps.cuentas.apps.CuentasConfig",
    "apps.cursos.apps.CursosConfig",
    "apps.estudiantes.apps.EstudiantesConfig",
    "apps.citaciones.apps.CitacionesConfig",
    "apps.notificaciones.apps.NotificacionesConfig",
    "apps.auditoria.apps.AuditoriaConfig",
]

WSGI_APPLICATION = "configuraciones.wsgi.application"
ASGI_APPLICATION = "configuraciones.asgi.application"

# Capa de canales para WebSockets
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# ==============================================================================
# 4. AUTENTICACIÓN Y MIDDLEWARE
# ==============================================================================
AUTH_USER_MODEL = "cuentas.Usuario"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/director/"
LOGOUT_REDIRECT_URL = "/login/"

AUTHENTICATION_BACKENDS = [
    "apps.cuentas.backends.CustomBackend",
    "django.contrib.auth.backends.ModelBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise justo después de Security
    "apps.cuentas.middleware.ThrottleLoginMiddleware",
    "apps.cuentas.middleware.CloseDBConnectionsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.cuentas.middleware.DisableClientCacheMiddleware",
    "apps.cuentas.middleware.AuthRequiredMiddleware",
    "apps.cuentas.middleware.LastOKURLMiddleware",
    "apps.auditoria.middleware.CurrentRequestMiddleware",
]

# ==============================================================================
# 5. RENDERIZADO DE TEMPLATES Y RUTAS
# ==============================================================================
ROOT_URLCONF = "configuraciones.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"] if os.path.isdir(BASE_DIR / "templates") else [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.notificaciones.context_processors.notificaciones_panel",
            ],
        },
    },
]

# ==============================================================================
# 6. BASE DE DATOS (Clever Cloud MySQL)
# ==============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "beu0hpduvweswzq20pvc"),
        "USER": os.environ.get("DB_USER", "uffjaj6pssk7gxuz"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "SNMfzxXMBbtDLKmHT5Y1"),
        "HOST": os.environ.get("DB_HOST", "beu0hpduvweswzq20pvc-mysql.services.clever-cloud.com"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "CONN_MAX_AGE": 60,  # Cambiado a 60 para reutilizar conexiones en producción
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "charset": "utf8mb4",
            "use_unicode": True,
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ==============================================================================
# 7. LOCALIZACIÓN Y ESTÁTICOS
# ==============================================================================
LANGUAGE_CODE = "es"
TIME_ZONE = "America/La_Paz"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Evita que falle de manera local si la carpeta 'static' raíz aún no se crea
STATICFILES_DIRS = [BASE_DIR / "static"] if os.path.isdir(BASE_DIR / "static") else []

# Almacenamiento optimizado para WhiteNoise en producción
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Validadores y otros
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]