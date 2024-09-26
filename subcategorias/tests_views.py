from django.test import TestCase, Client
from django.urls import reverse
from .models import Subcategoria
from appcms.models import Categoria
from .forms import SubcategoriaForm

class SubcategoriaViewTests(TestCase):
    def setUp(self):
        """
        Configura el entorno de pruebas creando una instancia de Categoria
        y una instancia de Subcategoria asociada a esa categoría.
        :return: None
        :rtype: None
        """
        # Crear una instancia de Categoria
        self.categoria = Categoria.objects.create(nombre='Categoria 1')
        # Crear una instancia de Subcategoria con la categoria_id correcta
        self.subcategoria = Subcategoria.objects.create(nombre='Subcategoria 1', categoria=self.categoria)
    
    def test_lista_subcategorias(self):
        """
        Prueba para verificar que la vista 'lista_subcategorias' se renderiza correctamente
        y contiene la subcategoría creada.
        :return: None
        :rtype: None
        """
        # Prueba para la vista lista_subcategorias.
        response = self.client.get(reverse('lista_subcategorias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista_subcategorias.html')
        self.assertContains(response, 'Subcategoria 1')
    
    def test_crear_subcategoria_get(self):
        """
        Prueba para la vista 'crear_subcategoria' con método GET para asegurarse de
        que el formulario se muestra correctamente.
        :return: None
        :rtype: None
        """
        # Prueba para la vista crear_subcategoria con método GET.
        response = self.client.get(reverse('crear_subcategorias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crear_subcategoria.html')
        self.assertIsInstance(response.context['form'], SubcategoriaForm)
    
    def test_crear_subcategoria_post_valid(self):
        """
        Prueba para la vista 'crear_subcategoria' con método POST válido. Verifica
        que una nueva subcategoría se crea y redirige correctamente.
        :return: None
        :rtype: None
        """
        # Prueba para la vista crear_subcategoria con método POST válido.
        # Usa el ID de la categoría creada en setUp
        data = {'nombre': 'Nueva Subcategoria', 'categoria': self.categoria.pk}
        response = self.client.post(reverse('crear_subcategorias'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de guardar.
        self.assertTrue(Subcategoria.objects.filter(nombre='Nueva Subcategoria').exists())
    
    def test_crear_subcategoria_post_invalid(self):
        """
        Prueba para la vista 'crear_subcategoria' con método POST inválido.
        Verifica que no se redirige si el nombre está vacío y que el formulario muestra el error adecuado.
        Además, prueba que el nombre duplicado también genera el mensaje de error correcto.
        :return: None
        :rtype: None
        """
        # Intentar crear una subcategoría con nombre vacío
        data_invalid = {'nombre': '', 'categoria': self.categoria.pk}
        response_invalid = self.client.post(reverse('crear_subcategorias'), data_invalid)
        # Verificar que el formulario muestra errores y no se redirige
        self.assertEqual(response_invalid.status_code, 200)  # Debe permanecer en la misma página
        self.assertTemplateUsed(response_invalid, 'crear_subcategoria.html')
        self.assertContains(response_invalid, "Este campo es obligatorio.")  # Mensaje para nombre vacío
        # Intentar crear una subcategoría con nombre duplicado
        data_duplicate = {'nombre': 'Subcategoria 1', 'categoria': self.categoria.pk}
        response_duplicate = self.client.post(reverse('crear_subcategorias'), data_duplicate)
        # Verificar que el formulario muestra errores y no se redirige
        self.assertEqual(response_duplicate.status_code, 200)  # Debe permanecer en la misma página
        self.assertTemplateUsed(response_duplicate, 'crear_subcategoria.html')
        self.assertContains(response_duplicate, "Ya existe Subcategoria con este Nombre.")  # Mensaje para nombre duplicado
        # Verificar que no se han creado subcategorías con nombre vacío o duplicado
        self.assertFalse(Subcategoria.objects.filter(nombre='').exists())
        self.assertEqual(Subcategoria.objects.filter(nombre='Subcategoria 1').count(), 1)
        
    def test_eliminar_subcategoria_get(self):
        """
        Prueba para la vista 'eliminar_subcategoria' con método GET para verificar que
        la vista se muestra correctamente y contiene la subcategoría a eliminar.
        :return: None
        :rtype: None
        """
        # Prueba para la vista eliminar_subcategoria con método GET.
        response = self.client.get(reverse('eliminar_subcategoria', args=[self.subcategoria.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eliminar_subcategoria.html')
        self.assertContains(response, 'Subcategoria 1')
    
    def test_eliminar_subcategoria_post(self):
        """
        Prueba para la vista 'eliminar_subcategoria' con método POST para verificar que
        la subcategoría se elimina correctamente y redirige.
        :return: None
        :rtype: None
        """
        # Prueba para la vista eliminar_subcategoria con método POST.
        response = self.client.post(reverse('eliminar_subcategoria', args=[self.subcategoria.pk]))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar.
        self.assertFalse(Subcategoria.objects.filter(pk=self.subcategoria.pk).exists())
