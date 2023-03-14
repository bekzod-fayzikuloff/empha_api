from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    """User register serializer class"""

    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Metaclass with Serializer getting model and included fields"""

        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data: dict) -> User:
        """Creating a new user instance."""
        user = User.objects.create_user(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()

        return user
