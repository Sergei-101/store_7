from django.urls import path
from orders.views import order_create, admin_order_detail, check_prices

app_name = 'orders'
urlpatterns = [
 path('create/', order_create, name='order_create'),
 path('complete/', order_create, name='order_complete'),
 path('admin/order/<int:order_id>/', admin_order_detail,  name='admin_order_detail'), 
 path('admin/order/<int:order_id>/check-prices/', check_prices, name='check_prices'),
]