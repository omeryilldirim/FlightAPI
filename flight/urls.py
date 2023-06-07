from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PassengerView,
    FlightView,
    ReservationView,
)

urlpatterns = []

router = DefaultRouter()
router.register('passenger', PassengerView)
router.register('flight', FlightView)
router.register('reservation', ReservationView)

urlpatterns += router.urls
