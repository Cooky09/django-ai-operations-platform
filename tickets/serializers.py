from rest_framework import serializers

from .models import AIJob, Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = [
            "id",
            "status",
            "ai_summary",
            "ai_category",
            "created_at",
            "updated_at",
        ]


class AIJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIJob
        fields = "__all__"
        read_only_fields = [
            "id",
            "ticket",
            "status",
            "error",
            "created_at",
            "completed_at",
        ]
