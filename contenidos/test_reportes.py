from django.test import TestCase,Client
from django.urls import reverse
from django.utils import timezone

from appcms.models import Categoria
from contenidos.models_cont import Contenido, Visualizacion
from subcategorias.models import Subcategoria


class ReportesEstadisticosTests(TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas:
        - Crea categorías y subcategorías.
        - Crea contenidos con diferentes características.
        - Crea visualizaciones para los contenidos.
        """
        self.client = Client()
        # Crear categorías y subcategorías
        self.categoria = Categoria.objects.create(nombre="Categoría 1")
        self.subcategoria = Subcategoria.objects.create(
            nombre="Subcategoría 1", categoria=self.categoria
        )

        # Crear contenidos
        self.contenido1 = Contenido.objects.create(
            tipo="Blog",
            estado="Publicado",
            titulo="Contenido 1",
            texto="Texto del contenido 1",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            megusta=10,
            visualizaciones=100,
            fecha_creacion=timezone.now() - timezone.timedelta(days=20),
        )
        self.contenido2 = Contenido.objects.create(
            tipo="Multimedia",
            estado="Publicado",
            titulo="Contenido 2",
            texto="Texto del contenido 2",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            megusta=20,
            visualizaciones=200,
            fecha_creacion=timezone.now() - timezone.timedelta(days=5),
        )

        # Crear visualizaciones
        Visualizacion.objects.create(
            contenido=self.contenido1, fecha=timezone.now() - timezone.timedelta(days=1)
        )
        Visualizacion.objects.create(
            contenido=self.contenido2, fecha=timezone.now() - timezone.timedelta(days=1)
        )

    def test_reporte_contenido(self):
        """
        Prueba que el reporte de contenido se genere correctamente.
        Verifica que la respuesta contenga los elementos esperados del reporte.
        """
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reporte de Contenidos")
        self.assertContains(response, "Total de Visitas")
        self.assertContains(response, "Total de Me Gusta")
        self.assertContains(response, "Total de Contenidos")
        self.assertContains(response, "Artículos Redactados")
        self.assertContains(response, "Promedio de Tiempo de Revisión")

    def test_top_5_mas_leidos(self):
        """
        Prueba que el reporte incluya los 5 artículos más leídos.
        Verifica que los títulos de los contenidos más leídos estén presentes en la respuesta.
        """
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Top 5 Artículos Más Leídos")
        self.assertContains(response, self.contenido2.titulo)
        self.assertContains(response, self.contenido1.titulo)

    def test_grafico_me_gusta(self):
        """
        Prueba que el reporte incluya un gráfico de 'Me Gusta' para los 5 contenidos más populares.
        Verifica que los valores de 'Me Gusta' de los contenidos estén presentes en la respuesta.
        """
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gráfico de Me Gusta (Top 5)")
        self.assertContains(response, self.contenido1.megusta)
        self.assertContains(response, self.contenido2.megusta)

    # Da fallo
    def test_filtrar_contenidos(self):
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": (timezone.now() - timezone.timedelta(days=10)).date(),
                "fecha_fin": (timezone.now() + timezone.timedelta(days=10)).date(),
                "estado": "Publicado",
                "categoria": self.categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contenido2.titulo)
        self.assertContains(response, self.contenido1.titulo)

    def test_reporte_sin_contenidos(self):
        """
        Prueba que el reporte se genere correctamente cuando no hay contenidos.
        Verifica que los totales de visitas, 'Me Gusta' y contenidos sean cero.
        """
        Contenido.objects.all().delete()
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reporte de Contenidos")
        self.assertContains(response, "Total de Visitas: 0")
        self.assertContains(response, "Total de Me Gusta: 0")
        self.assertContains(response, "Total de Contenidos: 0")

    # Da fallo
    def test_reporte_contenido_borrador(self):
        self.contenido1.estado = "Borrador"
        self.contenido1.save()
        response = self.client.get(reverse('reporte'),{
            'fecha_inicio':'',
            'fecha_fin':'',
            'estado':'Borrador',
            'categoria':'',
            'subcategoria':''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    # Da fallo
    def test_reporte_contenido_inactivo(self):
        self.contenido2.estado = "Inactivo"
        self.contenido2.save()
        response = self.client.get("http://localhost:8000/panel/reporte?fecha_inicio=&fecha_fin=&estado=Inactivo&categoria=&subcategoria=")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertContains(response, self.contenido2.titulo)

    def test_reporte_contenido_fecha_fuera_rango(self):
        """
        Prueba que el reporte no incluya contenidos fuera del rango de fechas especificado.
        Verifica que los títulos de los contenidos no estén presentes en la respuesta.
        """
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": (timezone.now() - timezone.timedelta(days=30)).date(),
                "fecha_fin": (timezone.now() - timezone.timedelta(days=25)).date(),
                "estado": "Publicado",
                "categoria": self.categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_categoria_incorrecta(self):
        """
        Prueba que el reporte no incluya contenidos de una categoría incorrecta.
        Verifica que los títulos de los contenidos no estén presentes en la respuesta.
        """
        otra_categoria = Categoria.objects.create(nombre="Otra Categoría")
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": '',
                "fecha_fin": '',
                "estado": "Publicado",
                "categoria": otra_categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_subcategoria_incorrecta(self):
        """
        Prueba que el reporte no incluya contenidos de una subcategoría incorrecta.
        Verifica que los títulos de los contenidos no estén presentes en la respuesta.
        """
        otra_subcategoria = Subcategoria.objects.create(
            nombre="Otra Subcategoría", categoria=self.categoria
        )
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": '',
                "fecha_fin": '',
                "estado": "Publicado",
                "categoria": self.categoria.id_categoria,
                "subcategoria": otra_subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_estado_incorrecto(self):
        """
        Prueba que el reporte no incluya contenidos con un estado incorrecto.
        Verifica que los títulos de los contenidos no estén presentes en la respuesta.
        """
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": '',
                "fecha_fin": '',
                "estado": "Borrador",
                "categoria": self.categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_sin_filtros(self):
        """
        Prueba que el reporte incluya todos los contenidos cuando no se aplican filtros.
        Verifica que los títulos de todos los contenidos estén presentes en la respuesta.
        """
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contenido1.titulo)
        self.assertContains(response, self.contenido2.titulo)

    def test_reporte_contenido_fecha_inicio_futura(self):
        """
        Prueba que el reporte no incluya contenidos cuando la fecha de inicio es futura.
        Verifica que los títulos de los contenidos no estén presentes en la respuesta.
        """
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": (timezone.now() + timezone.timedelta(days=1)).date(),
                "fecha_fin": (timezone.now() + timezone.timedelta(days=10)).date(),
                "estado": "Publicado",
                "categoria": self.categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_fecha_fin_pasada(self):
        """
        Prueba que el reporte no incluya contenidos cuando la fecha de fin es pasada.
        Verifica que los títulos de los contenidos no estén presentes en la respuesta.
        """
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": (timezone.now() - timezone.timedelta(days=20)).date(),
                "fecha_fin": (timezone.now() - timezone.timedelta(days=15)).date(),
                "estado": "Publicado",
                "categoria": self.categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)
        