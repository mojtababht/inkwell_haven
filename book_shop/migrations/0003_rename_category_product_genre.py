# Generated by Django 4.2.4 on 2023-08-17 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_shop', '0002_rename_category_genre_alter_product_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='genre',
        ),
    ]