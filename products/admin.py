import csv
from django.contrib import admin
from django.http import HttpResponse
from products.models import Product, ProductCategory, ProductImage, Promotion


admin.site.register(Promotion)

class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'is_active', 'category', 'id') # отоброжать поля
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ]
    actions = ['export_to_csv']

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
    list_display = ('name', 'slug', 'parent_prod_categories',)
    prepopulated_fields = {'slug': ('name',)}

