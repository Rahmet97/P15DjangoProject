import json

from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.http.response import JsonResponse

from .models import Service, Image, ShoppingCart, Comment, Order


class HomeTemplateView(View):
    template_name = 'index.html'
    context = {}

    def get(self, request):
        service_data = Service.objects.all()  # select * from main_service
        comments = Comment.objects.all().order_by('-created_at')[:4]
        services_data = []
        for service in service_data:
            image = Image.objects.filter(service=service).first()  #  select * from image where service_id=service_id
            service.image = image
            services_data.append(service)
        self.context.update({'service_data': services_data})
        self.context.update({'comments': comments})
        return render(request, self.template_name, self.context)

    def post(self, request):
        service_id = request.POST.get('service_id')
        if request.user is None:
            return redirect('/accounts/login')
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
        if request.user.id is None:
            return redirect('/accounts/login')
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        data = []
        for index, value in enumerate(shopping_cart):
            image = Image.objects.filter(service=value.service).first()
            print(image)
            value.img = image
            value.index = index+1
            data.append(value)
        self.context.update({'shopping_cart_products': data})
        return render(request, self.template_name, self.context)

    def post(self, request):
        shopping_cart_id = request.POST.get('shopping_cart_id')
        ShoppingCart.objects.get(pk=shopping_cart_id).delete()
        return redirect('/cart')


class IncrementCountAPIView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_cart_id = json_data.get('id')
            shopping_cart = ShoppingCart.objects.get(pk=shopping_cart_id)
            shopping_cart.count += 1
            shopping_cart.save()
        except Exception as e:
            return JsonResponse({'success': False, 'error': e})
        return JsonResponse({'success': True})


class DecrementCountAPIView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_cart_id = json_data.get('id')
            shopping_cart = ShoppingCart.objects.get(pk=shopping_cart_id)
            if shopping_cart.count > 0:
                shopping_cart.count -= 1
                shopping_cart.save()
        except Exception as e:
            return JsonResponse({'success': False, 'error': e})
        return JsonResponse({'success': True})


class ChangeCountAPIView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_cart_id = json_data.get('id')
            product_count = json_data.get('product_count')

            shopping_cart = ShoppingCart.objects.get(pk=shopping_cart_id)
            if product_count is not None:
                shopping_cart.count = product_count
                shopping_cart.save()
        except Exception as e:
            return JsonResponse({'success': False, 'error': e})
        return JsonResponse({'success': True})


class SearchView(View):
    template_name = 'search.html'
    context = {}

    def get(self, request):
        pass


class CheckoutView(View):

    def post(self, request):
        user_id = request.POST.get('user_id')
        shopping_cart = ShoppingCart.objects.filter(user_id=user_id)


class AddProductView(View):
    template_name = 'add_product.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('desc')
        price = request.POST.get('price')
        images = request.FILES.getlist('images')

        service = Service.objects.create(
            title=title,
            description=description,
            price=price,
            author=request.user
        )
        service.save()
        for image in images:
            img = Image.objects.create(
                img=image,
                service=service
            )
            img.save()
        return redirect('/add-product')


class CommentView(View):
    template_name = 'comment.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        message = request.POST.get('message')
        is_anonymous = request.POST.get('is_anonymous')
        user = None if is_anonymous == 'on' else request.user

        comment = Comment.objects.create(
            message=message,
            user=user
        )
        comment.save()
        return redirect('/')


class OrderView(View):
    template_name = 'checkout.html'
    context = {}

    def get(self, request):
        services_data = Order.objects.select_related('service').filter(user=request.user)
        self.context.update({'services_data': services_data})
        return render(request, self.template_name, self.context)

    def post(self, request):
        services = ShoppingCart.objects.select_related('service').filter(user=request.user)
        for service in services:
            order = Order.objects.create(
                user=request.user,
                service=service.service,
                count=service.count,
                status=1
            )
            order.save()
        return redirect('/checkout')


def about(request):
    return render(request, 'about.html')


def feature(request):
    return render(request, 'feature.html')


def services(request):
    return render(request, 'service.html')
def abdugani(request):
    return render(request,'404.html')