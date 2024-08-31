from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from keycloak import KeycloakOpenID

class KeycloakBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        KEYCLOAK_SERVER_URL = "http://localhost:8080/auth/"
        KEYCLOAK_REALM = "cmsweb"
        KEYCLOAK_CLIENT_ID = "cmsweb"
        KEYCLOAK_CLIENT_SECRET = "WdRVbq5nkzdHxVVSgAQqq5Ra0uhZfODS"
        KEYCLOAK_WELL_KNOWN = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration"

        keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_SERVER_URL,
                                         client_id=KEYCLOAK_CLIENT_ID,
                                         realm_name=KEYCLOAK_REALM,
                                         client_secret_key=KEYCLOAK_CLIENT_SECRET)
        try:
            token = keycloak_openid.token(username, password)
            userinfo = keycloak_openid.userinfo(token['access_token'])
            # Aquí puedes procesar el userinfo y crear o actualizar un usuario en Django
            user, _ = User.objects.get_or_create(username=userinfo['preferred_username'])
            user.email = userinfo.get('email', '')
            user.first_name = userinfo.get('given_name', '')
            user.last_name = userinfo.get('family_name', '')
            user.save()
            return user
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
