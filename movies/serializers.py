from rest_framework import serializers
from .models import Movie, Comment, Review, Genre 


class MoviesListSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie','create_user','like_users','dislike_users')


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    genre = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'create_user')


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'create_user')


class GenreSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields='__all__'