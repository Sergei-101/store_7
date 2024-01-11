from django.contrib import admin
from products.models import Product, ProductCategory, ProductImage


class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'id') # отоброжать поля
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ]



@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent_prod_categories',)
    prepopulated_fields = {'slug': ('name',)}