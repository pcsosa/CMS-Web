# appcms/templatetags/permisos.py
from django.template import Library
from ..services.keycloak_service import KeycloakService


register = Library()

@register.simple_tag(takes_context=True)
def tienePermiso(context, *args): 
  kc = KeycloakService.get_instance()
  token = context['request'].session.get('token')
  aux = kc.tienePermiso(token, args)
  print("TIENE PERMISOS ", args, ": ", aux)
  return aux 
