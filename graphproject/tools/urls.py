from django.urls import path
from .views import PostgresqlExtensionAPIView, EndPointCallAPIView

urlpatterns = [
    path('extensions/', PostgresqlExtensionAPIView.as_view(), name='postgresql-extensions'),
    path('call-count/', EndPointCallAPIView.as_view(), name='call-count')
]
