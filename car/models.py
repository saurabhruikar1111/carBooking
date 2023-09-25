from django.db import models

# Create your models here.
CAR_TYPES = (
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('convertible', 'Convertible'),
    )

class Car(models.Model):
    name = models.CharField(max_length=40)
    seating_capacity = models.IntegerField(default=4)
    type = models.CharField(
        max_length=20,
        choices=CAR_TYPES,
        default='sedan'  
    )
    brand = models.CharField(max_length=30,default="None")
    registration_number = models.CharField(max_length=40,unique=True)