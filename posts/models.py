from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField()
    image = models.ImageField(upload_to='post_images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ключевые слова (для Seo)")
    meta_description = models.TextField(blank=True, null=True, verbose_name="Описание (для Seo)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.meta_keywords:
            self.meta_keywords = self.title
        if not self.meta_description:
            self.meta_description = self.title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'




