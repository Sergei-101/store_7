from django.urls import path
from products.views import products, product_detail, upload_csv

app_name = 'products'

urlpatterns = [
    path('all_products/', products, name='products'),
    path('category/<int:category_id>', products, name='category'),
    path('page/<int:page>', products, name='paginator'),
    path('products_detail/<int:product_id>', product_detail, name='product_detail'),
    path('upload_csv/', upload_csv, name='upload_csv'),
]
