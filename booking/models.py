from django.db import models
from django.contrib.auth.models import User
from car.models import Car

# Create your models here.

class Booking(models.Model):
    source = models.CharField(max_length=100, db_column='source')
    destination = models.CharField(max_length=100, db_column='destination')
    journey_start_date = models.DateTimeField(db_column='journey_start_date')
    journey_end_date = models.DateTimeField(db_column='journey_end_date')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column='car_id')