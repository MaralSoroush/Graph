from django.urls import path
from .views import PostgresqlExtensionAPIView

urlpatterns = [
    path('extensions/', PostgresqlExtensionAPIView.as_view(), name='postgresql-extensions'),
]