from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from datetime import date

class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent_prod_categories = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Supplier(models.Model):
    supplier = models.CharField(max_length=255, blank=True, null=True) # Поставщик товара        

class Promotion(models.Model):
    name = models.CharField(max_length=100)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    categories = models.ManyToManyField(ProductCategory)
    supplier = models.ManyToManyField(Supplier)

    def is_active(self):
        from datetime import date
        today = date.today()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return self.name

class Characteristic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name      
      


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()    
    base_price = models.DecimalField(max_digits=6, decimal_places=2) # Базовая цена товара без наценок и ндс
    markup_percentage = models.DecimalField(max_digits=6, decimal_places=2, default=0) # Процент наценки на цену без ндс
    vat_price = models.DecimalField(max_digits=6, decimal_places=2, default=20) # НДС на цену
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True) # Поставщик товара
    is_active = models.BooleanField(default=True) # Активный товар
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, blank=True, null=True)
    characteristics = models.ManyToManyField(Characteristic, through='ProductCharacteristic')
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
    
    def price_with_markup_and_vat(self):
        price_with_markup = self.base_price * (1 + self.markup_percentage / 100)
        price_with_vat = price_with_markup * (1 + self.vat_price / 100)
        return round(price_with_vat, 2)

    def apply_discount_to_category(self, category, discount_percentage):
        products_in_category = Product.objects.filter(category=category)
        products_in_category.update(promotion=Promotion.objects.create(discount_percentage=discount_percentage))
    
    def is_promotion_active(self):
        if self.promotion:
            today = date.today()
            return self.promotion.start_date <= today <= self.promotion.end_date
        return False

@receiver(m2m_changed, sender=Promotion.categories.through)
def apply_discount_to_category_on_promotion_save(sender, instance, action, **kwargs):
    if action == 'post_add':
        products = Product.objects.filter(category__in=instance.categories.all())
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