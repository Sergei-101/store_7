from django.contrib import admin
from orders.models import Order, Customer_order

admin.site.register(Order)
admin.site.register(Customer_order)

