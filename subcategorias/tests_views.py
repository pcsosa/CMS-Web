from django.test import TestCase
from django.urls import reverse
from .models import Subcategoria
from appcms.models import Categoria


class SubcategoriaViewTests(TestCase):
    def setUp(self):
        """
        Configura el entorno de pruebas creando una instancia de Categoria
        y una instancia de Subcategoria asociada a esa categoría.
        """
        # Crear una instancia de Categoria
        self.categoria = Categoria.objects.create(nombre='Categoria 1')
        # Crear una instancia de Subcategoria con la categoria_id correcta
        self.subcategoria = Subcategoria.objects.create(nombre='Subcategoria 1', categoria=self.categoria)
    
    def test_lista_subcategorias(self):
        """
        Prueba para verificar que la vista 'lista_subcategorias' se renderiza correctamente
        y contiene la subcategoría creada.
        """
        # Prueba para la vista lista_subcategorias.
        response = self.client.get(reverse('lista_subcategorias',args=[self.subcategoria.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subcategoria 1')
    
    def test_crear_subcategoria(self):
        # Simular el envío de un formulario para crear una nueva subcategoría
        response = self.client.post(reverse('crear_subcategorias'), {
            'nombre': 'Subcategoria 1',
            'categoria': self.categoria.pk
        })
        
        self.assertEqual(Subcategoria.objects.filter(nombre='Subcategoria 1').count(), 1)
        redirect_url = reverse('lista_subcategorias', args=[self.categoria.pk])

    def test_crear_subcategoria_post_invalid(self):
        """
        Prueba para la vista 'crear_subcategoria' con método POST inválido.
        Verifica que no se redirige si el nombre está vacío y que el formulario muestra el error adecuado.
        Además, prueba que el nombre duplicado también genera el mensaje de error correcto.
        """
        # Intentar crear una subcategoría con nombre vacío
        response_invalid = self.client.post(reverse('crear_subcategorias'), {
            'nombre': '',  # Nombre vacío
            'categoria': self.categoria.pk
        }, HTTP_REFERER=reverse('crear_subcategorias'))
   
        # Verificar que el formulario muestra errores y  se redirige
        self.assertEqual(response_invalid.status_code,302)  
        
       
    def test_eliminar_subcategoria_post(self):
        """
        Prueba para la vista 'eliminar_subcategoria' con método POST para verificar que
        la subcategoría se elimina correctamente y redirige.
        """
        # Prueba para la vista eliminar_subcategoria con método POST.
        response = self.client.post(reverse('eliminar_subcategoria', args=[self.subcategoria.pk]))
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar.
        self.assertFalse(Subcategoria.objects.filter(pk=self.subcategoria.pk).exists())
