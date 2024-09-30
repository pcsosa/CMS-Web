from django.test import TestCase, Client
from django.urls import reverse
from appcms.models import Categoria

# ------------------------- Pruebas de buscar categoria ----------------------------------
'''
class BuscarCategoriasTest(TestCase):

    def setUp(self):
        # Crear algunas categorías de prueba
        Categoria.objects.create(nombre="Electronica")
        Categoria.objects.create(nombre="Ropa")
        Categoria.objects.create(nombre="Juguetes")

        # Instancia del cliente de prueba
        self.client = Client()

    def test_buscar_categoria_existente(self):
        # Prueba de búsqueda con una categoría existente
        response = self.client.get(reverse('buscar_categorias'), {'q': 'Electronica'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Electronica")
        self.assertNotContains(response, "No se encontraron categorías que coincidan con tu búsqueda.")

    def test_buscar_categoria_no_existente(self):
        # Prueba de búsqueda con una categoría que no existe
        response = self.client.get(reverse('buscar_categorias'), {'q': 'Automoviles'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No se encontraron categorías que coincidan con tu búsqueda.")
        self.assertEqual(list(response.context['categorias']), [])

    def test_buscar_con_acentos(self):
        # Prueba de búsqueda con acentos en la consulta
        response = self.client.get(reverse('buscar_categorias'), {'q': 'Electrónica'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Electronica")
        self.assertNotContains(response, "No se encontraron categorías que coincidan con tu búsqueda.")

    def test_buscar_numeros(self):
        # Prueba de búsqueda con números
        response = self.client.get(reverse('buscar_categorias'), {'q': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No se encontraron categorías que coincidan con tu búsqueda.")

'''
# ------------------------- Pruebas de crear categoria ----------------------------------

class CrearCategoriaTest(TestCase):

    def setUp(self):
        # Instancia del cliente de prueba
        self.client = Client()

    def test_crear_categoria_valida(self):
        # Prueba de creación de una categoría con datos válidos (POST request)
        data = {
            'nombre': 'Tecnología',
            'descripcion': 'Categoría relacionada con productos tecnológicos.',
        }
        response = self.client.post(reverse('crear_categoria'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nombre='Tecnología').exists())

  
# ------------------------- Pruebas de listar categorias ----------------------------------

class ListaCategoriasTest(TestCase):

    def setUp(self):
        # Instancia del cliente de prueba
        self.client = Client()

        # Crear algunas categorías de prueba
        Categoria.objects.create(nombre="Tecnología", descripcion="Categoría relacionada con tecnología.")
        Categoria.objects.create(nombre="Moda", descripcion="Categoría relacionada con la moda.")
        Categoria.objects.create(nombre="Hogar", descripcion="Categoría relacionada con el hogar.")

    def test_lista_categorias_view_status_code(self):
        # Prueba de que la vista responde con un código 200
        response = self.client.get(reverse('lista_categorias'))
        self.assertEqual(response.status_code, 200)

    def test_lista_categorias_usa_plantilla_correcta(self):
        # Prueba de que la vista utiliza la plantilla correcta
        response = self.client.get(reverse('lista_categorias'))
        self.assertTemplateUsed(response, 'lista_categorias.html')

    def test_lista_categorias_contenido(self):
        # Prueba de que la vista muestra todas las categorías
        response = self.client.get(reverse('lista_categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tecnología")
        self.assertContains(response, "Moda")
        self.assertContains(response, "Hogar")

        # Verificar que todas las categorías están en el contexto de la plantilla
        categorias = response.context['categorias']
        self.assertEqual(len(categorias), 3)

    def test_lista_categorias_sin_categorias(self):
        # Prueba de la vista cuando no hay categorías
        Categoria.objects.all().delete()  # Eliminar todas las categorías
        response = self.client.get(reverse('lista_categorias'))
        self.assertEqual(response.status_code, 200)


# ------------------------- Pruebas de eliminar categorias ----------------------------------

class EliminarCategoriaTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Categoria a eliminar')

    def test_eliminar_categoria_post(self):
        response = self.client.post(reverse('eliminar_categoria', args=[self.categoria.pk]))
        self.assertEqual(response.status_code, 302)  # Redirige después de eliminar
        self.assertFalse(Categoria.objects.filter(pk=self.categoria.pk).exists())

    def test_eliminar_categoria_get(self):
        response = self.client.get(reverse('eliminar_categoria', args=[self.categoria.pk]))
        self.assertEqual(response.status_code, 405)  # Método no permitido

    def test_eliminar_categoria_no_existente(self):
        # Prueba de que se maneja correctamente el intento de eliminar una categoría no existente
        response = self.client.get(reverse('eliminar_categoria', args=[999]))
        self.assertEqual(response.status_code, 404)
    '''
    def setUp(self):
        # Instancia del cliente de prueba
        self.client = Client()

        # Crear una categoría de prueba
        self.categoria = Categoria.objects.create(nombre="Tecnología", descripcion="Categoría de tecnología")

    def test_mostrar_confirmacion_eliminar_categoria(self):
        # Prueba de que la vista muestra el formulario de confirmación (GET request)
        response = self.client.get(reverse('eliminar_categoria', args=[self.categoria.pk]))
        self.assertEqual(response.status_code, 200)

        
        # Verifica el contenido del texto en la respuesta
        self.assertContains(response, f'¿Estás seguro de que deseas eliminar la categoría "{self.categoria.nombre}"?')

    def test_eliminar_categoria_post_request(self):
        # Prueba de que la categoría se elimina correctamente (POST request)
        response = self.client.post(reverse('eliminar_categoria', args=[self.categoria.pk]))
        
        # Verificar la redirección después de eliminar la categoría
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista_categorias'))

        # Verificar que la categoría ha sido eliminada
        with self.assertRaises(Categoria.DoesNotExist):
            Categoria.objects.get(pk=self.categoria.pk)

    def test_eliminar_categoria_get_no_elimina(self):
        # Prueba de que la categoría no se elimina con una solicitud GET
        response = self.client.get(reverse('eliminar_categoria', args=[self.categoria.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())
    '''
    
        