from rest_framework import serializers
from .models import Booking

class BookingSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
    