from django.contrib.auth.models import User  # Para manejar el publicador
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from contenidos.forms import ComentarioForm
from .models_cont import  Comentario,Contenido, Categoria
from appcms.models import Categoria
from subcategorias.models import Subcategoria
from appcms.utils.utils import obtenerToken, obtenerUserId, obtenerUsersConRol
from django.core.serializers import serialize
import requests, json
from django.db.models import Q  # Para realizar búsquedas

from django.core.paginator import Paginator


from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages

def crear_contenido(request):
    """
    Crea un nuevo contenido en el sistema a partir de los datos enviados a través del formulario.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Si la solicitud es POST y los datos son válidos, redirige a 'lista_contenidos'. 
             Si hay errores, renderiza el formulario con mensajes de error.
    :rtype: HttpResponse
    """
    editores = obtenerUsersConRol('Editor') # Obtener todos los usuarios con el rol de Editor
    categorias = Categoria.objects.all()  # Obtener todas las categorías para mostrarlas en el formulario
    subcategorias = Subcategoria.objects.all()  # Obtener todas las subcategorías
    sub_json = serialize('json', subcategorias)
    
    print("=============================================SUBCATEGORIAS")
    print(sub_json)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        title = request.POST.get('title')
        content = request.POST.get('content')
        if content:
            content = content.replace('<p>', '').replace('</p>', '')
        else:
            content = ''  # O puedes decidir usar un valor predeterminado
        image = request.FILES.get('image')
        categoria = request.POST.get('categoria')
        subcategoria = request.POST.get('subcategoria')
        editor_id = request.POST.get('editor')

        # Obtener el usuario actual como el autor
        token = obtenerToken(request)
        autor_id = obtenerUserId(token)
        
        # Obtener el publicador
        publicador = autor_id # Temporalmente asigna el autor como publicador
        
        
        # Imprimir todos los datos para comprobar que son correctos
        print("--------------Datos del formulario-------------")
        print(f'Título: {title}')
        print(f'Contenido: {content}')
        print(f'Imagen: {image}')
        print(f'Categoría: {categoria}')
        print(f'Subcategoría: {subcategoria}')
        print(f'Editor: {editor_id}')
        print(f'Autor: {autor_id}')
        print(f'Publicador: {publicador}')
        
        # Obtener la categoría obligatoria
        #categoria = Categoria.objects.get(id=categoria_id)
        #print("================================================================= CATEGORIAS")
        #print(categoria)

        # Obtener la subcategoría opcional si se proporciona
        #subcategoria = obtener_subcategorias(categoria_id)
        #print("================================================================= SUBCATEGORIAS")
        #print(subcategoria)

        # Obtener la instancia del modelo Categoria con el id proporcionado
        categoria_obj = Categoria.objects.get(id_categoria=categoria)

        # Obtener la instancia del modelo Subcategoria con el id proporcionado, si existe
        subcategoria_obj = Subcategoria.objects.get(id_subcategoria=subcategoria) if subcategoria else None

        # Crear y guardar el nuevo contenido
        nuevo_contenido = Contenido(
            titulo=title,
            texto=content,
            imagen=image,
            categoria=categoria_obj,
            subcategoria=subcategoria_obj,
            publicador_id=publicador,  # Asigna el publicador automáticamente
            estado='Borrador',  # Estado inicial automático
            editor_id=editor_id,
            autor_id=autor_id
        )
        
        # Imprimir el nuevo contenido
        print("--------------Nuevo contenido-------------")
        print(f'Título: {nuevo_contenido.titulo}')
        print(f'Texto: {nuevo_contenido.texto}')
        print(f'Imagen: {nuevo_contenido.imagen}')
        print(f'Categoría: {nuevo_contenido.categoria}')
        print(f'Subcategoría: {nuevo_contenido.subcategoria}')
        print(f'Publicador: {nuevo_contenido.publicador_id}')
        print(f'Estado: {nuevo_contenido.estado}')
        print(f'Editor: {nuevo_contenido.editor_id}')
        print(f'Autor: {nuevo_contenido.autor_id}')
        
        nuevo_contenido.save()

        # Redireccionar después de guardar
        return redirect('gestion_contenido')

    contexto = {
        'editores': editores,
        'categorias': categorias,
        'sub_json': sub_json
    }

    # Renderizar el formulario si la solicitud no es POST
    return render(request, 'crear_contenido.html', contexto)

