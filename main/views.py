from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.contrib import messages

from .models import Service, Image, ShoppingCart


class HomeTemplateView(View):
    template_name = 'index.html'
    context = {}

    def get(self, request):
        service_data = Service.objects.all()  # select * from main_service
        services_data = []
        for service in service_data:
            image = Image.objects.filter(service=service).first()  #  select * from image where service_id=service_id
            service.image = image
            services_data.append(service)
        self.context.update({'service_data': services_data})
        return render(request, self.template_name, self.context)

    def post(self, request):
        service_id = request.POST.get('service_id')
        user = request.user
        if not ShoppingCart.objects.filter(Q(user=user) & Q(service_id=service_id)).exists():
            shopping_cart = ShoppingCart.objects.create(
                user=user,
                service_id=service_id
            )
            shopping_cart.save()
            messages.info(request, 'Product added to cart')
            return redirect(f'/#service_{service_id}')

        messages.error(request, 'This service already exists in cart!')
        return redirect(f'/#service_{service_id}')

        # select * from service where user='birnarsalar' and service='ikkinarsalar'


class ShoppingCartTemplateView(View):
    template_name = 'shopping_cart.html'
    context = {}

    def get(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        data = []
        for index, value in enumerate(shopping_cart):
            image = Image.objects.filter(service=value.service).first()
            print(image)
            value.img = image
            value.index = index+1
            value.total = value.service.price * value.count
            data.append(value)
        self.context.update({'shopping_cart_products': data})
        return render(request, self.template_name, self.context)


def about(request):
    return render(request, 'about.html')


def feature(request):
    return render(request, 'feature.html')


def services(request):
    return render(request, 'service.html')
