from django.http import HttpResponseRedirect
from django.shortcuts import render
from products.models import Product, ProductCategory, ProductImage
from cart.forms import CartAddProductForm
from reviews.forms import ReviewForm
from reviews.models import Review


def products(request, category_id=None):
    catrgory = ProductCategory.objects.all()
    products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    images = ProductImage.objects.all()
    cart_product_form = CartAddProductForm()
    context = {'products': products,
               'catrgories': catrgory,
               'images': images,
               'cart_product_form': cart_product_form}
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    products = Product.objects.filter(id=product_id)
    images = ProductImage.objects.filter(product=product_id)
    cart_product_form = CartAddProductForm()
    review_form = ReviewForm()
    reviews = Review.objects.filter(product=product_id)
    context = {'products': products,
               'images': images,
               'cart_product_form': cart_product_form,
               'review_form': review_form,
               'reviews': reviews}
    return render(request, 'products/product_detail.html', context)


