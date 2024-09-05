from django.db import models
from django import forms

class Contenido(models.Model):
    titulo = models.CharField(max_length=255)  # Campo para el título del contenido
    texto = models.TextField()  # Campo para el texto
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)  # Campo para la imagen
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    fecha_actualizacion = models.DateTimeField(auto_now=True)  # Fecha de actualización automática

    class Meta:
        verbose_name_plural = "Contenidos"

    def __str__(self):
        return self.titulo

class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'texto', 'imagen']