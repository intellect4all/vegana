# Generated by Django 3.1.4 on 2020-12-04 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20201204_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='class_icon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]