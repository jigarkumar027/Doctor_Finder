# Generated by Django 2.0 on 2021-04-24 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210424_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_product',
            name='user_id',
        ),
        migrations.RenameField(
            model_name='shopping_cart',
            old_name='Cust_id',
            new_name='Patient_id',
        ),
        migrations.RenameField(
            model_name='shopping_cart',
            old_name='cqty',
            new_name='cartqty',
        ),
        migrations.RenameField(
            model_name='shopping_cart',
            old_name='pro_id',
            new_name='product_id',
        ),
        migrations.DeleteModel(
            name='Order_product',
        ),
    ]