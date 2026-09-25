from unittest.mock import patch

import pytest

from tickets.models import AIJob, Ticket

pytestmark = pytest.mark.django_db


def test_create_ticket(api_client):
    with patch("tickets.views.process_ticket_with_ai.delay") as mocked:
        response = api_client.post(
            "/api/tickets/",
            {
                "title": "Payment failed",
                "description": "My card was charged but the invoice shows an error.",
                "priority": "high",
            },
            format="json",
        )

    assert response.status_code == 201
    ticket = Ticket.objects.get()
    assert ticket.status == Ticket.Status.PROCESSING
    assert AIJob.objects.filter(ticket=ticket).exists()
    mocked.assert_called_once()


def test_ticket_process_endpoint(api_client):
    ticket = Ticket.objects.create(title="Login issue", description="I cannot log in.")
    with patch("tickets.views.process_ticket_with_ai.delay") as mocked:
        response = api_client.post(f"/api/tickets/{ticket.id}/process/")

    assert response.status_code == 202
    assert response.data["status"] == "queued"
    mocked.assert_called_once()


def test_ticket_list(api_client):
    Ticket.objects.create(title="Test", description="Something happened.")
    response = api_client.get("/api/tickets/")
    assert response.status_code == 200
    assert len(response.data) == 1
