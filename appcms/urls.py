# myapp/urls.py (Archivo de la aplicación 'myapp')
from django.urls import path
from . import views
from .views import Home

urlpatterns = [
    # Otras rutas de la aplicación
    path("", Home.as_view(), name="home")
]
