from django.urls import path,include
from . views import CarView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'',CarView,basename="car")
#print(router.urls)

urlpatterns = [
  path('',include(router.urls)),
] 
