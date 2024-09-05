# cmsweb/urls.py
from django.urls import path, include
from .views import buscar_categorias, crear_categoria, lista_categorias
from . import views
from .views import Home
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


"""
URL para la aplicación 'cmsweb'.

Este módulo define las rutas de URL para la aplicación 'cmsweb', mapeando los
patrones de URL a sus vistas correspondientes.

"""

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', buscar_categorias, name='buscar_categorias'),
    path('admincat/', views.administrar_categorias, name='administrar_categorias'),
    path('lista/', views.lista_categorias, name='lista_categorias'),
    path('eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('crear/', views.crear_categoria, name='crear_categoria'),
    path('cat/', views.interfaz_estandar, name='interfaz_estandar'), #CRUD DE Categorias: p/ ver json views.listar_categorias
    path('list_cat/', views.listar_categorias, name='listar_categorias'),
    path('adminsub/', include('subcategorias.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    #path('list_categorias/', views.list_programmers, name='list_programmers')
    #Debe ser funcional http://127.0.0.1:8000/cat/list_cat/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
