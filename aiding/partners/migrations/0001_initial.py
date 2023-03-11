# Generated by Django 4.1.7 on 2023-03-11 18:34

from django.db import migrations, models
import django.db.models.deletion
import partners.models
import partners.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=9, unique=True, validators=[partners.validators.validate_dni])),
                ('phone1', models.CharField(max_length=15, unique=True)),
                ('phone2', models.CharField(blank=True, max_length=15)),
                ('birthdate', models.DateField(validators=[partners.validators.validate_date])),
                ('sex', models.CharField(choices=[('Men', 'men'), ('Women', 'women'), ('None', 'none')], max_length=25)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=150)),
                ('postal_code', models.CharField(max_length=5)),
                ('township', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('language', models.CharField(choices=[('Spanish', 'spanish'), ('Catalan', 'catalan')], max_length=50)),
                ('iban', models.CharField(max_length=34, unique=True, validators=[partners.validators.validate_iban])),
                ('account_holder', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('Active', 'active'), ('Inactive', 'inactive')], default='active', max_length=8)),
                ('observations', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('donation_type', models.CharField(choices=[(partners.models.DonationType['FOOD'], 'FOOD'), (partners.models.DonationType['MONETARY'], 'MONETARY')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('periodicity', models.CharField(choices=[(partners.models.DonationPeriodicity['MONTHLY'], 'MONTHLY'), (partners.models.DonationPeriodicity['QUARTERLY'], 'QUARTERLY'), (partners.models.DonationPeriodicity['SEMIANNUAL'], 'SEMIANNUAL'), (partners.models.DonationPeriodicity['ANNUAL'], 'ANNUAL'), (partners.models.DonationPeriodicity['NONE'], 'NONE')], max_length=20)),
                ('total_donation', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation', to='partners.partners')),
            ],
        ),
    ]
