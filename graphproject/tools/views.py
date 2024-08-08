from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from .models import EndPointCall
from django.core.cache import cache


class PostgresqlExtensionAPIView(APIView):
    """
    This is The APIView to return the installed extensions of the database.
    """

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT extname, extversion FROM pg_extension;")
            extensions = cursor.fetchall()

        extensions_list = [{"name": ext[0], "version": ext[1]} for ext in extensions]
        return Response({"extensions": extensions_list})


class EndPointCallAPIView(APIView):
    def get(self, request, *args, **kwargs):
        db_data = EndPointCall.objects.all()
        data = []
        for record in db_data:
            cache_key = f"api_call_count:{record.path}"
            call_count = cache.get(cache_key, 0)
            data.append({
                'path': record.path,
                'call_count': call_count + record.call_count
            })

        return Response({"data": data})
