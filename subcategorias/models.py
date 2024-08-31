from django.db import models
from appcms.models import Categoria

# Create your models here.
class Subcategoria(models.Model):
    id_subcategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 100)
    categoria = models.ForeignKey(Categoria , on_delete= models.CASCADE)
    
    def __str__(self):
        return self.nombre
    


