from django.shortcuts import render
from django.db.models import Avg
from products.models import Product
from posts.models import Post

def index(request):
    top_rated_products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:10]
    products = Product.objects.order_by('-id')[:15]
    posts =  Post.objects.all()
    context = {'products': products,
               'top_rated_products':top_rated_products,
               'posts':posts,
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



