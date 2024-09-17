import time, asyncio
from appcms.services.keycloak_service import KeycloakService
from appcms.utils.utils import obtener_roles_desde_token, obtenerToken

def datos_basicos(request):
    start_time = time.time()
    
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