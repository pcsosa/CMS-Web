# myapp/urls.py (Archivo de la aplicación 'myapp')
from django.urls import path,include
from .views import buscar_categorias, crear_categoria, lista_categorias
from . import views
from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', buscar_categorias, name='buscar_categorias'),
    path('admincat/', views.administrar_categorias, name='administrar_categorias'),
    path('lista/', views.lista_categorias, name='lista_categorias'),
    path('eliminar/<int:pk>/',views.eliminar_categoria, name='eliminar_categoria'),
    path('crear/', views.crear_categoria, name='crear_categoria'),
    path('adminsub/', include('subcategorias.urls')),
]