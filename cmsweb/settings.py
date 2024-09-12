import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
# middleware.py
from django.utils.deprecation import MiddlewareMixin
import requests

#-------------------------------------------------
#------------------- PATHS ----------------------
#-------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Cargar variables de entorno desde un archivo .env
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'), override=True)

# Mostrar todas las variables de entorno (incluyendo las del sistema)
# expected_keys = ['KEYCLOAK_RS256_PUBLIC_KEY', 'DJ_PORT', 'DJ_URL']
# for key in expected_keys:
#     value = os.getenv(key)
#     print(f"{key}: {value}")

#-------------------------------------------------
#------------------- SEGURIDAD -------------------
#-------------------------------------------------

# Clave secreta para la aplicación Django
SECRET_KEY = 'django-insecure-)c$w1=-2dx9e&9^yi1tf*199nu(0d5yu2+0gpsak4d(%(8$2aq'

# Configuración de depuración (No debe estar habilitado en producción)
DEBUG = True

# Hosts permitidos
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'cms-web-mt3l.onrender.com',
]

#-------------------------------------------------
#----------------- APLICACIONES ------------------
#-------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appcms',
    'contenidos',
    'subcategorias',
]

#-------------------------------------------------
#----------------- MIDDLEWARES -------------------
#-------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'appcms.middleware.token_middleware.KeycloakTokenMiddleware',
]

# Configuración de URLs y WSGI
ROOT_URLCONF = 'cmsweb.urls'
WSGI_APPLICATION = 'cmsweb.wsgi.application'

#-------------------------------------------------
#------------------- TEMPLATES -------------------
#-------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'appcms.context_processors.datos_basicos',
            ],
        }
    },
]

#-------------------------------------------------
#---------------- STATIC FILES -------------------
#-------------------------------------------------

# Directorio donde se almacenarán los archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Directorio donde se almacenan los archivos estáticos recolectados para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de archivos multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#-------------------------------------------------
#---------------- AUTHENTICATION -----------------
#-------------------------------------------------

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

KEYCLOAK_SERVER_URL = os.getenv('KEYCLOAK_SERVER_URL')
KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID')
KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM')
KEYCLOAK_CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET')
KEYCLOAK_RS256_PUBLIC_KEY = os.getenv('KEYCLOAK_RS256_PUBLIC_KEY')

#-------------------------------------------------
#------------------- DATABASES -------------------
#-------------------------------------------------

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
DATABASES = {
     'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}

# SQLite en memoria (para pruebas)
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': ':memory:',
#    }
# }

# SQLite archivo local
#DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': 'db.sqlite3',
#   }
#}

#-------------------------------------------------
#----------------- PASSWORD VALIDATORS -----------
#-------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

#-------------------------------------------------
#---------------- INTERNATIONALIZATION -----------
#-------------------------------------------------

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

#-------------------------------------------------
#--------------- OTRAS CONFIGURACIONES------------
#-------------------------------------------------

# Tipo de dato predeterminado para los id de los modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py <- Para guardar automáticamente el autor del contenido pero desde su cuenta
AUTHENTICATION_BACKENDS = [
    'keycloak_auth.backend.KeycloakOpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
]

KEYCLOAK_OIDC_PROFILE_MODEL = 'yourapp.YourCustomProfile'
KEYCLOAK_OIDC_ID_TOKEN = 'your_keycloak_id_token'
KEYCLOAK_OIDC_AUTHORIZATION = {
    'BEARER_TOKEN': 'your_bearer_token',
}

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


class KeycloakMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            token = token.replace('Bearer ', '')
            user_info = self.get_user_info_from_keycloak(token)
            request.user_info = user_info

    def get_user_info_from_keycloak(self, token):
        # URL de tu Keycloak para obtener información del usuario
        user_info_url = 'https://<your-keycloak-server>/auth/realms/<your-realm>/protocol/openid-connect/userinfo'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return {}

# Agregar middleware a tu configuración
# settings.py
MIDDLEWARE = [
    # ...
    'path.to.KeycloakMiddleware',
    # ...
]
