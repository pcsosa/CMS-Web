from django.contrib.auth.models import User  # Para manejar el publicador
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models_cont import ContenidoForm, Contenido, Categoria
from appcms.models import Categoria
from subcategorias.models import Subcategoria
from appcms.utils.utils import obtenerUserId, obtenerUsersConRol
from django.core.serializers import serialize
import requests, json

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
        content = content.replace('<p>', '').replace('</p>', '')
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
        return redirect('lista_contenidos')

    contexto = {
        'editores': editores,
        'categorias': categorias,
        'sub_json': sub_json
    }

    # Renderizar el formulario si la solicitud no es POST
    return render(request, 'crear_contenido.html', contexto)

def lista_contenidos(request):
    contenidos = Contenido.objects.all()  # Obtén todos los contenidos
    return render(request, 'listar_contenidos.html', {'contenidos': contenidos})

def obtener_subcategorias(categoria_id):
    # Obtener la categoría seleccionada
    try:
        categoria = Categoria.objects.get(id=categoria_id)
        # Obtener las subcategorías relacionadas
        subcategorias = Categoria.objects.filter(padre=categoria)
        print("=============================================SUBCATEGORIAS")
        print(subcategorias)
        subcategorias_list = [{'id': subcategoria.id, 'nombre': subcategoria.nombre} for subcategoria in subcategorias]
        return JsonResponse({'subcategorias': subcategorias_list})
    except Categoria.DoesNotExist:
        return JsonResponse({'error': 'Categoría no encontrada'}, status=404)


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['file']
        # Guardar la imagen en el servidor
        image_url = 'ruta/donde/guardas/la/imagen/' + image.name
        # Retornar la URL de la imagen
        return JsonResponse({'location': image_url})
