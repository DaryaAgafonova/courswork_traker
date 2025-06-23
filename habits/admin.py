from django.contrib import admin
from .models import Habit, HabitLog


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'place', 'time', 'is_pleasant', 'is_public', 'periodicity', 'created_at']
    list_filter = ['is_pleasant', 'is_public', 'periodicity', 'created_at']
    search_fields = ['action', 'place', 'user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time', 'execution_time')
        }),
        ('Тип привычки', {
            'fields': ('is_pleasant', 'is_public')
        }),
        ('Вознаграждение', {
            'fields': ('reward', 'related_habit')
        }),
        ('Периодичность', {
            'fields': ('periodicity',)
        }),
        ('Дата создания', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['habit', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['habit__action', 'habit__user__username']
    readonly_fields = ['completed_at'] 