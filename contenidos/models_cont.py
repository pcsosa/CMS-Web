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
    """
    Modelo que representa un contenido en el sistema.

    :param titulo: Título del contenido, con un máximo de 255 caracteres.
    :param texto: Texto completo del contenido.
    :param imagen: Imagen opcional asociada al contenido, almacenada en la carpeta 'imagenes/'.
    :param fecha_creacion: Fecha en que el contenido fue creado, asignada automáticamente.
    :param fecha_actualizacion: Fecha de la última actualización del contenido, asignada automáticamente.
    """
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
    fecha_modificacion = models.DateTimeField(auto_now=True)  # Se actualiza en cada modificación
    
    def obtener_imagen(self):
        if self.imagen:
            return self.imagen.url
        elif self.imagen_url:
            return self.imagen_url
        return None

    class Meta:
        """
        Metadatos para el modelo Contenido.

        :param verbose_name_plural: Nombre en plural de la clase.
        :param app_label: Etiqueta de la aplicación asociada.
        :param db_table: Nombre de la tabla en la base de datos.
        """
        verbose_name_plural = "Contenidos"
        app_label = 'contenidos'

    def __str__(self):
        """
        Representación en cadena del contenido.

        :return: El título del contenido.
        :rtype: str
        """
        return self.titulo

class ContenidoForm(forms.ModelForm):
    """
    Formulario para el modelo Contenido.

    :param model: El modelo asociado al formulario.
    :param fields: Los campos que serán utilizados en el formulario.
    """
    class Meta:
        model = Contenido
        fields = ['tipo', 'titulo', 'texto', 'imagen', 'imagen_url', 'categoria', 'subcategoria', 'estado', 'autor_id', 'editor_id', 'publicador_id', 'id_historial_mod']
