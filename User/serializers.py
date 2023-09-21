from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserRegistrationSerializer(serializers.ModelSerializer):
    password =  serializers.CharField(write_only=True,required=True)
    username = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ["id","username","password"]
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
            )
        user.save()
        Token.objects.create(user=user)
        return user