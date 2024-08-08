from .views import ArtistViewSet, MovieViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('artists', ArtistViewSet, basename='artists')
router.register('movies', MovieViewSet, basename='movies')
