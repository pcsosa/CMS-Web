import time, asyncio
from appcms.services.keycloak_service import KeycloakService
from appcms.utils.utils import obtener_roles_desde_token, obtenerToken

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
    
    """
    Obtiene la información básica del usuario autenticado y sus roles desde Keycloak.

    :param request: Objeto HttpRequest que contiene los datos de la sesión, incluyendo el token.
    :return: Un diccionario con la información del usuario y sus roles si el token está presente, o un diccionario vacío si no hay token.
    :rtype: dict
    """
    kc = KeycloakService.get_instance()
    
    token = obtenerToken(request)
    
    if not token:
        return {}
    
    print("Obteniendo datos básicos")
    
    # Medir tiempo para obtener user_info
    user_info_start = time.time()
    user_info = kc.openid.userinfo(token)
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