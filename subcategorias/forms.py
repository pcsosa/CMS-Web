from django import forms
from .models import Subcategoria
class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre','categoria']