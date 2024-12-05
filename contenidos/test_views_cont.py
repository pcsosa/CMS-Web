from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import render
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from appcms.models import Categoria
from appcms.utils.utils import decode_token, obtenerToken, obtenerUserId, obtenerUserInfoById, obtenerUsersConRol
from cmsweb.settings import KEYCLOAK_RS256_PUBLIC_KEY
from contenidos.models_cont import Categoria, Comentario, Contenido,Historico
from subcategorias.models import Subcategoria


class ContenidoViewsTest(TestCase):

    def setUp(self):
        # Configurar el cliente y crear algunos datos para las pruebas
        self.client = Client()

        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.subcategoria = Subcategoria.objects.create(
            nombre="Móviles", categoria=self.categoria
        )

        self.autor = {"id": "1", "username": "autor1"}
        self.editor = {"id": "2", "username": "editor1"}
        self.publicador = {"id": "3", "username": "publicador1"}

        self.contenido = Contenido.objects.create(
            titulo="El futuro de los móviles",
            texto="Texto acerca de móviles",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            autor_id=self.autor["id"],
            editor_id=self.editor["id"],
            publicador_id=self.publicador["id"],
        )

    def test_lista_contenidos_view(self):
        """Prueba que la vista lista_contenidos devuelve una respuesta correcta."""
        response = self.client.get(reverse("lista_contenidos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lista_contenidos.html")
        self.assertContains(response, "El futuro de los móviles")

    def test_crear_contenido_view_get(self):
        """Prueba que la vista crear_contenido devuelve un formulario correctamente."""
        with patch("appcms.utils.utils.obtenerUsersConRol") as mock_obtenerUsersConRol:
            mock_obtenerUsersConRol.side_effect = lambda user_id: {
                "username": f"autor{user_id}"
            }
            response = self.client.get(reverse("crear_contenido"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "crear_contenido.html")
    @patch('contenidos.views_cont.obtenerUserId')
    def test_crear_contenido_view_post(self,mock_obtenerUserId):
        """Prueba que se puede crear un contenido a través del formulario."""
        mock_obtenerUserId.return_value = {'id':1,'nombre':'user1'}
        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        response = self.client.post(
            reverse("crear_contenido"),
            {
                "title": "Nuevo contenido",
                "content": "Este es un nuevo contenido",
                "image": image,
                "categoria": self.categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
                "editor": self.editor["id"],
            },
        )

        # Verificar que los campos del contenido creado coinciden con lo que se envió en el POST
        self.assertEqual(
            response.status_code, 302
        )  # Redirección después de crear contenido

        # Intentar obtener el contenido recién creado
        try:
            nuevo_contenido = Contenido.objects.get(titulo="Nuevo contenido")
        except Contenido.DoesNotExist:
            self.fail("El contenido no fue creado correctamente.")

        self.assertIsNotNone(nuevo_contenido)
        self.assertEqual(nuevo_contenido.texto, "Este es un nuevo contenido")
        self.assertEqual(
            nuevo_contenido.categoria.id_categoria, self.categoria.id_categoria
        )
        self.assertEqual(
            nuevo_contenido.subcategoria.id_subcategoria,
            self.subcategoria.id_subcategoria,
        )
        self.assertEqual(nuevo_contenido.editor_id, self.editor["id"])

        # Verificar que la imagen se haya guardado correctamente
        self.assertIsNotNone(nuevo_contenido.imagen)
    
    def test_editar_contenido_view_get(self):
        """Prueba que la vista editar_contenido devuelve el formulario correctamente."""
        with patch("appcms.utils.utils.obtenerUsersConRol") as mock_obtenerUsersConRol, \
            patch("contenidos.views_cont.obtenerUserId") as mock_obtenerUserId:
            mock_obtenerUsersConRol.side_effect = lambda user_id: {
                "username": f"autor{user_id}"
            }
            mock_obtenerUserId.return_value = {'id':1 , 'nombre':'user1'}
            response = self.client.get(
                reverse("editar_contenido", kwargs={"pk": self.contenido.id})
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "editar_contenido.html")
            self.assertContains(response, "El futuro de los móviles")
    @patch('contenidos.views_cont.obtenerUserId')
    def test_editar_contenido_view_post(self,mock_obtenerUserId):
        """Prueba que se puede editar un contenido a través del formulario."""
        mock_obtenerUserId.return_value = {'id':1,'nombre':'user1'}
        response = self.client.post(
            reverse("editar_contenido", kwargs={"pk": self.contenido.id}),
            {
                "title": "Contenido actualizado",
                "content": "Texto actualizado",
                "categoria": self.categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
                "editor": self.editor["id"],
            },
        )

        self.assertEqual(response.status_code, 302)  # Redirección después de editar
        contenido_actualizado = Contenido.objects.get(id=self.contenido.id)
        self.assertEqual(contenido_actualizado.titulo, "Contenido actualizado")
        self.assertEqual(contenido_actualizado.texto, "Texto actualizado")
    @patch('contenidos.views_cont.obtenerUserId')
    def test_eliminar_contenido_view(self,mock_obtenerUserId):
        """Prueba que se puede eliminar un contenido."""
        mock_obtenerUserId.return_value = {'id':1, 'nombre':'user1'}
        response = self.client.post(
            reverse("eliminar_contenido", kwargs={"pk": self.contenido.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        with self.assertRaises(Contenido.DoesNotExist):
            Contenido.objects.get(id=self.contenido.id)


# Sprint 3
# Tablero kanban
# Cambio de estados de publicaciones
# Visualización del contenido como suscriptor.
# Comentarios a las publicaciones


class TableroKanbanTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        # Create a category for the test content
        self.categoria = Categoria.objects.create(nombre="Test Category")
        # Create content with the required category ID
        Contenido.objects.create(
            titulo="Borrador Content", estado="Borrador", categoria=self.categoria
        )
        Contenido.objects.create(
            titulo="Revision Content", estado="Revisión", categoria=self.categoria
        )
        Contenido.objects.create(
            titulo="A Publicar Content", estado="A Publicar", categoria=self.categoria
        )
        Contenido.objects.create(
            titulo="Publicado Content", estado="Publicado", categoria=self.categoria
        )
        Contenido.objects.create(
            titulo="Inactivo Content", estado="Inactivo", categoria=self.categoria
        )

    # Verifica que la vista tablero_kanban responde con un código de estado 200 (OK).
    def test_tablero_kanban_status_code(self):
        response = self.client.get(reverse("tablero_kanban"))
        self.assertEqual(response.status_code, 200)

    # Comprueba que el contexto de la vista contiene los contenidos filtrados por estado y que el conteo de cada uno es el esperado.
    # def test_tablero_kanban_context(self):
    #     response = self.client.get(reverse("tablero_kanban"))
    #     self.assertIn("borrador", response.context)
    #     self.assertIn("en_revision", response.context)
    #     self.assertIn("a_publicar", response.context)
    #     self.assertIn("publicado", response.context)
    #     self.assertIn("inactivo", response.context)

    #     self.assertEqual(response.context["borrador"].count(), 1)
    #     self.assertEqual(response.context["en_revision"].count(), 1)
    #     self.assertEqual(response.context["a_publicar"].count(), 1)
    #     self.assertEqual(response.context["publicado"].count(), 1)
    #     self.assertEqual(response.context["inactivo"].count(), 1)

    # Verificar que los contenidos de cada estado se muestran correctamente
    # def test_tablero_kanban_content_in_context(self):
    #     response = self.client.get(reverse("tablero_kanban"))

    #     borrador_content = response.context["borrador"].first()
    #     self.assertEqual(borrador_content.titulo, "Borrador Content")

    #     revision_content = response.context["en_revision"].first()
    #     self.assertEqual(revision_content.titulo, "Revision Content")

    #     a_publicar_content = response.context["a_publicar"].first()
    #     self.assertEqual(a_publicar_content.titulo, "A Publicar Content")

    #     publicado_content = response.context["publicado"].first()
    #     self.assertEqual(publicado_content.titulo, "Publicado Content")

    #     inactivo_content = response.context["inactivo"].first()
    #     self.assertEqual(inactivo_content.titulo, "Inactivo Content")

    # Verificar que la plantilla correcta se está renderizando:
    def test_tablero_kanban_template_used(self):
        response = self.client.get(reverse("tablero_kanban"))
        self.assertTemplateUsed(response, "tablero_kanban.html")

    # Verificar que la vista maneja una solicitud GET correctamente:
    # def test_tablero_kanban_get_request(self):
    #     response = self.client.get(reverse("tablero_kanban"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Borrador Content")
    #     self.assertContains(response, "Revision Content")
    #     self.assertContains(response, "A Publicar Content")
    #     self.assertContains(response, "Publicado Content")
    #     self.assertContains(response, "Inactivo Content")


class VisualizarContenidoTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.autor = {"id": 1, "username": "autor1"}
        self.categoria = Categoria.objects.create(nombre="Test Category")
        self.contenido = Contenido.objects.create(
            titulo="Test Content",
            estado="Borrador",
            categoria=self.categoria,
            autor_id=self.autor["id"],
        )
        self.comentario = Comentario.objects.create(
            contenido=self.contenido,
            usuario=1,
            comentario="Este es un comentario de prueba.",
            active=True,
        )

    # Verificar que la vista devuelve un código de estado 200 para una solicitud válida:
    def test_visualizar_contenido_status_code(self):

        response = self.client.get(
            reverse("visualizar_contenido", args=[self.contenido.pk])
        )
        self.assertEqual(response.status_code, 200)

    # Verificar que la plantilla correcta se está utilizando:
    def test_visualizar_contenido_template_used(self):
        response = self.client.get(
            reverse("visualizar_contenido", args=[self.contenido.pk])
        )
        self.assertTemplateUsed(response, "contenido.html")

    # Verificar que el contenido y los comentarios se pasan correctamente al contexto:
    def test_visualizar_contenido_context_data(self):
        response = self.client.get(
            reverse("visualizar_contenido", args=[self.contenido.pk])
        )
        self.assertIn("contenido", response.context)
        self.assertIn("comentarios", response.context)
        self.assertEqual(response.context["contenido"], self.contenido)
        self.assertEqual(
            list(response.context["comentarios"]), list(self.contenido.comments.all())
        )

    # Verificar que se devuelve un error 404 si el contenido no existe:
    def test_visualizar_contenido_404(self):
        response = self.client.get(reverse("visualizar_contenido", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_visualizar_contenido_replace_user_id(self):
        with patch(
            "appcms.utils.utils.obtenerUserInfoById"
        ) as mock_obtenerUserInfoById:
            mock_obtenerUserInfoById.side_effect = lambda user_id: {
                "username": f"autor{user_id}"
            }
            response = self.client.get(
                reverse("visualizar_contenido", args=[self.contenido.pk])
            )
            contenido = response.context["contenido"]
            comentarios = response.context["comentarios"]
            self.assertEqual(contenido.autor_id, f"autor{self.contenido.autor_id}")
            for comentario in comentarios:
                self.assertEqual(comentario.usuario, f"{comentario.usuario}")

    def test_comentario_fecha(self):
        comentario = Comentario.objects.get(pk=self.comentario.pk)
        self.assertTrue((timezone.now() - comentario.fecha).seconds < 60)

    def test_comentario_ordering(self):
        otro_comentario = Comentario.objects.create(
            contenido=self.contenido,
            usuario=2,
            email="otrousuario@example.com",
            comentario="Este es otro comentario.",
            active=True,
        )
        comentarios = Comentario.objects.filter(contenido=self.contenido).order_by(
            "-fecha"
        )
        self.assertEqual(comentarios[0], otro_comentario)
        self.assertEqual(comentarios[1], self.comentario)


class CambiarEstadoTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        # Crea una categoría para el contenido de prueba
        self.categoria = Categoria.objects.create(nombre="Test Category")
        # Asegúrate de incluir la categoría en la creación de contenido
        self.contenido = Contenido.objects.create(
            titulo="Test Content", estado="Borrador", categoria=self.categoria
        )

    # Verifica una transición válida entre estados.
    # def test_cambiar_estado_valid_transition(self):
    #     response = self.client.post(
    #         reverse("cambiar_estado", args=[self.contenido.pk, "Borrador", "Revisión"])
    #     )
    #     self.contenido.refresh_from_db()
    #     self.assertEqual(self.contenido.estado, "Revisión")

    # Verifica una transición no válida entre estados.
    def test_cambiar_estado_invalid_transition(self):
        response = self.client.post(
            reverse("cambiar_estado", args=[self.contenido.pk, "Borrador", "Publicado"])
        )
        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.estado, "Borrador")

    # Verifica que el estado puede cambiarse a "Inactivo".
    @patch('contenidos.views_cont.obtenerUserId')
    def test_cambiar_estado_inactivo(self, mock_obtenerUserId):
        mock_obtenerUserId.return_value = {'id':1,'nombre':'autor2'}
        self.contenido.estado = "Publicado"
        self.contenido.save()
        response = self.client.post(
            reverse("cambiar_estado", args=[self.contenido.pk, "Publicado", "Inactivo"])
        )
        self.contenido.refresh_from_db()
        self.assertEqual(self.contenido.estado, "Inactivo")

    # Verifica que los estados inválidos no cambian el estado.
    def test_cambiar_estado_invalid_state(self):
        response = self.client.post(
            reverse(
                "cambiar_estado", args=[self.contenido.pk, "Inexistente", "Revisión"]
            )
        )
        self.contenido.refresh_from_db()
        self.assertNotEqual(self.contenido.estado, "Revisión")


class GuardarComentarioTestCase(TestCase):

    def setUp(self):
        # Configurar el cliente y crear algunos datos para las pruebas
        self.client = Client()

        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.subcategoria = Subcategoria.objects.create(
            nombre="Móviles", categoria=self.categoria
        )

        self.autor = {"id": "1", "username": "autor1"}
        self.editor = {"id": "2", "username": "editor1"}
        self.publicador = {"id": "3", "username": "publicador1"}

        self.contenido = Contenido.objects.create(
            titulo="El futuro de los móviles",
            texto="Texto acerca de móviles",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            autor_id=self.autor["id"],
            editor_id=self.editor["id"],
            publicador_id=self.publicador["id"],
        )

    # Verifica que un comentario se guarda exitosamente y se asocia al contenido.
    def test_guardar_comentario_exitoso(self):

        # Simular una solicitud POST para guardar un comentario
        response = self.client.post(
            reverse("guardar_comentario", args=[self.contenido.id]),
            {
                "comentario": "Este es un comentario de prueba.",
            },
        )
        # Verifica que la redirección fue exitosa
        self.assertEqual(response.status_code, 302)

        # Verifica que el comentario fue guardado en la base de datos
        comentario = Comentario.objects.get(contenido=self.contenido)
        self.assertEqual(comentario.comentario, "Este es un comentario de prueba.")

    # Verifica que no se guarda un comentario vacío.
    def test_guardar_comentario_vacio(self):
        # Simular una solicitud POST para guardar un comentario
        response = self.client.post(
            reverse("guardar_comentario", args=[self.contenido.id]),
            {
                "comentario": "",
            },
        )

        # Verifica que la respuesta fue una redirección
        self.assertEqual(response.status_code, 302)

        # Verificar que el comentario no existe en la base de datos
        with self.assertRaises(Comentario.DoesNotExist):
            Comentario.objects.get(contenido=self.contenido)

    # Verifica que el HTML en los comentarios se limpia correctamente.

    # Verifica que se maneja correctamente la ausencia del contenido.
    def test_guardar_comentario_no_contenido(self):
        response = self.client.post(
            reverse("guardar_comentario", args=[9999]),
            {"comentario": "Este es un comentario."},
        )
        self.assertEqual(response.status_code, 404)  # No encontrado


def visualizar_historial(request):
    """
    Visualiza el historial con detalles y permite filtrar por contenido, usuario y rango de fechas.

    :param request: Objeto de solicitud que contiene los datos de la petición.
    :type request: HttpRequest
    :return: Renderiza el template 'historial.html' con los datos filtrados.
    :rtype: HttpResponse
    """
    # Obtener parámetros de filtro desde la solicitud
    contenido_id = request.GET.get("articulo")  # ID del contenido
    usuario = request.GET.get("usuario")  # Nombre del usuario
    autor_id = request.GET.get("autor")  # ID del autor del contenido
    fecha_inicio = request.GET.get("fecha_inicio")  # Fecha inicial (YYYY-MM-DD)
    fecha_fin = request.GET.get("fecha_fin")  # Fecha final (YYYY-MM-DD)

    # Iniciar queryset base
    historial = Historico.objects.all()

    # Aplicar filtros dinámicamente
    if contenido_id:
        historial = historial.filter(contenido_id=contenido_id)
    if usuario:
        historial = historial.filter(usuario=usuario)
    if autor_id:
        historial = historial.filter(contenido_id__autor_id=autor_id)
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = (
                datetime.strptime(fecha_fin, "%Y-%m-%d")
                + timedelta(days=1)
                - timedelta(seconds=1)
            )
            historial = historial.filter(fecha__range=(fecha_inicio, fecha_fin))
        except ValueError:
            pass  # Ignorar si las fechas no tienen el formato correcto

    # Obtener todos los usuarios menos suscriptores
    autores = obtenerUsersConRol("Autor")
    editores = obtenerUsersConRol("Editor")
    administradores = obtenerUsersConRol("Administrador")
    publicadores = obtenerUsersConRol("Publicador")

    # Juntar los usuarios sin repetir
    usuarios = list(
        {
            usuario["id"]: usuario
            for usuario in autores + editores + administradores + publicadores
        }.values()
    )

    # Obtener los contenidos
    contenidos = Contenido.objects.all()

    # Reemplazar el nombre del usuario en el historial
    for historico in historial:
        historico.usuario = obtenerUserInfoById(historico.usuario).get("username")

    # Pasar los datos al template
    return render(
        request,
        "historial.html",
        {
            "historicos": historial,
            "usuarios": usuarios,
            "articulos": contenidos,
        },
    )