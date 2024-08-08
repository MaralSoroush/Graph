from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection


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
