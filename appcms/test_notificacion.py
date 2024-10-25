from django.test import TestCase, override_settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from appcms.utils.utils import enviar_notificacion
from django.test import TestCase
from unittest.mock import patch
from appcms.models import Categoria
from appcms.notificacion import (
    notificar_nueva_categoria,
    notificar_editar_categoria,
    notificar_borrar_categoria
)
@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class EnviarNotificacionTestCase(TestCase):

    def test_enviar_notificacion(self):
        # Datos de prueba
        asunto = "Prueba de Notificación"
        mensaje = "Este es un mensaje de prueba para el correo electrónico."
        destinatarios = ["destinatario@example.com"]

        # Llamada a la función
        enviar_notificacion(asunto, mensaje, destinatarios)

        # Verificaciones
        self.assertEqual(len(mail.outbox), 1)  # Verificar que se envió un correo
        email_enviado = mail.outbox[0]  # Obtener el correo enviado

        # Verificar asunto, destinatarios y contenido HTML y de texto plano
        self.assertEqual(email_enviado.subject, asunto)
        self.assertEqual(email_enviado.to, destinatarios)
        
        # Verificar el contenido HTML y el mensaje plano
        html_mensaje_esperado = render_to_string('notificacion.html', {'mensaje': mensaje})
        mensaje_plano_esperado = strip_tags(html_mensaje_esperado)
        
        self.assertEqual(email_enviado.body, mensaje_plano_esperado)
        self.assertEqual(email_enviado.alternatives[0][0], html_mensaje_esperado)
        self.assertEqual(email_enviado.alternatives[0][1], 'text/html')


class NotificacionTestCase(TestCase):

    @patch('appcms.notificacion.obtenerUsersConRol')
    @patch('appcms.notificacion.obtenerUserInfoById')
    @patch('appcms.notificacion.enviar_notificacion')
    def test_notificar_nueva_categoria(self, mock_enviar_notificacion, mock_obtenerUserInfoById, mock_obtenerUsersConRol):
        # Configurar mocks para devolver dos usuarios
        mock_obtenerUsersConRol.side_effect = lambda rol: [{'id': 1}, {'id': 2}]
        mock_obtenerUserInfoById.return_value = {"email": "usuario@example.com"}

        # Crear categoría que activa el signal
        categoria = Categoria.objects.create(nombre="Test Categoria")

        # Comprobar que se llama a enviar_notificacion
        asunto_esperado = f'Nueva categoria en {categoria.nombre}'
        mensaje_esperado = f'Una nueva categoria ha sido agregadoa: "{categoria.nombre}".'
        destinatarios_esperados = ['usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com']
        mock_enviar_notificacion.assert_called_once_with(asunto_esperado, mensaje_esperado, destinatarios_esperados)

    @patch('appcms.notificacion.obtenerUsersConRol')
    @patch('appcms.notificacion.obtenerUserInfoById')
    @patch('appcms.notificacion.enviar_notificacion')
    def test_notificar_editar_categoria(self, mock_enviar_notificacion, mock_obtenerUserInfoById, mock_obtenerUsersConRol):
        # Configurar mocks para devolver dos usuarios
        mock_obtenerUsersConRol.side_effect = lambda rol: [{'id': 1}, {'id': 2}]
        mock_obtenerUserInfoById.return_value = {"email": "usuario@example.com"}

        # Crear categoría de prueba
        categoria = Categoria(nombre="Test Categoria")

        # Llamar a la función para editar notificación
        notificar_editar_categoria(categoria)

        # Verificar que enviar_notificacion fue llamado con los valores esperados
        asunto_esperado = f'Edicion de categoria {categoria.nombre}'
        mensaje_esperado = f'La categoria"{categoria.nombre}" ha sido editada.'
        destinatarios_esperados = ['usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com']
        mock_enviar_notificacion.assert_called_once_with(asunto_esperado, mensaje_esperado, destinatarios_esperados)

    @patch('appcms.notificacion.obtenerUsersConRol')
    @patch('appcms.notificacion.obtenerUserInfoById')
    @patch('appcms.notificacion.enviar_notificacion')
    def test_notificar_borrar_categoria(self, mock_enviar_notificacion, mock_obtenerUserInfoById, mock_obtenerUsersConRol):
        # Configurar mocks para devolver dos usuarios
        mock_obtenerUsersConRol.side_effect = lambda rol: [{'id': 1}, {'id': 2}]
        mock_obtenerUserInfoById.return_value = {"email": "usuario@example.com"}

        # Crear categoría de prueba
        categoria = Categoria(nombre="Test Categoria")

        # Llamar a la función para eliminar notificación
        notificar_borrar_categoria(categoria)

        # Verificar que enviar_notificacion fue llamado con los valores esperados
        asunto_esperado = f'Edicion de eliminada: {categoria.nombre}'
        mensaje_esperado = f'La categoria"{categoria.nombre}" ha sido eliminada.'
        destinatarios_esperados = ['usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com', 'usuario@example.com']
        mock_enviar_notificacion.assert_called_once_with(asunto_esperado, mensaje_esperado, destinatarios_esperados)