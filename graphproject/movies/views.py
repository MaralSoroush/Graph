from rest_framework import viewsets, filters
from .models import Artist, Movie
from .serializers import ArtistSerializer, MovieDetailSerializer, MovieCreateUpdateSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role', None)

        if role == 'actor':
            queryset = queryset.filter(played_movies__isnull=False).distinct()
        elif role == 'director':
            queryset = queryset.filter(directed_movies__isnull=False).distinct()
        return queryset


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().select_related('director').prefetch_related('actors')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'year']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MovieCreateUpdateSerializer
        return MovieDetailSerializer
