from django.shortcuts import render
from products.models import Product, ProductCategory, ProductImage

def index(request):
    return render(request, 'products/index.html')

def products(request, category_id=None): #отоброжение категорийБ выбор товаров по категориям
    catrgory = ProductCategory.objects.all()
    products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    images = ProductImage.objects.all()
    context = {'products': products,
               'catrgories': catrgory,
               'images': images}
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    products = Product.objects.filter(id=product_id)
    images = ProductImage.objects.filter(product=product_id)
    context = {'products': products,
               'images': images}
    return render(request, 'products/product_detail.html', context)