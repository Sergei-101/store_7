from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from products.models import Product, ProductCategory
from posts.models import Post
from pages.models import StaticPage


def static_page(request, slug):
    page = get_object_or_404(StaticPage, slug=slug)  # Получение страницы по slug
    return render(request, 'pages/static_page.html', {'page': page})  # Рендеринг шаблона с переданными данными

def index(request):
    top_rated_products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('?')[:10]
    promotional_items = Product.objects.filter(promotion__isnull=False)[:10]
    products = Product.objects.order_by('?')[:15]
    posts =  Post.objects.all()
    categories = ProductCategory.objects.filter(parent=None)  # Получение корневых категорий    
    context = {'products': products,
               'promotional_items': promotional_items,
               'top_rated_products':top_rated_products,
               'posts':posts,               
               'categories': categories,
               'meta_keywords': 'Интернет магазин электротоваров',
               'meta_description': 'Интернет магазин электротоваров',
               'title': 'Интернет магазин электротоваров',
    }
    return render(request, 'pages/index.html', context)

def contact(request):
    context = {
        'meta_keywords': 'Интернет магазин электротоваров',
        'meta_description': 'Интернет магазин электротоваров',
        'title': 'Интернет магазин электротоваров',
    }
    return render(request, 'pages/contact.html', context)


def custom_404(request, exception):
    return render(request, 'errors/404.html', {}, status=404)


