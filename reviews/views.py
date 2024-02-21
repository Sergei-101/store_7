from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from reviews.models import Review
from reviews.forms import ReviewForm

def product_reviews(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    return render(request, 'reviews/product_reviews.html', {'product': product, 'reviews': reviews})

def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('products:products')
    else:
        form = ReviewForm()
    return render(request, 'products/product_detail.html', {'products': product, 'form': form})
