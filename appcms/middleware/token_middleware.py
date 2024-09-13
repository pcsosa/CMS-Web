from django.shortcuts import redirect
from appcms.services.keycloak_service import KeycloakService
from django.conf import settings
from appcms.utils.utils import comprobarToken

kc = KeycloakService.get_instance()

# Middleware que verifica el token antes de cada solicitud
class KeycloakTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
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
          
        return self.get_response(request)   