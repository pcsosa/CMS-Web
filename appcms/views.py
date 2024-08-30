from django.shortcuts import get_object_or_404, redirect, render
from .forms import BusquedaCategoriaForm
from appcms.forms import CategoriaForm
from .models import Categoria
from django.views.generic import TemplateView
from django.db.models import Q
import unicodedata

# Create your views here.
def quitar_acentos(texto):
    if texto is None:
        return ''
    # Normaliza el texto en forma NFD (Normalization Form Decomposition)
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Filtra los caracteres que no son marcas diacríticas (acentos)
    texto_sin_acentos = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
    return texto_sin_acentos

def buscar_categorias(request):
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
    """resultados = Categoria.objects.filter(nombre_incontains)
    return render(request, buscar_categorias, {categorias:resultados})"""
   
class Home(TemplateView):
    template_name = "home.html"

class search(TemplateView):
    template_name = "buscar_categorias.html"

class Vista2(TemplateView):
    template_name = "vista2.html"

def administrar_categorias(request):
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
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'crear_categoria.html', {'form': form})

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

