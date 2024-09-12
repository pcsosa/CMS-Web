from appcms.services.keycloak_service import KeycloakService
from appcms.utils.utils import obtener_roles_desde_token

def datos_basicos(request):
    kc = KeycloakService.get_instance()
    token = request.session.get('token')
    
    if token is None:
        return {}
    
    print("Obteniendo datos básicos")
    user_info = kc.openid.userinfo(token['access_token'])
    roles = obtener_roles_desde_token(token)
    print(roles)
    contexto = {
      'user_info': user_info,
      'roles': roles
    }
  
    return contexto
