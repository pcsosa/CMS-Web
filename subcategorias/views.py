from django.shortcuts import render, redirect,get_object_or_404
from appcms.models import Categoria
from subcategorias.forms import SubcategoriaForm
from .models import Subcategoria


# Create your views here.
def administrar_subcategorias(request):
    if request.method == 'POST':
        if 'create' in request.POST:
            form = SubcategoriaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('administrar_subcategorias')
    else:
        form = SubcategoriaForm()
    subcategorias = Subcategoria.objects.all()
    return render(request, 'administrar_subcategorias.html', {'subcategorias': subcategorias, 'form': form})


def crear_subcategoria(request):
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_subcategorias')  # Asegúrate de que esta URL exista
    else:
        form = SubcategoriaForm()
    return render(request, 'crear_subcategoria.html', {'form': form})


def lista_subcategorias(request):
    subcategorias = Subcategoria.objects.all()  # Recupera todas las subcategorías
    return render(request, 'lista_subcategorias.html', {'subcategorias': subcategorias})

def eliminar_subcategoria(request, pk):
    subcategoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        subcategoria.delete()
        return redirect('lista_subcategorias')  # Redirige a la lista de subcategorías después de eliminar
    
    return render(request, 'eliminar_subcategoria.html', {'subcategoria': subcategoria})
