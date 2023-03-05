# Generated by Django 4.1.7 on 2023-03-05 13:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=100)),
                ('number', models.PositiveIntegerField(blank=True)),
                ('city', models.CharField(max_length=100)),
                ('additional_comments', models.CharField(blank=True, max_length=255)),
                ('latitude', models.FloatField(validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(-90)])),
                ('longitude', models.FloatField(validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(-180)])),
            ],
        ),
    ]
