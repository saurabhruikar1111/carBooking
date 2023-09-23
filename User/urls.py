from django.urls import path,include
from . views import UserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'',UserView,basename="user")
#print(router.urls)

urlpatterns = [
  path('',include(router.urls)),
  #path('<str:username>', UserView.as_view({'delete': 'destroy'}), name='user-delete'),
] 
