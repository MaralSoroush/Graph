from django.urls import path
from .views import PostgresqlExtensionAPIView, EndPointCallViewSet

urlpatterns = [
    path('extensions/', PostgresqlExtensionAPIView.as_view(), name='postgresql-extensions'),
    path('call-count/', EndPointCallViewSet.as_view({'get': 'list'}), name='call-count')
]
