from django.test import TestCase,Client
from unittest.mock import patch
from subcategorias.models import Subcategoria
from appcms.models import Categoria 
from subcategorias.notificacion import *
import unittest

class SubcategorySignalsTestCase(TestCase):

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
    
    
    @patch('subcategorias.notificacion.obtenerUsersConRol')
    @patch('subcategorias.notificacion.obtenerUserInfoById')
    @patch('subcategorias.notificacion.enviar_notificacion')
    def test_notificar_nueva_subcategoria(self, 
        mock_enviar_notificacion, 
        mock_obtener_user_info, 
        mock_obtener_users_con_rol
    ):
        # Setup mock data for different user roles
        autores = [{'id': 1}, {'id': 2}]
        editores = [{'id': 3}, {'id': 4}]
        publicadores = [{'id': 5}, {'id': 6}]

        mock_obtener_users_con_rol.side_effect = [
            autores, editores, publicadores
        ]

        # Setup email mock for each user
        mock_obtener_user_info.side_effect = [
            {"email": f"autor{i}@example.com"} for i in range(1, 7)
        ]

        # Create a Subcategoria instance
        subcategoria = Subcategoria.objects.create(
            nombre="Test Subcategoria",
            categoria = self.categoria
        )

        # Verify notification parameters
        expected_emails = [
            "autor1@example.com", "autor2@example.com", 
            "autor3@example.com", "autor4@example.com", 
            "autor5@example.com", "autor6@example.com"
        ]
        mock_enviar_notificacion.assert_called_once_with(
            'Nueva Subcategoria en', 
            'Una nueva subcategoria ha sido agregada "Test Subcategoria".', 
            expected_emails
        )

    @patch('subcategorias.notificacion.enviar_notificacion')
    @patch('subcategorias.notificacion.obtenerUserInfoById')
    @patch('subcategorias.notificacion.obtenerUsersConRol')
    def test_notificar_editar_subcategoria(self, mock_obtenerUsersConRol, mock_obtenerUserInfoById, mock_enviar_notificacion):
        # Configuración de mocks
        mock_obtenerUsersConRol.side_effect = lambda rol: [{"id": 1}, {"id": 2}]
        mock_obtenerUserInfoById.side_effect = lambda user_id: {"email": f"user{user_id}@example.com"}
        mock_enviar_notificacion.return_value = None

        # Ejecutar la función
        notificar_editar_subcategoria(self.subcategoria)

        # Verificar destinatarios construidos
        destinatarios = []
        for role in ["Autor", "Editor", "Publicador"]:
            users = mock_obtenerUsersConRol(role)
            emails = [mock_obtenerUserInfoById(user["id"])["email"] for user in users]
            destinatarios.extend(emails)

        # Verificar que enviar_notificacion fue llamado con los datos correctos
        mock_enviar_notificacion.assert_called_once_with(
            "Edicion de subcategoria Prueba",
            'La subcategoria "Prueba" ha sido editada.',
            destinatarios
        )
    @patch('subcategorias.notificacion.enviar_notificacion')
    @patch('subcategorias.notificacion.obtenerUserInfoById')
    @patch('subcategorias.notificacion.obtenerUsersConRol')
    def test_notificar_borrar_subcategoria(
        self, mock_obtenerUsersConRol, mock_obtenerUserInfoById, mock_enviar_notificacion
    ):
        mock_obtenerUsersConRol.side_effect = [
            [{"id": 1}, {"id": 2}],  # Para 'Autor'
            [{"id": 3}, {"id": 4}],  # Para 'Editor'
            [{"id": 5}, {"id": 6}],  # Para 'Publicador'
        ]
        mock_obtenerUserInfoById.side_effect = lambda user_id: {"email": f"user{user_id}@example.com"}

        # Ejecutar la función
        notificar_borrar_subcategoria(self.subcategoria)

        # Verificar que se llamaron las funciones con los valores correctos
        mock_obtenerUsersConRol.assert_has_calls(
            [unittest.mock.call("Autor"), unittest.mock.call("Editor"), unittest.mock.call("Publicador")]
        )
        mock_obtenerUserInfoById.assert_any_call(1)
        mock_obtenerUserInfoById.assert_any_call(2)
        mock_obtenerUserInfoById.assert_any_call(3)
        mock_obtenerUserInfoById.assert_any_call(4)
        mock_obtenerUserInfoById.assert_any_call(5)
        mock_obtenerUserInfoById.assert_any_call(6)
        mock_enviar_notificacion.assert_called_once_with(
            "Edicion de subcategoria Prueba",
            'La subcategoria "Prueba" ha sido editada.',
            [
                "user1@example.com", "user2@example.com",  # Correos de 'Autor'
                "user3@example.com", "user4@example.com",  # Correos de 'Editor'
                "user5@example.com", "user6@example.com",  # Correos de 'Publicador'
            ]
        )