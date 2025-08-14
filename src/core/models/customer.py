from django.db import models


class Customer(models.Model):

    class CityChoices(models.TextChoices):
        KARACHI = 'KHI', 'Karachi'
        LAHORE = 'LHE', 'Lahore'
        ISLAMABAD = 'ISB', 'Islamabad'
        MULTAN = 'MUL', 'Multan'
        FAISALABAD = 'FSD', 'Faisalabad'
        HYDERABAD = 'HYD', 'Hyderabad'
        PESHAWAR = 'PSH', 'Peshawar'

    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    notes = models.TextField(null=True, blank=True)
    city = models.CharField(choices=CityChoices.choices, null=True, blank=True)

    def __str__(self):
        return self.name
