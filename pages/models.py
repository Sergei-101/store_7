from django.db import models


class StaticPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name="Полное описание")
    in_menu = models.BooleanField(default=True, help_text="Отображать в меню")    
    meta_keywords = models.CharField(max_length=200, verbose_name="Ключевые слова")
    meta_description = models.CharField(max_length=200, verbose_name="Описание для Seo")
    

    def __str__(self):
        return self.title
    
class Guarantee(models.Model):
    title = models.CharField(max_length=100, default='Быстрая и бесплатная доствака')
    content = models.CharField(max_length=100, default='Бесплатная доставка от 100 рублей')
    icon = models.CharField(max_length=100, default='#icon_shipping')

    def __str__(self):
        return self.title
    

class SliderItem(models.Model):
    image = models.ImageField(upload_to='slider/')
    text_1 = models.CharField(max_length=255, blank=True, null=True)
    text_2 = models.CharField(max_length=255, blank=True, null=True)
    text_3 = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField( blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text_1
    
class Tab(models.Model):
    POSITION = [
        ('how_to_buy', 'Как купить'),
        ('pay', 'Оплата'),
        ('delivery', 'Доставка'),
    ]

    title = models.CharField(max_length=10, choices=POSITION, default='client', verbose_name="Роль")
    description = models.TextField(verbose_name="Тест для заполнения")

    def __str__(self):
        return self.title

