from django.urls import path
from products.views import products, product_detail, product_add, product_remove

app_name = 'products'

urlpatterns = [
    path('', products, name='products'),
    path('category/<int:category_id>', products, name='category'),
    path('products_detail/<int:product_id>', product_detail, name='product_detail'),
    path('add/<int:product_id>', product_add, name='product_add'),
    path('remove/<int:basket_id>', product_remove, name='product_remove'),
]
