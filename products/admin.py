import csv
from django.contrib import admin
from django.http import HttpResponse
from products.models import Product, ProductCategory, ProductImage, Promotion, CSVFile, Supplier, Unit
from slugify import slugify
from products.forms import ProductForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django.forms import SelectMultiple

admin.site.register(Supplier)
admin.site.register(Promotion)
admin.site.register(Unit)

class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'quantity', 'category', 'id') # отоброжать поля
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ]
    actions = ['export_to_csv']
    form = ProductForm

    def export_to_csv(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'base_price', 'Description'])  # Заголовки столбцов

        for product in queryset:
            writer.writerow([product.name, product.slug, product.base_price, product.is_active, product.description, product.category])

        return response

    export_to_csv.short_description = "Выгрузить CSV"

    



@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent',)
    prepopulated_fields = {'slug': ('name',)}


class CSVFileAdmin(admin.ModelAdmin):
    actions = ['handle_uploaded_csv']

    def handle_uploaded_csv(self, request, queryset):
        for csv_file in queryset:
            decoded_file = csv_file.file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=';')
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
                        product_image = ProductImage(product=product, image=image_path.strip())
                        product_image.save()

            # Пометить файл как обработанный
            csv_file.processed = True
            csv_file.save()

        self.message_user(request, f"{queryset.count()} CSV файлов успешно обработаны.")
    handle_uploaded_csv.short_description = "Обработать выбранные CSV файлы"


admin.site.register(CSVFile, CSVFileAdmin)