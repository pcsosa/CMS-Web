from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from appcms.utils.utils import obtenerUserId
from contenidos.models_cont import Contenido
from subcategorias.models import Subcategoria

from .forms import CategoriaForm
from .models import Categoria
from .services.keycloak_service import KeycloakService
from .utils.utils import obtenerRPT, obtenerToken, quitar_acentos
from appcms.notificacion import *

load_dotenv()


# --------------- PRINCIPAL----------------


def home(request):
    """
    Vista para la página de inicio.

    Esta vista renderiza la plantilla 'home.html'.
    """
    return render(request, "home.html")


def panel(request):
    """
    Vista para la página del panel de administración.

    Esta vista renderiza la plantilla 'panel.html'.
    """
    return render(request, "panel.html")


# --------------- CATEGORIAS ----------------


def lista_categorias(request):
    """
    Muestra una lista de todas las categorías.

    Esta vista consulta todas las categorías de la base de datos y las muestra
    en la plantilla 'lista_categorias.html'.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: HttpResponse: La respuesta renderizada con la lista de categorías.
    """

    consulta = request.GET.get("q")
    consulta = quitar_acentos(consulta)
    categorias = []

    if consulta != "" and consulta is not None:
        categorias = Categoria.objects.filter(Q(nombre__icontains=consulta))
    else:
        categorias = Categoria.objects.all()

    contexto = {"categorias": categorias, "consulta": consulta}

    return render(request, "lista_categorias.html", contexto)


def crear_categoria(request):
    """
    Crea una nueva categoría.

    Si se envía una solicitud POST, se guarda la nueva categoría.
    En caso contrario, se muestra un formulario para crear una nueva categoría.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: HttpResponse.
    """
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_categorias")
    else:
        return HttpResponse("Error: Método no permitido", status=405)


def eliminar_categoria(request, pk):
    """
    Elimina una categoría específica.

    Esta vista permite la eliminación de una categoría a partir de su clave primaria (pk).
    Después de la eliminación, se redirige a la lista de categorías.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param pk: La clave primaria de la categoría a eliminar.
    :type pk: int
    :return: HttpResponse.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    articulos = Contenido.objects.filter(categoria=pk)
    subcategorias = Subcategoria.objects.filter(categoria=pk)

    if request.method == "POST":
        if not articulos:
            categoria.delete()
            messages.success(
                request,
                f'La categoría "{categoria.nombre}" ha sido eliminada correctamente.',
            )
            notificar_borrar_categoria(categoria)
            return redirect("lista_categorias")
        else:
            messages.error(
                request,
                f'La categoría "{categoria.nombre}" no se pudo borrar.Tiene articulos y subcategorias publicadas',
            )
            return redirect("lista_categorias")
    else:
        return HttpResponse("Error: Método no permitido", status=405)

    if request.method == "POST":
        categoria.delete()
        messages.success(
            request,
            f'La categoría "{categoria.nombre}" ha sido eliminada correctamente.',
        )
        return redirect("lista_categorias")
    else:
        return HttpResponse("Error: Método no permitido", status=405)


def editar_categoria(request, pk):
    """Editar campos de categoria

    Args:
        :param request: La solicitud HTTP.
        :type request: HttpRequest
        :param pk: La clave primaria de la categoría a modificar.
        :type pk: int
        :return: HttpResponse.
    """
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'La categoría "{categoria.nombre}" ha sido modificado correctamente.',
            )
            #notificar_editar_categoria(categoria)
            return redirect("lista_categorias")
    else:
        return HttpResponse("Error: Método no permitido", status=405)


# --------------- AUTENTICACIÓN --------------


def login(request):
    """
    Maneja el inicio de sesión del usuario.

    Esta función redirige al usuario a la página de autenticación de Keycloak.
    Se genera una URL de autorización con los permisos solicitados ('openid', 'profile', 'email')
    y la redirección después del inicio de sesión exitoso es manejada por la URI proporcionada.

    :param request: El objeto HTTP request de Django que contiene los detalles de la solicitud.
    :type request: HttpRequest
    :return: Redirige al usuario a la página de inicio de sesión de Keycloak.
    :rtype: HttpResponse
    """

    kc = KeycloakService.get_instance()
    authorization_url = kc.openid.auth_url(
        redirect_uri=settings.DJ_URL + ":" + settings.DJ_PORT + "/callback/",
        scope="openid profile email",
    )
    return redirect(authorization_url)


def callback(request):
    """
    Maneja el callback de Keycloak después del inicio de sesión.

    Recibe el código de autorización de Keycloak, lo intercambia por un token de acceso
    y lo guarda en la sesión del usuario. Si no se proporciona un código, devuelve un error.

    :param request: El objeto HTTP request de Django que contiene los detalles de la solicitud.
    :type request: HttpRequest
    :return: Si se proporciona un código válido, redirige al usuario al panel de control.
             Si no se proporciona el código, devuelve un error HTTP 400.
    :rtype: HttpResponse
    """

    code = request.GET.get("code")
    if not code:
        return HttpResponse("Error: No code provided", status=400)

    kc = KeycloakService.get_instance()
    token = kc.get_token(code)  # Obtener token normal sin permisos
    token = obtenerRPT(token["access_token"])  # Obtener token con permisos incluidos

    access_token = token["access_token"]  # Token normal
    refresh_token = token["refresh_token"]  # Token con permisos

    # Guardar tokens en la sesión
    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token

    # Cachear los tokens para mayor rendimiento
    cache.set("access_token", access_token, timeout=300)
    cache.set("refresh_token", refresh_token, timeout=1800)

    return redirect("panel")


def logout(request):
    """
    Maneja el cierre de sesión del usuario.

    Limpia la sesión del usuario y llama al servicio de Keycloak para cerrar la sesión
    de forma remota. Luego, redirige al usuario a la página de inicio.

    :param request: El objeto HTTP request de Django que contiene los detalles de la solicitud.
    :type request: HttpRequest
    :return: Redirige al usuario a la página de inicio después de cerrar la sesión.
    :rtype: HttpResponse
    """

    kc = KeycloakService.get_instance()

    refresh_token = cache.get("refresh_token")

    if not refresh_token:
        refresh_token = request.session.get("refresh_token")

    if refresh_token:
        request.session.clear()
        cache.clear()
        kc.openid.logout(refresh_token)

    return redirect("home")


@csrf_exempt
def upload_image(request):
    """Esta funcion maneja la subida de imagen en el contenido a traves de una solicitud POST

    Args:
        request (HttpRequest): la solicitud http que contiene la imagen

    Returns:
        JsonResponse: un objeto JSON que contiene la URL donde se ha guardado la imagen
    """
    if request.method == "POST":
        image = request.FILES["file"]
        # Guardar la imagen en el servidor
        image_url = "ruta/donde/guardas/la/imagen/" + image.name
        # Retornar la URL de la imagen
        return JsonResponse({"location": image_url})
