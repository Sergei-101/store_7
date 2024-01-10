from django.shortcuts import render
from posts.models import Post, Category


def all_post(request):
    posts = Post.objects.all()
    category = Category.objects.all()
    context = {'posts': posts, 'categories': category}
    return render(request, 'posts/blog.html', context)

def post_category(request, category_id):
    posts = Post.objects.filter(category=category_id)
    context = {'posts': posts}
    return render(request, 'posts/blog.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'posts/blog_single.html',context)


