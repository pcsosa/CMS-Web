# subcategorias/views.py
from django.shortcuts import render, redirect, get_object_or_404
from appcms.models import Categoria
from subcategorias.forms import SubcategoriaForm
from .models import Subcategoria

def administrar_subcategorias(request):
    """
    Administra subcategorías, mostrando un formulario para crear nuevas subcategorías
    y listando las subcategorías existentes.
    
    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Una respuesta con la vista de administración de subcategorías.
    :rtype: HttpResponse
    """
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
    """
    Crea una nueva subcategoría dentro de una categoría existente.
    
    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Una respuesta con la vista para crear una nueva subcategoría.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_subcategorias')  # Asegúrate de que esta URL exista
    else:
        form = SubcategoriaForm()
    
    return render(request, 'crear_subcategoria.html', {'form': form})

def lista_subcategorias(request):
    """
    Lista todas las subcategorías existentes.
    
    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Una respuesta con la vista de la lista de subcategorías.
    :rtype: HttpResponse
    """
    subcategorias = Subcategoria.objects.all()  # Recupera todas las subcategorías
    return render(request, 'lista_subcategorias.html', {'subcategorias': subcategorias})

def eliminar_subcategoria(request, pk):
    """
    Elimina una subcategoría específica.
    
    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param pk: La clave primaria de la subcategoría a eliminar.
    :type pk: int
    :return: Una respuesta con la vista de confirmación de eliminación.
    :rtype: HttpResponse
    """
    subcategoria = get_object_or_404(Subcategoria, pk=pk)
    
    if request.method == 'POST':
        subcategoria.delete()
        return redirect('lista_subcategorias')  # Redirige a la lista de subcategorías después de eliminar
    
    return render(request, 'eliminar_subcategoria.html', {'subcategoria': subcategoria})

def editar_subcategoria(request,pk):
    """Editar campos de subcategoria

    Args:
        :param request: La solicitud HTTP.
        :type request: HttpRequest
        :param pk: La clave primaria de la subcategoría a modificar.
        :type pk: int
        :return: HttpResponse.
    """
    subcategoria = get_object_or_404(Subcategoria, id=pk)
    
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            return redirect('')  
    else:
        form = SubcategoriaForm(instance=subcategoria)
    
    return render(request, 'editar_subcategoria.html', {'form': form})

