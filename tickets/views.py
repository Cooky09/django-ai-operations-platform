from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AIJob, Ticket
from .serializers import AIJobSerializer, TicketSerializer
from .tasks import process_ticket_with_ai


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        ticket = serializer.save()
        ticket.status = Ticket.Status.PROCESSING
        ticket.save(update_fields=["status", "updated_at"])
        job = AIJob.objects.create(ticket=ticket)
        process_ticket_with_ai.delay(job.id)

    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        ticket = self.get_object()
        job = AIJob.objects.create(ticket=ticket)
        ticket.status = Ticket.Status.PROCESSING
        ticket.save(update_fields=["status", "updated_at"])
        process_ticket_with_ai.delay(job.id)
        return Response(AIJobSerializer(job).data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["get"])
    def jobs(self, request, pk=None):
        jobs = self.get_object().ai_jobs.all()
        return Response(AIJobSerializer(jobs, many=True).data)


class AIJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AIJob.objects.select_related("ticket").all()
    serializer_class = AIJobSerializer

    @action(detail=False, methods=["get"])
    def health(self, request):
        return Response({"status": "ok"})
