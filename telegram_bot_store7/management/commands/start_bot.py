from django.core.management.base import BaseCommand
from telegram_bot_store7.telegram_bot import run_bot

class Command(BaseCommand):
    help = 'Запустить Telegram-бота'

    def handle(self, *args, **kwargs):
        self.stdout.write("Запуск Telegram-бота...")
        run_bot()
