import csv
from decimal import Decimal
from django.contrib import admin
from django.http import HttpResponse
from products.models import Product, ProductCategory, ProductImage, Promotion, CSVFile, Supplier, Unit, Characteristic, CharacteristicCategory
from slugify import slugify
from products.forms import ProductForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django.forms import DecimalField, SelectMultiple
from icrawler.builtin import GoogleImageCrawler
import os
from django.conf import settings
import shutil
# pip install openai
# Установите ваш API ключ
# openai.api_key = settings.OPENAI_API_KEY


admin.site.register(Supplier)
admin.site.register(Promotion)
admin.site.register(Unit)
admin.site.register(CharacteristicCategory)

class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 1


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'quantity', 'category', 'id', 'available')
    search_fields = ['name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CharacteristicInline, ProductImageInline]
    actions = ['export_to_csv', 'download_images_for_products', 'generate_description_for_products']
    form = ProductForm

    # Действие для экспорта в CSV
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'base_price', 'Description'])

        for product in queryset:
            writer.writerow([product.name, product.slug, product.base_price, product.is_active, product.description, product.category])

        return response
    export_to_csv.short_description = "Выгрузить CSV"

    # # Функция для генерации описания с использованием OpenAI
    # def generate_description_ai(self, product_name):
    #     prompt = f"Напишите привлекательное описание для товара: {product_name}."
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": prompt}],
    #         max_tokens=100  # Максимальное количество токенов в ответе
    #     )
    #     return response['choices'][0]['message']['content']

    # # Действие для генерации описания для выбранных товаров
    # def generate_description_for_products(self, request, queryset):
    #     for product in queryset:
    #         if not product.description:  # Если описание не установлено
    #             product.description = self.generate_description_ai(product.name)
    #             product.save()  # Сохраняем изменения

    #     self.message_user(request, f"Описание для {queryset.count()} товаров успешно сгенерировано.")
    
    # generate_description_for_products.short_description = "Сгенерировать описание для выбранных товаров"

    # Действие для загрузки изображений
    def download_images_for_products(self, request, queryset):
        save_dir = os.path.join(settings.MEDIA_ROOT, 'products/')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Обрабатываем каждый продукт
        for product in queryset:
            if not product.image:  # Если картинка не установлена вручную
                # Временная папка для скачивания изображений
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_images')
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                # Скачиваем изображение по названию товара
                google_crawler = GoogleImageCrawler(storage={'root_dir': temp_dir})
                google_crawler.crawl(keyword=product.name, max_num=1)

                # Переименовываем и перемещаем изображение в папку продуктов
                for index, filename in enumerate(os.listdir(temp_dir)):
                    if filename.endswith(('.jpg', '.png', '.jpeg')):
                        new_filename = f"{product.name.replace(' ', '_')}_{index + 1}.jpg"
                        src_path = os.path.join(temp_dir, filename)
                        dst_path = os.path.join(save_dir, new_filename)
                        shutil.move(src_path, dst_path)

                        # Сохраняем путь к изображению в поле image
                        product.image = f'products/{new_filename}'
                        product.save()  # Сохраняем изменения в продукте
                        break

                # Удаляем временную папку
                shutil.rmtree(temp_dir)

        self.message_user(request, f"Изображения для {queryset.count()} товаров были успешно загружены.")
    
    download_images_for_products.short_description = "Загрузить изображения для выбранных товаров"

    



@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}



class CSVFileAdmin(admin.ModelAdmin):
    actions = ['handle_uploaded_csv']

    def handle_uploaded_csv(self, request, queryset):
        for csv_file in queryset:
            decoded_file = csv_file.file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=';')

            # Пропускаем первую строку (заголовки)
            next(reader)

            for row in reader:
                categories = row[4].split(',')
                parent_category = None
                
                # Создание иерархии категорий
                for category_name in categories:
                    category_name = category_name.strip()
                    parent_category, created = ProductCategory.objects.get_or_create(
                        name=category_name,
                        slug=slugify(category_name),
                        parent=parent_category
                    )
                

                
                name = row[0]
                # base_price = row[1].replace(',', '.').strip()  # Заменяем запятую на точку
                base_price = 10
                description = row[2]
                description_2 = row[3]
                slug = slugify(name)
                product_link = row[5]
                image = row[6]
                quantity = 10
                print(f'{name} ----- price {base_price}-----тип {type(base_price)}')
                # Проверка уникальности slug
                original_slug = slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f'{original_slug}-{counter}'
                    counter += 1

                # Создание или обновление продукта
                product, created = Product.objects.get_or_create(
                    name=name,
                    base_price=base_price,
                    description=description,
                    description_2=description_2,
                    category=parent_category,
                    slug=slug,
                    quantity=quantity,
                    image=image,
                    product_link=product_link
                )

            # Пометка файла как обработанного
            csv_file.processed = True
            csv_file.save()

        self.message_user(request, f"{queryset.count()} CSV файлов успешно обработаны.")
    handle_uploaded_csv.short_description = "Обработать выбранные CSV файлы"



admin.site.register(CSVFile, CSVFileAdmin)