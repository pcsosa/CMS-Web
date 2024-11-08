# from django.test import TestCase
# from django.utils import timezone
# from unittest.mock import patch, MagicMock
# from contenidos.models_cont import Contenido, Comentario
# from appcms.models import Categoria
# from subcategorias.models import Subcategoria
# from contenidos.notificacion import (
#     notificar_nuevo_contenido,
#     notificar_edicion_contenido,
#     notificar_borrar_contenido,
#     notificar_nuevo_comentario,
#     enviar_notificacion_cambio_estado,
# )

# class NotificacionesTestCase(TestCase):
    
#     def setUp(self):
#         self.categoria = Categoria.objects.create(nombre="Categoría 1")
#         self.subcategoria = Subcategoria.objects.create(
#             nombre="Subcategoría 1", categoria=self.categoria
#         )
#         # Crear un contenido de prueba
#         self.contenido = Contenido.objects.create(
#             tipo="Blog",
#             estado="Publicado",
#             titulo="Contenido 1",
#             texto="Texto del contenido 1",
#             categoria=self.categoria,
#             subcategoria=self.subcategoria,
#             megusta=10,
#             visualizaciones=100,
#             fecha_creacion=timezone.now() - timezone.timedelta(days=20),
#             autor_id=1,
#         )
    
    # @patch("appcms.utils.utils.obtenerUserInfoById")
    # @patch("appcms.utils.utils.enviar_notificacion")
    # def test_notificar_nuevo_contenido(self, mock_enviar_notificacion, mock_obtener_user_info):
    #     mock_obtener_user_info.return_value = {"email": "autor@example.com"}
        
    #     # Simular la creación de un nuevo contenido
    #     nuevo_contenido =Contenido.objects.create(
    #         tipo="Blog",
    #         estado="Publicado",
    #         titulo="Contenido 1",
    #         texto="Texto del contenido 1",
    #         categoria=self.categoria,
    #         subcategoria=self.subcategoria,
    #         megusta=10,
    #         visualizaciones=100,
    #         fecha_creacion=timezone.now() - timezone.timedelta(days=20),
    #         autor_id=2)
        
    #     # Verificar que se llamaron las funciones esperadas
    #     mock_obtener_user_info.assert_called_once_with(nuevo_contenido.autor_id)
    #     mock_enviar_notificacion.assert_called_once_with(
    #         "Contenido creado en",
    #         "Un nuevo contenido ha sido creado .",
    #         ["autor@example.com"]
    #     )

    # @patch("appcms.utils.utils.obtenerUserInfoById")
    # @patch("appcms.utils.utils.enviar_notificacion")
    # def test_notificar_edicion_contenido(self, mock_enviar_notificacion, mock_obtener_user_info):
    #     mock_obtener_user_info.return_value = 1
        
    #     # Ejecutar la notificación de edición
    #     notificar_edicion_contenido(self.contenido)
        
    #     # Verificar llamadas esperadas
    #     mock_obtener_user_info.assert_called_once_with(self.contenido.autor_id)
    #     mock_enviar_notificacion.assert_called_once_with(
    #         f"Edicion de contenido {self.contenido.titulo}",
    #         f'El contenido "{self.contenido.titulo}" ha sido editada.',
    #         ["autor@example.com"]
    #     )

    # @patch("appcms.utils.utils.obtenerUserInfoById")
    # @patch("appcms.utils.utils.enviar_notificacion")
    # def test_notificar_borrar_contenido(self, mock_enviar_notificacion, mock_obtener_user_info):
    #     mock_obtener_user_info.return_value = 1
        
    #     # Ejecutar la notificación de borrado
    #     notificar_borrar_contenido(self.contenido)
        
    #     # Verificar llamadas esperadas
    #     mock_obtener_user_info.assert_called_once_with(self.contenido.autor_id)
    #     mock_enviar_notificacion.assert_called_once_with(
    #         f"eliminacion de contenido {self.contenido.titulo}",
    #         f'El contenido "{self.contenido.titulo}" ha sido eliminado.',
    #         ["autor@example.com"]
    #     )

    # @patch("appcms.utils.utils.obtenerUserInfoById")
    # @patch("appcms.utils.utils.enviar_notificacion")
    # def test_notificar_nuevo_comentario(self, mock_enviar_notificacion, mock_obtener_user_info):
    #     mock_obtener_user_info.return_value = 1
    #     # Crear un comentario de prueba
    #     comentario = Comentario.objects.create(
    #         contenido=self.contenido,
    #         comentario="Comentario de prueba"
    #     )
        
    #     # Simular la creación de un nuevo comentario
    #     notificar_nuevo_comentario(Comentario, instance=comentario, created=True)
        
    #     # Verificar llamadas esperadas
    #     mock_obtener_user_info.assert_called_once_with(self.contenido.autor_id)
    #     mock_enviar_notificacion.assert_called_once_with(
    #         f"Nuevo comentario en {self.contenido.titulo}",
    #         f'Un nuevo comentario ha sido agregado al contenido "{self.contenido.titulo}".',
    #         ["autor@example.com"]
    #     )

    # @patch("appcms.utils.utils.obtenerUserInfoById")
    # @patch("appcms.utils.utils.enviar_notificacion")
    # def test_enviar_notificacion_cambio_estado(self, mock_enviar_notificacion, mock_obtener_user_info):
    #     mock_obtener_user_info.return_value = 1
        
    #     # Probar el cambio de estado a "Publicado"
    #     enviar_notificacion_cambio_estado("Publicado", self.contenido)
        
    #     # Verificar llamadas esperadas
    #     mock_obtener_user_info.assert_called_with(self.contenido.autor_id)
    #     mock_enviar_notificacion.assert_called_once_with(
    #         f"Contenido en Publicado: {self.contenido.titulo}",
    #         f'El contenido "{self.contenido.titulo}" ha sido publicado.',
    #         ["autor@example.com"]
    #     )
