# Generated by Django 3.1.4 on 2020-12-07 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='store.Tag'),
        ),
    ]
