from django.shortcuts import get_object_or_404, redirect, render
from .forms import BusquedaCategoriaForm
from appcms.forms import CategoriaForm
from .models import Categoria
from django.views.generic import TemplateView
from django.db.models import Q
import unicodedata


def quitar_acentos(texto):
    """
    Elimina los acentos de un texto.
    Este método normaliza el texto en forma NFD y filtra los caracteres con acentos.

    Args:
        texto (str): El texto al que se le quitarán los acentos.
    Returns:
        str: El texto sin acentos.
    """
    if texto is None:
        return ''
    # Normaliza el texto en forma NFD (Normalization Form Decomposition)
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Filtra los caracteres que no son marcas diacríticas (acentos)
    texto_sin_acentos = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
    return texto_sin_acentos

def buscar_categorias(request):
    """
    Busca categorías en la base de datos basadas en una consulta proporcionada.

    Esta vista procesa una consulta GET y busca coincidencias en el nombre de las categorías,
    ignorando los acentos. Si no se encuentran coincidencias, se muestra un mensaje de
    "Categoría no encontrada".

    Args:
        request (HttpRequest): La solicitud HTTP.
    Returns:
        HttpResponse: La respuesta renderizada con las categorías encontradas y un mensaje.
    """
    print("--------VISTA 'buscar_categorias' ejecutada")
    consulta = request.GET.get('q')
    consulta = quitar_acentos(consulta)
    categorias = []
    mensaje = "Se ha encontado exitosamente"
    print(consulta)
    #import pdb; pdb.set_trace()
    if consulta:
        categorias = Categoria.objects.filter( Q(nombre__icontains = consulta)) #nombre__icontains = consulta
        if not categorias.exists():
            mensaje = "Categoría no encontrada"
        
    contexto = {
        'categorias': categorias,
        'mensaje': mensaje,
        'consulta': consulta
    }
    print("----------------------------RESULTADO DE CONSULTA")
    print(contexto)
    return render(request, 'buscar_categorias.html', contexto)
    """_summary_

    Returns:
        _type_: _description_
    """
   
class Home(TemplateView):
    """
        Vista para la página de inicio.
        Esta vista renderiza la plantilla 'home.html'.
    """
    template_name = "home.html"

class search(TemplateView):
    """
        Vista para la búsqueda de categorías.
        Esta vista renderiza la plantilla 'buscar_categorias.html'.
    """
    template_name = "buscar_categorias.html"

class admincat(TemplateView):
    """
        Vista para la administracion de categorías.
        Esta vista renderiza la plantilla 'administrar_categorias.html'.
    """
    template_name = "administrar_categorias.html"

class lista(TemplateView):
    """
        Vista para listar categorías.
        Esta vista renderiza la plantilla 'lista_categorias.html'.
    """
    template_name = "lista_categorias.html"

class crear(TemplateView):
    """
        Vista para crear categorías.
        Esta vista renderiza la plantilla 'crear_categorias.html'.
    """
    template_name = "crear_categoria.html"
      

def administrar_categorias(request):
    """
        Administra de categorías.

        Si se envía una solicitud POST con datos válidos, se crea una nueva categoría.
        En caso contrario, se muestra un formulario para crear una nueva categoría y luego se vizualiza junto
        con la lista de categorías existentes.

        Args:
            request (HttpRequest): La solicitud HTTP.

        Returns:
            HttpResponse: La respuesta renderizada con el formulario y la lista de categorías.
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

def crear_categoria(request):
    """
        Crea una nueva categoría:
        Si se envía una solicitud POST, se guarda la nueva categoría.
        En caso contrario, se muestra un formulario para crear una nueva categoría.

        Args:
            request (HttpRequest): La solicitud HTTP.
        Returns:
            HttpResponse: La respuesta renderizada con el formulario de creación de categoría.
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

        Args:
            request (HttpRequest): La solicitud HTTP.
        Returns:
            HttpResponse: La respuesta renderizada con la lista de categorías.
    """
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def eliminar_categoria(request, pk):
    """
        Elimina una categoría específica.
        Esta vista permite la eliminación de una categoría a partir de su clave primaria (pk).
        Después de la eliminación, se redirige a la lista de categorías.

        Args:
            request (HttpRequest): La solicitud HTTP.
            pk (int): La clave primaria de la categoría a eliminar.
        Returns:
            HttpResponse: La respuesta renderizada con la confirmación de eliminación.
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')  # Redirige a la lista de subcategorías después de eliminar
    
    return render(request, 'eliminar_categoria.html', {'categoria': categoria})