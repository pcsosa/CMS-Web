from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import JsonResponse
from .forms import BusquedaCategoriaForm
from appcms.forms import CategoriaForm
from .models import Categoria
from django.views.generic import TemplateView
from django.db.models import Q
import unicodedata
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import roles_requeridos
from django.http import HttpResponse
from keycloak import KeycloakOpenID
from django.conf import settings
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from .services.keycloak_service import KeycloakService
from .utils.utils import comprobarToken
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

def home(request):
  """
  Vista para la página de inicio.
  
  Esta vista renderiza la plantilla 'home.html'.
  """
  return render(request, 'home.html')

@roles_requeridos("Administrador", "Editor")
def panel(request):
  """
  Vista para la página del panel de administración.

  Esta vista renderiza la plantilla 'panel.html'.
  """
  kc = KeycloakService()
  token = request.session.get('token')
  contexto = {}
  if token:
    token = comprobarToken(request, token, kc)
    user_info = kc.openid.userinfo(token['access_token'])
    contexto = user_info
  return render(request, 'panel.html', contexto)

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

@roles_requeridos("Administrador")
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
        messages.success(request, f'La categoría "{categoria.nombre}" ha sido eliminada correctamente.')
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
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')  
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'editar_categoria.html', {'form': form, 'categoria': categoria})

def login(request):
    kc = KeycloakService()
    authorization_url = kc.openid.auth_url(
        redirect_uri = os.getenv('DJ_URL') + ':' + os.getenv('DJ_PORT') + '/callback/',
        scope='openid profile email'
    )
    return redirect(authorization_url)

def callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse('Error: No code provided', status=400)

    kc = KeycloakService()
    token = kc.get_token(code)
    request.session['token'] = token
    return redirect('panel')

def logout(request):
    kc = KeycloakService()
    token = request.session.get('token')
    if token:
      request.session.clear()
      kc.openid.logout(token['refresh_token'])    
    return redirect('home')

def listar_categorias(_request):
    categorias = list(Categoria.objects.values())
    data = {'categorias': categorias}
    return JsonResponse(data)
