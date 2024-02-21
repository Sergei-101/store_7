$(document).ready(function() {
    // Получение CSRF-токена из cookie
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

    // Обработчик клика на кнопку "Добавить в корзину"
    $('.js-add-cart').click(function(e) {
        e.preventDefault();
        var product_id = $(this).data('product-id');
        var quantity = 1; // Установка значения quantity равным 1
        var override = $('#override').val();
        var csrfToken = getCookie('csrftoken'); // Получение CSRF-токена

        $.ajax({
            type: 'POST',
            url: '/cart/adds/' + product_id + '/',
            data: {
                'quantity': quantity,
                'override': override
            },
            // Установка CSRF-токена в заголовок запроса
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            },
            success: function(data) {
                if (data.success) {
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
});