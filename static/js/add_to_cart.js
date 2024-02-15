$(document).ready(function() {
    // Устанавливаем значение поля quantity по умолчанию равным 1
    $('#quantity').val(1);

    // Обработчик клика на кнопку "Добавить в корзину"
    $('.js-add-cart').click(function(e) {
        e.preventDefault();
        var product_id = $(this).data('product-id');
        $.ajax({
            type: 'POST',
            url: '/cart/add/' + product_id + '/',
            data: {
                'quantity': $('#quantity').val(),
                'override': $('#override').val()
            },
            success: function(data) {
                if (data.success) {
                    // Обновить содержимое корзины или выполнить другие действия
                    alert('Товар успешно добавлен в корзину!');
                } else {
                    alert('Произошла ошибка: ' + data.error);
                }
            },
            error: function(xhr, status, error) {
                alert('Произошла ошибка при отправке запроса на сервер.');
            }
        });
    });
});