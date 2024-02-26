from django.db import models


class Content(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Контент")

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'

    def __str__(self):
        return self.name