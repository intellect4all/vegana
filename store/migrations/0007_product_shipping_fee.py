# Generated by Django 3.1.4 on 2020-12-16 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20201208_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shipping_fee',
            field=models.IntegerField(default=0),
        ),
    ]