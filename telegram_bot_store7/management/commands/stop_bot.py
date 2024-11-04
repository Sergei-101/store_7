from django.core.management.base import BaseCommand
from telegram_bot_store7.telegram_bot import stop_bot

class Command(BaseCommand):
    help = 'Остановить Telegram-бота'

    def handle(self, *args, **kwargs):
        self.stdout.write("Остановка Telegram-бота...")
        stop_bot()
