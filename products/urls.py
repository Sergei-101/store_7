from django.urls import path
from products.views import products, product_detail, quick_view, product_search

app_name = 'products'

urlpatterns = [
    path('', product_search, name='product_search'),
    path('all/', products, name='products'),
    path('<slug:category_slug>/', products, name='category'),
    path('<slug:category_slug>/page/<int:page>/', products, name='paginator'),
    path('page/<int:page>/', products, name='all_products_paginator'),  # для всех продуктов
    path('detail/<str:category_slug>/', product_detail, name='product_detail'),
    path('products/<int:product_id>/quick_view/', quick_view, name='quick_view'),



]
