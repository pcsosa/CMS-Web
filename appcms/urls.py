# myapp/urls.py (Archivo de la aplicación 'myapp')
from django.urls import path
from .views import buscar_categorias
from . import views
from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', buscar_categorias, name='buscar_categorias'),
]
