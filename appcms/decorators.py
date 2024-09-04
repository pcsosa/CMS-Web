from functools import wraps
from django.http import HttpResponseForbidden
from django.conf import settings
from keycloak import KeycloakOpenID
from .services.keycloak_service import KeycloakService

keycloak = KeycloakService()

def rol_requerido(required_role):
    def is_role_in_roles(roles, role_name):
      """
      Verifica si un rol con el nombre especificado está en la lista de roles.

      :param roles_list: Lista de roles, donde cada rol es un diccionario.
      :param role_name: Nombre del rol que se desea verificar.
      :return: True si el rol está en la lista, False en caso contrario.
      """
      return any(role['name'] == role_name for role in roles)
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = request.session.get('access_token')
            if token:
                userid = keycloak.get_userId(token)
                user_roles = keycloak.admin.get_realm_roles_of_user(userid)
                if is_role_in_roles(user_roles, required_role):
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator