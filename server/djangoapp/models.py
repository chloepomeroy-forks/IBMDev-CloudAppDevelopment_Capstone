import datetime
from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='car make')
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'SUV'
    WAGON = 'wagon'
    PICKUP = 'pickup'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (PICKUP, 'Pickup')
    ]
    YEAR_CHOICES = [(r,r) for r in range(1990, datetime.date.today().year+1)]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='car model')
    dealer_id = models.IntegerField()
    _type = models.CharField(null=False, max_length=30, choices=TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + \
                "Make: " + self.car_make + \
                "Dealer ID: " + self.dealer_id + \
                "Type: " + self._type + \
                "Year: " + self.year

