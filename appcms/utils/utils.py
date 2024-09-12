import unicodedata
from django.conf import settings
from django.http import HttpResponse
import jwt
import textwrap
from ..services.keycloak_service import KeycloakService
import json
import re

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
      print("RENOVANDO TOKEN...")
      newToken = kc.renovarToken(token)
      request.session['token'] = newToken
      return newToken
    else:
      print("TOKEN SIGUE ACTIVO")
      return token
    
def comprobarToken(request, token):
  if token:
    try:
      return obtenerTokenActivo(request, token)
    except Exception as e:
      return HttpResponse("Su inicio de sesión ha expirado, intente iniciar sesión de nuevo.")
  else:
    return HttpResponse("No se ha iniciado sesión.")
    
def obtener_roles_desde_token(token):
  kc = KeycloakService()
  userId = kc.get_userId(token)
  roles = kc.admin.get_all_roles_of_user(userId)
  # print("-----------------ROLES--------------")
  #  print(json.dumps(roles['realmMappings'], indent=2, ensure_ascii=False))
  role_names = [role['name'] for role in roles['realmMappings'] if role['name'] != 'default-roles-cmsweb']
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