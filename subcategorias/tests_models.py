# subcategorias/tests_models.py

from django.db.utils import IntegrityError
from django.test import TestCase
from appcms.models import Categoria
from .models import Subcategoria

class SubcategoriaModelTests(TestCase):
    """
    Pruebas unitarias para el modelo SubcategoriaModelTest
    """
    def setUp(self):
        """
        Configura el entorno para las pruebas creando una instancia de Categoria.
        :return: None
        :rtype: None
        """
        self.categoria = Categoria.objects.create(nombre='Categoria 1')

    def test_crear_subcategoria(self):
        """
        Prueba la creación de una instancia de Subcategoria.
        :return: None
        :rtype: None
        """
        subcategoria = Subcategoria.objects.create(
            nombre='Subcategoria 1',
            categoria=self.categoria
        )
        self.assertEqual(subcategoria.nombre, 'Subcategoria 1')
        self.assertEqual(subcategoria.categoria, self.categoria)

    def test_nombre_unico(self):
        """
        Prueba que no se pueden crear subcategorías con nombres duplicados.
        :return: None
        :rtype: None
        """
        # Crear la primera subcategoría con un nombre único
        Subcategoria.objects.create(
            nombre='Subcategoria Única',
            categoria=self.categoria
        )
        # Intentar crear una segunda subcategoría con el mismo nombre
        with self.assertRaises(IntegrityError):
            Subcategoria.objects.create(
                nombre='Subcategoria Única',
                categoria=self.categoria
            )


    def test_str_metodo(self):
        """
        Prueba que el método __str__() devuelve el nombre de la subcategoría.
        :return: None
        :rtype: None
        """
        subcategoria = Subcategoria.objects.create(
            nombre='Subcategoria de Prueba',
            categoria=self.categoria
        )
        self.assertEqual(str(subcategoria), 'Subcategoria de Prueba')
