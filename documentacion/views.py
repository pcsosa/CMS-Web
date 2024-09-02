from django.shortcuts import render

def documentation_view(request):
    # Renderiza la página principal de la documentación generada por Sphinx
    return render(request, 'index.html')  # Asegúrate de que 'index.html' esté en 'docs/_build/html'
