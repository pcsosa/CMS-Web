from django.shortcuts import get_object_or_404, redirect, render

from appcms.forms import CategoriaForm
from .models import Categoria
from django.views.generic import TemplateView

# Create your views here.

def buscar_categorias(request):
    consulta = request.GET.get('q')
    categorias = []
    mensaje = ''
    
    if consulta:
        categorias = Categoria.objects.filter(nombre__icono_contiene = consulta)
        if not categorias.exists():
            mensaje = "Categoría no encontrada"
    
    contexto = {
        'categorias': categorias,
        'mensaje': mensaje,
        'consulta': consulta
    }
    
    return render(request, 'buscar_categorias.html', contexto)

class Home(TemplateView):
    template_name = "home.html"

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

