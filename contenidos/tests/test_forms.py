from django.test import TestCase
from contenidos.forms import ContenidoForm
from appcms.models import Categoria
from subcategorias.models import Subcategoria

class ContenidoFormTest(TestCase):
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.subcategoria = Subcategoria.objects.create(nombre="Móviles", categoria=self.categoria)
    
    def test_form_valid_data(self):
        """Prueba que el formulario es válido con los datos correctos."""
        form_data = {
            'tipo': 'Blog',
            'titulo': 'El futuro de los móviles',
            'texto': 'Contenido acerca de los nuevos móviles del mercado.',
            'estado': 'Publicado',
            'categoria': self.categoria.id,
            'subcategoria': self.subcategoria.id,
            'autor_id': 'autor1',
            'editor_id': 'editor1',
            'publicador_id': 'publicador1'
        }
        form = ContenidoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        """Prueba que el formulario no es válido si faltan campos requeridos."""
        form_data = {
            'tipo': 'Blog',
            'titulo': '',
            'texto': 'Contenido acerca de los nuevos móviles del mercado.',
            'estado': 'Publicado',
            'categoria': self.categoria.id,
        }
        form = ContenidoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
    
    def test_form_invalid_choices(self):
        """Prueba que el formulario no es válido si se seleccionan opciones incorrectas."""
        form_data = {
            'tipo': 'Invalido',  # Opción incorrecta
            'titulo': 'El futuro de los móviles',
            'texto': 'Contenido acerca de los nuevos móviles del mercado.',
            'estado': 'Publicado',
            'categoria': self.categoria.id,
        }
        form = ContenidoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo', form.errors)
