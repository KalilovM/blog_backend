from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from .models import User


def validate_registration(attrs):
    email = attrs.get("email", "")
    username = attrs.get("username", "")
    if not username.isalnum():
        raise serializers.ValidationError(
            "The username should only contain alphanumeric characters"
        )

    if User.objects.filter(username=username).exists():
        raise serializers.ValidationError("The username is already taken")

    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError("The email is already taken")

    if len(attrs.get("password", "")) < 6:
        raise serializers.ValidationError(
            "The password should be at least 6 characters long"
        )

    if attrs.get("password", "") != attrs.get("confirm_password", ""):
        raise serializers.ValidationError("The passwords do not match")

    return attrs


def validate_login(attrs):
    username = attrs.get("username", "")
    password = attrs.get("password", "")
    user = auth.authenticate(username=username, password=password)
    if not user:
        raise AuthenticationFailed("Invalid credentials, try again")
    if not user.is_active:
        raise AuthenticationFailed("Account disabled, contact admin")
    return {"email": user.email, "username": user.username, "tokens": user.tokens}
