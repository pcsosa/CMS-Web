# CMS Web

Content Management System hecho en Django.

## Requisitos

- Linux, MacOS o WSL
- Python 3+
- PostgreSQL

## Instalación

Clonar el repositorio.

```bash
  git clone https://github.com/pcsosa/CMS-Web.git
```

Navegar al directorio.

```bash
  cd CMS-Web
```

Crear entorno virtual.

```bash
  python3 -m venv .venv
```

Activar entorno virtual.

```bash
  source .venv/bin/activate
```

Instalar los requerimientos.

```bash
  pip install -r requirements.txt
```

Necesitas crear el archivo `.env` en la raiz del repositorio y agregar las siguientes variables

```
  DATABASE_URL = <url de la base de datos>
  KEYCLOAK_SERVER_URL = <url de keycloak>
  KEYCLOAK_REALM = <realm de keycloak>
  KEYCLOAK_CLIENT_ID = <id cliente keycloak>
  KEYCLOAK_CLIENT_SECRET = <client secret>
  # Clave publica RS256 de keycloak, debe estar exactamente con este formato, ejemplo:
  KEYCLOAK_RS256_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwpqPNXDOYhOf+2MT54g\n6+X/1J+jkKAT/QXn8Iqtef8aWGapDy1LsU0kCRmJq0dkDtcSpZC5jsRa1mgyx0C\nlQFo0cLlMGkD50ebNSPLF+OPbjNtHsh61/Xc/5BltGTl8TpUs4WxU0OuVnuF42S\nD9iwPjz2HtlpwnsveBV2topCmtgnYGVt8NyOQdaijigkPoDGkRZ7BQt5blI3eyh\nWLyRiSoalovM2eAkCJURd9/eR5fjZObPuUAHzYCaVrVE78L+25hmTwmrXKVjQPH\npUjC5ziM9rkG8juoTxSr/ClY3jrTWL6noEBkZ8YlUVKV60VabDPyUDKteDp+i36\nqIpzMFAwIDAQAB\n-----END PUBLIC KEY-----"
  DJ_URL = <django host>
  DJ_PORT = <puerto django>
  # Configuración para enviar correos electrónicos a través de Gmail
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = <email>
  EMAIL_HOST_PASSWORD = <password>
  TESTING = "False" # poner True si se hacen pruebas unitarias
```

Realizar las migraciones a la base de datos.

```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
```

Iniciar el servidor.

```bash
  python3 manage.py runserver
```

Para mas info en como instalar e iniciar postgresSQL y Keycloak mirar el archivo pasos detallados.txt
