from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Habit, HabitLog
from .serializers import HabitSerializer, PublicHabitSerializer, HabitLogSerializer
from .permissions import IsOwnerOrReadOnly, IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_pleasant', 'is_public']
    ordering_fields = ['created_at', 'time']
    
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwner])
    def complete(self, request, pk=None):
        habit = self.get_object()
        HabitLog.objects.create(habit=habit)
        return Response({'message': 'Привычка отмечена как выполненная'}, status=status.HTTP_200_OK)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublicHabitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_pleasant']
    ordering_fields = ['created_at', 'time']
    
    def get_queryset(self):
        return Habit.objects.filter(is_public=True) 