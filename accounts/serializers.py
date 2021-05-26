from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Profile

from movies.serializers.nested import MoviesListSerializer


User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    wish_movies = MoviesListSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ('user', 'watch_movies', 'prefer_genres')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'id', 'profile')

