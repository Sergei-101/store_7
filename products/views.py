from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from products.models import Product, ProductCategory, ProductImage, Characteristic
from pages.models import Content
from cart.forms import CartAddProductForm
from reviews.forms import ReviewForm
from reviews.models import Review
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from products.forms import CSVUploadForm
import csv
from slugify import slugify




def products(request, category_slug=None, page=1):
    print(category_slug)
    categories = ProductCategory.objects.filter(parent=None)  # Получение корневых категорий
    products = Product.objects.filter(category__slug=category_slug) if category_slug else Product.objects.all()
    print(products)
    per_page = 25
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)
    images = ProductImage.objects.all()
    cart_product_form = CartAddProductForm()
    # Получаем ID активной категории из URL
    active_category_id = request.resolver_match.kwargs.get('category_id')
    context = {
        'products': products_paginator,
        'top_categories': categories,
        'images': images,
        'cart_product_form': cart_product_form,
        'active_category_id': active_category_id,
        'category_types': {category.id: 'parent' if category.children.exists() else 'child' for category in categories},
        }
    return render(request, 'products/products.html', context)

def product_list(request):
    products = Product.objects.all()

    # Получение всех доступных характеристик
    available_characteristics = Characteristic.objects.values('value').distinct()

    # Фильтрация по характеристикам
    characteristics = request.GET.getlist('characteristics')
    for characteristic in characteristics:
        products = products.filter(characteristics__value=characteristic)

    return render(request, 'products/product_list.html', {'products': products, 'available_characteristics': available_characteristics})

def product_detail(request, category_slug):
    categories = ProductCategory.objects.filter(parent=None)  # Получение корневых категорий
    products = Product.objects.filter(slug=category_slug)
    images = ProductImage.objects.filter(product__slug=category_slug)
    contents = Content.objects.all()
    cart_product_form = CartAddProductForm()
    review_form = ReviewForm()
    reviews = Review.objects.filter(product__slug=category_slug)
    context = {'products': products,
               'top_categories': categories,
               'images': images,
               'cart_product_form': cart_product_form,
               'review_form': review_form,
               'reviews': reviews,
               'contents': contents}
    return render(request, 'products/product_detail.html', context)


def quick_view(request, product_id):
    # Получаем объект товара по его идентификатору
    product = get_object_or_404(Product, id=product_id)

    # Формируем данные о товаре
    data = {
        'name': product.name,
        'oldprice': product.price_with_markup_and_vat(),
        'price': product.final_price(),
        'description': product.description,
        'image': product.image.url  # Путь к изображению
    }

    # Возвращаем JsonResponse с данными о товаре
    return JsonResponse(data)