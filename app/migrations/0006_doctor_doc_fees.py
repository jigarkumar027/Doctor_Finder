# Generated by Django 2.0 on 2021-05-01 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210424_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='doc_fees',
            field=models.BigIntegerField(default=100),
        ),
    ]