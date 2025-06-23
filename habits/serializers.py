from rest_framework import serializers
from .models import Habit, HabitLog


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'related_habit', 'periodicity', 'reward', 'execution_time',
            'is_public', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']
    
    def validate(self, attrs):
        if attrs.get('reward') and attrs.get('related_habit'):
            raise serializers.ValidationError({'reward': 'Нельзя одновременно указывать вознаграждение и связанную привычку', 'related_habit': 'Нельзя одновременно указывать вознаграждение и связанную привычку'})
        
        if attrs.get('execution_time', 0) > 120:
            raise serializers.ValidationError({'execution_time': 'Время выполнения не должно превышать 120 секунд'})
        
        if attrs.get('related_habit'):
            related_habit = attrs['related_habit']
            if not related_habit.is_pleasant:
                raise serializers.ValidationError({'related_habit': 'В связанные привычки можно добавлять только приятные привычки'})
        
        if attrs.get('is_pleasant', False) and (attrs.get('reward') or attrs.get('related_habit')):
            raise serializers.ValidationError({'is_pleasant': 'У приятной привычки не может быть вознаграждения или связанной привычки'})
        
        if attrs.get('periodicity', 1) > 7:
            raise serializers.ValidationError({'periodicity': 'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'})
        
        return attrs


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['id', 'habit', 'completed_at']
        read_only_fields = ['completed_at']


class PublicHabitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'periodicity', 'execution_time', 'created_at'
        ]
        read_only_fields = ['user', 'created_at'] 