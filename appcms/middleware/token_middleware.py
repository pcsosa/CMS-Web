from appcms.utils.utils import comprobarToken, obtenerToken
from django.shortcuts import redirect

# Middleware que verifica el token antes de cada solicitud
class KeycloakTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Omitir la verificación del token en la ruta de logout
        if request.path == '/logout/':
            return self.get_response(request)
        
        # Obtener token de la cache o la sesión
        token = obtenerToken(request)

        # Verificar el token
        try:
            comprobarToken(request, token)
        except Exception as e:
            print("El token ya expiró, redirigiendo a la página de inicio")
            return redirect('logout')


        return self.get_response(request)