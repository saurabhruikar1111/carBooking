from rest_framework import viewsets
from .models import Booking
from .serialiser import BookingSerialiser
from User.auth import TokenAuthenticationModified
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.db import transaction

# Create your views here.


class BookingView(viewsets.ViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerialiser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serialser = BookingSerialiser(data=request.data)
        if serialser.is_valid():
            serialser.save()
            return Response({"Booking Details":serialser.data,"message":"Booking confirmed"})
        
    def list(self, request):
        try:
            fields_to_display = [
                "id", "source", "destination", "journey_start_date", "journey_end_date","user","car"]
            bookings = Booking.objects.all()
            serialiser = BookingSerialiser(bookings, many=True)
            data = []
            for field in serialiser.data:
                data.append(
                    {key: value for key, value in field.items() if key in fields_to_display})
            return Response(data)
        except Exception as e:
            return Response(f"An Error Occured While Performing operations: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self,request,pk):
        try:
            with transaction.atomic():
                booking = Booking.objects.filter(id=pk).first()
                if booking:
                    # checking valid user
                    if request.user.id != booking.user.id:
                        return Response({"message":"You can not delete someone else's booking"},status.HTTP_401_UNAUTHORIZED)
                    
                    booking.delete()
                    return Response({"message": f"booking is deleted"})
                else:
                    return Response({"message": f"car {pk} not found"})
        except Exception as e:
            return Response({"message": f"An Exception Ocuured: {str(e)}"})