from django.db import models
from contenidos.models_cont import Contenido

class Comment(models.Model):
    contenido = models.ForeignKey(Contenido,on_delete=models.CASCADE,related_name='comments')
    usuario = models.CharField(max_length=80)
    email = models.EmailField()
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return 'Comentario {} por {}'.format(self.body, self.name)
