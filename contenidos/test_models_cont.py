from django.test import TestCase
from appcms.models import Categoria
from subcategorias.models import Subcategoria
from contenidos.models_cont import Contenido
from contenidos.models_cont import ContenidoForm

class ContenidoModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Contenido.
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas.

        Se crea una categoría y una subcategoría, y se instancia un objeto Contenido.

        """
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
        """
        Prueba que el modelo Contenido se crea correctamente.

        Se verifica que los atributos del objeto Contenido se han asignado
        correctamente al momento de su creación.

        :return: None
        :rtype: None
        """
        self.assertEqual(self.contenido.titulo, 'El futuro de los móviles')
        self.assertEqual(self.contenido.tipo, 'Blog')
        self.assertEqual(self.contenido.estado, 'Publicado')
        self.assertEqual(self.contenido.autor_id, 'autor1')

    def test_str_method(self):
        """
        Prueba que el método __str__ devuelve el título del contenido.

        Verifica que la representación en cadena del objeto Contenido
        devuelve el título esperado.

        :return: El título del contenido.
        :rtype: str
        """
        self.assertEqual(str(self.contenido), 'El futuro de los móviles')

    def test_obtener_imagen_con_imagen_subida(self):
        """
        Prueba que obtener_imagen devuelve la URL de la imagen subida.

        Se asigna una imagen al objeto Contenido y se verifica que
        el método obtener_imagen retorne la URL correcta de la imagen.

        :return: None
        :rtype: None
        """
        self.contenido.imagen = 'multimedia/test_image.jpg'
        self.contenido.save()
        self.assertEqual(self.contenido.obtener_imagen(), '/media/multimedia/test_image.jpg')

    def test_obtener_imagen_con_imagen_url(self):
        """
        Prueba que obtener_imagen devuelve la imagen de una URL externa.

        Se asigna una URL de imagen al objeto Contenido y se verifica
        que el método obtener_imagen retorne la URL correcta.

        :return: None
        :rtype: None
        """
        self.contenido.imagen_url = 'http://example.com/image.jpg'
        self.assertEqual(self.contenido.obtener_imagen(), 'http://example.com/image.jpg')

    def test_obtener_imagen_sin_imagen(self):
        """
        Prueba que obtener_imagen devuelve None si no hay imagen o URL.

        Verifica que si el objeto Contenido no tiene imagen ni URL,
        el método obtener_imagen retorne None.

        :return: None
        :rtype: None
        """
        self.assertIsNone(self.contenido.obtener_imagen())

class ContenidoFormTest(TestCase):
    """
    Pruebas unitarias para el formulario ContenidoForm.

    :param categoria: Categoría asociada al formulario.
    :param subcategoria: Subcategoría asociada al formulario.
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas del formulario.

        Se crea una categoría y una subcategoría para las pruebas.
        
        :return: None
        :rtype: None
        """
        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.subcategoria = Subcategoria.objects.create(nombre="Móviles", categoria=self.categoria)
    
    def test_form_valid_data(self):
        """
        Prueba que el formulario es válido con los datos correctos.

        Se verifica que al proporcionar datos válidos, el formulario
        se considera válido.

        :return: None
        :rtype: None
        """
        form_data = {
            'tipo': 'Blog',
            'titulo': 'El futuro de los móviles',
            'texto': 'Contenido acerca de los nuevos móviles del mercado.',
            'estado': 'Publicado',
            'categoria': self.categoria.id_categoria,
            'subcategoria': self.subcategoria.id_subcategoria,
            'autor_id': 'autor1',
            'editor_id': 'editor1',
            'publicador_id': 'publicador1'
        }
        form = ContenidoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_required_fields(self):
        """
        Prueba que el formulario no es válido si faltan campos requeridos.

        Se verifica que al faltar el título, el formulario se considere
        inválido y contenga el error correspondiente.

        :return: None
        :rtype: None
        """
        form_data = {
            'tipo': 'Blog',
            'titulo': '',
            'texto': 'Contenido acerca de los nuevos móviles del mercado.',
            'estado': 'Publicado',
            'categoria': self.categoria.id_categoria,
        }
        form = ContenidoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
    
    def test_form_invalid_choices(self):
        """
        Prueba que el formulario no es válido si se seleccionan opciones incorrectas.

        Se verifica que al proporcionar un tipo inválido, el formulario
        se considere inválido y contenga el error correspondiente.

        :return: None
        :rtype: None
        """
        form_data = {
            'tipo': 'Invalido',  # Opción incorrecta
            'titulo': 'El futuro de los móviles',
            'texto': 'Contenido acerca de los nuevos móviles del mercado.',
            'estado': 'Publicado',
            'categoria': self.categoria.id_categoria,
        }
        form = ContenidoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo', form.errors)
