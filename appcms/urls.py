# myapp/urls.py 
from django.urls import path,include
from .views import buscar_categorias, crear_categoria, lista_categorias
from . import views
from .views import Home

"""
    URL para la aplicación 'appcms'.

    Este módulo define la ruta de las URL para la aplicación 'appcms', mapeando los
    patrones de URL a sus vistas correspondientes.

    Rutas disponibles:
    - Página de inicio: Mapea la URL raíz a la vista `Home`.
    - Búsqueda: Mapea '/search/' a la vista `buscar_categorias`.
    - Administración de Categorías: Mapea '/admincat/' a la vista `administrar_categorias`.
    - Lista de Categorías: Mapea '/lista/' a la vista `lista_categorias`.
    - Eliminación de Categorías: Mapea '/eliminar/<int:pk>/' a la vista `eliminar_categoria`.
    - Creación de Categorías: Mapea '/crear/' a la vista `crear_categoria`.
    - Subcategorías: Incluye los patrones de URL de la aplicación 'subcategorias'.
"""
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', buscar_categorias, name='buscar_categorias'),
    path('admincat/', views.administrar_categorias, name='administrar_categorias'),
    path('lista/', views.lista_categorias, name='lista_categorias'),
    path('eliminar/<int:pk>/',views.eliminar_categoria, name='eliminar_categoria'),
    path('crear/', views.crear_categoria, name='crear_categoria'),
    path('adminsub/', include('subcategorias.urls')),
]
