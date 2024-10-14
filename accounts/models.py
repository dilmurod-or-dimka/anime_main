from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    title = models.CharField(verbose_name="Category title", max_length=150, unique=True)
    slug = models.SlugField(blank=True, unique=True, null=True)

    def get_absolute_url(self):
        return reverse("category_view", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            num = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Anime(models.Model):
    STATUS_CHOICES = [
        ('airing', 'Airing'),
        ('aired', 'Aired'),
        ('paused', 'Paused'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Anime name", max_length=150, unique=True)
    descr = models.TextField(verbose_name="Description")
    type = models.CharField(verbose_name="Type", max_length=150)
    studio = models.CharField(verbose_name="Studio", max_length=150)
    date = models.DateField(verbose_name="Date")
    status = models.CharField(verbose_name="Status", max_length=10, choices=STATUS_CHOICES, default='aired')
    genre = models.TextField(verbose_name="Genre")
    duration = models.IntegerField(verbose_name="Duration")
    quality = models.CharField(verbose_name="Quality", max_length=150, default="HD")
    slug = models.SlugField()
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("anime_details_view", kwargs={"slug": self.slug})

    def get_first_photo(self):
        photo = self.animeimage_set.first()
        if photo:
            return photo.photo.url
        return "https://cs8.pikabu.ru/post_img/big/2016/09/10/4/1473482891145853538.jpg"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            num = 1
            while Anime.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Anime"
        verbose_name_plural = "Anime"


class Episodes(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="episodes")
    number = models.IntegerField(verbose_name="Episode number")
    title = models.CharField(max_length=255, verbose_name="Episode title")
    video_url = models.URLField()

    def __str__(self):
        return f'Episode {self.number}: {self.title}'



class AnimeImage(models.Model):
    photo = models.ImageField(verbose_name="Photo", upload_to="photos/", blank=True, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.anime.title}"



class User(AbstractUser):
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    liked_anime = models.ManyToManyField(Anime, blank=True, related_name="liked_anime")

    def __str__(self):
        return self.username


class Blog(models.Model):
    title = models.CharField(verbose_name="Blog title", max_length=150, unique=True)
    descr = models.TextField(verbose_name="Blog description")
    date = models.DateField(verbose_name="Date")
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_first_photo(self):
        photo = self.blogimg_set.first()
        if photo:
            return photo.photo.url
        return "https://cs8.pikabu.ru/post_img/big/2016/09/10/4/1473482891145853538.jpg"

class BlogImg(models.Model):
    photo = models.ImageField(verbose_name="Photo", upload_to="photos/", blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.blog.title}"


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Comment")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content


class AnimeComment(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Comment")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content
