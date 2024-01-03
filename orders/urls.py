from django.urls import path
from orders.views import order_view

app_name = 'orders'

urlpatterns = [
    path('order-view/', order_view, name='order_view'),
]