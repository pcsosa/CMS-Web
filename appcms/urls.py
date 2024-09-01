# myapp/urls.py (Archivo de la aplicación 'myapp')
from django.urls import path,include
from .views import buscar_categorias, crear_categoria, lista_categorias
from . import views
from .views import Home
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', buscar_categorias, name='buscar_categorias'),
    path('admincat/', views.administrar_categorias, name='administrar_categorias'),
    path('lista/', views.lista_categorias, name='lista_categorias'),

    path('crear/', views.crear_categoria, name='crear_categoria'),
    path('lista/', views.lista_categorias, name='lista_categorias'),
    path('adminsub/', include('subcategorias.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]