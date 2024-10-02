from django.contrib import admin
from .models import Category, AnimeImage, Anime, User


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
