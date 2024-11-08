from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from products.models import Product, ProductCategory, ProductImage
from cart.forms import CartAddProductForm
from pages.models import StaticPage, Tab
from reviews.forms import ReviewForm
from reviews.models import Review
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from products.forms import CSVUploadForm
import csv
from slugify import slugify
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)  # Кеширование на 15 минут
def products(request, category_slug=None, page=1):
    categories = ProductCategory.objects.filter(parent=None).order_by('name')
    
    selected_category = None
    ancestors = []
    
    if category_slug:
        selected_category = get_object_or_404(ProductCategory, slug=category_slug)
        ancestors = selected_category.get_ancestors()
    
    # Предварительная загрузка изображений, связанных с продуктами
    products = Product.objects.filter(
        category__slug=category_slug, available=True
    ).prefetch_related('images') if category_slug else Product.objects.filter(
        available=True
    ).prefetch_related('images')
    
    # Пагинация
    per_page = 16
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)
    
    cart_product_form = CartAddProductForm()
    
    context = {
        'products': products_paginator,
        'top_categories': categories,
        'cart_product_form': cart_product_form,
        'meta_keywords': 'купить электротовары по хорошим ценам',
        'meta_description': 'Интернет магазин электротоваров',
        'title': 'Каталог товаров',
        'current_slug': category_slug,
        'ancestor_ids': [ancestor.id for ancestor in ancestors],
        'selected_category': selected_category,
    }
    
    return render(request, 'products/products.html', context)



def product_detail(request, category_slug):
    categories = ProductCategory.objects.filter(parent=None)  # Получение корневых категорий
    product = get_object_or_404(Product, slug=category_slug)
    images = ProductImage.objects.filter(product__slug=category_slug)    
    cart_product_form = CartAddProductForm()
    review_form = ReviewForm()
    reviews = Review.objects.filter(product__slug=category_slug)
    content_smal = Tab.objects.all()
    
    context = {'product': product,
               'top_categories': categories,
               'images': images,
               'cart_product_form': cart_product_form,
               'review_form': review_form,
               'reviews': reviews,               
               'meta_keywords': product.meta_keywords,
               'meta_description': product.meta_description,
               'title': product.name,
               'content_smal':content_smal,
            
               }
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
        'article': product.article,
        'category': product.category.name,
        'image': product.image.url  # Путь к изображению
    }
    # Возвращаем JsonResponse с данными о товаре
    return JsonResponse(data)

def product_search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = None
    context = {
        'products': products,
        'meta_keywords': 'купить электротовары по хорошим ценам',
        'meta_description': 'Интернет магазин электротоваров',
        'title': 'Поиск товаров',

    }
    return render(request, 'products/search_results.html', context)