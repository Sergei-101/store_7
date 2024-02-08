from django.shortcuts import render
from django.db.models import Avg
from products.models import Product
from posts.models import Post

def index(request):
    top_rated_products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:10]
    products = Product.objects.order_by('-id')[:15]
    posts =  Post.objects.all()
    context = {'products': products, 'top_rated_products':top_rated_products, 'posts':posts}
    return render(request, 'pages/index.html', context)

def contact(request):
    return render(request, 'pages/contact.html')


def product_line(requsest):
    products = Product.objects.order_by('-id')[:15]
    posts = Post.objects.all()
    context = {
        'products': products,
        'posts':posts
    }
    return render (request, 'pages/index.html', context)



