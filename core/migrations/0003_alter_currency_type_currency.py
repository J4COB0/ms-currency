# Generated by Django 3.2 on 2023-01-10 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_currency_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='type_currency',
            field=models.CharField(choices=[('EUR', 'Euro'), ('USD', 'Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Poun Sterling'), ('CHF', 'Swiss Franc'), ('AUD', 'Australlian dollar'), ('CAD', 'Canadian dollar'), ('NZD', 'New Zeland dollar')], max_length=3, unique=True),
        ),
    ]