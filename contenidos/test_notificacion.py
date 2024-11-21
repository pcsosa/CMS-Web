from django.test import Client, TestCase
from unittest.mock import patch
from contenidos.models_cont import Comentario, Contenido, Categoria
from subcategorias.models import Subcategoria
from appcms.utils.utils import obtenerUserInfoById
from contenidos.notificacion import *
class ContentSignalsTestCase(TestCase):
    def setUp(self):
        """Prepara los datos necesarios para las pruebas."""
        self.client = Client()

        self.categoria = Categoria.objects.create(nombre="Prueba")
        self.subcategoria = Subcategoria.objects.create(
            nombre="Prueba", categoria=self.categoria
        )
        self.autor = {"id": 1, "username": "autor1"}
        self.editor = {"id": 2, "username": "editor1"}
        self.publicador = {"id": 3, "username": "publicador1"}

    def test_notificar_nuevo_contenido(self):
        """Verifica que se envíe una notificación al crear un nuevo contenido."""
        with patch("contenidos.notificacion.obtenerUserInfoById") as mock_obtener_user_info, \
            patch("contenidos.notificacion.enviar_notificacion") as mock_enviar_notificacion:

            mock_obtener_user_info.return_value = {"email": "autor@example.com"}

            # Crear un contenido
            contenido = Contenido.objects.create(
                titulo="Test Contenido",
                categoria=self.categoria,
                subcategoria=self.subcategoria,
                autor_id=self.autor["id"],
                editor_id=self.editor["id"],
                publicador_id=self.publicador["id"],
            )
            # Verificar que la notificación fue enviada
            mock_enviar_notificacion.assert_called_once_with(
                'Contenido creado en',
                'Un nuevo contenido ha sido creado .',
                ['autor@example.com']
            )


    
    def test_notificar_nuevo_comentario(self):
        """Verifica que se envíe una notificación al crear un comentario."""
        with patch("contenidos.notificacion.obtenerUserInfoById") as mock_obtener_user_info, \
            patch("contenidos.notificacion.enviar_notificacion") as mock_enviar_notificacion:

            mock_obtener_user_info.return_value = {"email": "autor@example.com"}

            # Crear contenido y comentario
            contenido = Contenido.objects.create(
                titulo="Test Contenido para comentario",
                categoria=self.categoria,
                subcategoria=self.subcategoria,
                autor_id=self.autor["id"],
                editor_id=self.editor["id"],
                publicador_id=self.publicador["id"],
                
            )
            Comentario.objects.create(
                contenido=contenido,
                comentario="Test Comentario"
            
            )

            # Verificar que la notificación fue enviada
            mock_enviar_notificacion.assert_called_with('Nuevo comentario en Test Contenido para comentario', 'Un nuevo comentario ha sido agregado al contenido "Test Contenido para comentario".', ['autor@example.com']  
            )

    # def test_enviar_notificacion_cambio_estado(self):
    #     """Verifica que las notificaciones se envíen al cambiar el estado del contenido."""
    #     with patch("contenidos.notificacion.obtenerUserInfoById") as mock_obtener_user_info, \
    #         patch("contenidos.notificacion.obtenerUserConRol") as mock_obtener_user_con_rol,\
    #         patch("contenidos.notificacion.enviar_notificacion") as mock_enviar_notificacion:
    #         scenarios = [
    #             {
    #                 "estado": "Borrador",
    #                 "expected_emails": ["autor@example.com"],
    #                 "roles": []
    #             },
    #             {
    #                 "estado": "Revisión",
    #                 "expected_emails": ["editor@example.com", "autor@example.com"],
    #                 "roles": []
    #             },
    #             {
    #                 "estado": "A Publicar",
    #                 "expected_emails": ["publicador1@example.com", "publicador2@example.com", "autor@example.com"],
    #                 "roles": [{"id": 2, "nombre": "Publicador"}, {"id": 3, "nombre": "Publicador"}]
    #             },
    #             {
    #                 "estado": "Publicado",
    #                 "expected_emails": ["suscriptor1@example.com", "suscriptor2@example.com", "autor@example.com"],
    #                 "roles": [{"id": 4, "nombre": "Suscriptor"}, {"id": 5, "nombre": "Suscriptor"}]
    #             }
    #         ]

    #         for scenario in scenarios:
    #             mock_enviar_notificacion.reset_mock()
    #             mock_obtener_users_con_rol.return_value = scenario["roles"]
    #             mock_obtener_user_info.side_effect = [{"email": email} for email in scenario["expected_emails"]]

    #             contenido = Contenido.objects.create(
    #                 titulo="Test Contenido para cambio de estados",
    #                 categoria=self.categoria,
    #                 subcategoria=self.subcategoria,
    #                 autor_id=self.autor["id"],
    #                 editor_id=self.editor["id"],
    #                 publicador_id=self.publicador["id"],
    #             )

    #             enviar_notificacion_cambio_estado(scenario["estado"], contenido)

    #             mock_enviar_notificacion.assert_called_once_with(
    #                 f"Contenido en {scenario['estado']}: {contenido.titulo}",
    #                 f'El contenido "{contenido.titulo}" ha sido {" ".join(scenario["estado"].lower().split())}.',
    #                 scenario["expected_emails"]
    #             )

   
    def test_notificar_edicion_contenido(self):
        """Verifica que se envíe una notificación al editar un contenido."""
        with patch("contenidos.notificacion.obtenerUserInfoById") as mock_obtener_user_info, \
            patch("contenidos.notificacion.enviar_notificacion") as mock_enviar_notificacion:

            mock_obtener_user_info.return_value = {"email": "autor@example.com"}

            # Crear contenido y comentario
            contenido = Contenido.objects.create(
                titulo="Test Contenido para edicion",
                categoria=self.categoria,
                subcategoria=self.subcategoria,
                autor_id=self.autor["id"],
                editor_id=self.editor["id"],
                publicador_id=self.publicador["id"],
                
            )
            notificar_edicion_contenido(contenido)

            mock_enviar_notificacion.assert_called_with('Edicion de contenido Test Contenido para edicion', 'El contenido "Test Contenido para edicion" ha sido editada.', ['autor@example.com']
            )

    def test_notificar_borrar_contenido(self):
        with patch("contenidos.notificacion.obtenerUserInfoById") as mock_obtener_user_info, \
            patch("contenidos.notificacion.enviar_notificacion") as mock_enviar_notificacion:

            mock_obtener_user_info.return_value = {"email": "autor@example.com"}

            # Crear contenido y comentario
            contenido = Contenido.objects.create(
                titulo="Test Contenido para comentario",
                categoria=self.categoria,
                subcategoria=self.subcategoria,
                autor_id=self.autor["id"],
                editor_id=self.editor["id"],
                publicador_id=self.publicador["id"],
                
            )

            notificar_borrar_contenido(contenido)

            mock_enviar_notificacion.assert_called_with(
                'eliminacion de contenido Test Contenido para comentario',
                'El contenido "Test Contenido para comentario" ha sido eliminado.',
                ['autor@example.com']
            )
