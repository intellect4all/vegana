# Generated by Django 3.1.4 on 2020-12-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('actual_price', models.IntegerField()),
                ('discount_price', models.IntegerField(blank=True, null=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('description', models.TextField(max_length=3000)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('category', models.ManyToManyField(default='Uncategorized', related_name='category', to='store.Category')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='store.Category')),
            ],
        ),
    ]