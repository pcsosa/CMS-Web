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
import os, json, jwt
from dotenv import load_dotenv
from .services.keycloak_service import KeycloakService
from .utils.utils import comprobarToken, obtener_roles_desde_token, decode_token, obtenerTokenActivo, obtenerUserId
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

# @roles_requeridos("Administrador", "Editor")
def panel(request):
  """
  Vista para la página del panel de administración.

  Esta vista renderiza la plantilla 'panel.html'.
  """
  kc = KeycloakService.get_instance()
  token = request.session.get('token')
  token = comprobarToken(request, token) # Comprueba si el token sigue siendo valido y si no genera uno nuevo
  
  # print("ACCESS TOKEN")
  # print(token['access_token'])
  
  # print("DECODED TOKEN")
  # print(json.dumps(decode_token(token['access_token']), indent=2, ensure_ascii=False))
  
  # aux = kc.tienePermiso(token, ("Categoria#Crear", "Categoria#Editar", "Categoria#Eliminar"))
  
  # print("RPT TOKEN")
  # rpt = kc.get_rpt_token(token)
  # print(json.dumps(decode_token(rpt), indent=2, ensure_ascii=False))

  user_info = kc.openid.userinfo(token['access_token'])
  # permisos = kc.get_permisos(token)
  # print("PERMISOS")
  # print(json.dumps(permisos, indent=2))

  return render(request, 'panel.html', user_info)

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

def lista_categorias(request):
    """
    Muestra una lista de todas las categorías.

    Esta vista consulta todas las categorías de la base de datos y las muestra
    en la plantilla 'lista_categorias.html'.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: HttpResponse: La respuesta renderizada con la lista de categorías.
    """
    
    consulta = request.GET.get('q')
    consulta = quitar_acentos(consulta)
    categorias = []

    if consulta != "" and consulta is not None:
        categorias = Categoria.objects.filter(Q(nombre__icontains=consulta))
    else:
        categorias = Categoria.objects.all()
        
    contexto = {
        'categorias': categorias,
        'consulta': consulta
    }
    
    return render(request, 'lista_categorias.html', contexto)

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
        return HttpResponse('Error: Método no permitido', status=405)

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
    else:
        return HttpResponse('Error: Método no permitido', status=405)

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
            messages.success(request, f'La categoría "{categoria.nombre}" ha sido modificado correctamente.')
            return redirect('lista_categorias')  
    else:
        return HttpResponse('Error: Método no permitido', status=405)

def login(request):
    kc = KeycloakService.get_instance()
    authorization_url = kc.openid.auth_url(
        redirect_uri = os.getenv('DJ_URL') + ':' + os.getenv('DJ_PORT') + '/callback/',
        scope='openid profile email'
    )
    return redirect(authorization_url)

def callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse('Error: No code provided', status=400)

    kc = KeycloakService.get_instance()
    token = kc.get_token(code)
    request.session['token'] = token
    return redirect('panel')

def logout(request):
    kc = KeycloakService.get_instance()
    token = request.session.get('token')
    if token:
      request.session.clear()
      kc.openid.logout(token['refresh_token'])    
    return redirect('home')
