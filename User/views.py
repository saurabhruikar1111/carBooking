from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.decorators import action
from . serializers import UserRegistrationSerializer
from django.db import transaction
from django.contrib.auth import authenticate,login
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .auth import TokenAuthenticationModified
from rest_framework_simplejwt.tokens import RefreshToken,BlacklistMixin,SlidingToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserView(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        return Response({"message": "get request called Successfully"}, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def create(self, request):
        data = request.data
        try:
            # Create the serializer instance
            serializer = UserRegistrationSerializer(data=data)

            # Check if the data is valid by calling is_valid() on the serializer
            if not serializer.is_valid():
                # Handle validation errors with a 400 status code
                # In future we need to set more dynamic status codes
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the validated data to create a new user
            user = serializer.save()
            
            # You can access the validated data via serializer.validated_data
            # Return a success response with the created user data
            response_data = serializer.remove_sensitive_fields(
                serializer.validated_data)

            return Response({"message": "User Added Successfully", "data": response_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": f"something went wrong:{str(e)}"})

    def destroy(self, request, pk):
        # print(kwargs.get("username","noname"))
        pk = pk.strip()
        try:
            with transaction.atomic():
                user = User.objects.filter(username=pk).first()
                if user:
                    if user.is_superuser:
                        return Response({"message": "can not delete admin"})
                    # Note: these delete command internally also deletes token no
                    # need to delete to token specifically
                    user.delete()
                    return Response({"message": f"user {pk} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"message": "User Not Found"})
        except Exception as e:
            return Response({"message": f"Exception occured: {str(e)}"})

    @action(detail=False, methods=["post"])
    def login_(self, request):
        login_data = request.data
        serialiser = UserLoginSerializer(data=login_data)

        if serialiser.is_valid():
            username = login_data["username"]
            password = login_data["password"]

            try:
                user = authenticate(**serialiser.validated_data)
                if user:
                    #print(user.username)
                    login(request,user)
                    #print(user.is_authenticated)
                    #token,created = Token.objects.get_or_create(user=user)
                    refresh = RefreshToken.for_user(user=user)
                    token = str(refresh.access_token)
                    response = Response({"message": f"User {user.username} Login Successfully"})
                    response["Authorization"] = f"{token}"
                    print(token==str(refresh))
                    response.set_cookie("refresh_token",str(refresh))
                    return response
                else:
                    return Response({"message: ""Invalid Credentials, Try again"})
            except Exception as e:
                return Response({"message: ": f"AN error occured while performing operation: {str(e)}"})

        else:
            return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @authentication_classes([JWTAuthentication])
    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=["get"])
    def logout(self,request):
        return Response({"message":"Logout is called"})