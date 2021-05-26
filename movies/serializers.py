from rest_framework import serializers
from .models import Movie, Comment, Review, Genre
from accounts.serializers import UserSerializer


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
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislike_users.count', read_only=True)
    create_user = serializers.CharField(max_length=20, read_only=True, source='profile.name')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie','like_users','dislike_users')



class ReviewsListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislike_users.count', read_only=True)
    create_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie',)


class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewsListSerializer(many=True, read_only=True)
    genre = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Movie
        fields = '__all__'

class CommentsListSerializer(serializers.ModelSerializer):
    create_user = serializers.CharField(max_length=20, read_only=True, source='profile.name')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class GenreSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields='__all__'