# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models_cont import ContenidoForm, Contenido

def crear_contenido(request):
    """if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_contenidos')  # Redirige a donde lo necesites
    else:
        form = ContenidoForm()
    return render(request, 'crear_contenido.html', {'form': form})"""
    if request.method == 'POST':
        # Obtener datos del formulario
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Verificar que los campos requeridos no estén vacíos
        if not title or not content:
            return render(request, 'crear_contenido.html', {
                'error': 'Título y contenido son campos requeridos.'
            })

        # Crear y guardar el nuevo contenido
        nuevo_contenido = Contenido(
            titulo=title,
            texto=content,
            imagen=image  # Asigna la imagen si se proporciona
        )
        nuevo_contenido.save()

        # Redireccionar después de guardar
        return redirect('lista_contenidos')

    # Renderizar el formulario si la solicitud no es POST
    return render(request, 'crear_contenido.html')



def lista_contenidos(request):
    contenidos = Contenido.objects.all()
    return render(request, 'lista_contenidos.html', {'contenidos': contenidos})
  
def gestion_contenido(request):
    contenidos = Contenido.objects.all()
    return render(request, 'gestion_contenido.html', {'contenidos': contenidos})
  
def editar_contenido(request):
  # Falta codigo para editar contenido
  return render(request, 'editar_contenido.html')

def eliminar_contenido(request):
  # Falta codigo para eliminar contenido
  return render(request, 'eliminar_contenido.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['file']
        # Guardar la imagen en el servidor
        image_url = 'ruta/donde/guardas/la/imagen/' + image.name
        # Retornar la URL de la imagen
        return JsonResponse({'location': image_url})
