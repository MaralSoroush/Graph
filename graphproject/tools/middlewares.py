from django.core.cache import cache

from .models import EndPointCall


class EndPointCallMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        cache_key = f"api_call_count:{path}"
        call_count = cache.get(cache_key, 0)
        call_count += 1
        cache.set(cache_key, call_count, timeout=None)
        endpoint, created = EndPointCall.objects.get_or_create(path=path)

        if call_count and call_count % 100 == 0:
            endpoint.call_count += call_count
            endpoint.save()
            # Reset the counter in Redis
            cache.set(cache_key, 0, timeout=None)

        response = self.get_response(request)

        return response
