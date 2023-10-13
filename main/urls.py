from django.urls import path
from .views import HomeTemplateView, about, feature, services, ShoppingCartTemplateView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('cart', ShoppingCartTemplateView.as_view(), name='cart'),
    path('about', about, name='about'),
    path('feature', feature, name='feature'),
    path('services', services, name='services'),
]

# ORM - Object Relational Mapping
