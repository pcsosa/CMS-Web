from functools import wraps
from django.http import HttpResponseForbidden
from django.conf import settings
from keycloak import KeycloakOpenID
from .services.keycloak_service import KeycloakService
from .utils.utils import obtener_roles_desde_token, obtenerTokenActivo

kc = KeycloakService()

def roles_requeridos(*required_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = request.session.get('token')
            token = obtenerTokenActivo(request, token)
            if token:
                user_roles = obtener_roles_desde_token(token)
                if any(element in user_roles for element in required_roles):
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator
