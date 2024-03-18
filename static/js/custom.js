$(document).on("click", ".js-quick-view-cust", function () {

    // Получаем идентификатор товара из атрибута data-product-id кнопки
    var productId = $(this).data('product-id');
    // Получаем значение активности акции из атрибута data-promotion-active кнопки
    var isPromotionActive = $(this).data('promotion-active');

    // Отправляем AJAX-запрос на сервер для получения информации о товаре
    $.ajax({
        url: '/products/products/' + productId + '/quick_view/', // URL для обработки AJAX-запроса
        type: 'GET', // Метод запроса
        success: function (response) {
            // Обработка успешного ответа от сервера
            $('#quick-view-product-id').val(productId); // Устанавливаем идентификатор товара в скрытое поле формы
            // Вставляем остальные данные о товаре в окно быстрого просмотра
            $('#product-name').text(response.name); // Вставляем название товара
            $('#product-price').text(response.price + ' BYN'); // Вставляем цену товара
            $('#product-description').html(response.description);
            $('#product-image').attr('src', response.image); // Устанавливаем изображение товара
            if (isPromotionActive === 'True') {
                // Если акция активна, выполнить соответствующие действия
                // Например, изменить стиль или добавить дополнительную информацию
                // Пример:
                $('#product-price-old').text(response.oldprice +  ' BYN'); // Вставляем цену товара
            } else {
                $('#product-price-old').text('');
            }

        },
        error: function (xhr, status, error) {
            // Обработка ошибки
            console.error('Ошибка при загрузке информации о товаре:', error);
        }
    });
});

function updateCartContents() {
    $.ajax({
        url: '/cart/content/',
        type: 'GET',
        success: function(data) {
            // Очищаем текущее содержимое корзины
            $('#cart-items').empty();

            // Создаем HTML-разметку для каждого элемента корзины
            $.each(data.cart_items, function(index, item) {
                var cartItemHTML = '<div class="cart-drawer-item d-flex position-relative">';
                cartItemHTML += '<div class="position-relative">';
                cartItemHTML += '<img loading="lazy" class="cart-drawer-item__img" src="' + item.image + '" alt="' + item.name + '">';
                cartItemHTML += '</div>';
                cartItemHTML += '<div class="cart-drawer-item__info flex-grow-1">';
                cartItemHTML += '<h6 class="cart-drawer-item__title fw-normal">' + item.name + '</h6>';
                cartItemHTML += '<div class="d-flex align-items-center justify-content-between mt-1">';
                cartItemHTML += '<div class="qty-control position-relative">';
                cartItemHTML += '<input type="number" name="quantity" value="' + item.quantity + '" min="1" class="qty-control__number border-0 text-center" data-product-id="' + item.id + '">';
                cartItemHTML += '<div class="qty-control__reduce_1 text-start">-</div>';
                cartItemHTML += '<div class="qty-control__increase_1 text-end">+</div>';
                cartItemHTML += '</div><!-- .qty-control -->';
                cartItemHTML += '<span class="cart-drawer-item__price money price">' + item.total_price + '</span>';
                cartItemHTML += '</div>';
                cartItemHTML += '</div>';
                cartItemHTML += '<button class="btn-close-xs position-absolute top-0 end-0 js-cart-item-remove js-cart-item-remove-cust" data-product-id="' + item.id + '"></button>';
                cartItemHTML += '</div>';
                cartItemHTML += '<hr class="cart-drawer-divider">';
                // Вставляем HTML-разметку в корзину
                $('#cart-items').append(cartItemHTML);
            });

            // Обновляем общую цену корзины
            $('#total-price').text(data.total_price);

        },
        error: function(xhr, status, error) {
            console.error('Произошла ошибка при получении данных о корзине:', error);
        }
    });
}

$('.js-open-aside-update').click(function() {
    // В этом месте вы открываете боковую панель корзины (например, показываете модальное окно или сайдбар)
    // После открытия, сразу обновите содержимое корзины
    updateCartContents();
});

// Обработчик клика на кнопку "Добавить в корзину"
$('.js-add-cart-cust').click(function() {

    var product_id = $(this).data('product-id');
    var quantity = $('#quick-view-quantity').val();
    var override = $('#override').val();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Получение CSRF-токена из скрытого поля формы

    if (quantity < 1) {
        quantity = 1;
    }
    product_id = product_id ? product_id : $('#quick-view-product-id').val();  // Получаем идентификатор товара из скрытого поля формы
    $(this).css('background-color', 'green') // Изменение цветка кнопки при нажатии
    $.ajax({
        type: 'POST',
        url: '/cart/adds/' + product_id + '/',
        data: {
            'quantity': quantity,
            'override': override,
            'csrfmiddlewaretoken': csrfToken  // Передача CSRF-токена в запросе
        },
        success: function(data) {
            if (data.success) {
                // Обработка успешного добавления в корзину
                updateCartContents();
            } else {
                alert(data.message);
            }
        },
        error: function(xhr, status, error) {
            alert('Произошла ошибка при отправке запроса на сервер.');
        }
    });

});

