from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Habit(models.Model):
    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Каждые 2 дня'),
        (3, 'Каждые 3 дня'),
        (4, 'Каждые 4 дня'),
        (5, 'Каждые 5 дней'),
        (6, 'Каждые 6 дней'),
        (7, 'Еженедельно'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=200, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=500, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Связанная привычка')
    periodicity = models.IntegerField(choices=PERIODICITY_CHOICES, default=1, verbose_name='Периодичность')
    reward = models.CharField(max_length=200, blank=True, null=True, verbose_name='Вознаграждение')
    execution_time = models.IntegerField(verbose_name='Время выполнения (секунды)')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']
    
    def clean(self):
        super().clean()
        
        if self.reward and self.related_habit:
            raise ValidationError('Нельзя одновременно указывать вознаграждение и связанную привычку')
        
        if self.execution_time > 120:
            raise ValidationError('Время выполнения не должно превышать 120 секунд')
        
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('В связанные привычки можно добавлять только приятные привычки')
        
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')
        
        if self.periodicity > 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name='Привычка')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата выполнения')
    
    class Meta:
        verbose_name = 'Лог привычки'
        verbose_name_plural = 'Логи привычек'
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.habit.action} - {self.completed_at}" 