from rest_framework import serializers
from movies.models import Movie

class MoviesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id','title','poster_path','image','overview')