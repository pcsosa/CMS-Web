# appcms/templatetags/permisos.py
from django.template import Library
from ..services.keycloak_service import KeycloakService
import time

register = Library()

@register.simple_tag(takes_context=True)
def tienePermiso(context, *args):
  start_time = time.time()
  kc = KeycloakService.get_instance()
  token = context['request'].session.get('token')
  aux = kc.tienePermiso(token, args)
  print("TIENE PERMISOS ", args, ": ", aux)
  end_time = time.time()
  print("Tiempo para calcular permiso ", args, ": ", end_time - start_time)
  return aux 
