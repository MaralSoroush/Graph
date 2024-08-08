from rest_framework import serializers
from .models import Artist, Movie


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'country', 'birth_date']


class MovieDetailSerializer(serializers.ModelSerializer):
    director = ArtistSerializer()
    actors = ArtistSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'director', 'actors']


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'director', 'actors']
