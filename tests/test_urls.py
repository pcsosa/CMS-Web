from django.test import SimpleTestCase 
from django.urls import reverse, resolve
from appcms.views import buscar_categorias


class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse( 'buscar_categorias')
        self.assertEqual(resolve(url).func, buscar_categorias)