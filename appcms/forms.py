# appcms/forms.py
# appcms/forms.py
from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class BusquedaCategoriaForm(forms.Form):
    consulta = forms.CharField(label='Buscar', max_length=100)
