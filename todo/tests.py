from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

# Create your tests here.
from todo.views import index

class AnaSayfaTest(TestCase):
  
  """
  def testKökUrlYönlendiriyor(self):
    bulunan=resolve("/")
    #print (" BUrası = "+str(bulunan.func)+" <--")
    self.assertEqual(bulunan.func,index)
  """

  def testAnaSayfaDoğruHtml(self):
    request = HttpRequest()  
    response = index(request)  
    html = response.content.decode('utf8')  
    self.assertTrue(html.startswith('<!DOCTYPE html>'))  
    self.assertIn('<title> Anasayfa  | Yapılacaklar Listem</title>', html)  
    self.assertTrue(html.endswith('</html>'))  