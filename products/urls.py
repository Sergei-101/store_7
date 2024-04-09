from django.urls import path
from products.views import products, product_detail, quick_view

app_name = 'products'

urlpatterns = [
    path('all/', products, name='products'),
    path('<slug:category_slug>/', products, name='category'),
    path('page/<int:page>', products, name='paginator'),
    path('detail/<slug:category_slug>/', product_detail, name='product_detail'),
    path('products/<int:product_id>/quick_view/', quick_view, name='quick_view'),



]
