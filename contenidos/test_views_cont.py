from django.test import TestCase, Client
from django.urls import reverse
from appcms.models import Categoria
from subcategorias.models import Subcategoria
from contenidos.models_cont import Contenido
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class ContenidoViewsTest(TestCase):
    """
    Pruebas unitarias para las vistas del contenido.

    Esta clase contiene pruebas que verifican el correcto funcionamiento
    de las vistas relacionadas con la gestión de contenidos, incluyendo
    la lista, creación, edición y eliminación de contenidos.
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas.

        Se crea un cliente para simular peticiones, se configura una
        categoría, subcategoría y un contenido inicial. Además, se
        crea un usuario para las pruebas de autenticación.

        :return: None
        :rtype: None
        """
        # Configurar el cliente y crear algunos datos para las pruebas
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.subcategoria = Subcategoria.objects.create(nombre="Móviles", categoria=self.categoria)
        self.contenido = Contenido.objects.create(
            titulo='El futuro de los móviles',
            texto='Texto acerca de móviles',
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            autor_id='autor1',
            editor_id='editor1',
            publicador_id='publicador1'
        )
        self.user = User.objects.create_user(username='editor', password='password')
    
    def test_lista_contenidos_view(self):
        """
        Prueba que la vista lista_contenidos devuelve una respuesta correcta.

        Se verifica que al acceder a la vista, se reciba un código de
        estado 200, se utilice la plantilla adecuada y se muestre el
        contenido creado.

        :return: None
        :rtype: None
        """
        response = self.client.get(reverse('lista_contenidos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista_contenidos.html')
        self.assertContains(response, 'El futuro de los móviles')
    
    def test_crear_contenido_view_get(self):
        """
        Prueba que la vista crear_contenido devuelve un formulario correctamente.

        Se verifica que al acceder a la vista de creación de contenido,
        se reciba un código de estado 200 y se utilice la plantilla
        correcta para mostrar el formulario.

        :return: None
        :rtype: None
        """
        response = self.client.get(reverse('crear_contenido'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crear_contenido.html')
    
    def test_crear_contenido_view_post(self):
        """
        Prueba que se puede crear un contenido a través del formulario.

        Se simula el inicio de sesión de un usuario y se envían datos
        válidos a la vista de creación de contenido. Se verifica que
        se reciba un código de estado 302 (redirección) y que el nuevo
        contenido se haya creado correctamente en la base de datos.

        :return: None
        :rtype: None
        """
        self.client.login(username='editor', password='password')
        
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        
        response = self.client.post(reverse('crear_contenido'), {
            'title': 'Nuevo contenido',
            'content': 'Este es un nuevo contenido',
            'image': image,
            'categoria': self.categoria.id_categoria,
            'subcategoria': self.subcategoria.id_subcategoria,
            'editor': self.user.id,
        })
        
        self.assertEqual(response.status_code, 302)  # Redirección después de crear contenido
        nuevo_contenido = Contenido.objects.get(titulo='Nuevo contenido')
        self.assertIsNotNone(nuevo_contenido)
        self.assertEqual(nuevo_contenido.texto, 'Este es un nuevo contenido')
    
    def test_editar_contenido_view_get(self):
        """
        Prueba que la vista editar_contenido devuelve el formulario correctamente.

        Se verifica que al acceder a la vista de edición de contenido,
        se reciba un código de estado 200, se utilice la plantilla
        adecuada y que el contenido existente se muestre en el formulario.

        :return: None
        :rtype: None
        """
        response = self.client.get(reverse('editar_contenido', kwargs={'pk': self.contenido.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editar_contenido.html')
        self.assertContains(response, 'El futuro de los móviles')
    
    def test_editar_contenido_view_post(self):
        """
        Prueba que se puede editar un contenido a través del formulario.

        Se simula el inicio de sesión de un usuario y se envían datos
        válidos para editar un contenido existente. Se verifica que
        se reciba un código de estado 302 (redirección) y que el contenido
        se haya actualizado correctamente en la base de datos.

        :return: None
        :rtype: None
        """
        self.client.login(username='editor', password='password')
        
        response = self.client.post(reverse('editar_contenido', kwargs={'pk': self.contenido.id}), {
            'title': 'Contenido actualizado',
            'content': 'Texto actualizado',
            'categoria': self.categoria.id_categoria,
            'subcategoria': self.subcategoria.id_subcategoria,
            'editor': self.user.id,
        })
        
        self.assertEqual(response.status_code, 302)  # Redirección después de editar
        contenido_actualizado = Contenido.objects.get(id=self.contenido.id)
        self.assertEqual(contenido_actualizado.titulo, 'Contenido actualizado')
        self.assertEqual(contenido_actualizado.texto, 'Texto actualizado')

    def test_eliminar_contenido_view(self):
        """
        Prueba que se puede eliminar un contenido.

        Se envía una solicitud para eliminar un contenido existente y se
        verifica que se reciba un código de estado 302 (redirección).
        Además, se comprueba que el contenido ya no exista en la base de datos.

        :return: None
        :rtype: None
        """
        response = self.client.post(reverse('eliminar_contenido', kwargs={'pk': self.contenido.id}))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        with self.assertRaises(Contenido.DoesNotExist):
            Contenido.objects.get(id=self.contenido.id)


class ComentarioViewsTest(TestCase):
    