from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.events.serializers import UserEventSerializer
from apps.products.tasks import build_user_vector_task
from apps.products.recomendations import redis_client


class EventAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            cache_key = f"user_recommendations:{request.user.id}"
            redis_client.delete(cache_key)

            build_user_vector_task.delay(request.user.id)

            return Response({"ok": True})
        
        return Response(serializer.errors, status=400)