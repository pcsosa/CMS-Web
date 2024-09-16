import unicodedata
from django.conf import settings
from django.http import HttpResponse
import jwt
from ..services.keycloak_service import KeycloakService
import re
import time

def obtenerUsersConRol(rol):
    kc = KeycloakService()
    users = kc.admin.get_realm_role_members(rol)
    
    # Usar comprensión de lista para extraer solo los campos 'id' y 'username'
    filtered_data = [{'id': user['id'], 'username': user['username']} for user in users]
    
    return filtered_data

def obtenerUserId(token):
    if token is not None:
        payload = decode_token(token['access_token'])
        return payload['sub']
    else:
        return None

def decode_token(token):
    public_key = settings.KEYCLOAK_RS256_PUBLIC_KEY
    public_key = re.sub(r'\\n', '\n', public_key)
    return jwt.decode(token, public_key, algorithms=["RS256"], audience="account")

def obtenerTokenActivo(request, token):
    kc = KeycloakService.get_instance()
    if not kc.isActive(token['access_token']):
      newToken = kc.renovarToken(token)
      request.session['token'] = newToken
      print("TOKEN RENOVADO")
      return newToken
    else:
      print("TOKEN SIGUE ACTIVO")
      return token
    
def comprobarToken(request, token):
  if token:
      return obtenerTokenActivo(request, token)
    
def obtener_roles_desde_token(token):
    kc = KeycloakService.get_instance()
    
    # Medir tiempo para obtener userId
    user_id_start = time.time()
    userId = kc.get_userId(token)
    user_id_end = time.time()
    user_id_elapsed = user_id_end - user_id_start
    print(f"Tiempo tomado para obtener userId: {user_id_elapsed:.4f} segundos")
    
    # Medir tiempo para obtener roles
    roles_start = time.time()
    roles = kc.admin.get_all_roles_of_user(userId)
    roles_end = time.time()
    roles_elapsed = roles_end - roles_start
    print(f"Tiempo tomado para obtener roles: {roles_elapsed:.4f} segundos")
    
    # Medir tiempo para filtrar roles
    filter_roles_start = time.time()
    role_names = [role['name'] for role in roles['realmMappings'] if role['name'] != 'default-roles-cmsweb']
    filter_roles_end = time.time()
    filter_roles_elapsed = filter_roles_end - filter_roles_start
    print(f"Tiempo tomado para filtrar roles: {filter_roles_elapsed:.4f} segundos")
    
    return role_names

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
        return ''
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_acentos = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
    return texto_sin_acentos

