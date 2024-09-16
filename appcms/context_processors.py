import time, asyncio
from appcms.services.keycloak_service import KeycloakService
from appcms.utils.utils import obtener_roles_desde_token

def datos_basicos(request):
    start_time = time.time()
    
    """
    Obtiene la información básica del usuario autenticado y sus roles desde Keycloak.

    :param request: Objeto HttpRequest que contiene los datos de la sesión, incluyendo el token.
    :return: Un diccionario con la información del usuario y sus roles si el token está presente, o un diccionario vacío si no hay token.
    :rtype: dict
    """
    kc = KeycloakService.get_instance()
    token = request.session.get('token')
    
    if token is None:
        return {}
    
    print("Obteniendo datos básicos")
    
    # Medir tiempo para obtener user_info
    user_info_start = time.time()
    user_info = kc.openid.userinfo(token['access_token'])
    user_info_end = time.time()
    user_info_elapsed = user_info_end - user_info_start
    print(f"Tiempo tomado para obtener user_info: {user_info_elapsed:.4f} segundos")
    
    # Medir tiempo para obtener roles
    roles_start = time.time()
    roles = obtener_roles_desde_token(token)
    roles_end = time.time()
    roles_elapsed = roles_end - roles_start
    print(f"Tiempo tomado para obtener roles: {roles_elapsed:.4f} segundos")
    
    print(roles)
    contexto = {
      'user_info': user_info,
      'roles': roles
    }
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo total tomado en el context global: {elapsed_time:.4f} segundos")
  
    return contexto