from django.shortcuts import render
from rest_framework import status, viewsets
from . models import Car
from . serialiser import CarSerialiser
from rest_framework.authentication import TokenAuthentication
from User.auth import TokenAuthenticationModified
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.


class CarView(viewsets.ViewSet):
    #from django.conf import settings
    queryset = Car.objects.all()
    serializer_class = CarSerialiser
    authentication_classes = [JWTAuthentication]
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
                car = Car.objects.filter(name=pk).first()
                if car:
                    car.delete()
                    return Response({"message": f"car {car.name} is deleted"})
                else:
                    return Response({"message": f"car {pk} not found"})
        except Exception as e:
            return Response({"message": f"An Exception Ocuured: {str(e)}"})

    def list(self, request):
        try:
            fields_to_display = [
                "id", "name", "registration_number", "type", "seating_capacity"]
            cars = Car.objects.all()
            serialiser = CarSerialiser(cars, many=True)
            data = []
            for field in serialiser.data:
                data.append(
                    {key: value for key, value in field.items() if key in fields_to_display})
            return Response(data)
        except Exception as e:
            return Response(f"An Error Occured While Performing operations: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
