import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# -------------------------------------------------
# ------------------- PATHS ----------------------
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# -------------------------------------------------
# ------------- Variables de entorno --------------
# -------------------------------------------------

# Cargar variables de entorno desde un archivo .env
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)

# Guardar las variables de entorno en variables de Python
DATABASE_URL = os.getenv("DATABASE_URL")
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_RS256_PUBLIC_KEY = os.getenv("KEYCLOAK_RS256_PUBLIC_KEY")
DJ_PORT = os.getenv("DJ_PORT")
DJ_URL = os.getenv("DJ_URL")
<<<<<<< HEAD
=======
TESTING = os.getenv("TESTING")
>>>>>>> johis_dev

# Mostrar todas las variables de entorno (para depuración)
# expected_keys = [
#     "DATABASE_URL",
#     "KEYCLOAK_SERVER_URL",
#     "KEYCLOAK_REALM",
#     "KEYCLOAK_CLIENT_ID",
#     "KEYCLOAK_CLIENT_SECRET",
#     "KEYCLOAK_RS256_PUBLIC_KEY",
#     "DJ_PORT",
#     "DJ_URL",
# ]

# for key in expected_keys:
#     value = os.getenv(key)
#     print(f"{key}: {value}")

# -------------------------------------------------
# ------------------- SEGURIDAD -------------------
# -------------------------------------------------

# Clave secreta para la aplicación Django
SECRET_KEY = "django-insecure-)c$w1=-2dx9e&9^yi1tf*199nu(0d5yu2+0gpsak4d(%(8$2aq"

# Configuración de depuración (No debe estar habilitado en producción)
DEBUG = True

# Hosts permitidos
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "cms-web-mt3l.onrender.com",
]

# -------------------------------------------------
# ----------------- APLICACIONES ------------------
# -------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "appcms",
    "contenidos",
    "subcategorias",
<<<<<<< HEAD
] #
=======
]  #
>>>>>>> johis_dev

# -------------------------------------------------
# ----------------- MIDDLEWARES -------------------
# -------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "appcms.middleware.token_middleware.KeycloakTokenMiddleware",
]

# Configuración de URLs y WSGI
ROOT_URLCONF = "cmsweb.urls"
WSGI_APPLICATION = "cmsweb.wsgi.application"

# -------------------------------------------------
# ------------------- TEMPLATES -------------------
# -------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "appcms.context_processors.datos_basicos",
            ],
        },
    },
]

# -------------------------------------------------
# ---------------- STATIC FILES -------------------
# -------------------------------------------------

# Directorio donde se almacenarán los archivos estáticos
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Directorio donde se almacenan los archivos estáticos recolectados para producción
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Configuración de archivos multimedia
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# -------------------------------------------------
# ---------------- AUTHENTICATION -----------------
# -------------------------------------------------

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# -------------------------------------------------
# ------------------- DATABASES -------------------
# -------------------------------------------------

# Dependiendo del entorno, puede elegir una de las configuraciones de base de datos
# Descomente la configuración apropiada según sea necesario

# PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
#     }
# }

# PostgreSQL desde URL
DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}

# SQLite en memoria (para pruebas)
<<<<<<< HEAD
#DATABASES = {
 #  'default': {
 #      'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': ':memory:',
#   }
#}
=======
# DATABASES = {
#  'default': {
#      'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': ':memory:',
#   }
# }
>>>>>>> johis_dev

# SQLite archivo local
# DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': 'db.sqlite3',
#   }
# }

# -------------------------------------------------
# ----------------- PASSWORD VALIDATORS -----------
# -------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------------------------
# ---------------- INTERNATIONALIZATION -----------
# -------------------------------------------------

LANGUAGE_CODE = "es"
TIME_ZONE = 'America/Asuncion'  # O la zona horaria correcta para tu ubicación
USE_TZ = True  # Asegúrate de que esté habilitado el uso de zonas horarias
USE_I18N = True


# -------------------------------------------------
# --------------- OTRAS CONFIGURACIONES------------
# -------------------------------------------------

# Tipo de dato predeterminado para los id de los modelos
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
<<<<<<< HEAD

# Configuración para enviar correos electrónicos a través de Gmail
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
=======
>>>>>>> johis_dev
