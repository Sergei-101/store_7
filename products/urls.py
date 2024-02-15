from django.urls import path
from products.views import products, product_detail, quick_view

app_name = 'products'

urlpatterns = [
    path('all_products/', products, name='products'),
    path('category/<int:category_id>', products, name='category'),
    path('page/<int:page>', products, name='paginator'),
    path('products_detail/<int:product_id>', product_detail, name='product_detail'),
    path('products/<int:product_id>/quick_view/', quick_view, name='quick_view'),



]
