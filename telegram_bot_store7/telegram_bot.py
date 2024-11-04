from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from django.conf import settings
import asyncio

# Инициализация бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Функция для отправки уведомления о заказе
async def send_order_notification(order_details):
    await bot.send_message(settings.TELEGRAM_ADMIN_ID, order_details)

# Обработчик команды /start для получения Telegram ID администратора
@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")

# Основная функция запуска бота
async def start_bot():
    # Запуск бота в режиме polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Функция запуска бота в отдельном асинхронном процессе
def run_bot():
    asyncio.run(start_bot())



