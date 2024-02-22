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
                    cartItemHTML += '<img loading="lazy" class="cart-drawer-item__img" src="' + item.image_url + '" alt="' + item.name + '">';
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

    // Обработчик изменения количества товара в корзине
    $(document).on('change', '.qty-control__number', function() {
        var productId = $(this).data('product-id');
        var newQuantity = $(this).val();

        // Отправляем AJAX-запрос для обновления количества товара в корзине
        $.ajax({
            type: 'POST',
            url: '/cart/update/' + productId + '/',
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

    // Обновление корзины при загрузке страницы
    updateCartContents();
});
