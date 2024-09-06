# cmsweb/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from contenidos import views_cont


"""
URL para la aplicación 'cmsweb'.

Este módulo define las rutas de URL para la aplicación 'cmsweb', mapeando los
patrones de URL a sus vistas correspondientes.

"""

urlpatterns = [
    path('', views.home, name='home'),
    path('panel/', views.panel, name='panel'),
    path('search/', views.buscar_categorias, name='buscar_categorias'),
    path('admincat/', views.lista_categorias, name='lista_categorias'),
    path('editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('crear/', views.crear_categoria, name='crear_categoria'),
    path('list_cat/', views.listar_categorias, name='listar_categorias'),
    path('adminsub/', include('subcategorias.urls')),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('logout/', views.logout, name='logout'),
    path('crear_cont/', views_cont.crear_contenido, name='crear_contenido'),
    path('list_cont/', views_cont.lista_contenidos, name='lista_contenidos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
