$(document).ready(function() {
    // Функция для обновления содержимого корзины
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
                    cartItemHTML += '<div class="qty-control__reduce text-start">-</div>';
                    cartItemHTML += '<div class="qty-control__increase text-end">+</div>';
                    cartItemHTML += '</div><!-- .qty-control -->';
                    cartItemHTML += '<span class="cart-drawer-item__price money price">' + item.price + '</span>';
                    cartItemHTML += '</div>';
                    cartItemHTML += '</div>';
                    cartItemHTML += '<button class="btn-close-xs position-absolute top-0 end-0 js-cart-item-remove" data-product-id="' + item.id + '"></button>';
                    cartItemHTML += '</div>';
                    cartItemHTML += '<hr class="cart-drawer-divider">';
                    // Вставляем HTML-разметку в корзину
                    $('#cart-items').append(cartItemHTML);
                });
                $.each(data.cart_items, function(index, item) {
                    var existingCartItem = $('#cart-items-basket').find('[data-product-id="' + item.id + '"]');

                    if (existingCartItem.length) {
                        existingCartItem.find('.qty-control__number').val(item.quantity);
                    } else {
                        var cartItemHTML = '<tr>';
                        cartItemHTML += '<td>';
                        cartItemHTML += '<div class="shopping-cart__product-item">';
                        cartItemHTML += '<img loading="lazy" src="' + item.image + '" alt="' + item.name + '" width="120" height="120" alt="" />';
                        cartItemHTML += '</div>';
                        cartItemHTML += '</td>';
                        cartItemHTML += '<td>';
                        cartItemHTML += '<div class="shopping-cart__product-item__detail">';
                        cartItemHTML += '<h4>' + item.name + '</h4>';
                        cartItemHTML += '</div>';
                        cartItemHTML += '</td>';
                        cartItemHTML += '<td>';
                        cartItemHTML += '<span class="shopping-cart__product-price">' + item.price + '</span>';
                        cartItemHTML += '</td>';
                        cartItemHTML += '<td>';
                        cartItemHTML += '<div class="qty-control position-relative">';
                        cartItemHTML += '<input type="number" name="quantity" value="' + item.quantity + '" min="1" class="qty-control__number text-center" data-product-id="' + item.id + '">';
                        cartItemHTML += '<div class="qty-control__reduce">-</div>';
                        cartItemHTML += '<div class="qty-control__increase">+</div>';
                        cartItemHTML += '</div><!-- .qty-control -->';
                        cartItemHTML += '</td>';
                        cartItemHTML += '<td>';
                        cartItemHTML += '<span class="shopping-cart__subtotal">$</span>';
                        cartItemHTML += '</td>';
                        cartItemHTML += '<td>';
                        cartItemHTML += '<a href="#" class="js-cart-item-remove" data-product-id="' + item.id + '">';
                        cartItemHTML += '<svg width="10" height="10" viewBox="0 0 10 10" fill="#767676" xmlns="http://www.w3.org/2000/svg">';
                        cartItemHTML += '<path d="M0.259435 8.85506L9.11449 0L10 0.885506L1.14494 9.74056L0.259435 8.85506Z"/>';
                        cartItemHTML += '<path d="M0.885506 0.0889838L9.74057 8.94404L8.85506 9.82955L0 0.97449L0.885506 0.0889838Z"/>';
                        cartItemHTML += '</svg> ';
                        cartItemHTML += '</a>';
                        cartItemHTML += '</td>';
                        cartItemHTML += '</tr>';

                        $('#cart-items-basket').append(cartItemHTML);
                    }
                });

                // Обновляем общую цену корзины
                $('#total-price').text(data.total_price);
            },
            error: function(xhr, status, error) {
                console.error('Произошла ошибка при получении данных о корзине:', error);
            }
        });
    }

    // Обработчик изменения количества товара в корзине
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
                // Затем обновляем содержимое корзины
                updateCartContents();
            },
            error: function(xhr, status, error) {
                console.error('Произошла ошибка при отправке запроса на сервер:', error);
            }
        });
    });

    // Обработчик нажатия на кнопку уменьшения количества товара
    $(document).on('click', '.qty-control__reduce', function() {
        var inputField = $(this).siblings('.qty-control__number');
        var currentQuantity = parseInt(inputField.val());
        if (currentQuantity > 1) {
            inputField.val(currentQuantity - 1);
            inputField.change(); // Имитируем событие изменения, чтобы обработчик срабатывал
        }
    });

    // Обработчик нажатия на кнопку увеличения количества товара
    $(document).on('click', '.qty-control__increase', function() {
        var inputField = $(this).siblings('.qty-control__number');
        var currentQuantity = parseInt(inputField.val());
        inputField.val(currentQuantity + 1);
        inputField.change(); // Имитируем событие изменения, чтобы обработчик срабатывал
    });

    // Обработчик клика на кнопку "Добавить в корзину"
    $('.js-add-cart').click(function(e) {
        e.preventDefault();
        var product_id = $(this).data('product-id');
        var quantity = 1;
        var override = $('#override').val();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Получение CSRF-токена из скрытого поля формы

        $.ajax({
            type: 'POST',
            url: '/cart/adds/' + product_id + '/',
            data: {
                'quantity': quantity,
                'override': override,
                'csrfmiddlewaretoken': csrfToken  // Передача CSRF-токена в запросе
            },
            success: function(data) {
                updateCartContents();
                if (data.success) {
                    // Обработка успешного добавления в корзину
                    passive;
                } else {
                    alert(data.message);
                }
            },
            error: function(xhr, status, error) {
                alert('Произошла ошибка при отправке запроса на сервер.');
            }
        });
    });
    $(document).on('click', '.js-cart-item-remove', function(e) {
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
            updateCartContents();
            if (data.success) {
                passive;
            } else {
                alert(data.message);
            }
        },
        error: function(xhr, status, error) {
            console.error('Произошла ошибка при отправке запроса на сервер:', error);
        }
    });
    });

    // Обновление корзины при загрузке страницы
    updateCartContents();
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

