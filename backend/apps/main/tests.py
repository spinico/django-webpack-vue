from django.test import TestCase
from django.urls import resolve, reverse

from .views import GenericClassBasedView


class main_views(TestCase):
    def test_default_page_view_status_code(self):
        url = reverse('main')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_default_page_view_root_url(self):
        view = resolve('/')
        self.assertEquals(view.view_name, 'main')
