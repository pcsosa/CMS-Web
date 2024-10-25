import re
import time
import unicodedata

import jwt
import requests
from django.conf import settings
from django.core.cache import cache

from appcms.services.keycloak_service import KeycloakService


# Obtener información del usuario a partir del user id
def obtenerUserInfoById(user_id):
    if settings.TESTING == "True":
        return {"id": 1, "username": "autor1"}

    kc = KeycloakService()
    user = kc.admin.get_user(user_id)
    return user


def obtenerUserInfo(token):
    if not token:
        return None

    decoded_token = decode_token(token)

    user_info = {
        "email": decoded_token["email"],
        "name": decoded_token["name"],
        "preferred_username": decoded_token["preferred_username"],
        "given_name": decoded_token["given_name"],
        "family_name": decoded_token["family_name"],
    }

    return user_info


def obtenerToken(request):
    token = cache.get("access_token")
    if not token:
        print("Token obtenido de la sesión")
        token = request.session.get("access_token")
        cache.set("access_token", token, timeout=300)
    return token


def tienePermiso(token, resource, scopes_to_check):
    if not token:
        return {scope: False for scope in scopes_to_check}

    decoded_token = decode_token(token)
    authorization = decoded_token["authorization"]
    permissions = authorization["permissions"]
    results = {}

    for scope_to_check in scopes_to_check:
        has_permission = False
        for permission in permissions:
            if (
                permission["rsname"] == resource
                and scope_to_check in permission["scopes"]
            ):
                has_permission = True
                break
        results[scope_to_check] = has_permission

    return results


def obtenerRPT(token):
    if not token:
        return None

    host = settings.KEYCLOAK_SERVER_URL
    realm = settings.KEYCLOAK_REALM
    client_id = settings.KEYCLOAK_CLIENT_ID
    endpoint = f"{host}/realms/{realm}/protocol/openid-connect/token"

    # Crear el payload para la solicitud de RPT
    payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
        "audience": client_id,
    }

    # Crear el encabezado de la solicitud
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Realizar la solicitud de RPT
    response = requests.post(endpoint, data=payload, headers=headers)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "No se pudo obtener el RPT"}


def obtenerUsersConRol(rol):
    kc = KeycloakService()
    users = kc.admin.get_realm_role_members(rol)

    # Usar comprensión de lista para extraer solo los campos 'id' y 'username'
    filtered_data = [{"id": user["id"], "username": user["username"]} for user in users]

    return filtered_data


def obtenerUserId(token):
    if not token:
        return None
    payload = decode_token(token)
    return payload.get("sub")
    # return payload["sub"]


def decode_token(token, audience="cmsweb", verify_exp=True):
    public_key = settings.KEYCLOAK_RS256_PUBLIC_KEY
    public_key = re.sub(r"\\n", "\n", public_key)
    # Decodifica sin validar la audiencia para inspeccionarla
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        options={"verify_exp": verify_exp, "verify_aud": False},
    )
    print("Audiencia encontrada en el token:", payload.get("aud"))

    # Ahora valida la audiencia correcta
    return jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=audience,
        options={"verify_exp": verify_exp},
    )


def expiroToken(token):
    if not token:
        return None
    decoded_token = decode_token(token, verify_exp=False)
    return decoded_token["exp"] < time.time()


def comprobarToken(request, token):
    if not token:
        return None

    if not expiroToken(token):
        return token

    kc = KeycloakService.get_instance()

    refresh_token = cache.get("refresh_token")
    if not refresh_token:
        refresh_token = request.session.get("refresh_token")
        cache.set("refresh_token", refresh_token, timeout=1800)

    newToken = kc.renovarToken(refresh_token)
    newToken = obtenerRPT(newToken["access_token"])
    request.session["access_token"] = newToken["access_token"]
    cache.set("access_token", newToken["access_token"], timeout=300)

    print("TOKEN RENOVADO")
    return newToken["access_token"]


def obtenerRolesUser(token):
    decoded_token = decode_token(token)
    roles = decoded_token["realm_access"].get("roles", [])

    roles = [
        rol
        for rol in roles
        if "default-roles-cmsweb" not in rol
        and "offline_access" not in rol
        and "uma_authorization" not in rol
    ]

    return roles


def quitar_acentos(texto):
    """
    Elimina los acentos de un texto.

    Este método normaliza el texto en forma NFD y filtra los caracteres con acentos.

    :param texto: El texto al que se le quitarán los acentos.
    :type texto: str
    :return: El texto sin acentos.
    :rtype: str
    """
    if texto is None:
        return ""
    texto_normalizado = unicodedata.normalize("NFD", texto)
    texto_sin_acentos = "".join(
        char for char in texto_normalizado if unicodedata.category(char) != "Mn"
    )
    return texto_sin_acentos
