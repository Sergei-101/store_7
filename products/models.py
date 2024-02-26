from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from datetime import date
import random
import string


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя категории")
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Родительская категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Supplier(models.Model):
    supplier = models.CharField(max_length=255, blank=True, null=True, verbose_name="Поставщик") # Поставщик товара        

    def __str__(self):
        return self.supplier
    
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    categories = models.ManyToManyField(ProductCategory, blank=True)
    supplier = models.ManyToManyField(Supplier, blank=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def is_active(self):
        today = date.today()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'      
      


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(verbose_name="Описание")
    quantity = models.IntegerField(default=0, verbose_name="Кол-во") # Активный товар    
    base_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Базовая цена") # Базовая цена товара без наценок и ндс
    markup_percentage = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Процент к товару") # Процент наценки на цену без ндс
    vat_price = models.DecimalField(max_digits=6, decimal_places=2, default=20, verbose_name="НДС") # НДС на цену
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Поставщик") # Поставщик товара    
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Акция")
    characteristics = models.ManyToManyField(Characteristic, through='ProductCharacteristic', verbose_name="Характеристика")
    article = models.CharField(max_length=100, blank=True, verbose_name="Артикул")  # Поле для артикула товара
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
    
    def generate_sku(self):
        chars = string.ascii_letters + string.digits
        sku = ''.join(random.choice(chars) for _ in range(7))  # Генерируем случайную комбинацию из 7 символов
        return sku

    def save(self, *args, **kwargs):
        if not self.pk:  # Если объект еще не сохранен в базе данных
            if not self.article:  # Если артикул не указан, генерируем его
                unique_sku_generated = False
                while not unique_sku_generated:  # Генерируем уникальный артикул
                    sku = self.generate_sku()
                    if not Product.objects.filter(article=sku).exists():  # Проверяем уникальность артикула в базе данных
                        unique_sku_generated = True
                self.article = sku  # Присваиваем сгенерированный артикул
        super().save(*args, **kwargs)
    
    def price_with_markup_and_vat(self):
        price_with_markup = self.base_price * (1 + self.markup_percentage / 100)
        price_with_vat = price_with_markup * (1 + self.vat_price / 100)
        return round(price_with_vat, 2)

    def apply_discount_to_category(self, category, discount_percentage):
        products_in_category = Product.objects.filter(category=category)
        products_in_category.update(promotion=Promotion.objects.create(discount_percentage=discount_percentage))

    def apply_discount_to_supplier(self, supplier, discount_percentage):
        products_from_supplier = Product.objects.filter(supplier=supplier)
        products_from_supplier.update(promotion=Promotion.objects.create(discount_percentage=discount_percentage))
    
    def is_promotion_active(self):
        if self.promotion:
            today = date.today()
            return self.promotion.start_date <= today <= self.promotion.end_date
        return False
    
    def final_price(self):
        if self.promotion and self.promotion.is_active():
            price = self.price_with_markup_and_vat()  # вызываем метод для получения конечной цены
            discounted_price = price - (price * self.promotion.discount_percentage / 100)
            return round(discounted_price, 2)
        else:
            return self.price_with_markup_and_vat()

@receiver(m2m_changed, sender=Promotion.categories.through)
def apply_discount_to_category_on_promotion_save(sender, instance, action, **kwargs):
    if action == 'post_add':
        products = Product.objects.filter(category__in=instance.categories.all())
        products.update(promotion=instance)


@receiver(m2m_changed, sender=Promotion.supplier.through)
def apply_discount_to_supplier_on_promotion_save(sender, instance, action, **kwargs):
    if action == 'post_add':
        products = Product.objects.filter(supplier__in=instance.supplier.all())
        products.update(promotion=instance)


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product} - {self.characteristic}: {self.value}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(330, 300)],
                               format='JPEG',
                               options={'quality': 60})

    def __str__(self):
        return f"Image for {self.product.name}"
    

class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    
    class Meta:
        verbose_name = 'Загрузка CSV '
        verbose_name_plural = 'Загрузки CSV'
