# utils.py
from django.utils import timezone
import re
import requests
from bs4 import BeautifulSoup
from .models import ParserStore, PriceCheck, Product
from bs4 import BeautifulSoup
import requests


def update_price(product_id):
    print(f"Начало обновления цены для продукта с ID {product_id}...")
    product = Product.objects.get(id=product_id)
    today = timezone.now().date()

    # Проверяем, была ли проверка сегодня
    last_check = PriceCheck.objects.filter(product=product, check_date=today).first()
    
    if last_check:
        print(f"Цена уже проверялась сегодня для продукта '{product.name}'.")
        return {
            "name": product.name,
            "current_price": last_check.current_price,
            "new_price": last_check.new_price,
            "unit": str(product.unit.name),            
            "markup_percentage":product.markup_percentage,
            "supplier":product.supplier.supplier
        }
    

    supplier = product.supplier
    print(f"Получен продукт '{product.name}' от поставщика '{supplier}'.")

    try:
        parser = ParserStore.objects.get(supplier=supplier)
        print(f"Найден парсер для поставщика '{supplier}'.")
        if not parser.page_pars:
            print(f"Не заполнены поля для парсинга '{parser.page_pars}'.")
            return {
            "name": product.name,
            "current_price": product.final_price(),
            "new_price": "N/A",            
            "unit": str(product.unit.name),            
            "markup_percentage":product.markup_percentage,
            "supplier":product.supplier.supplier
            }
            
    except ParserStore.DoesNotExist:
        print(f"Нет настроек парсинга для поставщика '{supplier}'.")
        return {
            "name": product.name,
            "current_price": product.final_price(),
            "new_price": "N/A",
            "unit": str(product.unit.name),
            "markup_percentage":product.markup_percentage,
            "supplier":product.supplier.supplier
        }
    

    headers = {"User-Agent": parser.headers}
    url = product.product_link
    print(f"Отправка запроса к URL {url}...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Ошибка: не удалось получить данные от поставщика.")
        return {"error": "Не удалось получить данные от поставщика"}

    soup = BeautifulSoup(response.text, 'lxml')
    print("Запрос успешен. Начало парсинга данных...")

    try:
        page_pars = soup.find_all('div', class_=parser.page_pars)
        print(f"Найдено {len(page_pars)} элементов для парсинга.")
        print(f'Ищем элементы с параметрами: "div", class_="{parser.page_pars}"')

        for i in page_pars:
            name_from_site = i.find('h1')
            if name_from_site:
                name_from_site = name_from_site.text.strip()
                print(f"Название с сайта: {name_from_site}")
            else:
                print("Ошибка: не удалось найти название на сайте.")
                continue

            if product.name.lower() != name_from_site.lower():
                print("Название продукта не совпадает с названием на сайте.")
                return {
                    "name": product.name,
                    "current_price": product.final_price(),
                    "new_price": "N/A",
                    "unit": str(product.unit.name),
                    "markup_percentage":product.markup_percentage,
                    "supplier":product.supplier.supplier
                }

            new_price_element = i.find('span', class_=parser.price_pars)
            if new_price_element:
                price_text = new_price_element.text.strip()
                print(f"Полученная цена с сайта: '{price_text}'")  # Выводим для диагностики

                # Очистка цены от ненужных символов
                clean_price = re.sub(r"[^\d,\.]", "", price_text).rstrip(',')  # Убираем все символы, кроме цифр, запятой и точки
                clean_price = clean_price.replace(" ", "").replace(",", ".")  # Убираем пробелы и заменяем точку на запятую
                clean_price = clean_price.rstrip('.')  # Убираем запятую в конце, если она есть

                print(f"Очистенная цена: '{clean_price}'")

                # Проверяем, если результат пустой или не является числом
                if not clean_price or not clean_price.replace('.', '', 1).isdigit():
                    print(f"Ошибка: некорректная цена на сайте. Строка с ценой: {price_text}")
                    return {"error": "Некорректная цена на сайте"}

                # Преобразуем цену в число
                new_price = float(clean_price)
                print(f"Новая цена с сайта: {new_price}")
            else:
                print("Ошибка: цена не найдена на сайте.")
                return {"error": "Цена не найдена на сайте"}

            unit_element = i.find("div", class_=parser.unit_pars)
            unit = unit_element.text.strip() if unit_element else "N/A"
            print(f"Единица измерения с сайта: {unit}")
            
            
            current_price = float(product.final_price())               
            if new_price - current_price > 300:
                new_price = new_price / 1000
            new_price = round(new_price, 2)

            # Расчет цены без НДС (20%)
            new_price_bez_nds = round(new_price / 1.20, 2)  # Цена без НДС

            is_price_updated = product.base_price == new_price_bez_nds
            if not is_price_updated:
                product.base_price = new_price_bez_nds  # Обновляем цену как число
                product.save()
                print(f"Цена обновлена для продукта '{product.name}': новая цена {new_price_bez_nds}.")
            else:
                print(f"Цена актуальна для продукта '{product.name}'.")

            # Сохранение данных проверки в PriceCheck
            PriceCheck.objects.create(
                product=product,
                check_date=today,
                current_price=current_price,
                new_price=new_price,                
            )

            return {
                "name": product.name,
                "current_price": product.final_price(),
                "new_price": new_price,
                "is_price_updated": is_price_updated,
                "unit": str(product.unit.name),
                # "status": "Цена обновлена" if not is_price_updated else "Цена актуальна",
                "markup_percentage":product.markup_percentage,
                "supplier":product.supplier.supplier
            }

    except AttributeError as e:
        print(f"Ошибка парсинга данных: {e}")
        return {"error": "Ошибка парсинга данных: " + str(e)}
