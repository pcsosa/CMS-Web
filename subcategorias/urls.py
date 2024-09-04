from django.urls import path
from . import views

urlpatterns =[
    path('',views.administrar_subcategorias, name='administrar_subcategorias'),
    path('crear/',views.crear_subcategoria, name='crear_subcategorias'),
    path('lista/', views.lista_subcategorias, name='lista_subcategorias'),
    path('eliminar/<int:pk>/',views.eliminar_subcategoria, name='eliminar_subcategoria'),
     path('editar/<int:pk>/',views.editar_subcategoria, name='editar_subcategoria'),
]
