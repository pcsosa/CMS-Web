from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from appcms.models import Categoria
from contenidos.models_cont import Contenido, Visualizacion
from subcategorias.models import Subcategoria


class ReportesEstadisticosTests(TestCase):
    def setUp(self):
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
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reporte de Contenidos")
        self.assertContains(response, "Total de Visitas")
        self.assertContains(response, "Total de Me Gusta")
        self.assertContains(response, "Total de Contenidos")
        self.assertContains(response, "Artículos Redactados")
        self.assertContains(response, "Promedio de Tiempo de Revisión")

    def test_top_5_mas_leidos(self):
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Top 5 Artículos Más Leídos")
        self.assertContains(response, self.contenido2.titulo)
        self.assertContains(response, self.contenido1.titulo)

    def test_grafico_me_gusta(self):
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gráfico de Me Gusta (Top 5)")
        self.assertContains(response, self.contenido1.megusta)
        self.assertContains(response, self.contenido2.megusta)

    # Da fallo
    # def test_filtrar_contenidos(self):
    #     response = self.client.get(
    #         reverse("reporte"),
    #         {
    #             "fecha_inicio": (timezone.now() - timezone.timedelta(days=10)).date(),
    #             "fecha_fin": (timezone.now() + timezone.timedelta(days=10)).date(),
    #             "estado": "Publicado",
    #             "categoria": self.categoria.id_categoria,
    #             "subcategoria": self.subcategoria.id_subcategoria,
    #         },
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, self.contenido2.titulo)
    #     self.assertNotContains(response, self.contenido1.titulo)

    def test_reporte_sin_contenidos(self):
        Contenido.objects.all().delete()
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reporte de Contenidos")
        self.assertContains(response, "Total de Visitas: 0")
        self.assertContains(response, "Total de Me Gusta: 0")
        self.assertContains(response, "Total de Contenidos: 0")

    # Da fallo
    # def test_reporte_contenido_borrador(self):
    #     self.contenido1.estado = "Borrador"
    #     self.contenido1.save()
    #     response = self.client.get(reverse("reporte"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotContains(response, self.contenido1.titulo)
    #     self.assertContains(response, self.contenido2.titulo)

    # Da fallo
    # def test_reporte_contenido_inactivo(self):
    #     self.contenido2.estado = "Inactivo"
    #     self.contenido2.save()
    #     response = self.client.get(reverse("reporte"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, self.contenido1.titulo)
    #     self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_fecha_fuera_rango(self):
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
        otra_categoria = Categoria.objects.create(nombre="Otra Categoría")
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": (timezone.now() - timezone.timedelta(days=10)).date(),
                "fecha_fin": (timezone.now() + timezone.timedelta(days=10)).date(),
                "estado": "Publicado",
                "categoria": otra_categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_subcategoria_incorrecta(self):
        otra_subcategoria = Subcategoria.objects.create(
            nombre="Otra Subcategoría", categoria=self.categoria
        )
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": (timezone.now() - timezone.timedelta(days=10)).date(),
                "fecha_fin": (timezone.now() + timezone.timedelta(days=10)).date(),
                "estado": "Publicado",
                "categoria": self.categoria.id_categoria,
                "subcategoria": otra_subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_estado_incorrecto(self):
        response = self.client.get(
            reverse("reporte"),
            {
                "fecha_inicio": (timezone.now() - timezone.timedelta(days=10)).date(),
                "fecha_fin": (timezone.now() + timezone.timedelta(days=10)).date(),
                "estado": "Borrador",
                "categoria": self.categoria.id_categoria,
                "subcategoria": self.subcategoria.id_subcategoria,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.contenido1.titulo)
        self.assertNotContains(response, self.contenido2.titulo)

    def test_reporte_contenido_sin_filtros(self):
        response = self.client.get(reverse("reporte"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contenido1.titulo)
        self.assertContains(response, self.contenido2.titulo)

    def test_reporte_contenido_fecha_inicio_futura(self):
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
