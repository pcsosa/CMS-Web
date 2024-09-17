import time
from ..utils.utils import comprobarToken, obtenerToken
from django.shortcuts import redirect

# Middleware que verifica el token antes de cada solicitud
class KeycloakTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        total_start_time = time.time()
        print("Middleware de token ejecutado")

        # Omitir la verificación del token en la ruta de logout
        start_time = time.time()
        if request.path == '/logout/':
            return self.get_response(request)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tiempo en verificar la ruta de logout: {elapsed_time} segundos")
        
        # Obtener token de la cache o la sesión
        start_time = time.time()
        token = obtenerToken(request)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tiempo en obtener tokens de la sesión: {elapsed_time} segundos")

        # Verificar el token
        start_time = time.time()
        try:
            comprobarToken(request, token)
        except Exception as e:
            print("El token ya expiró, redirigiendo a la página de inicio")
            return redirect('logout')
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tiempo en verificar el token: {elapsed_time} segundos")

        total_end_time = time.time()
        total_elapsed_time = total_end_time - total_start_time
        print(f"Tiempo total en el middleware: {total_elapsed_time} segundos")

        return self.get_response(request)