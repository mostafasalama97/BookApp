from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
import jwt
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    def create(self, validated_data):
        author = self.context['request'].user.author  # Retrieve the associated Author instance
        validated_data['author'] = author  # Assign the author to the book

        book = Book.objects.create(**validated_data)
        return book


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'





class ObtainJSONWebTokenSerializer(serializers.Serializer):
    username  = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username  and password:
            user = authenticate(username =username, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username " and "password".'
            raise serializers.ValidationError(msg)

        data['user'] = user
        return data

# Serializer for refreshing JWT token
class RefreshJSONWebTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

        try:
            payload = jwt_decode_handler(data['token'])
            user_id = payload.get('user_id')  # Get the user ID from the payload
            user = User.objects.get(id=user_id)  # Retrieve the user instance using the ID
            data['payload'] = jwt_payload_handler(user)
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise serializers.ValidationError(msg)
        except jwt.InvalidTokenError:
            msg = 'Invalid token.'
            raise serializers.ValidationError(msg)

        return data
    



User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)  # Add the username field

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')  # Include the username field

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],  # Pass the username field
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    payload = jwt_payload_handler(user)
                    attrs['token'] = jwt_encode_handler(payload)
                    return attrs
                else:
                    msg = 'Invalid email or password.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Invalid email or password.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Email and password are required.'
            raise serializers.ValidationError(msg)