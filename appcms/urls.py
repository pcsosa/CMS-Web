# myapp/urls.py (Archivo de la aplicación 'myapp')
from django.urls import path
from .views import buscar_categorias, crear_categoria, lista_categorias, crear_subcategorias
from . import views
from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', buscar_categorias, name='buscar_categorias'),
    path('admincat/', views.administrar_categorias, name='administrar_categorias'),
    path('lista/', views.lista_categorias, name='lista_categorias'),
    path('crear/', views.crear_categoria, name='crear_categoria'),
    path('lista/', views.lista_categorias, name='lista_categorias'),
    path('crear_subcategorias/', views.crear_subcategorias, name='crear_subcategorias'),
    path('listar_sub/', views.lista_subcategorias, name='lista_subcategorias'),
]