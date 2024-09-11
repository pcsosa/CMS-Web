from keycloak import KeycloakOpenID, KeycloakOpenIDConnection
from keycloak import KeycloakAdmin
from keycloak import KeycloakUMA
from django.conf import settings
from dotenv import load_dotenv
import os, json
load_dotenv()

class KeycloakService:
  
  _instance = None

  def __init__(self):
    self.openid = KeycloakOpenID(
      server_url=settings.KEYCLOAK_SERVER_URL,
      client_id=settings.KEYCLOAK_CLIENT_ID,
      realm_name=settings.KEYCLOAK_REALM,
      client_secret_key=settings.KEYCLOAK_CLIENT_SECRET
    )
    self.admin = KeycloakAdmin(
      server_url=settings.KEYCLOAK_SERVER_URL,
      username="dios",
      password="dios",
      realm_name=settings.KEYCLOAK_REALM,
      user_realm_name="master"
    )
    
  @classmethod
  def get_instance(cls):
      if cls._instance is None:
          cls._instance = KeycloakService()
      return cls._instance

  def get_token(self, code):
    redirect_uri = os.getenv('DJ_URL') + ':' + os.getenv('DJ_PORT') + '/callback/'
    token = self.openid.token(
        code = code,
        redirect_uri = redirect_uri,
        grant_type = 'authorization_code'
    )
    return token
  
  def get_userId(self, token):
    user_info = self.openid.userinfo(token['access_token'])
    return user_info.get('sub')
  
  def isActive(self, token):
    return self.openid.introspect(token).get('active')
    
  def renovarToken(self, token):
    return self.openid.refresh_token(token['refresh_token'])
  
  def get_permisos(self, token):
    return self.openid.uma_permissions(token['access_token'])
  
  def tienePermiso(self, token, permiso):
    permisos = json.dumps(self.get_permisos(token), indent=2)
    print("PERMISOS: ", permisos)
    
    missing = self.openid.has_uma_access(token['access_token'], permiso).missing_permissions
    print("MISSING: ", missing)
    return self.openid.has_uma_access(token['access_token'], permiso).is_authorized