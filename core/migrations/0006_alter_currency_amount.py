# Generated by Django 3.2 on 2023-01-13 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_currency_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='amount',
            field=models.FloatField(max_length=10),
        ),
    ]