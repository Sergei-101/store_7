# models.py
from django.db import models
from products.models import Supplier, Product
from django.utils import timezone

class ParserStore(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products', verbose_name="Поставщик")
    headers = models.CharField(max_length=255, blank=True, null=True, verbose_name="Заголовки")
    page_pars = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тег страницы")    
    price_pars = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тег цены")
    unit_pars = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тег единицы измерения")

    def __str__(self):
        return str(self.supplier)

    class Meta:
        verbose_name = 'Парсер товаров'
        verbose_name_plural = 'Парсеры'




class PriceCheck(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_checks')
    current_price = models.FloatField(null=True, blank=True, verbose_name="Цена на сайте")
    new_price = models.FloatField(null=True, blank=True, verbose_name="Цена поставщика")
    unit = models.CharField(max_length=50, default="N/A", verbose_name="ед. изм.")
    check_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Проверка цены для {self.product.name} от {self.check_date}"