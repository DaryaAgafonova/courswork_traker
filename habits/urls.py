from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'habits', views.HabitViewSet, basename='habit')
router.register(r'public-habits', views.PublicHabitViewSet, basename='public-habit')

urlpatterns = [
    path('', include(router.urls)),
] 