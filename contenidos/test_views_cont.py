from django.test import TestCase, Client
from django.urls import reverse
from appcms.models import Categoria
from subcategorias.models import Subcategoria
from contenidos.models_cont import Contenido
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class ContenidoViewsTest(TestCase):
    
    def setUp(self):
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
        """Prueba que la vista lista_contenidos devuelve una respuesta correcta."""
        response = self.client.get(reverse('lista_contenidos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista_contenidos.html')
        self.assertContains(response, 'El futuro de los móviles')
    
    def test_crear_contenido_view_get(self):
        """Prueba que la vista crear_contenido devuelve un formulario correctamente."""
        response = self.client.get(reverse('crear_contenido'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crear_contenido.html')
    
    def test_crear_contenido_view_post(self):
        """Prueba que se puede crear un contenido a través del formulario."""
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
        """Prueba que la vista editar_contenido devuelve el formulario correctamente."""
        response = self.client.get(reverse('editar_contenido', kwargs={'pk': self.contenido.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editar_contenido.html')
        self.assertContains(response, 'El futuro de los móviles')
    
    def test_editar_contenido_view_post(self):
        """Prueba que se puede editar un contenido a través del formulario."""
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
        """Prueba que se puede eliminar un contenido."""
        response = self.client.post(reverse('eliminar_contenido', kwargs={'pk': self.contenido.id}))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        with self.assertRaises(Contenido.DoesNotExist):
            Contenido.objects.get(id=self.contenido.id)
#Sprint 3
    # Tablero kanban
    # Cambio de estados de publicaciones
    # Visualización del contenido como suscriptor.
    # Comentarios a las publicaciones
class TableroKanbanTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        # Crea contenidos de prueba con diferentes estados
        Contenido.objects.create(titulo="Borrador Content", estado="Borrador")
        Contenido.objects.create(titulo="Revision Content", estado="Revisión")
        Contenido.objects.create(titulo="A Publicar Content", estado="A Publicar")
        Contenido.objects.create(titulo="Publicado Content", estado="Publicado")
        Contenido.objects.create(titulo="Inactivo Content", estado="Inactivo")

#Verifica que la vista tablero_kanban responde con un código de estado 200 (OK).
    def test_tablero_kanban_status_code(self):
        response = self.client.get(reverse('tablero_kanban'))
        self.assertEqual(response.status_code, 200)

#Comprueba que el contexto de la vista contiene los contenidos filtrados por estado y que el conteo de cada uno es el esperado.
    def test_tablero_kanban_context(self):
        response = self.client.get(reverse('tablero_kanban'))
        self.assertIn('borrador', response.context)
        self.assertIn('en_revision', response.context)
        self.assertIn('a_publicar', response.context)
        self.assertIn('publicado', response.context)
        self.assertIn('inactivo', response.context)

        self.assertEqual(response.context['borrador'].count(), 1)
        self.assertEqual(response.context['en_revision'].count(), 1)
        self.assertEqual(response.context['a_publicar'].count(), 1)
        self.assertEqual(response.context['publicado'].count(), 1)
        self.assertEqual(response.context['inactivo'].count(), 1)

#Verificar que los contenidos de cada estado se muestran correctamente
    def test_tablero_kanban_content_in_context(self):
        response = self.client.get(reverse('tablero_kanban'))
        
        borrador_content = response.context['borrador'].first()
        self.assertEqual(borrador_content.titulo, "Borrador Content")

        revision_content = response.context['en_revision'].first()
        self.assertEqual(revision_content.titulo, "Revision Content")

        a_publicar_content = response.context['a_publicar'].first()
        self.assertEqual(a_publicar_content.titulo, "A Publicar Content")

        publicado_content = response.context['publicado'].first()
        self.assertEqual(publicado_content.titulo, "Publicado Content")

        inactivo_content = response.context['inactivo'].first()
        self.assertEqual(inactivo_content.titulo, "Inactivo Content")
    
#Verificar que la plantilla correcta se está renderizando:
    def test_tablero_kanban_template_used(self):
        response = self.client.get(reverse('tablero_kanban'))
        self.assertTemplateUsed(response, 'tablero_kanban.html')

#Verificar que la vista maneja una solicitud GET correctamente:
    def test_tablero_kanban_get_request(self):
        response = self.client.get(reverse('tablero_kanban'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Borrador Content")
        self.assertContains(response, "Revision Content")
        self.assertContains(response, "A Publicar Content")
        self.assertContains(response, "Publicado Content")
        self.assertContains(response, "Inactivo Content")

class VisualizarContenidoTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.contenido = Contenido.objects.create(titulo="Test Content", autor_id=1)
        self.comentario = Comentario.objects.create(
            contenido=self.contenido,
            usuario=1,
            email="testuser@example.com",
            comentario="Este es un comentario de prueba.",
            active=True
        )

#Verificar que la vista devuelve un código de estado 200 para una solicitud válida:
    def test_visualizar_contenido_status_code(self):
        response = self.client.get(reverse('visualizar_contenido', args=[self.contenido.pk]))
        self.assertEqual(response.status_code, 200)

#Verificar que la plantilla correcta se está utilizando:
    def test_visualizar_contenido_template_used(self):
        response = self.client.get(reverse('visualizar_contenido', args=[self.contenido.pk]))
        self.assertTemplateUsed(response, 'contenido.html')

#Verificar que el contenido y los comentarios se pasan correctamente al contexto:
    def test_visualizar_contenido_context_data(self):
        response = self.client.get(reverse('visualizar_contenido', args=[self.contenido.pk]))
        self.assertIn('contenido', response.context)
        self.assertIn('comentarios', response.context)
        self.assertEqual(response.context['contenido'], self.contenido)
        self.assertEqual(list(response.context['comentarios']), list(self.contenido.comments.all()))

#Verificar que se devuelve un error 404 si el contenido no existe:
    def test_visualizar_contenido_404(self):
        response = self.client.get(reverse('visualizar_contenido', args=[999]))
        self.assertEqual(response.status_code, 404)

#Verificar que los IDs de usuario se reemplazan correctamente por los nombres de usuario:
    def test_visualizar_contenido_replace_user_id(self):
        with patch('tu_app.views.obtenerUserInfoById') as mock_obtenerUserInfoById:
            mock_obtenerUserInfoById.side_effect = lambda user_id: {"username": f"Usuario{user_id}"}
            response = self.client.get(reverse('visualizar_contenido', args=[self.contenido.pk]))
            contenido = response.context['contenido']
            comentarios = response.context['comentarios']
            self.assertEqual(contenido.autor_id, f"Usuario{self.contenido.autor_id}")
            for comentario in comentarios:
                self.assertEqual(comentario.usuario, f"Usuario{comentario.usuario}")

#
    def test_comentario_fecha(self):
        comentario = Comentario.objects.get(pk=self.comentario.pk)
        self.assertTrue((timezone.now() - comentario.fecha).seconds < 60)

    def test_comentario_ordering(self):
        otro_comentario = Comentario.objects.create(
            contenido=self.contenido,
            usuario=2,
            email="otrousuario@example.com",
            comentario="Este es otro comentario.",
            active=True
        )
        comentarios = Comentario.objects.filter(contenido=self.contenido).order_by("-fecha")
        self.assertEqual(comentarios[0], otro_comentario)
        self.assertEqual(comentarios[1], self.comentario)

class CambiarEstadoTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.contenido = Contenido.objects.create(titulo="Test Content", estado="Borrador")

# Verifica una transición válida entre estados.
    def test_cambiar_estado_valid_transition(self):
        response = self.client.post(reverse('cambiar_estado', args=[self.contenido.pk, 'Borrador', 'Revisión']))
        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.estado, 'Revisión')

#Verifica una transición no válida entre estados.
    def test_cambiar_estado_invalid_transition(self):
        response = self.client.post(reverse('cambiar_estado', args=[self.contenido.pk, 'Borrador', 'Publicado']))
        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.estado, 'Borrador')

#Verifica que el estado puede cambiarse a "Inactivo".
    def test_cambiar_estado_inactivo(self):
        self.contenido.estado = 'Publicado'
        self.contenido.save()
        response = self.client.post(reverse('cambiar_estado', args=[self.contenido.pk, 'Publicado', 'Inactivo']))
        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.estado, 'Inactivo')

#Verifica que los estados inválidos no cambian el estado.
    def test_cambiar_estado_invalid_state(self):
        response = self.client.post(reverse('cambiar_estado', args=[self.contenido.pk, 'Inexistente', 'Revisión']))
        self.contenido.refresh_from_db()
        self.assertNotEqual(self.contenido.estado, 'Revisión')

#Verifica las redirecciones dependiendo del referer HTTP.
    def test_cambiar_estado_redirect(self):
        response = self.client.post(reverse('cambiar_estado', args=[self.contenido.pk, 'Borrador', 'Revisión']), HTTP_REFERER='/anterior/')
        self.assertRedirects(response, '/anterior/')
        response = self.client.post(reverse('cambiar_estado', args=[self.contenido.pk, 'Revisión', 'A Publicar']))
        self.assertRedirects(response, reverse('tablero_kanban'))


class GuardarComentarioTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.contenido = Contenido.objects.create(titulo="Test Content", autor_id=1)

    @patch('tu_app.views.obtenerUserId')
    @patch('tu_app.views.obtenerToken')

#Verifica que un comentario se guarda exitosamente y se asocia al contenido.
    def test_guardar_comentario_exitoso(self, mock_obtenerToken, mock_obtenerUserId):
        mock_obtenerToken.return_value = 'mock_token'
        mock_obtenerUserId.return_value = 1

        response = self.client.post(reverse('guardar_comentario', args=[self.contenido.pk]), {'comentario': 'Este es un comentario.'})
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertEqual(Comentario.objects.count(), 1)
        comentario = Comentario.objects.first()
        self.assertEqual(comentario.comentario, 'Este es un comentario.')
        self.assertEqual(comentario.usuario, 1)

#Verifica que no se guarda un comentario vacío.
    def test_guardar_comentario_vacio(self):
        response = self.client.post(reverse('guardar_comentario', args=[self.contenido.pk]), {'comentario': ''})
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertEqual(Comentario.objects.count(), 0)

#Verifica que el HTML en los comentarios se limpia correctamente.
    def test_guardar_comentario_html_injection(self):
        with patch('tu_app.views.obtenerUserId') as mock_obtenerUserId, patch('tu_app.views.obtenerToken') as mock_obtenerToken:
            mock_obtenerToken.return_value = 'mock_token'
            mock_obtenerUserId.return_value = 1

            comentario_con_html = "<p>Este es un comentario.</p>"
            response = self.client.post(reverse('guardar_comentario', args=[self.contenido.pk]), {'comentario': comentario_con_html})
            self.assertEqual(response.status_code, 302)  # Redirección
            comentario = Comentario.objects.first()
            self.assertEqual(comentario.comentario, 'Este es un comentario.')

#Verifica que se maneja correctamente la ausencia del contenido.
    def test_guardar_comentario_no_contenido(self):
        response = self.client.post(reverse('guardar_comentario', args=[999]), {'comentario': 'Este es un comentario.'})
        self.assertEqual(response.status_code, 404)  # No encontrado

#Verifica que la redirección después de guardar un comentario es correcta.
    def test_guardar_comentario_redireccion(self):
        response = self.client.post(reverse('guardar_comentario', args=[self.contenido.pk]), {'comentario': 'Este es un comentario.'})
        self.assertRedirects(response, reverse('visualizar_contenido', args=[self.contenido.pk]))
