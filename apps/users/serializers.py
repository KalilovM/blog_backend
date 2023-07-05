from rest_framework import serializers
from .validators import validate_registration, validate_login
from .services import create_user, get_user
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        return validate_registration(attrs)

    def create(self, validated_data):
        return create_user(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=50, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user: User = get_user(username=obj["username"])
        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

    class Meta:
        model = User
        fields = ["password", "username", "tokens"]

    def validate(self, attrs):
        return validate_login(attrs)


class LogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def create(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
