# Generated by Django 4.1.7 on 2023-03-05 19:51

from django.db import migrations, models
import django.db.models.deletion
import partners.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('communication_type', models.CharField(choices=[(partners.models.CommunicationType['TELEFONICA'], 'TELEFÓNICA'), (partners.models.CommunicationType['TELEMATICA'], 'TELEMÁTICA'), (partners.models.CommunicationType['PERSONAL'], 'PERSONAL'), (partners.models.CommunicationType['EMAIL'], 'EMAIL')], max_length=20)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communication', to='partners.partner')),
            ],
        ),
    ]
