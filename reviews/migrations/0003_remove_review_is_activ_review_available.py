# Generated by Django 5.0 on 2024-04-08 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_is_activ'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='is_activ',
        ),
        migrations.AddField(
            model_name='review',
            name='available',
            field=models.BooleanField(default=False, verbose_name='Видимость'),
        ),
    ]