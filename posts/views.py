from django.shortcuts import render
from posts.models import Post, Category


def all_post(request):
    posts = Post.objects.all()
    category = Category.objects.all()
    context = {
        'posts': posts,
        'categories': category,
        'meta_keywords': 'Магазин электротоваров',
        'meta_description': 'Магазин электротоваров',
        'title': 'Магазин электротоваров',
    }
    return render(request, 'posts/blog.html', context)

def post_category(request, category_slug):
    posts = Post.objects.filter(slug=category_slug)
    context = {
        'posts': posts,
        'meta_keywords': 'Магазин электротоваров',
        'meta_description': 'Магазин электротоваров',
        'title': 'Магазин электротоваров',
    }
    return render(request, 'posts/blog.html', context)


def post_detail(request, post_title):
    post = Post.objects.get(slug=post_title)
    context = {
        'post': post,
        'meta_keywords': post.title,
        'meta_description': post.content,
        'title': post.title,
    }
    return render(request, 'posts/blog_single.html',context)


