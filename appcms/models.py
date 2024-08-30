from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=500)
    padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategorias')

    """ def __str__(self): 
            return self.nombre

        def get_descripcion(self):
            return self.descripcion
        """
class subcategoria(models.Model):
    id_subcategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 100)
    categoria = models.ForeignKey(Categoria , on_delete= models.CASCADE)
    
    def __str__(self):
        return self.nombre
    


