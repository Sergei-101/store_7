# Generated by Django 5.0.1 on 2024-02-08 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_promotion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='suppler',
            new_name='supplier',
        ),
        migrations.AlterField(
            model_name='product',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.promotion'),
        ),
    ]