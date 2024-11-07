from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
    ]

    user_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID пользователя")
    chat_id = models.BigIntegerField(verbose_name="ID чата")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Никнейм")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client', verbose_name="Роль")

    def __str__(self):
        return f"{self.username or self.user_id} ({self.role})"
