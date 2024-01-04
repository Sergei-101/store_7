from django.http import HttpResponseRedirect
from django.shortcuts import render

from baskets.models import Basket
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


def product_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1
        baskets.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def product_remove(request, basket_id): # удаление товаров из корзины
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))