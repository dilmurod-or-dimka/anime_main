import random
import hashlib
from importlib.resources import contents

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import comment
from django.views import View
from django.contrib.auth import authenticate, login, logout

from amine_main import settings
from .models import Category, Anime, User, Blog, BlogComment, AnimeComment
from django.core.paginator import Paginator
from datetime import timedelta
from django.utils import timezone


def home_view(request):
    one_month_ago = timezone.now() - timedelta(days=30)
    anime_views = Anime.objects.filter(date__gte=one_month_ago).order_by('-views_count')
    categories = Category.objects.all()
    anime_views2 = Anime.objects.all().order_by('-views_count')[:4]
    anime_data = Anime.objects.all().order_by('-date')[:4]

    context = {
        'active_page': 'home',
        'categories': categories,
        'anime_views': anime_views[:6],
        'anime_data': anime_data,
        'anime_views2': anime_views2
    }

    return render(request, "pages/index.html", context)


def home_view2(request, slug):
    category = get_object_or_404(Category, slug=slug)
    anime = Anime.objects.filter(category=category)

    context = {
        'category': category,
        "anime": anime
    }
    return render(request, "pages/index.html", context)


def anime_details_view(request, slug):
    animes = get_object_or_404(Anime, slug=slug)
    animes.views_count += 1
    animes.save(update_fields=['views_count'])

    related_anime = Anime.objects.filter(category=animes.category).exclude(id=animes.id)[:4]

    comments = AnimeComment.objects.filter(anime=animes)

    context = {
        "comments": comments,
        "animes": animes,
        "related_anime": related_anime,
    }
    return render(request, "pages/anime_details.html", context)


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    anime = Anime.objects.filter(category=category)

    context = {
        "category": category,
        "anime": anime,
    }

    return render(request, "pages/categories.html", context)


def category_list_view(request):
    categories = Category.objects.all()
    anime_views = Anime.objects.all().order_by('-views_count')[:4]
    anime_data = Anime.objects.all().order_by('-date')[:4]

    paginator = Paginator(categories, 3)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)

    context = {
        'active_page': 'category',
        "anime_data": anime_data,
        "categories": categories,
        "anime_views": anime_views,
    }
    return render(request, "pages/categories.html", context)


def anime_watching_view(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    episodes = anime.episodes.all()

    context = {
        "anime": anime,
        "episodes": episodes,
    }
    return render(request, "pages/anime_watching.html", context)


def blog_view(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 2)

    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    context = {
        'active_page': 'blog',
        "blogs": blogs,
    }
    return render(request, "pages/blog.html", context)


def blog_details_view(request, slug):
    categories = Category.objects.all()[:3]
    blog = get_object_or_404(Blog, slug=slug)
    previous_blog = Blog.objects.filter(id__lt=blog.id).order_by('-id').first()
    next_blog = Blog.objects.filter(id__gt=blog.id).order_by('id').first()

    comments = BlogComment.objects.filter(blog=blog)

    context = {
        "categories": categories,
        "blog": blog,
        "previous_blog": previous_blog,
        "next_blog": next_blog,
        "comments": comments,
    }
    return render(request, "pages/blog_details.html", context)


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
        context = {
            'active_page': 'login',
        }
        return render(request, self.template_name, context)

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


class ProfileView(View):
    template_name = 'pages/profile.html'

    def get(self, request):
        user = request.user
        liked_anime = user.liked_anime.all()
        context = {
            'active_page': 'profile',
            "email": user.email,
            "photo": user.photo,
            "username": user.username,
            "liked_anime": liked_anime
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')

        if username:
            user.username = username
        if email:
            if not User.objects.filter(email=email).exclude(pk=user.pk).exists():
                user.email = email
            else:
                messages.warning(request, "This email is already in use.")
                return redirect('/profile')

        if photo:
            user.photo = photo

        user.save()
        messages.success(request, "Your profile has been updated.")
        return redirect('/profile')


@login_required
def delete_profile_picture(request):
    user = request.user
    try:
        if user.photo:
            user.photo.delete(save=False)
            user.photo = None
            user.save()

            messages.success(request, "Profile picture deleted successfully.")
        else:
            messages.info(request, "No profile picture to delete.")
    except User.DoesNotExist:
        messages.warning(request, "Profile does not exist.")

    return redirect('/profile')


@login_required
def like_anime(request, anime_slug):
    anime = get_object_or_404(Anime, slug=anime_slug)
    user = request.user
    if anime in user.liked_anime.all():
        user.liked_anime.remove(anime)
        messages.info(request, f"You removed {anime.title} from your liked anime.")
    else:
        user.liked_anime.add(anime)
        messages.success(request, f"You liked {anime.title}.")
    return redirect('anime_details_view', slug=anime_slug)


def add_blog_comment(request, slug):
    if request.method == "POST":
        blog = get_object_or_404(Blog, slug=slug)
        content = request.POST.get('content')

        if request.user.is_authenticated:
            comment = BlogComment(blog=blog, user=request.user, content=content)
            comment.save()

        return redirect('blog_details', slug=slug)



def add_anime_comment(request, slug):
    if request.method == "POST":
        anime = get_object_or_404(Anime, slug=slug)
        content = request.POST.get('content')

        if request.user.is_authenticated:
            comment = AnimeComment(anime=anime, user=request.user, content=content)
            comment.save()

        return redirect('anime_details_view', slug=slug)


def anime_search_view(request):
    query = request.GET.get('q')
    results = Anime.objects.none()

    anime_views = Anime.objects.all().order_by('-views_count')[:4]
    anime_data = Anime.objects.all().order_by('-date')[:4]

    if query:
        results = Anime.objects.filter(
            Q(title__icontains=query) | Q(descr__icontains=query)
        )
    context = {
        'results': results,
        'query': query,
        'anime_views': anime_views,
        'anime_data': anime_data
    }
    return render(request, 'pages/anime_search_results.html', context)


reset_tokens = {}


def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            token = hashlib.sha256(str(random.random()).encode('utf8')).hexdigest()
            reset_tokens[email] = token

            reset_link = request.build_absolute_uri(f'/reset_password/{token}/')

            send_mail(
                'Сброс пароля',
                f'Перейдите по следующей ссылке для сброса пароля: {reset_link}',
                'from@example.com',  # Замените на ваш email
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Ссылка для сброса пароля отправлена на вашу почту.')
            return redirect('forgot_password')
        except User.DoesNotExist:
            messages.info(request, 'Пользователь с таким email не найден.')

    return render(request, 'registration/forgot_password.html')


def reset_password_view(request, token):
    email = None
    for stored_email, stored_token in reset_tokens.items():
        if stored_token == token:
            email = stored_email
            break

    if not email:
        return HttpResponse("Неверный или устаревший токен.")

    if request.method == 'POST':
        new_password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            del reset_tokens[email]

            messages.success(request, "Пароль успешно изменён.")
            return redirect('login')
        except User.DoesNotExist:
            messages.info(request, "Пользователь не найден.")

    return render(request, 'registration/reset_password.html', {"token": token})
