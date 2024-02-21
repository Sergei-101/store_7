from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from products.models import Product, ProductCategory, ProductImage
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



def products(request, category_id=None, page=1):
    categories = ProductCategory.objects.filter(parent=None)  # Получение корневых категорий
    products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    per_page = 10
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)
    images = ProductImage.objects.all()
    cart_product_form = CartAddProductForm()
    context = {'products': products_paginator,
               'top_categories': categories,
               'images': images,
               'cart_product_form': cart_product_form}
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    categories = ProductCategory.objects.filter(parent=None)  # Получение корневых категорий
    products = Product.objects.filter(id=product_id)
    images = ProductImage.objects.filter(product=product_id)
    contents = Content.objects.all()
    cart_product_form = CartAddProductForm()
    review_form = ReviewForm()
    reviews = Review.objects.filter(product=product_id)
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
        'price': product.final_price(),
        'description': product.description,
        # 'image_url': product.image.url  # Путь к изображению
    }

    # Возвращаем JsonResponse с данными о товаре
    return JsonResponse(data)