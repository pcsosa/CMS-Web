from django.contrib.auth.models import User  # Para manejar el publicador
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from contenidos.forms import ComentarioForm
from .models_cont import Comentario, ContenidoForm, Contenido, Categoria
from appcms.models import Categoria
from subcategorias.models import Subcategoria
from appcms.utils.utils import obtenerUserId, obtenerUsersConRol
from django.core.serializers import serialize
import requests, json

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages

def crear_contenido(request):
  
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
        token = request.session.get("token")
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
    contenidos = Contenido.objects.all()  # Obtén todos los contenidos
    return render(request, 'lista_contenidos.html', {'contenidos': contenidos})

def gestion_contenido(request):
    contenidos = Contenido.objects.all()
    return render(request, 'gestion_contenido.html', {'contenidos': contenidos})
  
def editar_contenido(request):
  # Falta codigo para editar contenido
  return render(request, 'editar_contenido.html')


@csrf_exempt
def upload_image(request):
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
        token = request.session.get("token")
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

def dejar_comentario(request, id):
    contenido = get_object_or_404(Contenido, contenido_id=id)
    
    if request.method == 'POST':
        comentario_form = ComentarioForm(data=request.POST)
        if comentario_form.is_valid():
            print("Errores en el formulario:", comentario_form.errors) 
            nuevo_comentario = comentario_form.save(commit=False)
            nuevo_comentario.contenido = contenido
            nuevo_comentario.active = True
            nuevo_comentario.save()
            return redirect('visualizar_contenido', contenido_id=contenido.id)  
    else:
        comentario_form = ComentarioForm()

    comentarios = Comentario.objects.filter(contenido=contenido, active=True)
    print("Comentarios recuperados:", comentarios)

    return render(request, 'contenido.html', {
        'contenido': contenido,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
    })

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
        return render(request,'contenido.html',{'contenido':contenido})
    except Contenido.DoesNotExist:
        return JsonResponse({'error': 'Contenido no encontrado'}, status=404)
    
def cambiar_estado(request,pk,estado_actual,estado_siguiente):
    
    contenido = get_object_or_404(Contenido, pk=pk)
    estados_disponibles = ('Borrador', 'Revisión', 'A Publicar', 'Publicado', 'Inactivo')

    # Verifica que los estados actual y siguiente existan en la lista de estados
    if estado_actual in estados_disponibles and estado_siguiente in estados_disponibles:
        actual = estados_disponibles.index(estado_actual)
        siguiente = estados_disponibles.index(estado_siguiente)

        # Si el estado siguiente no es 'Inactivo' y el estado actual no es 'Publicado'
        if (estado_siguiente != 'Inactivo') and (estado_actual != 'Publicado'):
            
            # Verifica que los estados estén uno al lado del otro
            if abs(actual - siguiente) == 1 or estado_actual=='Inactivo':
                contenido.estado = estado_siguiente
                contenido.save()
                return redirect('visualizar_contenido', pk)
            else:
                messages.error(request, "No se pudo cambiar de estado")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            contenido.estado = estado_siguiente
            contenido.save()
            return redirect('visualizar_contenido', pk)
