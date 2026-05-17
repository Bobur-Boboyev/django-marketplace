import logging

from django.http import JsonResponse


logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            return response

        except Exception as e:
            logger.exception(str(e))

            return JsonResponse(
                {
                    "success": False,
                    "error": "Internal server error",
                },
                status=500,
            )
