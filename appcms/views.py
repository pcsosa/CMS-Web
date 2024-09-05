from django.shortcuts import get_object_or_404, redirect, render
from .forms import BusquedaCategoriaForm
from appcms.forms import CategoriaForm
from .models import Categoria
from django.views.generic import TemplateView
from django.db.models import Q
import unicodedata
from django.contrib.auth.decorators import login_required
from .decorators import rol_requerido
from django.http import HttpResponse
from keycloak import KeycloakOpenID
from django.conf import settings
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from .services.keycloak_service import KeycloakService
load_dotenv()


@login_required
def protected_view(request):
    return render(request, 'protected.html')


def quitar_acentos(texto):
    """
    Elimina los acentos de un texto.

    Este método normaliza el texto en forma NFD y filtra los caracteres con acentos.

    :param texto: El texto al que se le quitarán los acentos.
    :type texto: str
    :return: El texto sin acentos.
    :rtype: str
    """
    if texto is None:
        return ''
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_acentos = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
    return texto_sin_acentos

def buscar_categorias(request):
    """
    Busca categorías en la base de datos basadas en una consulta proporcionada.

    Esta vista procesa una consulta GET y busca coincidencias en el nombre de las categorías,
    ignorando los acentos. Si no se encuentran coincidencias, se muestra un mensaje de
    "Categoría no encontrada".

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: HttpResponse.
    """
    consulta = request.GET.get('q')
    consulta = quitar_acentos(consulta)
    categorias = []
    mensaje = "Se ha encontrado exitosamente"

    if consulta:
        categorias = Categoria.objects.filter(Q(nombre__icontains=consulta))
        if not categorias.exists():
            mensaje = "Categoría no encontrada"
        
    contexto = {
        'categorias': categorias,
        'mensaje': mensaje,
        'consulta': consulta
    }
    return render(request, 'buscar_categorias.html', contexto)

def interfaz_estandar(request):
    return render(request,"interfaz_estandar.html")

def Home(request):
    """
    Vista para la página de inicio.

    Esta vista renderiza la plantilla 'home.html'.
    """
    keycloak = KeycloakService()
    token = request.session.get('access_token')
    print(token)
    if token:
      # user_info = keycloak.openid.userinfo(token)
      # contexto = user_info
      # return render(request, 'home.html', contexto)
      return HttpResponse("Hola que tal")
    else:
      return HttpResponse("TENÉS QUE INICIAR SESIÓN!!!")

    

class Search(TemplateView):
    """
    Vista para la búsqueda de categorías.

    Esta vista renderiza la plantilla 'buscar_categorias.html'.
    """
    template_name = "buscar_categorias.html"

class AdminCat(TemplateView):
    """
    Vista para la administración de categorías.

    Esta vista renderiza la plantilla 'administrar_categorias.html'.
    """
    template_name = "administrar_categorias.html"

class Lista(TemplateView):
    """
    Vista para listar categorías.

    Esta vista renderiza la plantilla 'lista_categorias.html'.
    """
    template_name = "lista_categorias.html"

class Crear(TemplateView):
    """
    Vista para crear categorías.

    Esta vista renderiza la plantilla 'crear_categoria.html'.
    """
    template_name = "crear_categoria.html"

def administrar_categorias(request):
    """
    Administra categorías.

    Si se envía una solicitud POST con datos válidos, se crea una nueva categoría.
    En caso contrario, se muestra un formulario para crear una nueva categoría junto
    con la lista de categorías existentes.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: HttpResponse.
    """
    if request.method == 'POST':
        if 'create' in request.POST:
            form = CategoriaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('administrar_categorias')
    else:
        form = CategoriaForm()
    
    categorias = Categoria.objects.all()
    return render(request, 'administrar_categorias.html', {'categorias': categorias, 'form': form})

@rol_requerido("Administrador")
def crear_categoria(request):
    """
    Crea una nueva categoría.

    Si se envía una solicitud POST, se guarda la nueva categoría.
    En caso contrario, se muestra un formulario para crear una nueva categoría.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: HttpResponse.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    
    return render(request, 'crear_categoria.html', {'form': form})

def lista_categorias(request):
    """
    Muestra una lista de todas las categorías.

    Esta vista consulta todas las categorías de la base de datos y las muestra
    en la plantilla 'lista_categorias.html'.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: HttpResponse: La respuesta renderizada con la lista de categorías.
    """
    categorias = Categoria.objects.all()
    print(categorias) 
    return render(request, 'lista_categorias.html', {'categorias': categorias})

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
    
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
    
    return render(request, 'eliminar_categoria.html', {'categoria': categoria})

def editar_categoria(request,pk):
    """Editar campos de categoria

    Args:
        :param request: La solicitud HTTP.
        :type request: HttpRequest
        :param pk: La clave primaria de la categoría a modificar.
        :type pk: int
        :return: HttpResponse.
    """
    categoria = get_object_or_404(Categoria, id=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('')  # Redirige a la vista principal después de editar
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'editar_categoria.html', {'form': form})

def login(request):
    keycloak = KeycloakService()
    authorization_url = keycloak.openid.auth_url(
        redirect_uri = os.getenv('DJ_URL') + ':' + os.getenv('DJ_PORT') + '/callback/',
        scope='openid profile email'
    )
    return redirect(authorization_url)

def callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse('Error: No code provided', status=400)

    keycloak = KeycloakService()
    
    # try:
    token = keycloak.get_token(code)
    print(token)
    request.session['access_token'] = token['access_token']
    request.session['refresh_token'] = token['refresh_token']
    return redirect('/')
    # except Exception as e:
        # return HttpResponse(f'Error: {e}', status=500)

def logout(request):
    keycloak = KeycloakService()
    token = request.session.get('refresh_token')
    keycloak.openid.logout(token)
    request.session.clear()
    return HttpResponse("Chau")


