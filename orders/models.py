from django.contrib.auth.models import User
from django.db import models

from products.models import Product


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

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'#{self.id}. {self.first_name} {self.last_name}'

    class Meta:
        ordering = ['-created']

class OrderItem(models.Model):
     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
     product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     quantity = models.PositiveIntegerField(default=1)

     def __str__(self):
        return str(self.id)

     def get_cost(self):
        return self.price * self.quantity
