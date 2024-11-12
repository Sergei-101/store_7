from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from products.models import Product



class StoreDetails(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название магазина")
    address = models.CharField(max_length=500, verbose_name="Адрес")
    bank_check = models.CharField(max_length=50, verbose_name="Расчётный счёт")
    bank = models.CharField(max_length=255, verbose_name="Банк")
    address_bank = models.CharField(max_length=255, verbose_name="Адрес Банка")
    big_bank = models.CharField(max_length=8, verbose_name="Код банка")
    ynp = models.CharField(max_length=9, verbose_name="УНП")
    phone = models.CharField(max_length=255, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    description = models.JSONField(blank=True, null=True, verbose_name="Дополнительно в Json")  
    is_nds = models.BooleanField(default=False, verbose_name='Работаем с НДС')  
    
    def __str__(self):
        return self.name
    
    class Meta:        
        verbose_name = 'Store'
        verbose_name_plural = 'Store'


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    PERSONAL = 'personal'
    BUSINESS = 'business'
    CUSTOMER_TYPE_CHOICES = [
        (PERSONAL, 'Физическое лицо'),
        (BUSINESS, 'Юридическое лицо'),
    ]


    # Для Юр. лиц
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название компании')
    unp = models.CharField(max_length=9, blank=True, null=True, verbose_name='УНП')
    checking_account = models.CharField(max_length=20, blank=True, null=True, verbose_name='Расчетный счет')
    bic = models.CharField(max_length=20, blank=True, null=True, verbose_name='Бик банка')
    bank_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Наименование банка')
    legal_address = models.CharField(max_length=256, blank=True, null=True, verbose_name='Юридический адрес')

    # Общие для всех
    contact_person = models.CharField(max_length=128, verbose_name='Контактное лицо')
    address = models.CharField(max_length=256, blank=True, null=True, default='Самовывоз', verbose_name='Адрес доставки')
    email = models.EmailField(max_length=256, verbose_name='E-Mail')
    phone_number = PhoneNumberField(verbose_name='Телефон')
    description = models.TextField(blank=True, null=True, verbose_name='Комментарии к заказу')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES, verbose_name='Статус заказа')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Инициатор')
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES, verbose_name='Тип заказчика')
    store_details = models.ForeignKey(StoreDetails, related_name='store_details', on_delete=models.CASCADE)


    class Meta:
        ordering = ['-created']
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордера'

    def __str__(self):
        return f'#{self.id}. {self.company_name if self.company_name else f"{self.contact_person}"}'

   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    product_data = models.JSONField(blank=True, null=True, verbose_name="Данные о товаре")  # Новое поле
    

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
    
    class Meta:        
        verbose_name = 'Детали ордера'
        verbose_name_plural = 'Детали ордеров'

