import csv
from decimal import Decimal
from django.contrib import admin
from django.http import HttpResponse
from products.models import Manufacturer, Product, ProductCategory, ProductImage, Promotion, CSVFile, Supplier, Unit, Feature, ProductFeatureValue
from slugify import slugify
from products.forms import ProductForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models, IntegrityError
from django.forms import DecimalField, SelectMultiple
from icrawler.builtin import GoogleImageCrawler
from fuzzywuzzy import process  # Импортируем fuzzywuzzy для сравнения строк
import os
from django.conf import settings
import shutil
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
import re
from django.utils.safestring import mark_safe

# pip install openai
# Установите ваш API ключ
# openai.api_key = settings.OPENAI_API_KEY


admin.site.register(Supplier)
admin.site.register(Promotion)
admin.site.register(Unit)
admin.site.register(Feature)
admin.site.register(ProductFeatureValue)

class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 1

class ProductFeatureValueInline(admin.TabularInline):
    model = ProductFeatureValue
    extra = 1  # Количество пустых форм для добавления новых значений

@admin.action(description="Обновить наценку для товаров по данным поставщика")
def update_markup_percentage_from_supplier(modeladmin, request, queryset):
    for product in queryset:
        if product.supplier and product.supplier.markup_percentage is not None:
            product.markup_percentage = product.supplier.markup_percentage
            product.save()



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('get_image','name', 'base_price', 'quantity', 'category', 'id', 'available', 'image_down_auto',)
    list_filter = ('supplier',)
    search_fields = ['name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductFeatureValueInline]
    actions = ['export_to_csv', 'download_images_for_products', 'generate_description_for_products', 'parse_features',update_markup_percentage_from_supplier,]
    form = ProductForm

    def get_image(self, obj):        
        if obj.image and obj.image.url:  # Проверяем, есть ли файл у поля image
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="110">')
        return "Изображение отсутствует"

    get_image.short_description = "Изображение"

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

  

    # Действие для загрузки изображений
    def download_images_for_products(self, request, queryset):
        save_dir = os.path.join(settings.MEDIA_ROOT, 'products/')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Обрабатываем каждый продукт
        for product in queryset:
            # if not product.image:  # Только если изображение не установлено вручную
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_images')
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                # Очищаем название продукта, убирая недопустимые символы для имени файла
                sanitized_name = re.sub(r'[<>:"/\\|?*]', '', product.name)
                
                # Скачиваем изображение по названию товара
                google_crawler = GoogleImageCrawler(storage={'root_dir': temp_dir})
                google_crawler.crawl(keyword=product.name, max_num=1)

                # Переименовываем и перемещаем изображение в папку продуктов
                for index, filename in enumerate(os.listdir(temp_dir)):
                    if filename.endswith(('.jpg', '.png', '.jpeg')):
                        new_filename = f"{sanitized_name.replace(' ', '_')}_{index + 1}.jpg"
                        src_path = os.path.join(temp_dir, filename)
                        dst_path = os.path.join(save_dir, new_filename)
                        shutil.move(src_path, dst_path)

                        # Сохраняем путь к изображению в поле image
                        product.image = f'products/{new_filename}'
                        product.image_down_auto = True
                        product.save()  # Сохраняем изменения в продукте
                        break

                # Удаляем временную папку
                shutil.rmtree(temp_dir)

        self.message_user(request, f"Изображения для {queryset.count()} товаров были успешно загружены.")
    
    download_images_for_products.short_description = "Загрузить изображения для выбранных товаров"

    def parse_features(self, request, queryset):
        for product in queryset:
            if product.description_2:
                features_data = self.parse_table(product.description_2)
                self.message_user(request, f"Парсенные данные: {features_data}")  # Отладочное сообщение

                for feature_name, feature_value in features_data.items():
                    # Поиск существующих характеристик
                    existing_features = Feature.objects.values_list('name', flat=True)
                    match_result = process.extractOne(feature_name, existing_features)

                    if match_result:
                        match, score = match_result
                        if score >= 80:  # Если название похоже
                            # Обновление значения характеристики
                            product_feature = ProductFeatureValue.objects.filter(product=product, feature__name=match).first()
                            if product_feature:
                                product_feature.value = feature_value
                                product_feature.save()  # Сохраняем обновленное значение
                                self.message_user(request, f"Обновлено: {match} = {feature_value}")  # Отладочное сообщение
                        else:
                            # Если схожесть недостаточна, создаем новую характеристику
                            feature, created = Feature.objects.get_or_create(name=feature_name)
                            ProductFeatureValue.objects.create(product=product, feature=feature, value=feature_value)
                            self.message_user(request, f"Создано: {feature_name} = {feature_value}")  # Отладочное сообщение
                    else:
                        # Если нет похожих характеристик, создаем новую
                        feature, created = Feature.objects.get_or_create(name=feature_name)
                        ProductFeatureValue.objects.create(product=product, feature=feature, value=feature_value)
                        self.message_user(request, f"Создано: {feature_name} = {feature_value}")  # Отладочное сообщение

                self.message_user(request, f"Характеристики для '{product.name}' успешно обновлены.")
            else:
                self.message_user(request, f"У товара '{product.name}' нет HTML-кода.", level='error')

        return HttpResponseRedirect(request.get_full_path())

    def parse_table(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('tr')
        
        features_data = {}
        
        for row in rows:
            cols = row.find_all(['th', 'td'])  # Изменили на поиск как th, так и td
            if len(cols) == 2:  # Проверяем, что есть две колонки
                feature_name = cols[0].get_text(strip=True)
                feature_value = cols[1].get_text(strip=True)
                features_data[feature_name] = feature_value
                
        return features_data

    parse_features.short_description = "Парсить характеристики из HTML"
    



@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', 'slug')
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
            zagr_count = 1
            for row in reader:
                categories = row[4].split(',')
                parent_category = None

                # Создание иерархии категорий с уникальным `slug`
                for category_name in categories:
                    category_name = category_name.strip()
                    original_slug = slugify(category_name)
                    slug = original_slug
                    counter = 1

                    # Определяем, является ли категория главной или подкатегорией
                    if parent_category is None:
                        # Для главных категорий проверяем уникальность `slug` среди главных категорий
                        while ProductCategory.objects.filter(slug=slug, parent=None).exists():
                            slug = f"{original_slug}-{counter}"
                            counter += 1
                    else:
                        # Для подкатегорий проверяем уникальность `slug` внутри родительской категории
                        while ProductCategory.objects.filter(slug=slug, parent=parent_category).exists():
                            slug = f"{original_slug}-{counter}"
                            counter += 1

                    try:
                        # Создание или получение категории
                        category, created = ProductCategory.objects.get_or_create(
                            name=category_name,
                            parent=parent_category,
                            defaults={'slug': slug}
                        )
                        # if created:
                        #     print(f"Создана {'главная' if parent_category is None else 'под'} категория: {category_name}")
                        # else:
                        #     print(f"Категория уже существует: {category_name}")

                        # Обновляем родительскую категорию для следующего уровня
                        parent_category = category

                    except IntegrityError as e:
                        print(f"Ошибка целостности данных при создании категории '{category_name}': {e}")
                        continue  # Переходим к следующей категории

                # Создание продукта (оставьте ваш существующий код здесь)
                name = row[0]
                base_price = row[1].replace(',', '.').strip()
                description = row[2]
                description_2 = row[3]
                slug = slugify(name)
                product_link = row[5]
                image = row[6] if row[6] else 'product_images/1-klavishnij_prohodnoj_viklyuchatel_10A_250V_CHINT.jpg'
                quantity = row[7]
                unit = row[8]
                manufacturer = row[9]
                supplier = row[10]
                vat_price = row[11]
                markup_percentage = 15

                unit, _ = Unit.objects.get_or_create(name=unit)
                manufacturer, _ = Manufacturer.objects.get_or_create(name=manufacturer)
                supplier, _ = Supplier.objects.get_or_create(supplier=supplier)

                # Проверка уникальности `slug` для продукта
                original_slug = slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1

                try:
                    product, created = Product.objects.get_or_create(
                        name=name,
                        defaults={
                            'base_price': base_price,
                            'description': description,
                            'description_2': description_2,
                            'category': parent_category,
                            'slug': slug,
                            'quantity': quantity,
                            'image': image,
                            'product_link': product_link,
                            'unit': unit,
                            'manufacturer': manufacturer,
                            'supplier': supplier,
                            'vat_price': vat_price,
                            'markup_percentage': markup_percentage,
                        }
                    )
                    print(f'{zagr_count}) {name}')
                    zagr_count += 1
                except IntegrityError:
                    print("Ошибка при создании продукта.")

            # Пометка файла как обработанного
            csv_file.processed = True
            csv_file.save()

        self.message_user(request, f"{queryset.count()} CSV файлов успешно обработаны.")
    handle_uploaded_csv.short_description = "Обработать выбранные CSV файлы"

admin.site.register(CSVFile, CSVFileAdmin)

