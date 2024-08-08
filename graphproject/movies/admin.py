from django.contrib import admin
from .models import Artist, Movie


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'birth_date')
    search_fields = ('name',)
    list_filter = ('country', 'birth_date')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director')
    search_fields = ('title', 'director__name')
    list_filter = ('year', 'director')
    filter_horizontal = ('actors',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('actors').select_related('director')
        return queryset
