from rest_framework import serializers
from .models import Movie, Comment, Review


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields= '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields= '__all__'


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields= '__all__'