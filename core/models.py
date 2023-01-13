from django.db import models

class Currency(models.Model):
    
    type_currency_list = [
        ('EUR', 'Euro'),
        ('USD', 'Dollar'),
        ('JPY', 'Japanese Yen'),
        ('GBP', 'Poun Sterling'),
        ('CHF', 'Swiss Franc'),
        ('AUD', 'Australlian dollar'),
        ('CAD', 'Canadian dollar'),
        ('NZD', 'New Zeland dollar'),
    ]

    type_currency = models.CharField(unique=True, choices=type_currency_list, max_length=3)
    amount = models.FloatField(max_length=10)
    available = models.BooleanField(default=True)

