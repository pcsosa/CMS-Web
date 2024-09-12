from django.contrib.auth.models import User  # Para manejar el publicador
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models_cont import ContenidoForm, Contenido, Categoria
from appcms.models import Categoria
from appcms.utils.utils import obtenerUserId
import requests

def crear_contenido(request):
    editores = [
    {'id': 1, 'nombre': 'Editor 1'},
    {'id': 2, 'nombre': 'Editor 2'},
    {'id': 3, 'nombre': 'Editor 3'},
    ]
    print("================================================================= EDITORES")
    print(editores)

    if request.method == 'POST':
        # Obtener datos del formulario
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        categoria_id = request.POST.get('categoria')
        subcategoria_id = request.POST.get('subcategoria')

        # Obtener el usuario autenticado


        # Verificar que los campos requeridos no estén vacíos
        if not title or not content or not categoria_id:
            return render(request, 'crear_contenido.html', {
                'error': 'Título, contenido y categoría son campos requeridos.'
            })

        # Obtener la categoría obligatoria
        #categoria = Categoria.objects.get(id=categoria_id)
        #print("================================================================= CATEGORIAS")
        #print(categoria)

        # Obtener la subcategoría opcional si se proporciona
        #subcategoria = obtener_subcategorias(categoria_id)
        #print("================================================================= SUBCATEGORIAS")
        #print(subcategoria)

        # Obtener el usuario actual como el publicador
        token = request.session.get("token")
        autor = obtenerUserId(token)
        print(autor)

    # Obtener el usuario actual como el publicador
        #editor = request.user if request.user.is_authenticated else None

        # Obtener el usuario actual como el publicador
        publicador = request.user if request.user.is_authenticated else None

        # Crear y guardar el nuevo contenido
        nuevo_contenido = Contenido(
            titulo=title,
            texto=content,
            imagen=image,  # Asigna la imagen si se proporciona
            categoria=categoria_id,
            subcategoria=subcategoria_id,
            publicador=publicador,  # Asigna el publicador automáticamente
            estado='Borrador'  # Estado inicial automático
            
        )
        nuevo_contenido.save()

        # Redireccionar después de guardar
        #return redirect('lista_contenidos')

        # Renderizar el formulario si la solicitud no es POST
    categorias = Categoria.objects.all()  # Obtener todas las categorías para mostrarlas en el formulario

    return render(request, 'crear_contenido.html', {'editores': editores,'categorias': categorias})

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