$(document).ready(function() {
    // Обработчик клика на кнопку "Быстрый просмотр"
    $(document).on("click", ".js-quick-view", function (e) {
        e.preventDefault(); // Предотвращаем стандартное действие кнопки

        // Получаем идентификатор товара из атрибута data-product-id кнопки
        var productId = $(this).data('product-id');

        // Отправляем AJAX-запрос на сервер для получения информации о товаре
        $.ajax({
            url: '/products/products/' + productId + '/quick_view/', // URL для обработки AJAX-запроса
            type: 'GET', // Метод запроса
            success: function (response) {
                // Обработка успешного ответа от сервера
                $('#quick-view-product-id').val(productId); // Устанавливаем идентификатор товара в скрытое поле формы
                // Вставляем остальные данные о товаре в окно быстрого просмотра
                $('#product-name').text(response.name); // Вставляем название товара
                $('#product-price').text('Цена: ' + response.price); // Вставляем цену товара
                $('#product-description').html(response.description);
                $('#product-image').attr('src', response.image); // Устанавливаем изображение товара
                // Показываем окно быстрого просмотра
            },
            error: function (xhr, status, error) {
                // Обработка ошибки
                console.error('Ошибка при загрузке информации о товаре:', error);
            }
        });
    });

    // Здесь вы можете добавить другие обработчики событий и функции, если это необходимо
});

//Добавление из быстрого просмотра
$(document).on("click", ".js-addtocart", function (e) {
    e.preventDefault(); // Предотвращаем стандартное действие кнопки
    var productId = $('#quick-view-product-id').val(); // Получаем идентификатор товара из скрытого поля формы
    var quantity = $('#quick-view-quantity').val(); // Получаем количество товара из поля формы
    var csrfToken = getCookie('csrftoken'); // Получаем CSRF-токен

    $.ajax({
        type: 'POST',
        url: '/cart/adds/' + productId + '/',
        data: {
            'quantity': quantity
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        success: function(data) {
            if (data.success) {
                // Если товар успешно добавлен в корзину, выведите сообщение об этом
                // alert('Товар успешно добавлен в корзину!');
                passive;
                // Закрываем окно быстрого просмотра после успешного добавления в корзину
                $('#quick-view-modal').modal('hide');
            } else {
                // Если возникла ошибка при добавлении товара в корзину, выведите сообщение об ошибке
                alert('Произошла ошибка: ' + data.message);
            }
        },
        error: function(xhr, status, error) {
            // Выводим сообщение об ошибке, если возникла проблема с AJAX-запросом
            alert('Произошла ошибка при отправке запроса на сервер.');
        }
    });
});


// Функция для получения CSRF-токена из cookie
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Находим CSRF-токен в cookie
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}