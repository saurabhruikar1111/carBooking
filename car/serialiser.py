from rest_framework import serializers
from . models import Car
from django.db import transaction

class CarSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        
    def create(self,validate_data):
        try:
            with transaction.atomic():
                car = Car(**validate_data)
                car.save()
        except Exception as e:
            raise e
        return car
        