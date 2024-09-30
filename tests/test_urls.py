from django.test import SimpleTestCase 
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from appcms.views import lista_categorias, login


class TestUrls(SimpleTestCase):
  """
  Clase para testear todas las urls
  """

  def test_buscar_categorias_url_resolves(self):
      '''
      url = reverse( 'buscar_categorias')
      self.assertEqual(resolve(url).func, buscar_categorias)
       '''

  def test_lista_categorias_url_resolves(self):
      url = reverse( 'lista_categorias')
      self.assertEqual(resolve(url).func, lista_categorias)

  def test_login_url_is_resolved(self): 
      url = reverse('login')
      resolved_view = resolve(url)
      self.assertEqual(resolved_view.func, login)


            
