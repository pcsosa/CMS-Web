# appcms/forms.py
# appcms/forms.py
from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    """
    Formulario para el modelo Categoria.
        Este formulario utiliza el modelo Categoria para crear o actualizar instancias.
        
    Clase Meta:
        :model (models.Model): El modelo asociado a este formulario.
        :fields (list): Lista de campos que se incluirán en el formulario,incluye los campos nombre y descripcion.
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class BusquedaCategoriaForm(forms.Form):
    """
    Formulario para buscar instancias del modelo Categoria.
        Este formulario permite realizar búsquedas por el campo consulta.

    Attributes:
        consulta (forms.CharField): Campo de texto para introducir texto de busqueda.
    """
    consulta = forms.CharField(label='Buscar', max_length=100)
