import datetime
from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='car make')
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

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
        return "Name: " + self.name 
                #"Make: " + self.car_make + \
                #"Dealer ID: " + self.dealer_id + \
                #"Type: " + self._type + \
                #"Year: " + self.year

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.id = id
        self.review = review
        self.ourchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review :" + self.review + \
                "Name: " + self.name + \
                "Sentiment: " + self.sentiment


