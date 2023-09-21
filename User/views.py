from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import UserRegistrationSerializer


class UserView(APIView):
    def get(self, request):
        return Response({"message": "get request called Successfully"}, status=status.HTTP_201_CREATED)

    def post(self, request):

        data = request.data

        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
