from django.db import models

class Categoria(models.Model):
    """
    Modelo que representa una categoría en el sistema.

    :param id_categoria: Clave primaria de la categoría.
    :param nombre: Nombre de la categoría, único en el sistema, con un máximo de 100 caracteres.
    :param descripcion: Descripción detallada de la categoría, con un máximo de 500 caracteres.
    """

    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=500)
    
    def __str__(self):
        """
        Representación en cadena de la categoría.

        :return: El nombre de la categoría.
        :rtype: str
        """
        return self.nombre

    def get_descripcion(self):
        """
        Obtiene la descripción de la categoría.

        :return: La descripción de la categoría.
        :rtype: str
        """
        return self.descripcion

class Contenido(models.Model):
    titulo = models.CharField(max_length=255)  # Campo para el título del contenido
    texto = models.TextField()  # Campo para el texto
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)  # Campo para la imagen
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    fecha_actualizacion = models.DateTimeField(auto_now=True)  # Fecha de actualización automática

    def __str__(self):
        return self.titulo




