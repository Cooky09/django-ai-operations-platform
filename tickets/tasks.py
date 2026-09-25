from celery import shared_task
from django.utils import timezone

from .models import AIJob, Ticket
from .services import classify_ticket


@shared_task(bind=True, max_retries=2)
def process_ticket_with_ai(self, job_id: int):
    job = AIJob.objects.select_related("ticket").get(pk=job_id)
    job.status = AIJob.Status.RUNNING
    job.save(update_fields=["status"])

    try:
        ticket = job.ticket
        category, summary = classify_ticket(ticket.title, ticket.description)
        ticket.ai_category = category
        ticket.ai_summary = summary
        ticket.status = Ticket.Status.RESOLVED
        ticket.save(update_fields=["ai_category", "ai_summary", "status", "updated_at"])

        job.status = AIJob.Status.COMPLETED
        job.completed_at = timezone.now()
        job.save(update_fields=["status", "completed_at"])
        return {"ticket_id": ticket.id, "category": category}
    except Exception as exc:
        job.status = AIJob.Status.FAILED
        job.error = str(exc)
        job.save(update_fields=["status", "error"])
        raise
