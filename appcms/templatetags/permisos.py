# appcms/templatetags/permisos.py
from django.template import Library
from ..services.keycloak_service import KeycloakService
from ..utils import utils
import ast

register = Library()

@register.simple_tag(takes_context=True)
def tienePermiso(context, resource, scopes_to_check):
  """Verifica si el usuario tiene permiso para acceder a un recurso específico.

    Esta función evalúa los permisos del usuario en función del token de autenticación
    y los scopes proporcionados. Utiliza el contexto de la solicitud para obtener el token
    y luego verifica si el usuario tiene los permisos necesarios para el recurso solicitado.

    Args:
        context (dict): Un diccionario que contiene el contexto de la solicitud,
                        incluyendo el objeto de la solicitud.
        resource (str): El recurso al que se desea acceder.
        scopes_to_check (str): Una cadena que representa los scopes que se deben verificar,
                               en formato de lista.

    Returns:
        result: Devuelve True si el usuario tiene permiso para acceder al recurso,
              de lo contrario, devuelve False.
    """
  list_scopes = ast.literal_eval(scopes_to_check)
  request = context['request']
  token = utils.obtenerToken(request)
  result = utils.tienePermiso(token, resource, list_scopes)
  return result
