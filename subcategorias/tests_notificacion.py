from django.core import mail
from django.test import TestCase

from subcategorias.notificacion import notificar_nueva_subcategoria

from .models import Subcategoria


class NotificacionSubcategoriaTests(TestCase):
    def setUp(self):
        # Configura el entorno de prueba, crea una subcategoría de ejemplo
        self.subcategoria = Subcategoria.objects.create(nombre="Subcategoria Test")

    # def test_notificar_nueva_subcategoria(self):
    #     # Llama a la función de señal manualmente
    #     notificar_nueva_subcategoria(
    #         sender=Subcategoria, instance=self.subcategoria, created=True
    #     )

    #     # Verifica que se haya enviado un correo
    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertEqual(mail.outbox[0].subject, "Nueva Subcategoria en")
    #     self.assertIn("Una nueva subcategoria ha sido agregada", mail.outbox[0].body)

    # def test_no_enviar_correo_si_no_es_creado(self):
    #     # Llama a la función de señal  usualmente sin crear
    #     notificar_nueva_subcategoria(sender=Subcategoria, instance=self.subcategoria, created=False)

    #     # Verifica que no se haya enviado ningún correo
    #     self.assertEqual(len(mail.outbox), 0)
