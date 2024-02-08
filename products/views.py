from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from products.models import Product, ProductCategory, ProductImage
from cart.forms import CartAddProductForm
from reviews.forms import ReviewForm
from reviews.models import Review
from django.core.paginator import Paginator
from products.forms import CSVUploadForm
import csv
from slugify import slugify



def products(request, category_id=None, page=1):
    catrgory = ProductCategory.objects.all()
    products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    per_page = 10
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)
    images = ProductImage.objects.all()
    cart_product_form = CartAddProductForm()
    context = {'products': products_paginator,
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

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Чтение CSV файла и сохранение данных в базу данных
            handle_uploaded_file(csv_file)

            return redirect('index')
    else:
        form = CSVUploadForm()

    return render(request, 'products/upload_csv.html', {'form': form})

def handle_uploaded_file(file):
    # Чтение CSV файла и сохранение данных в базу данных
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file, delimiter=';') #Установка разделителя ";"
    for row in reader:
        category_name = row[3]
        category_name_slug = category_name
        category, created = ProductCategory.objects.get_or_create(name=category_name, slug=category_name_slug)
        name = row[0]
        price = row[1]
        description = row[2]
        slug = slugify(name)
        quantity = row[4]

        product, created = Product.objects.get_or_create(
            name=name,
            price=price,
            description=description,
            category=category,
            slug=slug,
            quantity=quantity
        )
        images_paths = row[5].split(',') if row[5] else []
        for image_path in images_paths:
            if image_path:
                product_image = ProductImage(product=product, image=image_path.strip())  # Убираем пробелы
                product_image.save()