from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal

class OrderQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(order.sum() for order in self)

    def total_quantity(self):
        return sum(order.quantity for order in self)


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = OrderQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.email} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity








class Customer_order(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='order')
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=250, blank=False)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=False)
    order_details = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)