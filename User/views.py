from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import UserRegistrationSerializer
from rest_framework.decorators import action
from . serializers import UserRegistrationSerializer
from django.db import transaction


class UserView(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        return Response({"message": "get request called Successfully"}, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def create(self, request):
        data = request.data

        # Create the serializer instance
        serializer = UserRegistrationSerializer(data=data)

        # Check if the data is valid by calling is_valid() on the serializer
        if not serializer.is_valid():
            # Handle validation errors with a 400 status code
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the validated data to create a new user
            user = serializer.save()
        except Exception as e:
            return Response({"message": str(e)})

        # You can access the validated data via serializer.validated_data
        # Return a success response with the created user data
        response_data = serializer.remove_sensitive_fields(serializer.validated_data)
        return Response({"message": "User Added Successfully", "data": response_data}, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def destroy(self, request, pk):
        # print(kwargs.get("username","noname"))
        pk = pk.strip()
        try:
            user = User.objects.filter(username=pk).first()
            if user:
                if user.is_superuser:
                    return Response({"message": "can not delete admin"})
                user.delete()
                return Response({"message": "user deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "User Not Found"})
        except Exception as e:
            return Response({"message": f"Exception occured: {str(e)}"})

    @action(detail=False, methods=["post"])
    def login(self, request):
        return Response({"msg": "Login method run successfully"})
