from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import transaction

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ["id","username","password"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def validate_username(self, value): 
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")        
        return value

    def remove_sensitive_fields(self, data):
        # Iterate through serializer fields and exclude write-only fields
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.CharField) and field.write_only:
                data.pop(field_name, None)

        return data

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=validated_data["username"],
                    password=validated_data["password"]
                )
                user.save()
                Token.objects.create(user=user)
        except Exception as e:
            raise serializers.ValidationError(f"Something went Wrong:")
        return user
