from django.db import models
from django import forms
from appcms.models import Categoria
from subcategorias.models import Subcategoria

class Contenido(models.Model):
    """
    Modelo que representa el contenido que puede ser de tipo Blog o Multimedia.

    :param id: Clave primaria generada automáticamente para el contenido.
    :param tipo: Tipo de contenido (Blog o Multimedia).
    :param estado: Estado del contenido (Borrador, Revisión, A Publicar, Publicado, Inactivo).
    :param titulo: Título del contenido, con un máximo de 255 caracteres.
    :param texto: Texto del contenido.
    :param imagen: Imagen asociada al contenido, que se sube a la carpeta 'multimedia/'.
    :param imagen_url: URL de una imagen externa asociada al contenido.
    :param categoria: Relación de clave foránea a la categoría a la que pertenece el contenido.
    :param subcategoria: Relación de clave foránea a la subcategoría a la que pertenece el contenido (opcional).
    :param id_historial_mod: ID del historial de modificaciones del contenido (opcional).
    :param publicador_id: ID del publicador asociado al contenido (opcional).
    :param autor_id: ID del autor del contenido (opcional).
    :param editor_id: ID del editor del contenido (opcional).
    :param fecha_creacion: Fecha y hora de creación automática del contenido.
    """
    
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
        """
        Obtiene la URL de la imagen asociada al contenido.

        :return: La URL de la imagen si existe; de lo contrario, retorna None.
        :rtype: str or None
        """
        if self.imagen:
            return self.imagen.url
        elif self.imagen_url:
            return self.imagen_url
        return None

    class Meta:
        """
        Clase que define las opciones de configuración para el modelo Contenido.

        :param verbose_name_plural: Nombre plural del modelo en la interfaz de administración.
        :param app_label: Etiqueta del nombre de la aplicación a la que pertenece el modelo.
        """
        verbose_name_plural = "Contenidos"
        app_label = 'contenidos'

    def __str__(self):

        return self.titulo

class ContenidoForm(forms.ModelForm):
    """
    Formulario para el modelo Contenido.

    Este formulario permite la creación y edición de instancias del modelo Contenido,
    incluyendo la validación de los datos proporcionados por el usuario.
    """
    class Meta:
        """
        Clase que define las opciones de configuración para el formulario ContenidoForm.

        :param model: El modelo relacionado con este formulario, en este caso, Contenido.
        :param fields: Lista de campos que se incluirán en el formulario.
        """
        model = Contenido
        fields = ['tipo', 'titulo', 'texto', 'imagen', 'imagen_url', 'categoria', 'subcategoria', 'estado', 'autor_id', 'editor_id', 'publicador_id', 'id_historial_mod']
