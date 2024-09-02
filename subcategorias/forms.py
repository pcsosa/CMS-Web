# subcategorias/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Subcategoria

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
            """
            Valida el campo 'nombre' del formulario.

            :raises ValidationError: Si el nombre está vacío, solo contiene espacios,
                                     o si ya existe en la base de datos (insensible a mayúsculas).
            :returns: El nombre validado si pasa todas las validaciones.
            """
            nombre = self.cleaned_data.get('nombre')
            
            # Validar que el nombre no esté vacío o solo contenga espacios
            if not nombre.strip():
                raise ValidationError(_('El nombre no puede estar vacío o solo contener espacios.'))

            # Validar que el nombre no exista ya en la base de datos
            if Subcategoria.objects.filter(nombre__iexact=nombre).exists():
                raise ValidationError(_('Ya existe Subcategoria con este Nombre.'))
            
            return nombre
        
        def clean_categoria(self):
            """
            Valida el campo 'categoria' del formulario.

            :raises ValidationError: Si la categoría no está seleccionada o es None.
            :returns: La categoría validada si pasa todas las validaciones.
            """
            categoria = self.cleaned_data.get('categoria')
            
            # Validar que la categoría no sea None (o en blanco)
            if not categoria:
                raise ValidationError(_('Debe seleccionar una categoría.'))
            
            return categoria
