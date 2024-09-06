from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin
from django.conf import settings
from dotenv import load_dotenv
import os
load_dotenv()

class KeycloakService:

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

  def get_token(self, code):
    redirect_uri = os.getenv('DJ_URL') + ':' + os.getenv('DJ_PORT') + '/callback/'
    token = self.openid.token(
        code = code,
        redirect_uri = redirect_uri,
        grant_type = 'authorization_code'
    )
    return token
  
  def get_userId(self, token):
    user_info = self.openid.userinfo(token)
    return user_info.get('sub')
  
  def isActive(self, token):
    return self.openid.introspect(token).get('active')
    
  def renovarToken(self, token):
    return self.openid.refresh_token(token['refresh_token'])
