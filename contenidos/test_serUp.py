import os
import requests
from dotenv import load_dotenv

load_dotenv()

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_USERNAME = os.getenv("KEYCLOAK_USERNAME")
KEYCLOAK_PASSWORD = os.getenv("KEYCLOAK_PASSWORD")

# Verificar que las variables de entorno están cargadas correctamente
print(f'SERVER URL: {KEYCLOAK_SERVER_URL}')
print(f'REALM: {KEYCLOAK_REALM}')
print(f'CLIENT ID: {KEYCLOAK_CLIENT_ID}')
print(f'CLIENT SECRET: {KEYCLOAK_CLIENT_SECRET}')
print(f'USERNAME: {KEYCLOAK_USERNAME}')
print(f'PASSWORD: {KEYCLOAK_PASSWORD}')

def get_token():
    url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "username": KEYCLOAK_USERNAME,
        "password": KEYCLOAK_PASSWORD
    }
    response = requests.post(url, data=data)
    if response.status_code == 401:
        print(f'Error: {response.content}')
    response.raise_for_status()
    return response.json()['access_token']

try:
    token = get_token()
    print(f'Token de acceso: {token}')
except requests.exceptions.HTTPError as e:
    print(f'Error al obtener el token: {e}')