// Обработчик клика на кнопку "удаление товаров из корзины"
$(document).on('click', '.js-cart-item-remove-cust', function(e) {
    e.preventDefault();
    var product_id = $(this).data('product-id');

    // Отправляем AJAX-запрос для удаления товара из корзины
    $.ajax({
        type: 'POST',
        url: '/cart/remove/' + product_id + '/',
        data: {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data) {
            if (data.success) {
                updateCartContents();
            } else {
                updateCartContents();
            }
        },
        error: function(xhr, status, error) {
            console.error('Произошла ошибка при отправке запроса на сервер:', error);
        }
    });

});

$(document).on('change', '.qty-control__number', function() {
    var productId = $(this).data('product-id');
    var newQuantity = $(this).val();

    // Отправляем AJAX-запрос для обновления количества товара в корзине
    $.ajax({
        type: 'POST',
        url: '/cart/adds/' + productId + '/',
        data: {
            'quantity': newQuantity,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(data) {
            // После успешного обновления количества товара, обновляем общую цену корзины
            $('#total-price').text(data.total_price);
            updateCartContents();
            // Затем обновляем содержимое корзины
        },
        error: function(xhr, status, error) {
            console.error('Произошла ошибка при отправке запроса на сервер:', error);
        }
    });

});
$(document).on('click', '.qty-control__reduce_1', function() {
    var inputField = $(this).siblings('.qty-control__number');

    var currentQuantity = parseInt(inputField.val());
    console.log(inputField, currentQuantity )
    if (currentQuantity > 1) {
        inputField.val(currentQuantity - 1);
        inputField.change(); // Имитируем событие изменения, чтобы обработчик срабатывал
    }
});

// Обработчик нажатия на кнопку увеличения количества товара
$(document).on('click', '.qty-control__increase_1', function() {
    var inputField = $(this).siblings('.qty-control__number');
    var currentQuantity = parseInt(inputField.val());
    inputField.val(currentQuantity + 1);
    inputField.change(); // Имитируем событие изменения, чтобы обработчик срабатывал
});

document.addEventListener('DOMContentLoaded', function() {
    const personalForm = document.getElementById('personal-form');
    const businessForm = document.getElementById('business-form');
    const customerTypeSelect = document.getElementById('customer-type');

    const deliveryMethodSelectPersonal = document.getElementById('delivery-method');
    const deliveryMethodSelectBusiness = document.getElementById('delivery-method-business');
    const addressFieldPersonal = document.getElementById('address-field');
    const addressFieldBusiness = document.getElementById('address-field-business');

    customerTypeSelect.addEventListener('change', function() {
        if (this.value === 'personal') {
            personalForm.style.display = 'block';
            businessForm.style.display = 'none';
        } else {
            personalForm.style.display = 'none';
            businessForm.style.display = 'block';
        }
    });

    deliveryMethodSelectPersonal.addEventListener('change', function() {
        toggleAddressField.call(this, addressFieldPersonal);
    });

    deliveryMethodSelectBusiness.addEventListener('change', function() {
        toggleAddressField.call(this, addressFieldBusiness);
    });

    function toggleAddressField(addressField) {
        if (this.value === 'delivery') {
            addressField.style.display = 'block';
        } else {
            addressField.style.display = 'none';
        }
    }

    // Изначально скрываем или показываем поле в зависимости от выбранного метода доставки
    toggleAddressField.call(deliveryMethodSelectPersonal, addressFieldPersonal);
    toggleAddressField.call(deliveryMethodSelectBusiness, addressFieldBusiness);
});

// Аккордеон меню боковое
const boxes = Array.from(document.querySelectorAll(".box_product")); // считываем все элементы аккордеона в массив
boxes.forEach((box) => {
  box.addEventListener("click", boxHandler); // при нажатии на бокс вызываем ф-ию boxHanlder
});
function boxHandler(e) {
  e.preventDefault(); // сбрасываем стандартное поведение
  let currentBox = e.target.closest(".box_product"); // определяем текущий бокс
  let currentContent = e.target.nextElementSibling; // находим скрытый контент
  currentBox.classList.toggle("active"); // присваиваем ему активный класс
  if (currentBox.classList.contains("active")) {
    // если класс активный ..
    currentContent.style.maxHeight = currentContent.scrollHeight + "px"; // открываем контент
  } else {
    // в противном случае
    currentContent.style.maxHeight = 0; // скрываем контент
  }
}