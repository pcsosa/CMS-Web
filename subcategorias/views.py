# subcategorias/views.py
from django.shortcuts import render, redirect, get_object_or_404
from appcms.models import Categoria
from subcategorias.forms import SubcategoriaForm
from .models import Subcategoria
from django.contrib import messages
from django.views.decorators.http import require_POST

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
        # Obtener el nombre de la subcategoría y el ID de la categoría desde la solicitud POST
        nombre = request.POST.get('nombre').strip()  # Elimina espacios en blanco
        categoria_id = request.POST.get('categoria_id')

        # Validar que el nombre no esté vacío
        if not nombre:
            messages.error(request, "El nombre de la subcategoría no puede estar vacío.")
            return redirect(request.META.get('HTTP_REFERER'))  # Regresar a la página anterior con el mensaje de error
        
        # Obtener la categoría correspondiente al ID
        categoria = get_object_or_404(Categoria, pk=categoria_id)
    
        # Validar que no exista una subcategoría con el mismo nombre en la categoría
        if Subcategoria.objects.filter(nombre=nombre, categoria=categoria).exists():
            messages.error(request, "Ya existe una subcategoría con este nombre en la categoría seleccionada.")
            return redirect(request.META.get('HTTP_REFERER'))  # Regresar a la página anterior con el mensaje de error
        
        # Crear una nueva subcategoría
        Subcategoria.objects.create(nombre=nombre, categoria=categoria)
        messages.success(request, "Subcategoría creada con éxito.")
        
        return redirect('lista_subcategorias', pk=categoria_id)  # Redirigir a la lista de subcategorías de la categoría

    # En caso de GET, mostrar el formulario vacío (aunque aquí no aplicaría si solo usas POST en el script)
    return render(request, 'crear_subcategoria.html')

def lista_subcategorias(request, pk):
    """
    Lista todas las subcategorías existentes.
    
    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param pk: primary key de categoria
    :type: int
    :return: Una respuesta con la vista de la lista de subcategorías.
    :rtype: HttpResponse
    """
    categoria = get_object_or_404(Categoria, pk=pk)
    # Filtrar subcategorías que pertenecen a esta categoría
    subcategorias = Subcategoria.objects.filter(categoria=categoria)

    return render(request, 'lista_subcategorias.html', {'subcategorias': subcategorias,
                                                        'categoria': categoria})

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
    categoria = subcategoria.categoria
    
    if request.method == 'POST':
        subcategoria.delete()
        messages.success(request, "La eliminacion ha sido exitosa")
        return redirect('lista_subcategorias',pk=categoria.pk)  # Redirige a la lista de subcategorías después de eliminar
    
    return render(request, 'eliminar_subcategoria.html', {'subcategoria': subcategoria})

@require_POST
def actualizar_subcategoria(request):
    """
    Actualiza el nombre de una subcategoría existente.
    
    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Redirige a la lista de subcategorías.
    :rtype: HttpResponseRedirect
    """
    id = request.POST.get('id')
    nombre = request.POST.get('nombre')
    
    subcategoria = get_object_or_404(Subcategoria, pk=id)
    subcategoria.nombre = nombre
    subcategoria.save()

    return redirect(request.META.get('HTTP_REFERER'))