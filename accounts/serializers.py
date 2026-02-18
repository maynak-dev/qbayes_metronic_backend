from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TrafficSource, ActiveAuthor, Designation, UserActivity, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'status', 'pan', 'aadhar', 'pan_card', 'aadhar_card', 'signature']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'profile']

class UserCreateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        # Create user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        # Create or update profile
        UserProfile.objects.update_or_create(user=user, defaults=profile_data)
        return user

class TrafficSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficSource
        fields = '__all__'

class ActiveAuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = ActiveAuthor
        fields = ['id', 'user', 'name', 'role', 'contribution_score']
        read_only_fields = ['name']

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class UserActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'username', 'last_active', 'session_count']