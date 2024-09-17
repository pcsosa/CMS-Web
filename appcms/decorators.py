from functools import wraps
from django.http import HttpResponseForbidden
from django.conf import settings
from django.core.cache import cache
from keycloak import KeycloakOpenID
from appcms.services.keycloak_service import KeycloakService
from appcms.utils.utils import obtener_roles_desde_token, obtenerTokenActivo, obtenerToken

kc = KeycloakService()

def roles_requeridos(*required_roles):
    """
    Decorador para restringir el acceso a vistas basado en los roles del usuario.

    Este decorador verifica si el usuario tiene uno de los roles requeridos para acceder a una vista. 
    Si el usuario tiene el rol adecuado, la vista se ejecuta; de lo contrario, se devuelve una respuesta de 
    prohibición de acceso.

    :param required_roles: Roles requeridos para acceder a la vista. Puede incluir uno o más roles.
    :type required_roles: str
    :return: Una función decoradora que envuelve la vista objetivo.
    :rtype: function
    """
    def decorator(view_func):
        """
        Función interna que envuelve la vista objetivo y aplica la lógica de autorización.

        :param view_func: La vista que se desea decorar.
        :type view_func: function
        :return: La vista decorada con la lógica de autorización aplicada.
        :rtype: function
        """
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            """
            Verifica los roles del usuario y decide si permitir el acceso a la vista.

            Obtiene el token de sesión, comprueba su validez y verifica los roles del usuario. 
            Si el usuario tiene uno de los roles requeridos, ejecuta la vista. De lo contrario, 
            devuelve una respuesta de prohibición de acceso.

            :param request: El objeto de solicitud HTTP.
            :type request: django.http.HttpRequest
            :param args: Argumentos adicionales para la vista.
            :param kwargs: Argumentos de palabra clave adicionales para la vista.
            :return: La respuesta de la vista si el usuario tiene los roles adecuados, 
                     o una respuesta de prohibición de acceso si no los tiene.
            :rtype: django.http.HttpResponse
            """
            
            token = obtenerToken(request)

            token = obtenerTokenActivo(request, token)
            
            if not token:
              return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            
            user_roles = obtener_roles_desde_token(token)
            if any(element in user_roles for element in required_roles):
                return view_func(request, *args, **kwargs)
            
        return _wrapped_view
    return decorator
