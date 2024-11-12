from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
from django.conf import settings
from datetime import datetime
from asgiref.sync import sync_to_async
import asyncio
import logging



# Инициализация бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Настройка логирования
logger = logging.getLogger(__name__)

# Функция для проверки, является ли пользователь администратором
def is_admin(user_id):
    from telegram_bot_store7.models import UserProfile  # Импорт модели внутри функции
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        return user_profile.role == 'admin'
    except UserProfile.DoesNotExist:
        return False

@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    username = message.from_user.username
    from telegram_bot_store7.models import UserProfile
    # Создание профиля пользователя или обновление существующего
    user_profile, created = await sync_to_async(UserProfile.objects.get_or_create)(
        user_id=user_id,
        defaults={
            'chat_id': chat_id,
            'username': username,
            'role': 'client',  # Назначаем "клиент" по умолчанию
        }
    )

    if not created:
        # Если профиль существует, обновляем его данные
        user_profile.chat_id = chat_id
        user_profile.username = username
        await sync_to_async(user_profile.save)()

    admin_status = "Вы являетесь администратором." if user_profile.role == 'admin' else "Вы не являетесь администратором."
    await message.answer(f"Ваш Telegram ID: {user_id}. {admin_status}")

async def send_order_notification(user_id, order_details):
    # Проверка, является ли пользователь администратором
    if not is_admin(user_id):
        logger.warning(f"User {user_id} is not an admin, notification will not be sent.")
        return None

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
                json={
                    "chat_id": settings.TELEGRAM_ADMIN_ID,  # ID админа
                    "text": order_details,
                }
            ) as response:
                # Проверяем статус ответа
                response_data = await response.json()
                if response.status != 200:
                    logger.error(f"Failed to send message: {response_data}")
                    return None
                return response_data
    except Exception as e:
        logger.error(f"Error sending order notification: {e}")
        return None

# @dp.message(Command(commands=["today_orders"]))
# async def cmd_today_orders(message: types.Message):
#     if not is_admin(message.from_user.id):
#         await message.answer("У вас нет прав для доступа к этой команде.")
#         return

#     from orders.models import Order  # Импортируем модель здесь
    

#     # Получаем сегодняшнюю дату
#     today = datetime.today().date()
    
#     # Используем sync_to_async для выполнения запроса к базе данных
#     orders_today = await sync_to_async(Order.objects.filter)(created__date=today)

#     # Выполняем запрос к базе данных асинхронно
#     orders_today_list = await sync_to_async(list)(orders_today)  # Преобразуем QuerySet в список асинхронно

#     if orders_today_list:
#         # Создаем клавиатуру с кнопками для каждого заказа
#         keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
#             [types.InlineKeyboardButton(text=f"Заказ ID: {order.id} (Клиент: {order.contact_person})", callback_data=f"order_{order.id}")]
#              for order in orders_today_list]
#         )

#         await message.answer("Выберите заказ для просмотра деталей:", reply_markup=keyboard)
        
        

# @dp.callback_query(lambda callback: callback.data.startswith("order_"))
# async def process_order(callback: types.CallbackQuery):
#     # Вывод информации о колбек-данных
#     print(f"Callback data: {callback.data}")  # Отладочный вывод в консоль
#     # Проверяем, является ли пользователь администратором
#     if not is_admin(callback.from_user.id):
#         await callback.answer("У вас нет прав для доступа к этой команде.")
#         return
#     print('Admin')
#     order_id = callback.data.split("_")[1]
    
#     from orders.models import Order  # Импортируем модель здесь    
#     order = await sync_to_async(Order.objects.get)(id=order_id)    
#     # Формируем сообщение с деталями заказа
#     order_details = f"Детали заказа ID: {order.id}\n" \
#                     f"Клиент: {order.contact_person}\n" \
#                     f"Сумма: {order.total_cost}\n" \
#                     # f"Товары: {', '.join([f'{item.product.name} (кол-во: {item.quantity})' for item in order.items.all])}"                   
                    
#     await callback.message.answer(order_details)

# Основная функция запуска бота
async def start_bot():
    # Запуск бота в режиме polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Функция запуска бота в отдельном асинхронном процессе
def run_bot():    
    asyncio.run(start_bot())
