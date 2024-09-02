from dotenv import load_dotenv
import os
from pathlib import Path
import dj_database_url
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
load_dotenv()

KEYCLOAK_SERVER_URL = "https://keycloak-production-63af.up.railway.app/auth"
KEYCLOAK_REALM = "cmsweb"
KEYCLOAK_CLIENT_ID = "cmsweb"
KEYCLOAK_CLIENT_SECRET = "0zVx5AbaO6fLkn9YH5N1qdFeyl95ctoU"
KEYCLOAK_WELL_KNOWN = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration"

OAUTH2_CLIENT_CONFIG = {
    "client_id": KEYCLOAK_CLIENT_ID,
    "client_secret": KEYCLOAK_CLIENT_SECRET,
    "authorize_url": f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth",
    "access_token_url": f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
    "refresh_token_url": f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
    "base_url": f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect",
}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR,"templates")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)c$w1=-2dx9e&9^yi1tf*199nu(0d5yu2+0gpsak4d(%(8$2aq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appcms',
    'subcategorias',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware"
]

SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "keycloak",
                "name": "Keycloak",
                "client_id": "cmsweb",
                "secret": "0zVx5AbaO6fLkn9YH5N1qdFeyl95ctoU",
                "settings": {
                    "server_url": "https://keycloak-production-63af.up.railway.app/realms/cmsweb/.well-known/openid-configuration",
                },
            }
        ]
    }
}

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'cms-web-mt3l.onrender.com',
]

ROOT_URLCONF = 'cmsweb.urls'

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
                'django.template.context_processors.request'
            ],
        },
    },
]

# Directorio donde se almacenarán los archivos estáticos
STATIC_URL = '/static/'

# Directorio en tu sistema de archivos donde se recogerán los archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Directorio donde se almacenan los archivos estáticos recolectados para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'appcms.auth_backends.KeycloakBackend',
    
]


WSGI_APPLICATION = 'cmsweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('DB_NAME'),  # Nombre de la base de datos en PostgreSQL
#        'USER': os.getenv('DB_USER'),                  # Usuario de PostgreSQL
#        'PASSWORD': os.getenv('DB_PASSWORD'),           # Contraseña del usuario
#        'HOST': os.getenv('DB_HOST'),                   # O la IP del servidor si está en otra máquina
#        'PORT': os.getenv('DB_PORT'),                        # Puerto por defecto para PostgreSQL
#    }
#}

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))   
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': ':memory:',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_ON_GET = True

SESSION_COOKIE_AGE = 1200  # Tiempo en segundos, por ejemplo 20 minutos
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
