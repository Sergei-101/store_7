# Generated by Django 5.0 on 2024-11-06 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parser_store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parserstore',
            name='name_pars',
        ),
    ]