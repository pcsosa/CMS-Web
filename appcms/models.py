from django.db import models

class Categoria(models.Model):
    """
    Modelo que representa una categoría en el sistema.

    Attributes:
        id_categoria (AutoField): Clave primaria de la categoría.
        nombre (CharField): Nombre de la categoría, único en el sistema, con un máximo de 100 caracteres.
        descripcion (CharField): Descripción detallada de la categoría, con un máximo de 500 caracteres.
    """
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=500)
    
    
    def __str__(self): 
        """
        Representación en cadena del modelo `Categoria`.

        Returns:
            str: El nombre de la categoría.
        """
        return self.nombre

    def get_descripcion(self):
        """
        Representación en cadena del modelo `Categoria`.

        Returns:
            str: la descripcion de la categoría.
        """
        return self.descripcion
        
    




