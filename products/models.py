from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from datetime import date, datetime
import random
import string
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Родительская категория")
    image = models.ImageField(upload_to='other_images', blank=True, null=True, verbose_name="Изображение")
    text_icon = models.CharField(max_length=255, blank=True, null=True, verbose_name="Иконка")
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'category_slug':self.slug})
    
    def has_children(self):
        return self.children.exists()  # Возвращает True, если есть дочерние категории
    
    def get_sorted_children(self):
        return self.children.all().order_by('name')  # сортировка по имени
    
    def get_ancestors(self):
        """
        Возвращает список всех родительских категорий, включая самого себя.
        """
        ancestors = []
        category = self
        while category.parent is not None:
            ancestors.append(category.parent)
            category = category.parent
        return ancestors


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Supplier(models.Model):
    supplier = models.CharField(max_length=255, blank=True, null=True, verbose_name="Поставщик") # Поставщик товара
    link_supplier = models.CharField(max_length=500,blank=True,null=True, verbose_name="Ссылка на поставщика")

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

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Производители'
        verbose_name_plural = 'Производитель'

      
class Unit(models.Model): # Еденица измерения
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Еденица измерения'
        verbose_name_plural = 'Еденицы измерения'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='product_images', blank=True, null=True, verbose_name="Изображение")
    description = models.TextField(blank=True,null=True,verbose_name="Описание")
    description_2 = models.TextField(blank=True,null=True,verbose_name="Характеристики")
    quantity = models.IntegerField(default=0, verbose_name="Кол-во") # Активный товар
    unit =  models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit', blank=True,null=True, verbose_name="ед. изм.")         
    base_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Базовая цена") # Базовая цена товара без наценок и ндс
    markup_percentage = models.DecimalField(max_digits=6, decimal_places=2, default=25, verbose_name="Процент к товару") # Процент наценки на цену без ндс
    vat_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="НДС") # НДС на цену
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Поставщик") # Поставщик товара
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Производитель")
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Акция")
    article = models.CharField(max_length=100, blank=True, verbose_name="Артикул")  # Поле для артикула товара
    available = models.BooleanField(default=True, verbose_name='Видимость')
    meta_keywords = models.CharField(max_length=255,blank=True,null=True,verbose_name="Ключевые слова (для Seo)")
    meta_description = models.TextField(blank=True,null=True,verbose_name="Описание (для Seo)")
    updated_at = models.DateTimeField(auto_now=True)
    product_link = models.CharField(max_length=500, blank=True, null=True, verbose_name="Ссылка на продукт")


    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'category_slug':self.slug})


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
        if not self.meta_keywords:
            self.meta_keywords = f"купить, {self.name}"
        if not self.meta_description:
            self.meta_description = self.description
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

    def get_sales_count(self, month=None, year=None):
        # Если month и year не переданы, используем текущий месяц и год
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year

        # Подсчёт количества продаж товара за указанный месяц
        return sum(
            item.quantity for item in self.order_items.filter(order__created__month=month, order__created__year=year))

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


# Модель характеристики товара
class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Связующая модель для значений характеристик товара
class ProductFeatureValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.feature.name}: {self.value}"

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
