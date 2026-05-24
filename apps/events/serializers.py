from rest_framework.serializers import ModelSerializer

from .models import UserEvent


class UserEventSerializer(ModelSerializer):
    class Meta:
        model = UserEvent
        fields = "__all__"
        read_only_fields = ["user", "created_at"]