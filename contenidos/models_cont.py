from django import forms
from django.db import models

from appcms.models import Categoria
from subcategorias.models import Subcategoria


class Contenido(models.Model):
    """Representa el contenido que puede ser de tipo Blog o Multimedia."""

    # Opciones para el tipo de contenido
    TIPO_CONTENIDO = [
        ("Blog", "Blog"),
        ("Multimedia", "Multimedia"),
    ]

    # Opciones para el estado del contenido
    ESTADO_CONTENIDO = [
        ("Borrador", "Borrador"),
        ("Revisión", "Revisión"),
        ("A Publicar", "A Publicar"),
        ("Publicado", "Publicado"),
        ("Inactivo", "Inactivo"),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CONTENIDO)
    estado = models.CharField(
        max_length=20, choices=ESTADO_CONTENIDO, default="Borrador"
    )
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
    imagen = models.ImageField(
        upload_to="multimedia/", blank=True, null=True
    )  # Para imágenes subidas
    imagen_url = models.URLField(
        blank=True, null=True
    )  # Para imágenes desde una URL externa
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="contenidos"
    )  # Categoría obligatoria
    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subcontenidos",
    )  # Subcategoría opcional
    id_historial_mod = models.IntegerField(
        null=True, blank=True
    )  # ID del historial de modificaciones
    publicador_id = models.CharField(
        max_length=255, null=True, blank=True
    )  # Almacena el ID de Keycloak
    autor_id = models.CharField(max_length=255, null=True, blank=True)
    editor_id = models.CharField(max_length=255, null=True, blank=True)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )  # Fecha de creación automática
    fecha_modificacion = models.DateTimeField(
        auto_now=True
    )  # Se actualiza en cada modificación

    megusta = models.PositiveIntegerField(default=0)  # Número de "me gusta"
    visualizaciones = models.PositiveIntegerField(default=0)  # Número de visualizaciones
    

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
        app_label = "contenidos"

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
        fields = [
            "tipo",
            "titulo",
            "texto",
            "imagen",
            "imagen_url",
            "categoria",
            "subcategoria",
            "estado",
            "autor_id",
            "editor_id",
            "publicador_id",
            "id_historial_mod",
        ]


class Comentario(models.Model):
    """
    Modelo que representa un comentario asociado a un contenido específico.

    Atributos:
        contenido (ForeignKey): Referencia al contenido relacionado con este comentario.
        usuario (str): Nombre del usuario que realizó el comentario.
        email (EmailField): Dirección de correo del usuario.
        comentario (TextField): Texto del comentario.
        fecha (DateTimeField): Fecha en que fue creado el comentario.
        active (bool): Indica si el comentario está activo y es visible.

    Meta:
        ordering (list): Ordena los comentarios por fecha, mostrando los más recientes primero.

    Métodos:
        __str__: Devuelve una representación en cadena del comentario, incluyendo el texto del comentario y el usuario que lo realizó.
    """

    contenido = models.ForeignKey(
        Contenido, on_delete=models.CASCADE, related_name="comments"
    )
    usuario = models.CharField(max_length=255)
    email = models.EmailField()
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return "Comentario {} por {}".format(self.comentario, self.usuario)

class ComentarioRoles(models.Model):
    """
    Modelo que representa un comentario asociado a un contenido específico.

    Atributos:
        contenido (ForeignKey): Referencia al contenido relacionado con este comentario.
        usuario (str): Nombre del usuario que realizó el comentario.
        email (EmailField): Dirección de correo del usuario.
        comentario (TextField): Texto del comentario.
        fecha (DateTimeField): Fecha en que fue creado el comentario.
        active (bool): Indica si el comentario está activo y es visible.

    Meta:
        ordering (list): Ordena los comentarios por fecha, mostrando los más recientes primero.

    Métodos:
        __str__: Devuelve una representación en cadena del comentario, incluyendo el texto del comentario y el usuario que lo realizó.
    """

    contenido = models.ForeignKey(
        Contenido, on_delete=models.CASCADE, related_name="comment_Roles"
    )
    usuario = models.CharField(max_length=255)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return "Comentario {} por {}".format(self.comentario, self.usuario)

class Visualizacion(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
class Historico(models.Model):
    titulo = models.CharField(max_length=255)
    usuario = models.CharField(max_length=255)
    accion = models.CharField(max_length=50, choices=[
        ('CREADO','CREADO'), ('EDITADO','EDITADO'), ('ELIMINADO','ELIMINADO'), ('PUBLICADO','PUBLICADO'), 
        ('ENVIADO A BORRADOR','ENVIADO A BORRADOR'),
        ('ENVIADO A PUBLICAR','ENVIADO A PUBLICAR'),('ENVIADO A EDICION','ENVIADO A EDICION')
    ])
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Histórico de Contenido"
        verbose_name_plural = "Históricos de Contenidos"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.contenido} - {self.accion} - {self.fecha}"
