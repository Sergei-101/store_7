function updateCartContent(cartContent) {
    // Находим элемент корзины на странице
    var cartElement = $('.cart-content');

    // Заменяем содержимое корзины новым содержимым
    cartElement.html(cartContent);
}


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
                // Показываем окно быстрого просмотра
            },
            error: function (xhr, status, error) {
                // Обработка ошибки
                console.error('Ошибка при загрузке информации о товаре:', error);
            }
        });
    });

    // Обработчик клика на кнопку "Добавить в корзину"
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