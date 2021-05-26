from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('user', 'wish_movies', 'watch_movies', 'prefer_genres')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'id', 'profile')