def lista_contenidos(request):
    """
    Muestra una lista de todos los contenidos en el sistema.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Respuesta renderizada con la plantilla 'lista_contenidos.html' y el contexto que incluye los contenidos.
    :rtype: HttpResponse
    """
    # Obtener todos los contenidos inicialmente
    contenidos = Contenido.objects.all()
    autores = obtenerUsersConRol('Autor')

    # Obtener los parámetros del filtro desde la solicitud
    orden = request.GET.get('orden', 'desc')  # Por defecto descendente
    categoria_id = request.GET.get('categoria')
    autor_id = request.GET.get('autor')
    busqueda = request.GET.get('busqueda', '')

    # Filtrar por categoría si se proporciona
    if categoria_id:
        contenidos = contenidos.filter(categoria_id=categoria_id)
    
    # Filtrar por autor si se proporciona
    if autor_id:
        
        contenidos = contenidos.filter(autor_id=autor_id)


    # Filtrar por búsqueda en el título o el contenido
    if busqueda:
        contenidos = contenidos.filter(Q(titulo__icontains=busqueda) | Q(texto__icontains=busqueda))

    # Ordenar por fecha de creación
    if orden == 'asc':
        contenidos = contenidos.order_by('fecha_modificacion')
    else:
        contenidos = contenidos.order_by('-fecha_modificacion')

    # Pasar la lista de contenidos y categorías al contexto
    categorias = Categoria.objects.all()
    paginator = Paginator(contenidos, 10)  # 10 contenidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'page_obj': page_obj,
        'contenidos': contenidos,
        'categorias': categorias,
        'busqueda': busqueda,
        'autores' : autores,
    }
    
    return render(request, 'lista_contenidos.html', contexto)


def gestion_contenido(request):
    """
    Muestra la página de gestión de contenidos, que incluye todos los contenidos disponibles.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Respuesta renderizada con la plantilla 'gestion_contenido.html' y el contexto que incluye los contenidos.
    :rtype: HttpResponse
    """
    contenidos = Contenido.objects.all()
    return render(request, 'gestion_contenido.html', {'contenidos': contenidos})
  
def editar_contenido(request):
    """
    Muestra la página para editar un contenido específico.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Respuesta renderizada con la plantilla 'editar_contenido.html'.
    :rtype: HttpResponse
    """

    # Falta codigo para editar contenido
    return render(request, 'editar_contenido.html')

def eliminar_contenido(request):
    """
    Muestra la página para eliminar un contenido específico.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Respuesta renderizada con la plantilla 'eliminar_contenido.html'.
    :rtype: HttpResponse
    """
    # Falta codigo para eliminar contenido
    return render(request, 'eliminar_contenido.html')

@csrf_exempt
def upload_image(request):
    """
    Sube una imagen al servidor y retorna su URL.

    :param request: Objeto HttpRequest que contiene los datos de la solicitud.
    :return: Un JsonResponse con la URL de la imagen subida.
    :rtype: JsonResponse
    """
    if request.method == 'POST':
        image = request.FILES['file']
        # Guardar la imagen en el servidor
        image_url = 'ruta/donde/guardas/la/imagen/' + image.name
        # Retornar la URL de la imagen
        return JsonResponse({'location': image_url})
    

@csrf_exempt
def eliminar_contenido(request, pk):
    try:
        contenido = Contenido.objects.get(pk=pk)
        contenido.delete()
        return redirect('lista_contenidos')
    except Contenido.DoesNotExist:
        return JsonResponse({'error': 'Contenido no encontrado'}, status=404)


