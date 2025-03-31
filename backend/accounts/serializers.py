from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True, max_length=15)
    location = serializers.CharField(required=True, max_length=255)
    area_of_interest = serializers.CharField(required=True, max_length=100)

    class Meta:
        model = CustomUser   
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number', 'location', 'area_of_interest']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone_number(self, value):
        """Check if phone number already exists"""
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        """Create and return a new user"""
        username = f"{validated_data['first_name'].lower()}_{validated_data['last_name'].lower()}"  # ✅ Generate username

        user = CustomUser.objects.create_user(
            username=username,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],  # ✅ No need to call `set_password`
            phone_number=validated_data.get('phone_number', ''),
            location=validated_data.get('location', ''),
            area_of_interest=validated_data.get('area_of_interest', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        user = CustomUser.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError({"non_field_errors": ["Invalid email or password"]})

        return {"user": user}  # ✅ Return wrapped user
