# Generated by Django 4.1.7 on 2023-03-05 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partners',
            name='state',
            field=models.CharField(choices=[('ACTIVE', 'active'), ('INACTIVE', 'INACTIVE')], default='alta', max_length=8),
        ),
    ]