def editar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, id=pk)  # Obtener el contenido por ID o lanzar un error 404
    editores = obtenerUsersConRol('Editor')  # Obtener los usuarios con el rol 'Editor'
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    subcategorias = Subcategoria.objects.all()  # Obtener todas las subcategorías
    sub_json = serialize('json', subcategorias)

    if request.method == 'POST':
        # Obtener datos del formulario
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        categoria = request.POST.get('categoria')
        subcategoria = request.POST.get('subcategoria')
        editor_id = request.POST.get('editor')

        # Validar y limpiar el contenido
        if content:
            content = content.replace('<p>', '').replace('</p>', '')
        else:
            content = contenido.texto  # Mantener el contenido original si no se proporciona uno nuevo

        # Obtener el usuario actual como el autor
        token = obtenerToken(request)
        autor_id = obtenerUserId(token)
        
        # Obtener la categoría y subcategoría
        categoria_obj = Categoria.objects.get(id_categoria=categoria)
        subcategoria_obj = Subcategoria.objects.get(id_subcategoria=subcategoria) if subcategoria else None

        # Actualizar el contenido con los nuevos datos
        contenido.titulo = title
        contenido.texto = content
        contenido.imagen = image if image else contenido.imagen  # Mantener la imagen original si no se sube una nueva
        contenido.categoria = categoria_obj
        contenido.subcategoria = subcategoria_obj
        contenido.editor_id = editor_id
        contenido.autor_id = autor_id  # Mantener el autor actual

        # Guardar los cambios en el contenido
        contenido.save()

        # Redireccionar a la lista de contenidos después de guardar
        return redirect('gestion_contenido')

    contexto = {
        'contenido': contenido,
        'editores': editores,
        'categorias': categorias,
        'sub_json': sub_json,
    }

    # Renderizar el formulario de edición con los datos actuales del contenido
    return render(request, 'editar_contenido.html', contexto)


def tablero_kanban(request):
    # Obtener artículos filtrados por estado
    borrador = Contenido.objects.filter(estado='Borrador')
    en_revision = Contenido.objects.filter(estado='Revisión')
    a_publicar = Contenido.objects.filter(estado='A Publicar')
    publicado = Contenido.objects.filter(estado='Publicado')
    inactivo = Contenido.objects.filter(estado='Inactivo')

    contexto = {
        'borrador': borrador,
        'en_revision': en_revision,
        'a_publicar': a_publicar,
        'publicado': publicado,
        'inactivo': inactivo,
    }

    return render(request, 'tablero_kanban.html', contexto)

def visualizar_contenido(request, pk):
    """
    Despliega la informacion de un solo contenido y los comentarios para ese contenido
    
    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param pk: La clave primaria del contenido a ser desplegado
    :type pk: int
    :return: HttpResponse: La respuesta renderizada con la lista de categorías.
    """
    try:
        contenido = Contenido.objects.get(pk=pk)
        comentarios = Comentario.objects.filter(contenido=pk)
        return render(request,'contenido.html',{'contenido':contenido,'comentarios':comentarios})
    except Contenido.DoesNotExist:
        return JsonResponse({'error': 'Contenido no encontrado'}, status=404)
    
def cambiar_estado(request, pk, estado_actual, estado_siguiente):
    contenido = get_object_or_404(Contenido, pk=pk)
    estados_disponibles = ('Borrador', 'Revisión', 'A Publicar', 'Publicado', 'Inactivo')

    # Verifica que los estados actual y siguiente existan en la lista de estados
    if estado_actual in estados_disponibles and estado_siguiente in estados_disponibles:
        actual = estados_disponibles.index(estado_actual)
        siguiente = estados_disponibles.index(estado_siguiente)

        # Si el estado siguiente no es 'Inactivo' y el estado actual no es 'Publicado'
        if estado_siguiente != 'Inactivo':
            # Verifica que los estados estén uno al lado del otro
            if abs(actual - siguiente) == 1 or estado_actual == 'Inactivo':
                contenido.estado = estado_siguiente
                contenido.save()
                #messages.success(request, "El estado ha sido cambiado exitosamente.")
            #else:
                #messages.error(request, "No se pudo cambiar de estado.")
        else:
            contenido.estado = estado_siguiente
            contenido.save()
            #messages.success(request, "El contenido ha sido inactivado.")
    #else:
        #messages.error(request, "Estados inválidos proporcionados.")

    # Manejar la redirección si HTTP_REFERER no está presente
    referer = request.META.get('HTTP_REFERER')

    if referer:
        return redirect(referer)
    else:
        # Si no hay referer, redirigir a una vista por defecto
        return redirect('tablero_kanban')

def guardar_comentario(request, pk ):
    
    contenido_ = get_object_or_404(Contenido, pk=pk)
    
    if request.method == 'POST':
        comentario_ = request.POST.get('comentario')
        if comentario_:
            comentario_ = comentario_.replace('<p>', '').replace('</p>', '')
            nuevo_comentario = Comentario(
                contenido = contenido_,
                comentario = comentario_,
                usuario = request.user,
                active =True
            )
            nuevo_comentario.save()
        else:
           error_message = "El comentario no puede estar vacío."
            
    
    return redirect('visualizar_contenido',pk)
