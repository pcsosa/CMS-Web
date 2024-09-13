# appcms/forms.py
# appcms/forms.py
from django import forms
from .models import Categoria,Contenido

class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear una subcategoria nueva.
    
    :meta: Forma relacionada con el modelo UserProfile.
    :fields: Los campos que se incluirán en el formulario.
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'texto', 'imagen']
