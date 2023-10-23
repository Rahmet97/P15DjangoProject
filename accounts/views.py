from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, hashers, authenticate, login, logout
from django.contrib import messages
from django.views import View

from .forms import LoginForm

User = get_user_model()


class LoginView(View):
    template_name = 'login.html'
    context = {}

    def get(self, request):
        form = LoginForm()
        self.context.update({'form': form})
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Username or password is not valid!')
        return redirect('/accounts/login')


class RegisterView(View):
    template_name = 'register.html'
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('/accounts/register')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return redirect('/accounts/register')
            else:
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=hashers.make_password(password1)
                )
                user.save()
                return redirect('/accounts/login')
        else:
            messages.error(request, 'Passwords are not same!')
            return redirect('/accounts/register')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/accounts/login')
