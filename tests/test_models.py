from django.test import TestCase
from appcms.models import Categoria

class CategoriaModelTest(TestCase):

    def setUp(self):
        # Crear una instancia de Categoria para usar en las pruebas
        self.categoria = Categoria.objects.create(
            nombre="Tecnología",
            descripcion="Categoría relacionada con temas tecnológicos."
        )

    def test_categoria_str(self):
        # Prueba la representación en cadena (__str__) del modelo
        self.assertEqual(str(self.categoria), "Tecnología")

    def test_get_descripcion(self):
        # Prueba el método get_descripcion
        descripcion = self.categoria.get_descripcion()
        self.assertEqual(descripcion, "Categoría relacionada con temas tecnológicos.")

    def test_nombre_unico(self):
        # Prueba que el nombre de la categoría sea único
        with self.assertRaises(Exception):
            Categoria.objects.create(
                nombre="Tecnología",
                descripcion="Otra descripción."
            )

    def test_max_length_nombre(self):
        # Prueba la longitud máxima del campo nombre
        max_length = self.categoria._meta.get_field('nombre').max_length
        self.assertEqual(max_length, 100)

    def test_max_length_descripcion(self):
        # Prueba la longitud máxima del campo descripcion
        max_length = self.categoria._meta.get_field('descripcion').max_length
        self.assertEqual(max_length, 500)
