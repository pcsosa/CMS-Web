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
