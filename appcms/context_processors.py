import time, asyncio
from appcms.services.keycloak_service import KeycloakService
from appcms.utils.utils import obtener_roles_desde_token

def datos_basicos(request):
    """
    Obtiene información básica del usuario y sus roles.

    Esta función utiliza el token de sesión del usuario para obtener información 
    básica y roles asociados desde el servicio Keycloak. Se mide el tiempo de 
    ejecución para cada llamada de servicio y se imprime en la consola.

    :param request: El objeto HTTP request de Django que contiene los detalles de la solicitud.
    :type request: HttpRequest
    :return: Un diccionario que contiene la información del usuario y sus roles.
    :rtype: dict
    """
    start_time = time.time()
    
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