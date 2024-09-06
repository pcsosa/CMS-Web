from django.conf import settings
import jwt
from jwt import algorithms
import textwrap
from ..services.keycloak_service import KeycloakService
import json

def comprobarToken(request, token, kc):
    if not kc.isActive(token['access_token']):
      print("RENOVANDO TOKEN...")
      newToken = kc.renovarToken(token)
      request.session['token'] = newToken
      return newToken
    else:
      return token
    
def obtener_roles_desde_token(token):
  kc = KeycloakService()
  userId = kc.get_userId(token)
  roles = kc.admin.get_all_roles_of_user(userId)
  print("-----------------ROLES--------------")
  #  print(json.dumps(roles['realmMappings'], indent=2, ensure_ascii=False))
  role_names = [role['name'] for role in roles['realmMappings']]
  return role_names