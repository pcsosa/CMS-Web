from django.shortcuts import redirect
from appcms.services.keycloak_service import KeycloakService
from django.conf import settings
from appcms.utils.utils import comprobarToken
import time

kc = KeycloakService.get_instance()

# Middleware que verifica el token antes de cada solicitud
class KeycloakTokenMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    start_time = time.time()
    print("Middleware de token ejecutado")

    # Omitir la verificación del token en la ruta de logout
    if request.path == '/logout/':
      return self.get_response(request)

    # Obtener tokens de la sesión
    token = request.session.get('token')

    try:
      comprobarToken(request, token)
    except Exception as e:
      print("El token ya expiró, redirigiendo a la página de inicio")
      return redirect('logout')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tiempo transcurrido en el middleware: {elapsed_time} segundos")

    return self.get_response(request)