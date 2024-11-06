# models.py
from django.db import models
from products.models import Supplier, Product

class ParserStore(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products', verbose_name="Поставщик")
    headers = models.CharField(max_length=255, blank=True, null=True, verbose_name="Заголовки")
    page_pars = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тег страницы")
    name_pars = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тег названия товара")
    price_pars = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тег цены")
    unit_pars = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тег единицы измерения")

    def __str__(self):
        return str(self.supplier)

    class Meta:
        verbose_name = 'Парсер товаров'
        verbose_name_plural = 'Парсеры'

