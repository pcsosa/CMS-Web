# appcms/forms.py
# appcms/forms.py
from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear una subcategoria nueva.
    
    :meta: Forma relacionada con el modelo UserProfile.
    :fields: Los campos que se incluirán en el formulario.
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
