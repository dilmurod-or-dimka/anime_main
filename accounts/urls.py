from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path('anime/<slug:slug>/', views.anime_details_view, name='anime_details_view'),
    path("categories/<slug:slug>/", views.category_view, name="category"),
    path("category/", views.category_list_view, name="category_list"),
    path("anime_watching/", views.anime_watching_view, name="anime_watching"),
    path("blog/", views.blog_view, name="blog"),
    path("blog_details/<slug:slug>/", views.blog_details_view, name="blog_details"),
    path("sign_up/", views.RegisterView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("delete_profile_picture/", views.delete_profile_picture, name="delete_profile_picture"),
    path('anime/<slug:anime_slug>/like/', views.like_anime, name='like_anime'),
    path('add_blog_comment/<slug:slug>/', views.add_blog_comment, name='add_blog_comment'),
    path('add_anime_comment/<slug:slug>/', views.add_anime_comment, name='add_anime_comment'),
    path("<slug:slug>/", views.home_view2, name="home2"),
]
