from functools import wraps
from django.http import HttpResponseForbidden
from django.conf import settings
from keycloak import KeycloakOpenID
from .services.keycloak_service import KeycloakService
from .utils.utils import comprobarToken

kc = KeycloakService()

def roles_requeridos(*required_roles):
    def is_role_in_roles(roles, role_names):
        """
        Verifica si alguno de los roles con nombres especificados está en la lista de roles.

        :param roles: Lista de roles, donde cada rol es un diccionario.
        :param role_names: Lista de nombres de roles que se desean verificar.
        :return: True si al menos uno de los roles está en la lista, False en caso contrario.
        """
        role_names_set = set(role_names)
        return any(role['name'] in role_names_set for role in roles)
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = request.session.get('token')
            token = comprobarToken(request, token, kc)
            if token:
                userid = kc.get_userId(token['access_token'])
                user_roles = kc.admin.get_realm_roles_of_user(userid)
                if is_role_in_roles(user_roles, required_roles):
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator
