from django.apps import AppConfig
from .telegram_bot import run_bot
import threading

class TelegramBotStore7Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot_store7'

    # def ready(self):
    #     # Проверяем, что бот запускается только один раз
    #     bot_thread = threading.Thread(target=run_bot)
    #     bot_thread.daemon = True  # Поток завершится, когда завершится основной процесс
    #     bot_thread.start()