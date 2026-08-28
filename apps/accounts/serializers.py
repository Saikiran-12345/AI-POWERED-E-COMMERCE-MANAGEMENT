"""
Serializers for the accounts application.
"""

from rest_framework import serializers
from .models import User, UserProfile, UserRole


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile data."""

    class Meta:
        model = UserProfile
        fields = (
            'bio', 'date_of_birth', 'gender',
            'address_line1', 'address_line2', 'city',
            'state', 'pincode', 'country',
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data (read-only sensitive fields)."""

    full_name = serializers.SerializerMethodField()
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone_number', 'is_active', 'date_joined', 'profile'
        )
        read_only_fields = ('id', 'date_joined', 'is_active')

    def get_full_name(self, obj: User) -> str:
        return obj.get_full_name()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration via API."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[UserRole.CUSTOMER, UserRole.SELLER],
        default=UserRole.CUSTOMER
    )

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'role'
        )

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()

    def validate(self, attrs: dict) -> dict:
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data: dict) -> User:
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for user listings."""

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'is_active')
