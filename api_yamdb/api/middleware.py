from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class BlockPutMethodMiddleware(MiddlewareMixin):
    """Middleware для блокировки PUT методов на уровне проекта"""

    def process_request(self, request):
        if request.method == 'PUT':
            return JsonResponse(
                {'detail': 'PUT метод запрещен.'},
                status=405
            )
        return None
