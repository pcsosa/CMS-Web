from django.test import TestCase,Client
from unittest.mock import patch
from subcategorias.models import Subcategoria
from appcms.models import Categoria 
from subcategorias.notificacion import *
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
            nombre="Test Subcategoria"
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

    @patch('subcategorias.notificacion.obtenerUsersConRol')
    @patch('subcategorias.notificacion.obtenerUserInfoById')
    @patch('subcategorias.notificacion.enviar_notificacion')
    def test_notificar_editar_subcategoria(self, 
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
            nombre="Test Subcategoria Edit"
        )

        # Import and call the edit notification function
        from subcategorias.signals import notificar_editar_subcategoria
        notificar_editar_subcategoria(subcategoria)

        # Verify notification parameters
        expected_emails = [
            "autor1@example.com", "autor2@example.com", 
            "autor3@example.com", "autor4@example.com", 
            "autor5@example.com", "autor6@example.com"
        ]
        mock_enviar_notificacion.assert_called_once_with(
            'Edicion de subcategoria Test Subcategoria Edit', 
            'La subcategoria "Test Subcategoria Edit" ha sido editada.', 
            expected_emails
        )

    @patch('subcategorias.notificacion.obtenerUsersConRol')
    @patch('subcategorias.notificacion.obtenerUserInfoById')
    @patch('subcategorias.notificacion.enviar_notificacion')
    def test_notificar_borrar_subcategoria(self, 
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
            nombre="Test Subcategoria Delete",
            categoria=self.categoria
        )

        # Import and call the delete notification function
        notificar_borrar_subcategoria(subcategoria)

        # Verify notification parameters
        expected_emails = [
            "autor1@example.com", "autor2@example.com", 
            "autor3@example.com", "autor4@example.com", 
            "autor5@example.com", "autor6@example.com"
        ]
        mock_enviar_notificacion.assert_called_once_with(
            'Edicion de subcategoria Test Subcategoria Delete', 
            'La subcategoria "Test Subcategoria Delete" ha sido editada.', 
            expected_emails
        )
