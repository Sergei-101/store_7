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
                $('#product-name').text(response.name); // Вставляем название товара
                $('#product-price').text('Цена: ' + response.price); // Вставляем цену товара
                $('#product-description').text(response.description); // Вставляем описание товара
//                $('#product-image').attr('src', response.image_url); // Вставляем изображение товара
            },
            error: function (xhr, status, error) {
                // Обработка ошибки
                console.error('Ошибка при загрузке информации о товаре:', error);
            }
        });
    });
});