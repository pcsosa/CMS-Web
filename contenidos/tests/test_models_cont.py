from django.test import TestCase
from appcms.models import Categoria
from subcategorias.models import Subcategoria
from contenidos.models import Contenido

class ContenidoModelTest(TestCase):
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.subcategoria = Subcategoria.objects.create(nombre="Móviles", categoria=self.categoria)
        self.contenido = Contenido.objects.create(
            tipo='Blog',
            estado='Publicado',
            titulo='El futuro de los móviles',
            texto='Contenido acerca de los nuevos móviles del mercado.',
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            autor_id='autor1',
            editor_id='editor1',
            publicador_id='publicador1'
        )
    
    def test_contenido_creation(self):
        """Prueba que el modelo Contenido se crea correctamente."""
        self.assertEqual(self.contenido.titulo, 'El futuro de los móviles')
        self.assertEqual(self.contenido.tipo, 'Blog')
        self.assertEqual(self.contenido.estado, 'Publicado')
        self.assertEqual(self.contenido.autor_id, 'autor1')

    def test_str_method(self):
        """Prueba que el método __str__ devuelve el título del contenido."""
        self.assertEqual(str(self.contenido), 'El futuro de los móviles')

    def test_obtener_imagen_con_imagen_subida(self):
        """Prueba que obtener_imagen devuelve la URL de la imagen subida."""
        self.contenido.imagen = 'multimedia/test_image.jpg'
        self.contenido.save()
        self.assertEqual(self.contenido.obtener_imagen(), '/media/multimedia/test_image.jpg')

    def test_obtener_imagen_con_imagen_url(self):
        """Prueba que obtener_imagen devuelve la imagen de una URL externa."""
        self.contenido.imagen_url = 'http://example.com/image.jpg'
        self.assertEqual(self.contenido.obtener_imagen(), 'http://example.com/image.jpg')

    def test_obtener_imagen_sin_imagen(self):
        """Prueba que obtener_imagen devuelve None si no hay imagen o URL."""
        self.assertIsNone(self.contenido.obtener_imagen())
