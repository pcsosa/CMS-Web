from django.test import TestCase
from appcms.models import Categoria
from .models import Subcategoria
from .forms import SubcategoriaForm

class SubcategoriaFormTests(TestCase):
    """
    Pruebas unitarias para el formulario de SubcategoriaForm.
    """

    def setUp(self):
        """
        Configura el entorno para las pruebas creando una instancia de Categoria.

        :meta: Método de configuración antes de cada prueba.
        :ivar categoria: Instancia de Categoria creada para ser usada en las pruebas.
        """
        self.categoria = Categoria.objects.create(nombre='Categoria 1')
    
    def test_form_valid_data(self):
        """
        Prueba que el formulario acepta datos válidos.

        :meta: Verifica que el formulario es válido con datos correctos.
        :assert: Comprueba que el formulario es válido y que la subcategoría se guarda correctamente.
        """
        form_data = {'nombre': 'Subcategoria Válida', 'categoria': self.categoria.pk}
        form = SubcategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(Subcategoria.objects.filter(nombre='Subcategoria Válida').exists())
    
    def test_form_nombre_vacio(self):
        """
        Prueba que el formulario no acepta un nombre vacío.

        :meta: Verifica que el formulario no es válido con un nombre vacío.
        :assert: Comprueba que se muestra el mensaje de error adecuado cuando el nombre está vacío.
        """
        form_data = {'nombre': '', 'categoria': self.categoria.pk}
        form = SubcategoriaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        # Espera el mensaje predeterminado de Django
        self.assertEqual(form.errors['nombre'], ['Este campo es obligatorio.'])
    
    def test_form_nombre_duplicado(self):
        """
        Prueba que el formulario no acepta nombres duplicados.

        :meta: Verifica que el formulario no es válido si el nombre ya existe.
        :assert: Comprueba que se muestra el mensaje de error adecuado cuando el nombre está duplicado.
        """
        Subcategoria.objects.create(nombre='Subcategoria Duplicada', categoria=self.categoria)
        form_data = {'nombre': 'Subcategoria Duplicada', 'categoria': self.categoria.pk}
        form = SubcategoriaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertEqual(form.errors['nombre'], ['Ya existe Subcategoria con este Nombre.'])
    
    def test_form_categoria_no_seleccionada(self):
        """
        Prueba que el formulario no acepta una categoría no seleccionada.

        :meta: Verifica que el formulario no es válido si la categoría no está seleccionada.
        :assert: Comprueba que se muestra el mensaje de error adecuado cuando no se selecciona una categoría.
        """
        form_data = {'nombre': 'Subcategoria Sin Categoria', 'categoria': ''}
        form = SubcategoriaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('categoria', form.errors)
        self.assertEqual(form.errors['categoria'], ['Este campo es obligatorio.'])
