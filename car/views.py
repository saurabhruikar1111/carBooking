from django.shortcuts import render
from rest_framework import status, viewsets
from . models import Car
from . serialiser import CarSerialiser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

# Create your views here.


class CarView(viewsets.ViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerialiser

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        serialiser = CarSerialiser(data=request.data)
        if not serialiser.is_valid():
            return Response(serialiser.errors)
        try:
            car = serialiser.save()
        except Exception as e:
            return Response({"message": f"An exception occur while performinng operations {str(e)}"})

        return Response({"message": f"car {car.name} is added"})

    def destroy(self, request, pk):
        try:
            with transaction.atomic():
                car=Car.objects.filter(name=pk).first()
                if car:
                    car.delete()
                    return Response({"message":f"car {car.name} is deleted"})
                else: 
                    return Response({"message":f"car {pk} not found"})
        except Exception as e:
            return Response({"message":f"An Exception Ocuured: {str(e)}"})
