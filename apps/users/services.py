from .models import User
from django.db import IntegrityError


def create_user(validated_data):
    """
    Creates a new user with the provided information.
    """
    try:
        return User.objects.create_user(**validated_data)
    except IntegrityError:
        raise ValueError("User creation failed: Integrity error")
    except Exception as e:
        raise ValueError(f"User creation failed: {str(e)}")


def get_user(username):
    """
    Retrieves a user based on the provided username.
    Returns None if the user does not exist.
    """
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        return None
