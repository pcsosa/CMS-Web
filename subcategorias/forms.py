# subcategorias/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Subcategoria
import re

class SubcategoriaForm(forms.ModelForm):
    """
    Formulario para crear una nueva subcategoría.
    
    :meta: Forma relacionada con el modelo Subcategoria.
    :fields: Los campos que se incluirán en el formulario.
    """
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'categoria']
        
        def clean_nombre(self):
            nombre = self.cleaned_data.get('nombre')
            
            # Validar que el nombre no esté vacío o solo contenga espacios
            if not nombre.strip():
                raise ValidationError(_('El nombre no puede estar vacío o solo contener espacios.'))
            
            # Validar que el nombre no contenga símbolos no permitidos
            if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                raise ValidationError(_('El nombre solo puede contener letras, números y espacios.'))
            
            # Validar que el nombre no exista ya en la base de datos
            if Subcategoria.objects.filter(nombre__iexact=nombre).exists():
                raise ValidationError(_('Ya existe Subcategoria con este Nombre.'))
            
            return nombre
        
        
        def clean_categoria(self):
            categoria = self.cleaned_data.get('categoria')
            
            # Validar que la categoría no sea None (o en blanco)
            if not categoria:
                raise ValidationError(_('Debe seleccionar una categoría.'))
            
            return categoria