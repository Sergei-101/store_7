from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField()
    description = models.TextField(blank=True,null=True,verbose_name="Контент")

    class Meta:
        verbose_name = 'Секции'
        verbose_name_plural = 'Секция'

    def __str__(self):
        return self.name

class Content(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Сецкия")
    name = models.CharField(max_length=255, verbose_name="Название")
    text_1 = models.CharField(max_length=255,blank=True,null=True, verbose_name="Текст")
    text_2 = models.CharField(max_length=255,blank=True,null=True, verbose_name="Текст_2")
    text_3 = models.CharField(max_length=255,blank=True,null=True, verbose_name="Текст_3")
    text_icon = models.CharField(max_length=255,blank=True,null=True, verbose_name="Иконка")
    image = models.ImageField(upload_to='other_images', blank=True, null=True, verbose_name="Изображение")
    description = models.TextField(blank=True,null=True,verbose_name="Контент")

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'

    def __str__(self):
        return self.name