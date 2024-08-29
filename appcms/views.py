from django.shortcuts import render
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
