from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import User
from django.contrib.auth import authenticate, login, logout


def home_view(request):
    return render(request, "pages/index.html")


def anime_details_view(request):
    return render(request, "pages/anime_details.html")


def category_view(request):
    return render(request, "pages/categories.html")


def anime_watching_view(request):
    return render(request, "pages/anime_watching.html")


def blog_view(request):
    return render(request, "pages/blog.html")


def blog_details_view(request):
    return render(request, "pages/blog_details.html")


class RegisterView(View):
    template_name = 'pages/sign_up.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')


        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('/sign_up')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email already exists")
            return redirect('/sign_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists")
            return redirect('/sign_up')

        is_first_user = not User.objects.exists()

        user = User.objects.create(
            email=email,
            password=make_password(password1),
            is_superuser=is_first_user,
            is_staff=is_first_user,
            username=username
        )
        user.save()
        login(request, user)

        return redirect('/')


class LoginView(View):
    template_name = "pages/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name)

def logout_view(request):
    logout(request)
    return redirect('/')
