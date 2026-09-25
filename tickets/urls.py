from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AIJobViewSet, TicketViewSet

router = DefaultRouter()
router.register("tickets", TicketViewSet)
router.register("jobs", AIJobViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
