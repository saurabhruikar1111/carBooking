from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import BookingView

router = DefaultRouter()
router.register(r'',BookingView,basename="booking")


urlpatterns = [
    path('',include(router.urls)),
]
