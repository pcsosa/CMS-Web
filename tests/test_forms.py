from django.test import TestCase
from appcms.forms import CategoriaForm, BusquedaCategoriaForm
from appcms.models import Categoria

class CategoriaFormTest(TestCase):
    def test_categoria_form_valid_data(self):
        """
        Prueba que el formulario de categoría sea válido cuando se proporcionan
        datos correctos.   
        """
        form = CategoriaForm(data={
            'nombre': 'Tecnología',
            'descripcion': 'Categoría relacionada con tecnología.',
        })
        self.assertTrue(form.is_valid())

    def test_categoria_form_invalid_data(self):
        """
        Prueba que el formulario de categoría sea inválido cuando se proporciona
        un nombre demasiado largo.
        """
        form = CategoriaForm(data={
            'nombre': 'T' * 101,  # Excede el máximo de 100 caracteres
            'descripcion': 'Categoría relacionada con tecnología.',
        })
        self.assertFalse(form.is_valid())

    def test_categoria_form_empty_data(self):
        """
        Prueba que el formulario de categoría sea inválido cuando no se proporcionan
        datos.
        """
        form = CategoriaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Debería haber errores para 'nombre' y 'descripcion'