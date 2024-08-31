from django import forms
from .models import Subcategoria
class SubcategoriaForm(forms.ModelForm):
    """
    Formulario para crear una subcategoria nueva.
    
    :meta: Forma relacionada con el modelo UserProfile.
    :fields: Los campos que se incluirán en el formulario.
    """
    class Meta:
        model = Subcategoria
        fields = ['nombre','categoria']