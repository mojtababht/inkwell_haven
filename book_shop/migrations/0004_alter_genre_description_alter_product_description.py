# Generated by Django 4.2.4 on 2023-08-17 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_shop', '0003_rename_category_product_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]