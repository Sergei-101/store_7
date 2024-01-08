from django.urls import path
from products.views import products, product_detail

app_name = 'products'

urlpatterns = [
    path('', products, name='products'),
    path('category/<int:category_id>', products, name='category'),
    path('products_detail/<int:product_id>', product_detail, name='product_detail'),    
]
