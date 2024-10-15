from django.db import models


class StaticPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name="Полное описание")
    content_little = models.TextField(blank=True,null=True,verbose_name="Короткое описание")
    meta_keywords = models.CharField(max_length=200, verbose_name="Ключевые слова")
    meta_description = models.CharField(max_length=200, verbose_name="Описание для Seo")
    

    def __str__(self):
        return self.title