from django.shortcuts import render, redirect
from .models import ContenidoForm

def crear_contenido(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_contenidos')  # Redirige a donde lo necesites
    else:
        form = ContenidoForm()
    return render(request, 'crear_contenido.html', {'form': form})
