from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("anime_details/", views.anime_details_view, name="anime_details"),
    path("categories/", views.category_view, name="category"),
    path("anime_watching/", views.anime_watching_view, name="anime_watching"),
    path("blog/", views.blog_view, name="blog"),
    path("blog_details/", views.blog_details_view, name="blog_details"),
    path("sign_up/", views.RegisterView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

]
