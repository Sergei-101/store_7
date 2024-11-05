from django.core.management.base import BaseCommand
from telegram_bot_store7.telegram_bot import run_bot

class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        run_bot()
