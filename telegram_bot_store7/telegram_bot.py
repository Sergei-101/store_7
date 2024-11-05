from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
from django.conf import settings
import asyncio
from datetime import datetime
from asgiref.sync import sync_to_async

# Инициализация бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Функция для проверки, является ли пользователь администратором
def is_admin(user_id):
    return user_id == int(settings.TELEGRAM_ADMIN_ID)

@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    admin_status = "Вы являетесь администратором." if is_admin(user_id) else "Вы не являетесь администратором."
    await message.answer(f"Ваш Telegram ID: {user_id}. {admin_status}")

# Функция для отправки уведомления о заказе только администратору
async def send_order_notification(order_details):
    # Убедимся, что это уведомление отправляется только администратору
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
            json={
                "chat_id": settings.TELEGRAM_ADMIN_ID,  # ID админа
                "text": order_details,
            }
        ) as response:
            return await response.json()

@dp.message(Command(commands=["today_orders"]))
async def cmd_today_orders(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав для доступа к этой команде.")
        return

    from orders.models import Order  # Переместили импорт сюда

    # Получаем сегодняшнюю дату
    today = datetime.today().date()
    
    # Используем sync_to_async для выполнения запроса к базе данных
    orders_today = await sync_to_async(Order.objects.filter)(created__date=today)  # Заменили created_at на created

    # Выполняем запрос к базе данных асинхронно
    orders_today_list = await sync_to_async(list)(orders_today)  # Преобразуем QuerySet в список асинхронно

    if orders_today_list:
        # Формируем сообщение с заказами
        order_list = "\n".join([f"Заказ ID: {order.id}, Клиент: {order.contact_person}, Сумма: {order.total_cost}" 
                                 for order in orders_today_list])
        await message.answer(f"Заказы за сегодня:\n{order_list}")

        # Отправляем уведомление администратору
        await send_order_notification(f"Новые заказы за сегодня:\n{order_list}")
    else:
        await message.answer("За сегодня заказов нет.")

# Основная функция запуска бота
async def start_bot():
    # Запуск бота в режиме polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Функция запуска бота в отдельном асинхронном процессе
def run_bot():
    asyncio.run(start_bot())
