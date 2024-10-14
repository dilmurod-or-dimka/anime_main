from django.contrib import admin
from .models import Category, AnimeImage, Anime, Episodes, User, Blog, BlogImg, BlogComment, AnimeComment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug")
    list_display_links = ("pk", "title")
    prepopulated_fields = {"slug": ("title",)}


class AnimeImageInline(admin.TabularInline):
    model = AnimeImage
    extra = 1


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "type", "status", "quality", "category")
    list_display_links = ("title", "pk")
    list_filter = ("category",)
    prepopulated_fields = {'slug': ("title",)}
    inlines = [AnimeImageInline]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "photo")

class BlogImgInline(admin.TabularInline):
    model = BlogImg
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "date", "slug")
    list_display_links = ("pk", "title")
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogImgInline]

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "content", "created_at", "blog")
    list_display_links = ("pk", "user")

@admin.register(AnimeComment)
class AnimeCommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "content", "created_at", "anime")
    list_display_links = ("pk", "user")

@admin.register(Episodes)
class EpisodesAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "number")
    list_display_links = ("pk", "title")
