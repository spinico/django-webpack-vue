from django.urls import path

from .api import animals
from .views import ClassBasedView, GenericClassBasedView

urlpatterns = [
    path('', GenericClassBasedView.as_view(), name='main'),
    path('frontend', ClassBasedView.as_view(), {'template': 'frontend.html'}, name='frontend'),
    path('api/animals/', animals, name='animals'),
]
