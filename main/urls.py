from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    HomeTemplateView,
    about,
    feature,
    services,
    abdugani,
    ShoppingCartTemplateView,
    IncrementCountAPIView,
    DecrementCountAPIView, ChangeCountAPIView, AddProductView, CommentView
)

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('cart', ShoppingCartTemplateView.as_view(), name='cart'),
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('comment', CommentView.as_view(), name='comment'),
    path('about', about, name='about'),
    path('feature', feature, name='feature'),
    path('services', services, name='services'),
    path('abdugani',abdugani,name=('abdugani')),

    # API
    path('increment', csrf_exempt(IncrementCountAPIView.as_view()), name='increment'),
    path('decrement', csrf_exempt(DecrementCountAPIView.as_view()), name='decrement'),
    path('change', csrf_exempt(ChangeCountAPIView.as_view()), name='change'),
]

# ORM - Object Relational Mapping
