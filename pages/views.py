from django.shortcuts import render
from django.db.models import Avg
from products.models import Product, ProductCategory
from posts.models import Post
from pages.models import Content

def index(request):
    top_rated_products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('?')[:10]
    promotional_items = Product.objects.filter(promotion__isnull=False)[:10]
    products = Product.objects.order_by('?')[:15]
    posts =  Post.objects.all()
    sliders = Content.objects.filter(section__slug='slider')
    categories = ProductCategory.objects.filter(parent=None)  # Получение корневых категорий
    servis_promotion = Content.objects.filter(section__slug='servis-promotion')
    context = {'products': products,
               'promotional_items': promotional_items,
               'top_rated_products':top_rated_products,
               'posts':posts,
               'sliders': sliders,
               'servis_promotion': servis_promotion,
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


