from django.db import models
from django import forms
from appcms.models import Categoria
from subcategorias.models import Subcategoria

class Contenido(models.Model):
    """Representa el contenido que puede ser de tipo Blog o Multimedia."""
    
    # Opciones para el tipo de contenido
    TIPO_CONTENIDO = [
        ('Blog', 'Blog'),
        ('Multimedia', 'Multimedia'),
    ]
    
    # Opciones para el estado del contenido
    ESTADO_CONTENIDO = [
        ('Borrador', 'Borrador'),
        ('Revisión', 'Revisión'),
        ('A Publicar', 'A Publicar'),
        ('Publicado', 'Publicado'),
        ('Inactivo', 'Inactivo'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CONTENIDO)
    estado = models.CharField(max_length=20, choices=ESTADO_CONTENIDO, default='Borrador')
    titulo = models.CharField(max_length=255)  # Campo para el título del contenido
    texto = models.TextField()  # Campo para el texto
    imagen = models.ImageField(upload_to='multimedia/', blank=True, null=True)  # Para imágenes subidas
    imagen_url = models.URLField(blank=True, null=True)  # Para imágenes desde una URL externa
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='contenidos')  # Categoría obligatoria
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, blank=True, null=True, related_name='subcontenidos')  # Subcategoría opcional
    id_historial_mod = models.IntegerField(null=True, blank=True)  # ID del historial de modificaciones
    publicador_id = models.CharField(max_length=255, null=True, blank=True)  # Almacena el ID de Keycloak
    autor_id = models.CharField(max_length=255, null=True, blank=True)
    editor_id = models.CharField(max_length=255, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    
    def obtener_imagen(self):
        if self.imagen:
            return self.imagen.url
        elif self.imagen_url:
            return self.imagen_url
        return None

    class Meta:
        verbose_name_plural = "Contenidos"
        app_label = 'contenidos'

    def __str__(self):
        return self.titulo

class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['tipo', 'titulo', 'texto', 'imagen', 'imagen_url', 'categoria', 'subcategoria', 'estado', 'autor_id', 'editor_id', 'publicador_id', 'id_historial_mod']

class Comentario(models.Model):
    contenido = models.ForeignKey(Contenido,on_delete=models.CASCADE,related_name='comments')
    usuario = models.CharField(max_length=80)
    email = models.EmailField()
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return 'Comentario {} por {}'.format(self.comentario, self.usuario)