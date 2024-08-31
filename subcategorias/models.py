from django.db import models
from appcms.models import Categoria

# Create your models here.
class Subcategoria(models.Model):
    """
    El modelo Subcategoria representa una subcategoría que está asociada a una categoría principal.
    
    Este modelo se utiliza para organizar y categorizar elementos dentro de una jerarquía de categorías
    en la aplicación.
    
    :param id_subcategoria: Identificador único y autoincremental de la subcategoría.
    :type id_subcategoria: int
    :param nombre: Nombre de la subcategoría.
    :type nombre: str
    :param categoria: Relación con el modelo Categoria, indicando a qué categoría principal pertenece esta subcategoría.
    :type categoria: Categoria
    
    :ivar id_subcategoria: Campo clave primaria autoincremental de la subcategoría.
    :ivar nombre: Campo de texto que almacena el nombre de la subcategoría.
    :ivar categoria: Relación ForeignKey con el modelo Categoria, define la asociación con la categoría principal.
   
    """
    id_subcategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 100)
    categoria = models.ForeignKey(Categoria , on_delete= models.CASCADE)
    
    def __str__(self):
        """
        Representación en cadena de la subcategoría.

        :return: El nombre de la subcategoría.
        :rtype: str
        """
        return self.nombre
    


